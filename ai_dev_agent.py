import subprocess
import os
import re
from datetime import datetime
from zoneinfo import ZoneInfo
from openai import OpenAI

client = OpenAI()

CHANGELOG = "CHANGELOG.md"
BRANCH_BASE = "ai_dev_agent"
NO_CHANGE = "NO_CHANGE"
NO_CHANGE_MESSAGE = "No worthwhile improvements found; repo looks solid from here."
REVIEWED_FILES = ".ai_dev_agent_reviewed_files"
MAX_ATTEMPTS = 3
IGNORE_PREFIXES = ("log/", "tmp/", "storage/", "vendor/", "node_modules/")
IGNORE_EXTENSIONS = (".sql",)
PATH_BONUSES = {
    "app/": 2,
    "lib/": 2,
    "config/": 1,
    "db/": 1,
    "docs/": 1,
    "test/": 1,
}
CLEANUP_SIGNAL_PATTERNS = [
    ("FIXME", re.compile(r"\bFIXME\b", re.IGNORECASE), 4),
    ("TODO", re.compile(r"\bTODO\b", re.IGNORECASE), 3),
    ("HACK", re.compile(r"\bHACK\b", re.IGNORECASE), 3),
    ("XXX", re.compile(r"\bXXX\b", re.IGNORECASE), 3),
    ("TEMP", re.compile(r"\bTEMP(?:ORARY)?\b", re.IGNORECASE), 2),
    ("DEPRECATED", re.compile(r"\bDEPRECATED\b|\bDEPRECATION\b", re.IGNORECASE), 2),
    ("DEBUG", re.compile(r"\bDEBUG\b", re.IGNORECASE), 2),
    ("binding.pry", re.compile(r"\bbinding\.pry\b"), 4),
    ("byebug", re.compile(r"\bbyebug\b"), 4),
    ("pry", re.compile(r"\bpry\b"), 2),
    ("console.log", re.compile(r"\bconsole\.log\b"), 3),
    ("debugger", re.compile(r"\bdebugger\b"), 3),
]


def normalize_model_output(text, original):
    """
    Clean up AI model output and match original file's trailing newline.
    Removes Markdown fences if present.
    """
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            cleaned = "\n".join(lines[1:-1]).strip()
    if original.endswith("\n") and not cleaned.endswith("\n"):
        cleaned += "\n"
    return cleaned


def diff_has_meaningful_changes(diff):
    comment_prefixes = ("#", "//", "/*", "*/", "*", "--", "<!--", "-->", "<%#")
    for line in diff.splitlines():
        if not line.startswith(("+", "-")) or line.startswith(("+++", "---")):
            continue
        content = line[1:].strip()
        if not content:
            continue
        if content.startswith(comment_prefixes):
            continue
        if content.endswith("-->") and content.startswith("<!--"):
            continue
        return True
    return False


def is_whitespace_only_change(original, updated):
    def normalize(text):
        return "\n".join(line.strip() for line in text.splitlines())

    return normalize(original) == normalize(updated)


def read_text_file(path):
    with open(path, "rb") as f:
        data = f.read()
    if b"\x00" in data:
        return None
    return data.decode("utf-8", errors="replace")


def score_file_for_cleanup(path):
    text = read_text_file(path)
    if text is None:
        return 0, []
    signal_score = 0
    signals = []
    for label, pattern, weight in CLEANUP_SIGNAL_PATTERNS:
        count = len(pattern.findall(text))
        if count:
            signal_score += min(count, 3) * weight
            signals.append(f"{label}x{count}")
    if signal_score == 0:
        return 0, []
    path_bonus = 0
    for prefix, bonus in PATH_BONUSES.items():
        if path.startswith(prefix):
            path_bonus = bonus
            break
    line_count = text.count("\n") + 1
    size_penalty = 0
    if line_count > 2000:
        size_penalty = 2
    elif line_count > 800:
        size_penalty = 1
    return max(signal_score + path_bonus - size_penalty, 1), signals


def cleanup_candidates_for(paths):
    scored = []
    for path in paths:
        score, signals = score_file_for_cleanup(path)
        if score > 0:
            scored.append((score, path, signals))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return scored


def readme_guided_target(readme_path, target, files):
    with open(readme_path, "r") as f:
        lines = f.readlines()

    same_dir = os.path.dirname(readme_path)
    preferred = []
    avoid = set()
    avoid_phrases = ["do not edit", "don't edit", "avoid editing", "avoid changing"]
    prefer_phrases = ["use ", "write to", "update ", "add to"]
    for line in lines:
        lower = line.lower()
        matches = [(m.group(1).strip(), m.start()) for m in re.finditer(r"`([^`]+)`", line)]
        if not matches:
            continue
        split_index = -1
        for phrase in ("rather than", "instead of"):
            idx = lower.find(phrase)
            if idx != -1:
                split_index = idx
                break
        avoid_index = -1
        for phrase in avoid_phrases:
            idx = lower.find(phrase)
            if idx != -1:
                avoid_index = idx
                break
        prefer_index = -1
        for phrase in prefer_phrases:
            idx = lower.find(phrase)
            if idx != -1:
                prefer_index = idx
                break
        for mention, pos in matches:
            if avoid_index != -1 and pos > avoid_index:
                avoid.add(mention)
                continue
            if split_index != -1:
                if pos > split_index:
                    avoid.add(mention)
                else:
                    preferred.append(mention)
                continue
            if prefer_index != -1 and pos > prefer_index:
                preferred.append(mention)

    def resolve(mention):
        return mention if "/" in mention else f"{same_dir}/{mention}" if same_dir else mention

    avoid_paths = {resolve(m) for m in avoid if resolve(m) in files and resolve(m) != readme_path}
    candidates = []
    for mention in preferred:
        path = resolve(mention)
        if path in files and path != readme_path and path not in candidates:
            candidates.append(path)

    if target == readme_path or target in avoid_paths:
        for path in candidates:
            if path not in avoid_paths and os.path.basename(path) != "README.md":
                context_files = [p for p in avoid_paths if p != path]
                return path, context_files, False
        siblings = [
            f for f in files
            if f.startswith(f"{same_dir}/")
            and f not in avoid_paths
            and f != readme_path
            and os.path.basename(f) != "README.md"
        ]
        if siblings:
            context_files = [p for p in avoid_paths if p != siblings[0]]
            return siblings[0], context_files, False
        return None, list(avoid_paths), True
    context_files = [p for p in avoid_paths if p != target]
    return target, context_files, False


def load_reviewed():
    if not os.path.exists(REVIEWED_FILES):
        return set()
    with open(REVIEWED_FILES, "r") as f:
        return {line.strip() for line in f if line.strip()}


def record_reviewed(path, reviewed):
    if path in reviewed:
        return
    with open(REVIEWED_FILES, "a") as f:
        f.write(f"{path}\n")
    reviewed.add(path)


def branch_exists(name):
    """
    Check if a git branch exists.
    """
    return subprocess.call(
        ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{name}"]
    ) == 0


def create_work_branch():
    """
    Create a new work branch, appending date/counter if needed.
    """
    if not branch_exists(BRANCH_BASE):
        branch_name = BRANCH_BASE
    else:
        date_suffix = datetime.now().strftime("%Y%m%d")
        branch_name = f"{BRANCH_BASE}-{date_suffix}"
        counter = 1
        while branch_exists(branch_name):
            branch_name = f"{BRANCH_BASE}-{date_suffix}-{counter}"
            counter += 1

    subprocess.check_call(["git", "checkout", "-b", branch_name])
    print("Created branch:", branch_name)


def next_patch_version(lines):
    header_re = re.compile(r"^## \[(\d+)\.(\d+)\.(\d+)\] - ")
    scan = lines[:50] if len(lines) > 50 else lines
    for line in scan:
        match = header_re.match(line.strip())
        if match:
            major, minor, patch = map(int, match.groups())
            return f"{major}.{minor}.{patch + 1}"
    for line in lines:
        match = header_re.match(line.strip())
        if match:
            major, minor, patch = map(int, match.groups())
            return f"{major}.{minor}.{patch + 1}"
    return "0.1.0"


def is_ignored_path(path, ignore_exact):
    if path in ignore_exact:
        return True
    if path.endswith(IGNORE_EXTENSIONS):
        return True
    return path.startswith(IGNORE_PREFIXES)

# -----------------------------
# Create work branch
# -----------------------------

create_work_branch()

# -----------------------------
# Get repository files
# -----------------------------

files = subprocess.check_output(["git", "ls-files"]).decode().splitlines()
reviewed = load_reviewed()

ignore = [
    "CHANGELOG.md",
    ".gitignore",
    "ai_dev_agent.py",
    "Dockerfile",
    "docs/docs.json",
]

all_files = [f for f in files if not is_ignored_path(f, ignore)]

if not all_files:
    print("No repo files found.")
    exit()

unreviewed_files = [f for f in all_files if f not in reviewed]
if not unreviewed_files:
    print(f"All tracked files have been reviewed; clear {REVIEWED_FILES} to reset.")
    exit()

max_files = 40
cleanup_candidates = cleanup_candidates_for(unreviewed_files)
cleanup_signals = {path: signals for _, path, signals in cleanup_candidates}
file_candidates = unreviewed_files[:max_files]
file_list = "\n".join(file_candidates)

# -----------------------------
# AI selects file
# -----------------------------

selection_prompt = """
You are reviewing a software repository.

Choose ONE file where a meaningful cleanup is likely.
Prefer files with TODO/FIXME, debug leftovers, deprecated notes, or stale instructions.
Avoid files where only a trivial comment tweak is possible.
Avoid CSS unless there are clear text issues to fix.

Allowed improvements:
- documentation
- readability
- small bug fixes

Return ONLY the filename.

FILES:
{file_list}
"""

attempt = 0
tried = set()
target = None
original = ""
updated = ""
diff = ""
success = False
while attempt < MAX_ATTEMPTS:
    attempt += 1
    if cleanup_candidates:
        candidates = [path for _, path, _ in cleanup_candidates if path not in tried]
        if not candidates:
            print(NO_CHANGE_MESSAGE)
            exit()
        target = candidates[0]
        print("Selected cleanup candidate:", target)
    else:
        candidates = [f for f in file_candidates if f not in tried]
        if not candidates:
            print(NO_CHANGE_MESSAGE)
            exit()
        file_list = "\n".join(candidates)
        resp = client.responses.create(
            model="gpt-4.1",
            input=selection_prompt.format(file_list=file_list)
        )
        target = resp.output_text.strip()
        print("Selected file:", target)
    if target not in all_files:
        print("Model returned invalid file. Aborting.")
        exit()
    if target in reviewed:
        tried.add(target)
        print("Previously reviewed file; retrying.")
        continue
    selected_target = target
    record_reviewed(selected_target, reviewed)
    readme_path = os.path.join(os.path.dirname(target), "README.md")
    context_files = []
    blocked = False
    if readme_path in all_files:
        next_target, context_files, blocked = readme_guided_target(readme_path, target, all_files)
        if blocked:
            tried.add(selected_target)
            print("README guidance blocked selection; retrying.")
            continue
        if next_target and next_target != target:
            tried.add(selected_target)
            if next_target in reviewed:
                tried.add(next_target)
                print("README guidance chose a previously reviewed file; retrying.")
                continue
            record_reviewed(next_target, reviewed)
            target = next_target
            print("README guidance; switching to:", target)
    tried.add(target)
    original = read_text_file(target)
    if original is None:
        continue
    context_blocks = ""
    for path in context_files:
        with open(path, "r") as f:
            context_blocks += f"\nCONTEXT_FILE: {path}\n{f.read()}\n"
    cleanup_hint = ""
    signals = cleanup_signals.get(target, [])
    if signals:
        cleanup_hint = f"CLEANUP_HINTS: {', '.join(signals)}\n"
    improve_prompt = f"""
Improve this file with a meaningful janitor cleanup.

Rules:
- do not change functionality unless removing obvious dead/debug code
- prioritize cleanup with real impact (resolve TODO/FIXME when simple, remove debug leftovers, fix stale instructions)
- avoid comment-only or style-only edits
- do not add new comments unless correcting misleading ones
- return the FULL updated file
- no explanation
- do not wrap the response in markdown or code fences
- if no improvement is needed, return exactly {NO_CHANGE}

{cleanup_hint}
FILE:
{original}
{context_blocks}
"""
    resp2 = client.responses.create(
        model="gpt-4.1",
        input=improve_prompt
    )
    updated = resp2.output_text.strip()
    if updated == NO_CHANGE:
        continue
    updated = normalize_model_output(updated, original)
    if updated.lstrip().startswith("```") and not original.lstrip().startswith("```"):
        retry_prompt = improve_prompt + "\nIMPORTANT: Return raw file contents only."
        resp2_retry = client.responses.create(
            model="gpt-4.1",
            input=retry_prompt
        )
        updated = normalize_model_output(resp2_retry.output_text, original)
    if updated.lstrip().startswith("```") and not original.lstrip().startswith("```"):
        continue
    if updated.strip() == original.strip():
        continue
    if is_whitespace_only_change(original, updated):
        continue
    with open(target, "w") as f:
        f.write(updated)
    diff = subprocess.check_output(["git", "diff", target]).decode()
    if not diff_has_meaningful_changes(diff):
        with open(target, "w") as f:
            f.write(original)
        updated = ""
        diff = ""
        continue
    success = True
    break

if not success:
    print(NO_CHANGE_MESSAGE)
    exit()

# -----------------------------
# Write file
# -----------------------------

with open(target, "w") as f:
    f.write(updated)

print("File updated.")

# -----------------------------
# Generate diff
# -----------------------------

if not diff:
    diff = subprocess.check_output(["git", "diff", target]).decode()

if not diff.strip():
    print("No diff detected.")
    exit()

# -----------------------------
# AI writes changelog entry
# -----------------------------

changelog_prompt = f"""
Write ONE changelog bullet describing this change.

Rules:
- 5 to 15 words
- no punctuation at start
- no explanation

DIFF:
{diff}
"""

resp3 = client.responses.create(
    model="gpt-4.1",
    input=changelog_prompt
)

entry = resp3.output_text.strip()

print("Changelog entry:", entry)

# -----------------------------
# Insert into CHANGELOG
# -----------------------------

if not os.path.exists(CHANGELOG):
    with open(CHANGELOG, "w") as f:
        f.write("# Changelog\n\n")

with open(CHANGELOG, "r") as f:
    lines = f.readlines()

version = next_patch_version(lines)
today = datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d")
new_section = [
    f"## [{version}] - {today}\n",
    "### Changed\n",
    f"- {entry}\n",
    "\n",
]

insert_at = None
for i, line in enumerate(lines):
    if line.startswith("## ["):
        insert_at = i
        break

if insert_at is None:
    lines.extend(new_section)
else:
    lines[insert_at:insert_at] = new_section

with open(CHANGELOG, "w") as f:
    f.writelines(lines)

print("CHANGELOG updated.")

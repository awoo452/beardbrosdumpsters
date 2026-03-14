import subprocess
import os
import re
from datetime import datetime
from openai import OpenAI

client = OpenAI()

CHANGELOG = "CHANGELOG.md"
BRANCH_BASE = "ai_dev_agent"
NO_CHANGE = "NO_CHANGE"
NO_CHANGE_MESSAGE = "No worthwhile improvements found; repo looks solid from here."
LAST_SELECTED_FILE = ".ai_dev_agent_last_file"


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
    for line in diff.splitlines():
        if not line.startswith(("+", "-")) or line.startswith(("+++", "---")):
            continue
        content = line[1:].strip()
        if not content:
            continue
        if content.startswith(("#", "//", "/*", "*/", "*")):
            continue
        return True
    return False


def readme_guided_target(readme_path, target, files):
    with open(readme_path, "r") as f:
        lines = f.readlines()

    same_dir = os.path.dirname(readme_path)
    mentions = []
    avoid = set()
    avoid_prefixes = ["do not", "don't", "avoid", "rather than", "instead of"]
    for line in lines:
        lower = line.lower()
        for match in re.finditer(r"`([^`]+)`", line):
            mention = match.group(1).strip()
            mentions.append(mention)
            prefix = lower[: match.start()]
            if any(p in prefix for p in avoid_prefixes) and "edit" in prefix:
                avoid.add(mention)
            elif "edit" in lower and any(p in lower for p in avoid_prefixes):
                avoid.add(mention)

    def resolve(mention):
        return mention if "/" in mention else f"{same_dir}/{mention}" if same_dir else mention

    avoid_paths = {resolve(m) for m in avoid}
    candidates = []
    for mention in mentions:
        path = resolve(mention)
        if path in files and path != readme_path and path not in candidates:
            candidates.append(path)

    if target == readme_path or target in avoid_paths:
        for path in candidates:
            if path not in avoid_paths and os.path.basename(path) != "README.md":
                context_files = [p for p in avoid_paths if p in files and p != path]
                return path, context_files
    return target, []


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

# -----------------------------
# Create work branch
# -----------------------------

create_work_branch()

# -----------------------------
# Get repository files
# -----------------------------

files = subprocess.check_output(["git", "ls-files"]).decode().splitlines()

ignore = [
    "CHANGELOG.md",
    ".gitignore",
    "ai_dev_agent.py"
]

files = [f for f in files if f not in ignore]

if not files:
    print("No repo files found.")
    exit()

max_files = 40
file_candidates = files[:max_files]
last_selected = None
if os.path.exists(LAST_SELECTED_FILE):
    with open(LAST_SELECTED_FILE, "r") as f:
        last_selected = f.read().strip()
if last_selected in file_candidates and len(file_candidates) > 1:
    file_candidates = [f for f in file_candidates if f != last_selected]
file_list = "\n".join(file_candidates)

# -----------------------------
# AI selects file
# -----------------------------

selection_prompt = """
You are reviewing a software repository.

Choose ONE file that could benefit from a small improvement.

Allowed improvements:
- documentation
- readability
- comments
- small bug fixes

Return ONLY the filename.

FILES:
{file_list}
""".format(file_list=file_list)

resp = client.responses.create(
    model="gpt-4.1",
    input=selection_prompt
)

target = resp.output_text.strip()

print("Selected file:", target)

if target not in files:
    print("Model returned invalid file. Aborting.")
    exit()

readme_path = os.path.join(os.path.dirname(target), "README.md")
context_files = []
if readme_path in files:
    next_target, context_files = readme_guided_target(readme_path, target, files)
    if next_target != target:
        target = next_target
        print("README guidance; switching to:", target)

with open(LAST_SELECTED_FILE, "w") as f:
    f.write(f"{target}\n")

# -----------------------------
# Read file
# -----------------------------

with open(target, "r") as f:
    original = f.read()

context_blocks = ""
for path in context_files:
    with open(path, "r") as f:
        context_blocks += f"\nCONTEXT_FILE: {path}\n{f.read()}\n"

# -----------------------------
# AI improves file
# -----------------------------

improve_prompt = f"""
Improve this file slightly.

Rules:
- do not change functionality
- only readability or documentation
- return the FULL updated file
- no explanation
- do not wrap the response in markdown or code fences
- if no improvement is needed, return exactly {NO_CHANGE}

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
    print(NO_CHANGE_MESSAGE)
    exit()

updated = normalize_model_output(updated, original)

if updated.lstrip().startswith("```") and not original.lstrip().startswith("```"):
    retry_prompt = improve_prompt + "\nIMPORTANT: Return raw file contents only."
    resp2_retry = client.responses.create(
        model="gpt-4.1",
        input=retry_prompt
    )
    updated = normalize_model_output(resp2_retry.output_text, original)

if updated.lstrip().startswith("```") and not original.lstrip().startswith("```"):
    print("Model returned fenced output. Aborting.")
    exit()

if updated.strip() == original.strip():
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

diff = subprocess.check_output(["git", "diff", target]).decode()

if not diff.strip():
    print("No diff detected.")
    exit()

if not diff_has_meaningful_changes(diff):
    with open(target, "w") as f:
        f.write(original)
    print(NO_CHANGE_MESSAGE)
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
        f.write("# Changelog\n\n## Unreleased\n")

with open(CHANGELOG, "r") as f:
    lines = f.readlines()

# Ensure '## Unreleased' is at the top
unreleased_index = None
for i, line in enumerate(lines):
    if line.strip().lower() == "## unreleased":
        unreleased_index = i
        break

if unreleased_index is None:
    # If not present, insert at the top
    lines = ["## Unreleased\n", "\n"] + lines
    unreleased_index = 0
elif unreleased_index != 0:
    # Move "## Unreleased" section to the top
    end_index = unreleased_index + 1
    while end_index < len(lines):
        if lines[end_index].startswith("## ") and end_index != unreleased_index:
            break
        end_index += 1
    unreleased_section = lines[unreleased_index:end_index]
    del lines[unreleased_index:end_index]
    lines = unreleased_section + lines
    unreleased_index = 0

insert_index = unreleased_index + 1
if insert_index < len(lines) and lines[insert_index].strip() == "":
    insert_index += 1

lines.insert(insert_index, f"- {entry}\n")

# Ensure a blank line after the last bullet before the next section
next_index = insert_index + 1
scan_index = next_index
while scan_index < len(lines) and lines[scan_index].strip() == "":
    scan_index += 1

if scan_index < len(lines) and lines[scan_index].startswith("## "):
    if next_index >= len(lines) or lines[next_index].strip() != "":
        lines.insert(next_index, "\n")

with open(CHANGELOG, "w") as f:
    f.writelines(lines)

print("CHANGELOG updated.")

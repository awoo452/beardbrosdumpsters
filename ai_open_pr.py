#!/usr/bin/env python3
import argparse
import os
import re
import subprocess
import sys


def run(cmd, check=True):
    result = subprocess.run(cmd, text=True, capture_output=True)
    if check and result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        message = stderr or stdout or "Command failed"
        raise RuntimeError(message)
    return result.stdout.strip()


def git(*args, check=True):
    return run(["git", *args], check=check)


def gh_available():
    try:
        run(["gh", "--version"], check=True)
        return True
    except Exception:
        return False


def branch_exists(name):
    return subprocess.call(
        ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{name}"]
    ) == 0


def default_base_branch():
    try:
        ref = git("symbolic-ref", "refs/remotes/origin/HEAD")
        return ref.split("/")[-1]
    except Exception:
        pass
    for candidate in ("main", "master"):
        if branch_exists(candidate):
            return candidate
    return None


def current_branch():
    return git("rev-parse", "--abbrev-ref", "HEAD")


def working_tree_clean():
    return git("status", "--porcelain") == ""


def commits_ahead(base):
    count = git("rev-list", "--count", f"{base}..HEAD")
    try:
        return int(count)
    except ValueError:
        return 0


def latest_changelog_version(path="CHANGELOG.md"):
    if not os.path.exists(path):
        return None
    header_re = re.compile(r"^## \[(\d+\.\d+\.\d+)\]")
    with open(path, "r", encoding="utf-8") as changelog:
        for line in changelog:
            match = header_re.match(line.strip())
            if match:
                return match.group(1)
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Open a GitHub PR for the current branch using gh."
    )
    parser.add_argument("--base", help="Base branch (defaults to origin/HEAD)")
    parser.add_argument("--title", help="PR title")
    parser.add_argument("--body", help="PR body")
    parser.add_argument(
        "--fill",
        action="store_true",
        help="Let gh auto-fill title/body from commits",
    )
    parser.add_argument(
        "--draft",
        action="store_true",
        help="Create the PR as a draft",
    )
    parser.add_argument(
        "--no-commit",
        action="store_true",
        help="Skip auto-committing dirty changes before opening the PR",
    )
    args = parser.parse_args()

    if not gh_available():
        print("gh CLI is not installed or not on PATH.")
        print("Install it from GitHub CLI and authenticate first.")
        sys.exit(1)

    branch = current_branch()
    if branch in ("main", "master"):
        print("Refusing to open a PR from main/master. Create a feature branch first.")
        sys.exit(1)

    if not args.no_commit and not working_tree_clean():
        version = latest_changelog_version()
        if not version:
            print("Unable to find a changelog version header in CHANGELOG.md.")
            sys.exit(1)
        try:
            git("add", "-A")
            git("commit", "-m", version)
            print(f"Committed changes with message: {version}")
        except RuntimeError as exc:
            print(str(exc))
            sys.exit(1)

    base = args.base or default_base_branch()
    if not base:
        print("Could not determine base branch. Pass --base explicitly.")
        sys.exit(1)

    if commits_ahead(base) == 0:
        print(f"No commits ahead of {base}. Nothing to open a PR for.")
        sys.exit(1)

    cmd = ["gh", "pr", "create", "--base", base, "--head", branch]
    if args.draft:
        cmd.append("--draft")

    if args.fill:
        cmd.append("--fill")
    else:
        title = args.title or branch.replace("-", " ").replace("_", " ")
        body = args.body or "## Summary\n- \n\n## Testing\n- Not run (not requested)\n"
        cmd.extend(["--title", title, "--body", body])

    try:
        output = run(cmd, check=True)
    except RuntimeError as exc:
        print(str(exc))
        sys.exit(1)

    if output:
        print(output)


if __name__ == "__main__":
    main()

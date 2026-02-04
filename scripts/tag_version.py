#!/usr/bin/env python3
"""
Script to create and push a new git tag with minor version bump.
When PR is merged to master, this script bumps the minor version and pushes to both repos.
"""
import os
import re
import subprocess
import sys
from typing import Optional

if __name__ not in ("__main__", "__mp_main__"):
    raise SystemExit(
        "This file is intended to be executed as an executable program. You cannot use it as a module."
        f"To run this script, run the ./{__file__} command"
    )


def run_command(command: list, capture_output: bool = True, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    result = subprocess.run(
        command,
        capture_output=capture_output,
        text=True,
        check=check,
    )
    return result


def get_latest_tag() -> Optional[str]:
    """Get the latest git tag matching semantic versioning pattern (vX.Y.Z)."""
    try:
        # Get all tags matching v*.*.* pattern, sorted by version
        result = run_command(
            ["git", "tag", "-l", "v*.*.*", "--sort=-version:refname"],
            check=False,
        )
        tags = [tag.strip() for tag in result.stdout.strip().split("\n") if tag.strip()]

        # Filter to only semantic version tags (vX.Y.Z)
        semantic_tags = [tag for tag in tags if re.match(r"^v\d+\.\d+\.\d+$", tag)]

        if semantic_tags:
            return semantic_tags[0]
        return None
    except Exception as e:
        print(f"Error getting latest tag: {e}", file=sys.stderr)
        return None


def parse_version(tag: str) -> tuple[int, int, int]:
    """Parse version tag (vX.Y.Z) into (major, minor, patch)."""
    match = re.match(r"^v(\d+)\.(\d+)\.(\d+)$", tag)
    if not match:
        raise ValueError(f"Invalid version tag format: {tag}")
    return (int(match.group(1)), int(match.group(2)), int(match.group(3)))


def bump_minor_version(current_tag: Optional[str]) -> str:
    """Bump minor version. If no tag exists, start with v0.1.0."""
    if current_tag is None:
        return "v0.1.0"

    major, minor, patch = parse_version(current_tag)
    new_minor = minor + 1
    # Reset patch to 0 when bumping minor
    return f"v{major}.{new_minor}.0"


def create_and_push_tag(tag: str, push_to_all: bool = True) -> bool:
    """Create a git tag and push it to remote(s)."""
    try:
        # Create the tag
        print(f"Creating tag: {tag}")
        run_command(["git", "tag", "-a", tag, "-m", f"Release {tag}"])

        # Push to origin
        print(f"Pushing tag {tag} to origin")
        run_command(["git", "push", "origin", tag])

        # Optionally push to all remotes
        if push_to_all:
            print(f"Pushing tag {tag} to all remotes")
            run_command(["git", "push", "--tags", "--all"])

        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating/pushing tag: {e}", file=sys.stderr)
        if e.stderr:
            print(f"stderr: {e.stderr}", file=sys.stderr)
        return False


def main():
    """Main function to bump version and create tag."""
    # Ensure we're on master branch
    try:
        result = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        current_branch = result.stdout.strip()
        if current_branch != "master":
            print(f"Warning: Not on master branch (current: {current_branch})", file=sys.stderr)
            print("Continuing anyway...", file=sys.stderr)
    except Exception as e:
        print(f"Warning: Could not determine current branch: {e}", file=sys.stderr)

    # Get latest tag
    latest_tag = get_latest_tag()
    print(f"Latest tag: {latest_tag or 'none (starting from v0.1.0)'}")

    # Bump minor version
    new_tag = bump_minor_version(latest_tag)
    print(f"New tag: {new_tag}")

    # Confirm (optional, can be skipped in CI)
    if os.environ.get("CI") != "true":
        response = input(f"Create and push tag {new_tag}? (y/N): ")
        if response.lower() != "y":
            print("Aborted.")
            sys.exit(0)

    # Create and push tag
    success = create_and_push_tag(new_tag, push_to_all=True)

    if success:
        print(f"Successfully created and pushed tag: {new_tag}")
        # Output tag for use in GitHub Actions (both old and new format)
        github_output = os.environ.get("GITHUB_OUTPUT")
        if github_output:
            with open(github_output, "a") as f:
                f.write(f"tag={new_tag}\n")
        else:
            # Fallback to old format
            print(f"::set-output name=tag::{new_tag}")
        # Also set as environment variable
        print(f"NEW_TAG={new_tag}")
    else:
        print("Failed to create/push tag", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

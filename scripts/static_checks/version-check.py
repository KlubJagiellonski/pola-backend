#!/usr/bin/env python3
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DJANGO_VERSION = next(
    line
    for line in (ROOT_DIR / "dependencies/constraints-production.txt").read_text().splitlines()
    if line.lower().startswith("django==")
).split("==")[1]

PYTHON_VERSION = Path(ROOT_DIR / ".python-version").read_text().strip()

files_to_check = [
    ROOT_DIR / "docker-compose.yaml",
    ROOT_DIR / "scripts/ci-docker-image/Dockerfile",
    ROOT_DIR / "self-management/Dockerfile",
]

patterns = [
    (r'DJANGO_VERSION=\${DJANGO_VERSION-.*}', f'DJANGO_VERSION=${{DJANGO_VERSION-{DJANGO_VERSION}}}'),
    (r'PYTHON_VERSION=\${PYTHON_VERSION-.*}', f'PYTHON_VERSION=${{PYTHON_VERSION-{PYTHON_VERSION}}}'),
    (r'ARG PYTHON_VERSION=.*', f'ARG PYTHON_VERSION="{PYTHON_VERSION}"'),
]

has_changes = False
for file in files_to_check:
    old_content = Path(file).read_text()
    new_content = old_content
    for pattern in patterns:
        new_content = re.sub(
            pattern[0],
            pattern[1],
            new_content,
        )
    if old_content != new_content:
        Path(file).write_text(new_content)
        print(f"File updated: {file}")
        has_changes = True

if not has_changes:
    print("No changes needed.")
    sys.exit(0)
else:
    sys.exit(1)

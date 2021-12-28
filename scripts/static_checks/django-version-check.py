#!/usr/bin/env python3
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DJANGO_VERSION = next(
    line
    for line in (ROOT_DIR / "requirements" / "production.txt").read_text().splitlines()
    if line.lower().startswith("django==")
).split("==")[1]

docker_compose_content: str = (ROOT_DIR / "docker-compose.yaml").read_text()
new_docker_compose_content = re.sub(
    r'DJANGO_VERSION=\${DJANGO_VERSION-.*}',
    f'DJANGO_VERSION=${{DJANGO_VERSION-{DJANGO_VERSION}}}',
    docker_compose_content,
)
if docker_compose_content != new_docker_compose_content:
    (ROOT_DIR / "docker-compose.yaml").write_text(new_docker_compose_content)
    print("File updated!")
    sys.exit(1)
else:
    print("Not changed needed. ")

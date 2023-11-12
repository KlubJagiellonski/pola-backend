#!/usr/bin/env python3
import os
import subprocess
import sys

if __name__ not in ("__main__", "__mp_main__"):
    raise SystemExit(
        "This file is intended to be executed as an executable program. You cannot use it as a module."
        f"To run this script, run the ./{__file__} command"
    )

GITHUB_ORGANIZATION = os.environ.get('GITHUB_ORGANIZATION', 'KlubJagiellonski')

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    print("Missing environment variable: GITHUB_TOKEN", file=sys.stderr)
    sys.exit(1)

USERNAME = GITHUB_ORGANIZATION.lower()

print(f"Logging in to the Github Registry as {USERNAME!r}.")

subprocess.run(
    [
        'docker',
        'login',
        '--username',
        USERNAME,
        '--password-stdin',
        "ghcr.io",
    ],
    input=GITHUB_TOKEN.encode(),
    check=True,
)
print("Logged in")

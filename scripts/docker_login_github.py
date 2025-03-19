#!/usr/bin/env python3
import os
import subprocess
import sys
from shutil import which

if __name__ not in ("__main__", "__mp_main__"):
    raise SystemExit(
        "This file is intended to be executed as an executable program. You cannot use it as a module."
        f"To run this script, run the ./{__file__} command"
    )

GITHUB_ORGANIZATION = os.environ.get('GITHUB_ORGANIZATION', 'KlubJagiellonski')

github_token = os.environ.get('GITHUB_TOKEN')
if not github_token and which('gh'):
    # Use the GitHub CLI to login
    github_token = subprocess.check_output(['gh', 'auth', 'token'], text=True)
if not github_token:
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
    input=github_token.encode(),
    check=True,
)
print("Logged in")

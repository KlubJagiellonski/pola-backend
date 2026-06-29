#!/usr/bin/env python3
import os
import subprocess
import sys
import time
from shutil import which

if __name__ not in ("__main__", "__mp_main__"):
    raise SystemExit(
        "This file is intended to be executed as an executable program. You cannot use it as a module."
        f"To run this script, run the ./{__file__} command"
    )

GITHUB_ORGANIZATION = os.environ.get('GITHUB_ORGANIZATION', 'KlubJagiellonski')
MAX_ATTEMPTS = 5
RETRY_DELAY_SECONDS = 10

github_token = os.environ.get('GITHUB_TOKEN')
if not github_token and which('gh'):
    # Use the GitHub CLI to login
    github_token = subprocess.check_output(['gh', 'auth', 'token'], text=True)
if not github_token:
    print("Missing environment variable: GITHUB_TOKEN", file=sys.stderr)
    sys.exit(1)

USERNAME = GITHUB_ORGANIZATION.lower()

print(f"Logging in to the Github Registry as {USERNAME!r}.")

for attempt in range(1, MAX_ATTEMPTS + 1):
    result = subprocess.run(
        [
            'docker',
            'login',
            '--username',
            USERNAME,
            '--password-stdin',
            "ghcr.io",
        ],
        input=github_token.encode(),
        capture_output=True,
        text=False,
    )
    if result.returncode == 0:
        print("Logged in")
        sys.exit(0)

    stderr = result.stderr.decode(errors="replace").strip()
    print(f"Docker login attempt {attempt}/{MAX_ATTEMPTS} failed: {stderr}", file=sys.stderr)
    if attempt < MAX_ATTEMPTS:
        print(f"Retrying in {RETRY_DELAY_SECONDS}s...", file=sys.stderr)
        time.sleep(RETRY_DELAY_SECONDS)

print("Docker login to ghcr.io failed after all retries.", file=sys.stderr)
sys.exit(1)

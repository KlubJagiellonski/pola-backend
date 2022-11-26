#!/usr/bin/env python3
import os
import sys

if __name__ not in ("__main__", "__mp_main__"):
    raise SystemExit(
        "This file is intended to be executed as an executable program. You cannot use it as a module."
        f"To run this script, run the ./{__file__} command"
    )

GITHUB_REF = os.environ.get('GITHUB_REF')

if not GITHUB_REF:
    print("GITHUB_REF environment variable is unset", file=sys.stderr)
    sys.exit(1)


assert GITHUB_REF.startswith('refs/heads/')

_, _, branch = GITHUB_REF.split('/', 3)

if branch == "prod":
    print('pola-app')
elif branch == 'master':
    print('pola-staging')
else:
    print(f"Unknown app. Current ref: {GITHUB_REF!r} (branch: {branch!r})")
    sys.exit(1)

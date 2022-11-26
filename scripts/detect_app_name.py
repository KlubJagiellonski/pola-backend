#!/usr/bin/env python
import os
import sys

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

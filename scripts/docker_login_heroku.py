#!/usr/bin/env python3
import os
import subprocess
import sys

if __name__ not in ("__main__", "__mp_main__"):
    raise SystemExit(
        "This file is intended to be executed as an executable program. You cannot use it as a module."
        f"To run this script, run the ./{__file__} command"
    )

HEROKU_API_KEY = os.environ.get('HEROKU_API_KEY')
if not HEROKU_API_KEY:
    print("Missing environment variable: HEROKU_API_KEY", file=sys.stderr)
    print("You can obtain it using \"heroku auth:token\" command", file=sys.stderr)
    sys.exit(1)

subprocess.run(
    ['docker', 'login', '--username=_', '--password-stdin', 'registry.heroku.com'],
    check=True,
    input=HEROKU_API_KEY.encode(),
)

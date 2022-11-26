#!/usr/bin/env python3
import os
import subprocess
import sys

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

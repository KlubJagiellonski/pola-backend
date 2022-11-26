#!/usr/bin/env python
import os
import subprocess
import sys

heroku_api_key = os.environ.get('HEROKU_API_KEY')
if not heroku_api_key:
    print("Missing environment variable: HEROKU_API_KEY", file=sys.stderr)
    print("You can obtain it using \"heroku auth:token\" command", file=sys.stderr)
    sys.exit(1)

subprocess.run(
    ['docker', 'login', '--username=_', '--password-stdin', 'registry.heroku.com'], check=True, input=heroku_api_key
)

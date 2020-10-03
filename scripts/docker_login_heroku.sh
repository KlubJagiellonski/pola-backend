#!/usr/bin/env bash

set -euo pipefail

if [[ -z "${HEROKU_API_KEY=}" ]]; then
  echo "Missing environment variable: HEROKU_API_KEY"
  echo "You can obtain it using \"heroku auth:token\" command"
  exit 1
fi

echo "${HEROKU_API_KEY}" | docker login --username=_  --password-stdin registry.heroku.com

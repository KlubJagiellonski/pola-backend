#!/usr/bin/env bash


set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

function usage() {
CMDNAME="$(basename -- "$0")"

  cat << EOF
Usage: ${CMDNAME} <app_name>

Fetch preferred domain for Heroku aapp.

EOF

}

if [[ "$#" -ne 1 ]]; then
    echo "You must provide a one command."
    echo
    usage
    exit 1
fi

APP_NAME="${1}"

DOMAIN_LIST=$(\
  heroku domains --app "${APP_NAME}" --json \
    | jq '.[].hostname' -r \
    | sed "s@^@https://@g"
  )
echo "$DOMAIN_LIST" | tail -n 1

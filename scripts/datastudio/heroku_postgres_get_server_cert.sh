#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

function usage() {
CMDNAME="$(basename -- "$0")"

  cat << EOF
Usage: ${CMDNAME} <app_name>

Fetch server certificate for Heroku app.

EOF

}

if [[ "$#" -ne 0 ]]; then
    echo "You must provide one argument."
    echo
    usage
    exit 1
fi

APP_NAME="${1}"

DATABASE_URL="$(heroku config --app "${APP_NAME}" --json | jq -r ".DATABASE_URL")"
"${SCRIPT_DIR}/postgres_get_server_cert.py" "${DATABASE_URL}"

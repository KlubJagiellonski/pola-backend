#!/usr/bin/env bash

set -euo pipefail

function usage() {
CMDNAME="$(basename -- "$0")"

  cat << EOF
Usage: ${CMDNAME} <app_name> [<credentials_name>]

Generate client certificate for Postgress connection

EXAMPLE:
$ ${CMDNAME} pola-app
$ ${CMDNAME} pola-app datastudio-kj

EOF

}

if [[ "$#" -lt 1 ]]; then
    echo "You must provide at least one argument."
    echo
    usage
    exit 1
fi

APP_NAME="${1}"
CREDENTIAL_NAME="${2:-default}"
DATABASE_URL="$(heroku pg:credentials:url DATABASE_URL --app "${APP_NAME}" --name "${CREDENTIAL_NAME}" | grep -e "Connection URL" -A2 | tail -n+2 | xargs)"

[[ ${DATABASE_URL} =~ ([^:]*)://([^:@]*):?([^@]*)@?([^/:]*):?([0-9]*)/([^\?]*)\??(.*) ]] && \
    detected_backend=${BASH_REMATCH[1]} &&
    detected_user=${BASH_REMATCH[2]} &&
    detected_password=${BASH_REMATCH[3]} &&
    detected_host=${BASH_REMATCH[4]} &&
    detected_port=${BASH_REMATCH[5]} &&
    detected_schema=${BASH_REMATCH[6]}

if [[ ${detected_backend} != "posttgres" ]]; then
    echo "Unknown backend: ${detected_backend}"
    exit 1
fi
if [[ -z "${detected_port=}" ]]; then
    detected_port=5432
fi
(
export "PGHOST=${detected_host}" "PGPORT=${detected_port}" "PGUSER=${detected_user}" "PGPASSWORD=${detected_password}" "PGDATABASE=${detected_schema}";
psql
)

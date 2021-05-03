#!/usr/bin/env bash

set -euo pipefail

function usage() {
CMDNAME="$(basename -- "$0")"

  cat << EOF
Usage: ${CMDNAME} <client_key_path> <client_cert_path>

Generate client certificate for Postgress connection

EXAMPLE:
$ ${CMDNAME} client.key client.crt

EOF

}

if [[ "$#" -ne 2 ]]; then
    echo "You must provide two arguments."
    echo
    usage
    exit 1
fi

CLIENT_KEY_PATH="${1}"
CLIENT_CERT_PATH="${2}"

openssl req \
       -newkey rsa:2048 -nodes -keyout "${CLIENT_KEY_PATH}" \
       -x509 -days 365 -out "${CLIENT_CERT_PATH}" \
       -subj "/C=PL/ST=$(hostname)/L=pola-app/O=pola-app/OU=pola-app/CN=pola-app"

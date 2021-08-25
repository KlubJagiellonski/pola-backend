#!/usr/bin/env bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT_NAME="${BASH_SOURCE[0]}"
VENVS_DIR="${SCRIPT_DIR}/.virtualenvs"

function tap_postgres_config() {
  jq '{
    "dbname": $PGDATABASE,
    "host": $PGHOST,
    "port": $PGPORT,
    "user": $PGUSER,
    "password": $PGPASSWORD,
  }' \
  -n \
  --arg PGDATABASE "$PGDATABASE" \
  --arg PGHOST "$PGHOST"  \
  --arg PGPASSWORD "$PGPASSWORD"  \
  --arg PGPORT "$PGPORT"  \
  --arg PGUSER "$PGUSER"
}

TAP_POSTGRES_BIN="${VENVS_DIR}/tap-postgres/bin/tap-postgres"

exec "${TAP_POSTGRES_BIN}" -c <(tap_postgres_config) "${@}"

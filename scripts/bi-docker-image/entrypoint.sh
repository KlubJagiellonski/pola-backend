#!/usr/bin/env bash

COMMAND="${1}"
set -euo pipefail

if command -v "${COMMAND}"; then
  echo "Running: ${*}"
  exec "${@}"
fi

exec "dbt" "${@}"

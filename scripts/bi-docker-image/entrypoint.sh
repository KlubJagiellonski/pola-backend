#!/usr/bin/env bash

COMMAND="${1}"
set -euo pipefail

if command -v -- "${COMMAND}"; then
  echo "Running: ${*}" >&2
  exec "${@}"
fi

exec "dbt" "${@}"

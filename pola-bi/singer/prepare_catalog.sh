#!/usr/bin/env bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

${SCRIPT_DIR}/tap_postgres.sh -d | jq '.streams|=map(select(.table_name | startswith("bi")))' > catalog.json

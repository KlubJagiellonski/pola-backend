#!/usr/bin/env bash

set -euo pipefail
cd "$( dirname "${BASH_SOURCE[0]}" )"

COMPOSE_FILE=${COMPOSE_FILE:-"$PWD/docker-compose.dbt.yaml:$PWD/docker-compose.dbt-local.yaml:$PWD/docker-compose.yaml"}
export COMPOSE_FILE
echo "COMPOSE_FILE=${COMPOSE_FILE}"
docker-compose run --rm dbt "${@}"

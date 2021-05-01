#!/usr/bin/env bash

set -euo pipefail

BOLD=$'\e[36m'
RESET=$'\e[0m'

function start_group {
  if [ "${GITHUB_ACTIONS:=}" == "true" ]; then
    echo "::group::${1}";
  else
    echo ":::${BOLD}${1}${RESET}:::"
  fi
}

function end_group {
  if [ "${GITHUB_ACTIONS:=}" == "true" ]; then
    echo "::endgroup::";
  fi
}

docker-compose ps --services | while read -r service_name; do
  start_group "${service_name}";
  docker-compose pull -- "${service_name}";
  end_group;
done

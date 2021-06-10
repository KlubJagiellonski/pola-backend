#!/usr/bin/env bash

set -euo pipefail

test -v GITHUB_BRANCH

if [[ "$(echo "${GITHUB_BRANCH}" | cut -d / -f 3)" == "prod" ]]; then
  echo "pola-app"
elif [[ "$(echo "${GITHUB_BRANCH}" | cut -d / -f 3)" == "master" ]]; then
  echo "pola-staging"
else
  >&2 echo "Unknown app."
  exit 1;
fi

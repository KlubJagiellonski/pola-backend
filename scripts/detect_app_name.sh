#!/usr/bin/env bash

set -euo pipefail

export
if [[ -z "${GITHUB_BRANCH}" ]]; then
  echo "GITHUB_BRANCH variable is unset"
  exit 1
fi

if [[ "$(echo "${GITHUB_BRANCH}" | cut -d / -f 3)" == "prod" ]]; then
  echo "pola-app"
elif [[ "$(echo "${GITHUB_BRANCH}" | cut -d / -f 3)" == "master" ]]; then
  echo "pola-staging"
else
  >&2 echo "Unknown app. Current branch: ${GITHUB_BRANCH}"
  exit 1;
fi

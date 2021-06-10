#!/usr/bin/env bash

set -euo pipefail

if [[ -z "${GITHUB_REF}" ]]; then
  >&2 echo "GITHUB_REF variable is unset"
  exit 1
fi

if [[ "$(echo "${GITHUB_REF}" | cut -d / -f 3)" == "prod" ]]; then
  echo "pola-app"
elif [[ "$(echo "${GITHUB_REF}" | cut -d / -f 3)" == "master" ]]; then
  echo "pola-staging"
else
  >&2 echo "Unknown app. Current branch: ${GITHUB_REF}"
  exit 1;
fi

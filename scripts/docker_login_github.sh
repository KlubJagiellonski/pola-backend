#!/usr/bin/env bash

set -euo pipefail

# shellcheck source=scripts/_base_variables.sh
source "$( dirname "${BASH_SOURCE[0]}" )/_base_variables.sh"

if [[ -z "${GITHUB_TOKEN=}" ]]; then
  echo "Missing environment variable: GITHUB_TOKEN"
  exit 1
fi

USERNAME="$(echo "${GITHUB_ORGANIZATION}" | tr '[:upper:]' '[:lower:]')"
readonly USERNAME

echo "Logging in to the Github Registry as ${USERNAME}."
echo "${GITHUB_TOKEN}" | docker login \
  --username "${USERNAME}" \
  --password-stdin \
  "https://docker.pkg.github.com"
echo "Logged in"

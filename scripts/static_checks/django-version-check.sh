#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../../" && pwd )"
cd "$ROOT_DIR"

DJANGO_VERSION_PROD=$(grep -i "^django==" "requirements/production.txt" | cut -d "=" -f 3)
SED_EXPRESSION="s/DJANGO_VERSION=\${DJANGO_VERSION-.*}/DJANGO_VERSION=\${DJANGO_VERSION-${DJANGO_VERSION_PROD}}/g"

PLATFORM="$(uname)"
if [[ "${PLATFORM}" == 'Linux' ]]; then
  sed -i "${SED_EXPRESSION}" docker-compose.yaml
elif [[ "${PLATFORM}" == 'Darwin' ]]; then
  sed -i '' "${SED_EXPRESSION}" docker-compose.yaml
else
  echo "Unknown system: ${PLATFORM}"
  exit 1;
fi

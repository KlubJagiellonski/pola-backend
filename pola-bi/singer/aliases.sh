#!/usr/bin/env bash

# shellcheck disable=SC2034
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT_NAME="${BASH_SOURCE[0]}"
VENVS_DIR="${SCRIPT_DIR}/.virtualenvs"

while read package_info; do
  package_name="$(echo "${package_info}" | cut -d "=" -f 1)"
  echo "alias ${package_name}=${VENVS_DIR}/${package_name}/bin/${package_name}"
done < "${SCRIPT_DIR}/requirements.txt"

echo '# To install aliases:'
echo "# eval \$(bash '${SCRIPT_NAME}')"

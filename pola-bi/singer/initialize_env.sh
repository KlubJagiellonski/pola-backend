#!/usr/bin/env bash
set -euo pipefail

# shellcheck disable=SC2034
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENVS_DIR="${SCRIPT_DIR}/.virtualenvs"

while read package_info; do
  package_name="$(echo "${package_info}" | cut -d "=" -f 1)"
  echo "Installing '${package_info}' package"
  python3 -m venv "${VENVS_DIR}/${package_name}"
  source "${VENVS_DIR}/${package_name}/bin/activate"
  pip install -U pip
  pip install "${package_info}"
done < "${SCRIPT_DIR}/requirements.txt"

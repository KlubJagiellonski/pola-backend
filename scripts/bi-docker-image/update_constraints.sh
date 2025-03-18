#!/usr/bin/env bash

set -euo pipefail
# shellcheck source=scripts/bi-docker-image/_functions.sh
source "$( dirname "${BASH_SOURCE[0]}" )/_functions.sh"

initialize
update_constraints

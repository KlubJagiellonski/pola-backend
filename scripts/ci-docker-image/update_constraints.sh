#!/usr/bin/env bash

set -euo pipefail
# shellcheck source=scripts/ci-docker-image/_functions.sh
source "$( dirname "${BASH_SOURCE[0]}" )/_functions.sh"

initialize
update_constraints

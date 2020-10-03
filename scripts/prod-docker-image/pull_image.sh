#!/usr/bin/env bash

set -euo pipefail
# shellcheck source=scripts/prod-docker-image/_functions.sh
source "$( dirname "${BASH_SOURCE[0]}" )/_functions.sh"

initialize
pull_image

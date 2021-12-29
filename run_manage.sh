#!/usr/bin/env bash

set -euo pipefail

docker-compose run --rm --no-deps web ./manage.py "${@}"

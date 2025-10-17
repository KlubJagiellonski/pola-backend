#!/usr/bin/env bash

set -euo pipefail

docker compose run --rm web pytest -n auto --junitxml=junit.xml -o junit_family=legacy

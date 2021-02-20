#!/usr/bin/env bash

set -euo pipefail

docker-compose run --rm web bash -x -c "
  coverage run \
    --source=. \
    /app/manage.py test \
      --verbosity=2 \
      --keepdb;
  EXIT_CODE=\$?;
  coverage xml;
  exit \${EXIT_CODE};
"

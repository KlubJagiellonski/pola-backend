#!/usr/bin/env bash


set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# shellcheck source=scripts/_base_variables.sh
source "$SCRIPT_DIR/_base_variables.sh"

IMAGE_NAME="${2:-"${PROD_IMAGE_NAME}"}"

function usage() {
CMDNAME="$(basename -- "$0")"

  cat << EOF
Usage: ${CMDNAME} <app_name> [<image_name>]

Deploy docker image to Heroku.

By default, it deploys "${PROD_IMAGE_NAME}" image.

EOF

}

if [[ "$#" -eq 0 ]]; then
    echo "You must provide at least one command."
    echo
    usage
    exit 1
fi

APP_NAME="${1}"

if [[ "$(docker images -q "${IMAGE_NAME}" 2> /dev/null)" == "" ]]; then
  echo "Image missing: ${IMAGE_NAME}"
  exit
fi

HEROKU_REGISTRY_URL="registry.heroku.com/${APP_NAME}"

docker tag "${IMAGE_NAME}:latest" "${HEROKU_REGISTRY_URL}/web"
docker build prod-docker-image \
  --build-arg "BASE_IMAGE=${IMAGE_NAME}" \
  --file=prod-docker-image/Dockerfile.release \
  --tag "${HEROKU_REGISTRY_URL}/release"
docker tag "${IMAGE_NAME}:latest" "${IMAGE_NAME}:${APP_NAME}"

docker push "${HEROKU_REGISTRY_URL}/release"
docker push "${HEROKU_REGISTRY_URL}/web"
heroku container:release --verbose --app "${APP_NAME}" web release

DOMAIN_LIST=$(\
  heroku domains --app "${APP_NAME}" --json \
    | jq 'map(.hostname) | join(", ")' -r \
    | sed "s@^@https://@g"
  )

docker push "${IMAGE_NAME}:${APP_NAME}"
echo "App deployed: ${DOMAIN_LIST}"

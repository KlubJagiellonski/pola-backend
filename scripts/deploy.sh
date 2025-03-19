#!/usr/bin/env bash


set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

IMAGE_TAG="${IMAGE_TAG:="latest"}"
PROD_IMAGE_NAME="pola-backend_prod"

IMAGE_NAME="${2:-"${PROD_IMAGE_NAME}:${IMAGE_TAG}"}"

function usage() {
CMDNAME="$(basename -- "$0")"

  cat << EOF
Usage: ${CMDNAME} <app_name> [<image_name>]

Deploy docker image to Heroku.

By default, it deploys "${PROD_IMAGE_NAME}:${IMAGE_TAG}" image.

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

echo "Start deploying '${IMAGE_NAME}' to '${APP_NAME}' app"
echo "Preparing images:"
docker tag "${IMAGE_NAME}" "${HEROKU_REGISTRY_URL}/web"
docker build prod-docker-image \
  --build-arg "BASE_IMAGE=${IMAGE_NAME}" \
  --file=prod-docker-image/Dockerfile.release \
  --tag "${HEROKU_REGISTRY_URL}/release"
docker tag "${IMAGE_NAME}" "${PROD_IMAGE_NAME}:${APP_NAME}"
docker images -a

echo "Publishing images to Heroku registry"
docker push "${HEROKU_REGISTRY_URL}/release"
docker push "${HEROKU_REGISTRY_URL}/web"
echo "Start a new release in Heroku"
heroku container:release --verbose --app "${APP_NAME}" web release

DOMAIN_LIST=$(\
  heroku domains --app "${APP_NAME}" --json \
    | jq '.[].hostname' -r \
    | sed "s@^@https://@g"
  )

echo "Pushing image to GitHub registry"
GITHUB_REGISTRY_IMAGE_NAME="ghcr.io/klubjagiellonski/pola-backend"
docker tag "${IMAGE_NAME}" "${GITHUB_REGISTRY_IMAGE_NAME}:${APP_NAME}"
docker push "${GITHUB_REGISTRY_IMAGE_NAME}:${APP_NAME}"
echo "App deployed: ${DOMAIN_LIST}"

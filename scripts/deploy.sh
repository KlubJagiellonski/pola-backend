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
echo "Deploying to app: ${APP_NAME}"
echo "Image name: ${IMAGE_NAME}"

if [[ "$(docker images -q "${IMAGE_NAME}" 2> /dev/null)" == "" ]]; then
  echo "Image missing: ${IMAGE_NAME}"
  exit 1
fi

HEROKU_REGISTRY_URL="registry.heroku.com/${APP_NAME}"

echo "Preparing images:"
docker tag "${IMAGE_NAME}" "${HEROKU_REGISTRY_URL}/web"
docker build prod-docker-image \
  --build-arg "BASE_IMAGE=${IMAGE_NAME}" \
  --file=prod-docker-image/Dockerfile.release \
  --tag "${HEROKU_REGISTRY_URL}/release"
echo ""

echo "Publishing images to Heroku registry"
docker push "${HEROKU_REGISTRY_URL}/release"
docker push "${HEROKU_REGISTRY_URL}/web"
echo ""

echo "Start a new release in Heroku"
heroku container:release --verbose --app "${APP_NAME}" web release
echo ""

echo "Pushing image to GitHub registry"
GITHUB_REGISTRY_IMAGE_NAME="ghcr.io/klubjagiellonski/pola-backend"
docker tag "${IMAGE_NAME}" "${GITHUB_REGISTRY_IMAGE_NAME}:${APP_NAME}"
docker push "${GITHUB_REGISTRY_IMAGE_NAME}:${APP_NAME}"
echo ""
DOMAIN_LIST=$(\
  heroku domains --app "${APP_NAME}" --json \
    | jq '.[].hostname' -r \
    | sed "s@^@https://@g"
  )
echo "App deployed: ${DOMAIN_LIST}"

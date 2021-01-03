#!/usr/bin/env bash


set -euo pipefail

DOCKER_ARGS=(
  --rm
  --interactive
  --network pola-backend_default
  -w "$PWD"
  -v "$PWD:$PWD"
  -e "AWS_ACCESS_KEY_ID=minio"
  -e "AWS_SECRET_ACCESS_KEY=minio123"
  -e "AWS_EC2_METADATA_DISABLED=true"
)

if [ -t 0 ] ; then
  DOCKER_ARGS+=(
    --tty
  )
fi

if [[ "$#" -eq 0 ]]; then
  docker run "${DOCKER_ARGS[@]}" \
    --entrypoint bash \
    amazon/aws-cli
else
  docker run "${DOCKER_ARGS[@]}" \
    amazon/aws-cli \
      --endpoint-url http://minio:9000 \
      "${@}"
fi

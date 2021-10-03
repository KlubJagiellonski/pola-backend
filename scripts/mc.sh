#!/usr/bin/env bash


set -euo pipefail

DOCKER_ARGS=(
  --rm
  --interactive
  --network pola-backend_default
  -w "$PWD"
  -v "$PWD:$PWD"
  -e "MC_HOST_local=http://minio:minio123@minio:9000/"
)

if [ -t 0 ] ; then
  DOCKER_ARGS+=(
    --tty
  )
fi

if [[ "$#" -eq 0 ]]; then
  docker run "${DOCKER_ARGS[@]}" \
    minio/mc
else
  docker run "${DOCKER_ARGS[@]}" \
    minio/mc \
      "${@}"
fi

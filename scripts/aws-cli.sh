#!/usr/bin/env bash


set -euo pipefail

if [[ -z "${DJANGO_AWS_ACCESS_KEY_ID=}" ]]; then
  echo "Missing environment variable: DJANGO_AWS_ACCESS_KEY_ID"
  exit 1
fi

if [[ -z "${DJANGO_AWS_SECRET_ACCESS_KEY=}" ]]; then
  echo "Missing environment variable: DJANGO_AWS_SECRET_ACCESS_KEY"
  exit 1
fi

DOCKER_ARGS=(
  --rm
  --interactive
  -w "$PWD"
  -v "$PWD:$PWD"
  -e "AWS_ACCESS_KEY_ID=${DJANGO_AWS_ACCESS_KEY_ID}"
  -e "AWS_SECRET_ACCESS_KEY=${DJANGO_AWS_SECRET_ACCESS_KEY}"
)

if [ -t 0 ] ; then
  DOCKER_ARGS+=(
    --tty
  )
fi

if [[ "$#" -eq 0 ]]; then
  docker run "${DOCKER_ARGS[@]}" --entrypoint bash amazon/aws-cli
else
  docker run "${DOCKER_ARGS[@]}" amazon/aws-cli "${@}"
fi

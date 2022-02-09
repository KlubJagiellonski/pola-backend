#!/usr/bin/env bash

function initialize() {
  # shellcheck source=scripts/_base_variables.sh
  source "$( dirname "${BASH_SOURCE[0]}" )/../_base_variables.sh"

  cd "$( dirname "${BASH_SOURCE[0]}" )/../../" || exit 1
}

function build_image() {
    echo "Building image: ${BI_IMAGE_NAME}:${IMAGE_TAG}"

    docker pull "${BI_IMAGE_NAME}:latest" || true

    if [[ ${PREPARE_BUILDX_CACHE:-"false"} == "true" ]]; then
          extra_build_args+=(
              "--cache-to=type=registry,ref=${BI_IMAGE_NAME}:cache"
              "--load"
          )
      fi

    docker build \
      "." \
      --pull \
      "${extra_build_args[@]}" \
      --file=scripts/bi-docker-image/Dockerfile \
      --tag "${BI_IMAGE_NAME}:${IMAGE_TAG}"

    docker tag "${BI_IMAGE_NAME}:${IMAGE_TAG}" "pola-bi:latest"
    echo
    echo
}

function verify_image() {
    echo "Verifying image: ${BI_IMAGE_NAME}:${IMAGE_TAG}"
    docker run --rm "${BI_IMAGE_NAME}:${IMAGE_TAG}" pip freeze
    echo "=== Compare requirements ==="
    diff \
      <(docker run --entrypoint /bin/bash --rm "${BI_IMAGE_NAME}:${IMAGE_TAG}" -c "pip freeze" | sort) \
      <(sort < ./requirements/bi.txt)
    echo "======"
    echo
    echo
}

function push_image() {
    echo "Pushing image: ${BI_IMAGE_NAME}:${IMAGE_TAG}"
    docker tag "pola-bi" "${BI_IMAGE_NAME}:${IMAGE_TAG}"
    docker push "${BI_IMAGE_NAME}:${IMAGE_TAG}"
    echo
    echo
}

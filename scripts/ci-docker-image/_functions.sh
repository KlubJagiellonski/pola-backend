#!/usr/bin/env bash

function initialize() {
  # shellcheck source=scripts/_base_variables.sh
  source "$( dirname "${BASH_SOURCE[0]}" )/../_base_variables.sh"

  cd "$( dirname "${BASH_SOURCE[0]}" )/../../" || exit 1
}

function build_image() {
  echo "Building image: ${CI_IMAGE_NAME}:${IMAGE_TAG}"

  docker pull "${CI_IMAGE_NAME}:latest" || true

  if [[ ! "$(docker images -q "${CI_IMAGE_NAME}" 2> /dev/null)" == "" ]]; then
      extra_build_args=("--cache-from=${CI_IMAGE_NAME}:latest")
  fi
  echo "Building image: ${CI_IMAGE_NAME}:${IMAGE_TAG}"

  docker build \
    . \
    "${extra_build_args[@]}" \
    --build-arg PYTHON_VERSION="${PYTHON_VERSION}" \
    --build-arg DJANGO_VERSION="${DJANGO_VERSION}" \
    --file=scripts/ci-docker-image/Dockerfile \
    --tag "${CI_IMAGE_NAME}:${IMAGE_TAG}"

  docker tag "${CI_IMAGE_NAME}:${IMAGE_TAG}" "pola-backend_web:latest"
}

function verify_image() {
    echo "Verifying image: ${CI_IMAGE_NAME}:${IMAGE_TAG}"
    docker run --rm "${CI_IMAGE_NAME}:${IMAGE_TAG}" pip freeze
    echo "=== Compare requirements ==="
    diff \
      <(
        docker run --entrypoint /bin/bash --rm "${CI_IMAGE_NAME}:${IMAGE_TAG}" -c "pip freeze" | \
          grep -v -i "Django==" | sort \
      ) \
      <(sort < ./requirements/ci.txt | grep -v -i "Django==")
    echo "======"
}

function push_image() {
    echo "Pushing image: ${CI_IMAGE_NAME}:${IMAGE_TAG}"
    docker tag "pola-backend_web" "${CI_IMAGE_NAME}:${IMAGE_TAG}"
    docker push "${CI_IMAGE_NAME}:${IMAGE_TAG}"
}

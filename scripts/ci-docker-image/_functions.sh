#!/usr/bin/env bash

function initialize() {
    # shellcheck source=scripts/_base_variables.sh
    source "$( dirname "${BASH_SOURCE[0]}" )/../_base_variables.sh"

    cd "$( dirname "${BASH_SOURCE[0]}" )/../../" || exit 1
}

function build_image() {
    echo "Building image: ${CI_IMAGE_NAME}:${IMAGE_TAG}"

    extra_build_args=()

    if [[ ${PREPARE_BUILDX_CACHE:-"false"} == "true" ]]; then
        extra_build_args+=(
            "--cache-to=type=registry,ref=${CI_IMAGE_NAME}:cache"
            "--load"
            "--builder" "pola_cache"
        )
        docker buildx inspect pola_cache || docker buildx create --name pola_cache
    fi

    DOCKER_BUILDKIT=1 docker buildx build \
        "." \
        --pull \
        "${extra_build_args[@]}" \
        --build-arg PYTHON_VERSION="${PYTHON_VERSION}" \
        --build-arg DJANGO_VERSION="${DJANGO_VERSION}" \
        "--cache-from=${CI_IMAGE_NAME}:cache" \
        --file=scripts/ci-docker-image/Dockerfile \
        --tag "${CI_IMAGE_NAME}:${IMAGE_TAG}"

    docker tag "${CI_IMAGE_NAME}:${IMAGE_TAG}" "pola-backend_web:latest"
    echo
    echo
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
    echo
    echo
}

function push_image() {
    echo "Pushing image: ${CI_IMAGE_NAME}:${IMAGE_TAG}"
    docker tag "pola-backend_web" "${CI_IMAGE_NAME}:${IMAGE_TAG}"
    docker push "${CI_IMAGE_NAME}:${IMAGE_TAG}"
    echo
    echo
}

#!/usr/bin/env bash

function initialize() {
    # shellcheck source=scripts/_base_variables.sh
    source "$( dirname "${BASH_SOURCE[0]}" )/../_base_variables.sh"

    cd "$( dirname "${BASH_SOURCE[0]}" )/../../" || exit 1
}

function build_image() {
    echo "Building image: ${PROD_IMAGE_NAME}:${IMAGE_TAG}"
    echo "IMAGE_TAG=${IMAGE_TAG}"

    RELEASE_SHA=$(git rev-parse HEAD)
    readonly RELEASE_SHA
    echo "RELEASE_SHA=${RELEASE_SHA}"

    extra_build_args=()

    if [[ ${PREPARE_BUILDX_CACHE:-"false"} == "true" ]]; then
        extra_build_args+=(
            "--cache-to=type=registry,ref=${PROD_IMAGE_NAME}:cache"
            "--load"
            "--builder" "pola_cache"
        )
        docker buildx inspect pola_cache || docker buildx create --name pola_cache
    fi

    DOCKER_BUILDKIT=1 docker buildx build \
        "." \
        "--file=scripts/prod-docker-image/Dockerfile" \
        --pull \
        "${extra_build_args[@]}" \
        "--cache-from=${PROD_IMAGE_NAME}:cache" \
        --build-arg "RELEASE_SHA=${RELEASE_SHA}" \
        --tag "${PROD_IMAGE_NAME}:${IMAGE_TAG}"
        echo
        echo
}

function verify_image() {
    echo "Verifying image: ${PROD_IMAGE_NAME}:${IMAGE_TAG}"
    docker run --rm "${PROD_IMAGE_NAME}:${IMAGE_TAG}" pip freeze
    echo "=== Compare requirements ==="
    diff \
      <(docker run --entrypoint /bin/bash --rm "${PROD_IMAGE_NAME}:${IMAGE_TAG}" -c "pip freeze" | sort) \
      <(sort < ./requirements/production.txt)
    echo "======"
    echo
    echo
}

function push_image() {
    echo "Pushing image: ${PROD_IMAGE_NAME}:${IMAGE_TAG}"
    docker push "${PROD_IMAGE_NAME}:${IMAGE_TAG}"
    docker tag "${PROD_IMAGE_NAME}:${IMAGE_TAG}" "${PROD_IMAGE_NAME}:latest"
    docker push "${PROD_IMAGE_NAME}:latest"
    echo
    echo
}

function pull_image() {
    echo "Pulling image: ${PROD_IMAGE_NAME}:${IMAGE_TAG}"
    docker pull "${PROD_IMAGE_NAME}:${IMAGE_TAG}"
    echo
    echo
}

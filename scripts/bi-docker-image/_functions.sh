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
            "--cache-to=type=registry,ref=${BI_IMAGE_NAME}:cache,mode=max"
            "--load"
            "--builder" "pola_cache"
        )
        docker buildx inspect pola_cache || docker buildx create --name pola_cache
      fi

    DOCKER_BUILDKIT=1 docker buildx build \
      "." \
      --pull \
      "${extra_build_args[@]}" \
      "--cache-from=${BI_IMAGE_NAME}:cache" \
      --file=scripts/bi-docker-image/Dockerfile \
      --tag "${BI_IMAGE_NAME}:${IMAGE_TAG}"

    docker tag "${BI_IMAGE_NAME}:${IMAGE_TAG}" "pola-bi:latest"
    echo
    echo "Image build completed"
    echo "Tags:"
    echo " ${BI_IMAGE_NAME}:${IMAGE_TAG}"
    echo " pola-bi:latest"
    echo
}

function verify_image() {
    echo "Verifying image: ${BI_IMAGE_NAME}:${IMAGE_TAG}"
    docker run --rm "${BI_IMAGE_NAME}:${IMAGE_TAG}" pip freeze
    echo "=== Compare constraints ==="
    diff -y \
      <(docker run --entrypoint /bin/bash --rm "${BI_IMAGE_NAME}:${IMAGE_TAG}" -c "pip freeze" | LC_ALL=C sort -f) \
      <(LC_ALL=C sort -f < ./dependencies/constraints-bi.txt)
    echo "======"
    echo
    echo
}

function update_constraints() {
    echo "Updating constraints"
    docker run --entrypoint /bin/bash --rm "${BI_IMAGE_NAME}:${IMAGE_TAG}" -c "pip freeze" | LC_ALL=C sort -f > ./dependencies/constraints-bi.txt
    echo
    echo "Updated constraints in file: ./dependencies/constraints-bi.txt"
    echo
}

function push_image() {
    echo "Pushing image: ${BI_IMAGE_NAME}:${IMAGE_TAG}"
    docker tag "pola-bi" "${BI_IMAGE_NAME}:${IMAGE_TAG}"
    docker push "${BI_IMAGE_NAME}:${IMAGE_TAG}"
    echo
    echo
}

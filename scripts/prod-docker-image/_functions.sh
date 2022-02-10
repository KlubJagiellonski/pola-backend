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
    GIT_REF=$(git rev-parse HEAD)
    IMAGE_DESCRIPTION="Pola pomoze Ci odnaleźć polskie wyroby. Zabierając Pole na zakupy odnajdujesz produkty \"z duszą\" i wspierasz polską gospodarkę."

    BASE_PYTHON_IMAGE="python:${PYTHON_VERSION}-slim-buster"
    docker pull "${BASE_PYTHON_IMAGE}"
    BASE_PYTHON_IMAGE_DIGEST=$(docker inspect python:3.9-slim-buster --format='{{ index (split (index .RepoDigests 0) "@") 1 }}')

    DOCKER_BUILDKIT=1 docker buildx build \
        . \
        --file=scripts/prod-docker-image/Dockerfile \
        --pull \
        "${extra_build_args[@]}" \
        "--cache-from=${PROD_IMAGE_NAME}:cache" \
        --build-arg "BASE_PYTHON_IMAGE=${BASE_PYTHON_IMAGE}@${BASE_PYTHON_IMAGE_DIGEST}" \
        --build-arg "RELEASE_SHA=${RELEASE_SHA}" \
        --label "org.opencontainers.image.created=$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
        --label "org.opencontainers.image.authors=pola@klubjagiellonski.pl" \
        --label "org.opencontainers.image.url=https://www.pola-app.pl/" \
        --label "org.opencontainers.image.documentation=https://github.com/KlubJagiellonski/pola-backend/blob/${GIT_REF}/README.rst" \
        --label "org.opencontainers.image.source=${CONTAINER_REGISTRY}" \
        --label "org.opencontainers.image.version=DEV" \
        --label "org.opencontainers.image.revision=${GIT_REF}" \
        --label "org.opencontainers.image.vendor=Klub Jagielloński" \
        --label "org.opencontainers.image.licenses=BSD-3-Clause" \
        --label "org.opencontainers.image.ref.name=pola-backend" \
        --label "org.opencontainers.image.title=Pola-backend - based on ${BASE_PYTHON_IMAGE}" \
        --label "org.opencontainers.image.description=${IMAGE_DESCRIPTION}" \
        --label "org.opencontainers.image.base.digest=${BASE_PYTHON_IMAGE_DIGEST}" \
        --label "org.opencontainers.image.base.name=${BASE_PYTHON_IMAGE}" \
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

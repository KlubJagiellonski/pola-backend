#!/usr/bin/env bash
# shellcheck disable=SC2034
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Registry
GITHUB_REPOSITORY="${GITHUB_REPOSITORY:="KlubJagiellonski/pola-backend"}"
readonly GITHUB_REPOSITORY
GITHUB_ORGANIZATION="${GITHUB_ORGANIZATION:="KlubJagiellonski"}"
readonly GITHUB_ORGANIZATION
CONTAINER_REGISTRY="${CONTAINER_REGISTRY:="ghcr.io/${GITHUB_REPOSITORY}"}"
CONTAINER_REGISTRY="$(echo "${CONTAINER_REGISTRY}" | tr '[:upper:]' '[:lower:]')"
readonly CONTAINER_REGISTRY

# Django/Python
DJANGO_VERSION_PROD=$(grep -i "^django==" "${SCRIPT_DIR}/../dependencies/constraints-production.txt" | cut -d "=" -f 3)
readonly DJANGO_VERSION_PROD
DJANGO_VERSION="${DJANGO_VERSION:="${DJANGO_VERSION_PROD}"}"
readonly DJANGO_VERSION
PYTHON_VERSION="${PYTHON_VERSION:="3.11"}"
readonly PYTHON_VERSION

# Docker
IMAGE_TAG="${IMAGE_TAG:="latest"}"
CI_IMAGE_NAME="${CONTAINER_REGISTRY}/pola-backend-${DJANGO_VERSION}-${PYTHON_VERSION}-ci"
BI_IMAGE_NAME="${CONTAINER_REGISTRY}/pola-bi"
PROD_IMAGE_NAME="${CONTAINER_REGISTRY}/pola-backend"

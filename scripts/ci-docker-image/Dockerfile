# syntax=docker/dockerfile:1.14.0
# check=error=true;experimental=all

ARG PYTHON_VERSION="3.11"
FROM python:${PYTHON_VERSION}-slim-bullseye

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        apt-transport-https \
        apt-utils \
        binutils \
        binutils-common \
        binutils-x86-64-linux-gnu \
        ca-certificates \
        curl \
        gcc \
        gnupg2 \
        libc6-dev \
        libcc1-0 \
        libffi-dev \
        linux-libc-dev \
        lsb-release \
        netcat-openbsd \
        pkg-config \
        libcairo2-dev \
    && curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && echo "deb https://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client-13 \
        libpq-dev \
        libpq5 \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
RUN mkdir /app
WORKDIR /app

COPY ./scripts/ci-docker-image/entrypoint.sh /entrypoint
ENTRYPOINT ["/entrypoint"]

RUN pip install --no-cache-dir --upgrade "pip" && pip --version

ARG DJANGO_VERSION
ENV DJANGO_VERSION=${DJANGO_VERSION}

RUN pip install --no-cache-dir --no-deps "django==${DJANGO_VERSION}"

COPY dependencies/constraints-ci.txt dependencies/requirements-ci.txt dependencies/requirements-production.txt dependencies/requirements-production.txt /app/dependencies/

RUN pip install \
      --no-cache-dir \
      "django==${DJANGO_VERSION}" \
      --requirement /app/dependencies/requirements-ci.txt \
      --constraint /app/dependencies/constraints-ci.txt && pip check

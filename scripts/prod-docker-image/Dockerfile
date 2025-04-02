# syntax=docker/dockerfile:1.14.0
# check=error=true
# CopyIgnoredFile is broken. It can not detect ./manage.py file, because it is excluded and added again.

ARG APP_UID="50000"
ARG APP_GID="50000"

ARG BASE_PYTHON_IMAGE="python:3.11-slim-bookworm"

######################### NODE BUILD IMAGE ##########################
# build-js builds the frontend assets
FROM node:17.3.0-alpine3.12 AS build-js

WORKDIR /app/

COPY package.json package-lock.json ./
RUN npm install --global gulp-cli \
    && npm install \
    && npm cache clean --force
COPY gulpfile.esm.js ./
COPY pola/assets pola/assets
RUN npm run build

######################### PYTHON BUILD IMAGE ########################
# build-py installs the python dependencies
FROM ${BASE_PYTHON_IMAGE} AS build-py

ENV APP_HOME=/opt/pola-backend/ \
    DEBIAN_FRONTEND=noninteractive \
    LANGUAGE=C.UTF-8 LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    LC_CTYPE=C.UTF-8 LC_MESSAGES=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
        g++ \
        gcc \
        git \
        gnupg2 \
        libc6-dev \
        libcairo2-dev \
        libcc1-0 \
        libpq-dev \
        libpq5 \
        linux-libc-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY dependencies/constraints-production.txt \
     dependencies/requirements-production.txt \
     dependencies/requirements-production-django.txt \
     /opt/pola-backend/dependencies/

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --user \
       -r /opt/pola-backend/dependencies/requirements-production.txt \
       -r /opt/pola-backend/dependencies/requirements-production-django.txt \
       -c /opt/pola-backend/dependencies/constraints-production.txt \
    && pip check \
    && find /root/.local/ -name '*.pyc' -delete \
    && find /root/.local/ -type d -name '__pycache__' -delete \
    # make sure that all directories and files in .local are also group accessible
    && find /root/.local -executable -print0 | xargs --null chmod g+x  \
    && find /root/.local -print0 | xargs --null chmod g+rw

######################### MAIN IMAGE ################################
# main is the final image that will be used in production
FROM ${BASE_PYTHON_IMAGE} AS main

ARG APP_UID
ARG APP_GID
ARG APP_USER_HOME_DIR=/home/pola-backend

ENV APP_UID=${APP_UID} \
    APP_GID=${APP_GID} \
    APP_USER_HOME_DIR=${APP_USER_HOME_DIR} \
    APP_HOME=/opt/pola-backend/ \
    DEBIAN_FRONTEND=noninteractive \
    LANGUAGE=C.UTF-8 LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    LC_CTYPE=C.UTF-8 LC_MESSAGES=C.UTF-8 \
    PATH="${APP_USER_HOME_DIR}/.local/bin:${PATH}" \
    GUNICORN_CMD_ARGS="--worker-tmp-dir /dev/shm"

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates dumb-init curl \
        postgresql-client libpq5 \
        # Required by encrypoint.sh
        netcat-openbsd \
        # Required by Heroku-exec
        openssh-client \
        openssh-server \
        iproute2 \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /var/log/* /var/cache/* /usr/share/doc /usr/share/man \
    && groupadd --gid "${APP_GID}" pola-backend \
    && useradd --uid "${APP_UID}" --gid "${APP_GID}" \
       --home "${APP_USER_HOME_DIR}" --create-home pola-backend \
    && mkdir -p "/opt/pola-backend" \
    && chown -R pola-backend:root "${APP_USER_HOME_DIR}" "/opt/pola-backend" \
    # Enable heroku-exec
    # See: https://devcenter.heroku.com/articles/exec#using-with-docker
    && chmod g=u /etc/passwd \
    && rm /bin/sh \
    && ln -s /bin/bash /bin/sh

COPY --chown=pola-backend:root --from=build-py /root/.local "${APP_USER_HOME_DIR}/.local"
COPY --chown=pola-backend:root --from=build-js /app/pola/static/ "/opt/pola-backend/pola/static/"

COPY ./scripts/prod-docker-image/heroku-exec.sh /app/.profile.d/heroku-exec.sh
COPY --chown=pola-backend:root ./scripts/prod-docker-image/entrypoint.sh /entrypoint
COPY --chown=pola-backend:root ./pola /opt/pola-backend/pola
COPY --chown=pola-backend:root ./manage.py /opt/pola-backend/

RUN chmod -R g+rw "/opt/pola-backend"

WORKDIR /opt/pola-backend

USER ${APP_UID}

EXPOSE 8080

ARG RELEASE_SHA
ENV RELEASE_SHA=${RELEASE_SHA}

ENTRYPOINT ["/usr/bin/dumb-init", "--", "/entrypoint"]
CMD ["gunicorn", "pola.config.wsgi:application"]

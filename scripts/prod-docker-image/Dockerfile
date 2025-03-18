ARG APP_UID="50000"
ARG APP_GID="50000"
ARG APP_HOME=/opt/pola-backend

ARG BASE_PYTHON_IMAGE="python:3.11-slim-bookworm"

######################### NODE BUILD IMAGE ##########################

FROM --platform=linux/amd64 node:16.13.1-alpine3.12 as build-js

WORKDIR /app/

COPY package.json package-lock.json ./
RUN npm install --global gulp-cli \
    && npm install \
    && npm cache clean --force
COPY gulpfile.esm.js ./
COPY pola/assets pola/assets
RUN npm run build

######################### PYTHON BUILD IMAGE ########################

FROM --platform=linux/amd64 ${BASE_PYTHON_IMAGE} as build-py

ENV APP_HOME=${APP_HOME} \
    DEBIAN_FRONTEND=noninteractive \
    LANGUAGE=C.UTF-8 LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    LC_CTYPE=C.UTF-8 LC_MESSAGES=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc g++ git libpq-dev libpq5 gnupg2 libc6-dev libcc1-0 linux-libc-dev\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY dependencies/constraints-production.txt \
     dependencies/requirements-production.txt \
     dependencies/requirements-production-django.txt \
     ${APP_HOME}/dependencies/

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --user \
       -r ${APP_HOME}/dependencies/requirements-production.txt \
       -r ${APP_HOME}/dependencies/requirements-production-django.txt \
       -c ${APP_HOME}/dependencies/constraints-production.txt \
    && pip check \
    && find /root/.local/ -name '*.pyc' -delete \
    && find /root/.local/ -type d -name '__pycache__' -delete \
    # make sure that all directories and files in .local are also group accessible
    && find /root/.local -executable -print0 | xargs --null chmod g+x  \
    && find /root/.local -print0 | xargs --null chmod g+rw

######################### MAIN IMAGE ################################

FROM --platform=linux/amd64 ${BASE_PYTHON_IMAGE} as main

ARG APP_UID
ARG APP_GID
ARG APP_USER_HOME_DIR=/home/pola-backend
ARG APP_HOME
ENV APP_UID=${APP_UID} \
    APP_GID=${APP_GID} \
    APP_USER_HOME_DIR=${APP_USER_HOME_DIR} \
    APP_HOME=${APP_HOME} \
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
    && mkdir -p "${APP_HOME}" \
    && chown -R pola-backend:root "${APP_USER_HOME_DIR}" "${APP_HOME}" \
    # Enable heroku-exec
    # See: https://devcenter.heroku.com/articles/exec#using-with-docker
    && chmod g=u /etc/passwd \
    && rm /bin/sh \
    && ln -s /bin/bash /bin/sh

COPY --chown=pola-backend:root --from=build-py /root/.local "${APP_USER_HOME_DIR}/.local"
COPY --chown=pola-backend:root --from=build-js /app/pola/static/ "${APP_HOME}/pola/static/"

COPY ./scripts/prod-docker-image/heroku-exec.sh /app/.profile.d/heroku-exec.sh
COPY --chown=pola-backend:root ./scripts/prod-docker-image/entrypoint.sh /entrypoint
COPY --chown=pola-backend:root ./ ${APP_HOME}
RUN chmod -R g+rw "${APP_HOME}"

WORKDIR ${APP_HOME}

USER ${APP_UID}

EXPOSE 8080

ARG RELEASE_SHA
ENV RELEASE_SHA=${RELEASE_SHA}

ENTRYPOINT ["/usr/bin/dumb-init", "--", "/entrypoint"]
CMD ["gunicorn", "pola.config.wsgi:application"]

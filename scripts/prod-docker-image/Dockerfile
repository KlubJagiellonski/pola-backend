ARG APP_UID="50000"
ARG APP_GID="50000"

ARG APP_HOME=/opt/pola-backend

ARG BASE_PYTHON_IMAGE="python:3.9-slim-buster"

######################### NODE BUILD IMAGE ##########################

FROM node:16.13.1-alpine3.12 as build-js

WORKDIR /app/
COPY ./package.json  /app/
COPY ./package-lock.json /app/
RUN npm install && npm cache clean --force
COPY ./gulpfile.esm.js /app/
COPY ./pola/assets /app/pola/assets
RUN npm run build

######################### PYTHON BUILD IMAGE ########################
ARG BASE_PYTHON_IMAGE
ARG APP_HOME

# hadolint ignore=DL3006
FROM ${BASE_PYTHON_IMAGE} as build-py

ARG APP_HOME
ENV APP_HOME=${APP_HOME}

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

# Make sure noninteractive debian install is used and language variables set
ENV DEBIAN_FRONTEND=noninteractive LANGUAGE=C.UTF-8 LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    LC_CTYPE=C.UTF-8 LC_MESSAGES=C.UTF-8

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        binutils \
        binutils-common \
        binutils-x86-64-linux-gnu \
        gcc \
        git \
        libc6-dev \
        libcc1-0 \
        libgcc-8-dev \
        libpq-dev \
        libpq5 \
        linux-libc-dev \
        netcat-openbsd \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# hadolint ignore=DL3044
ENV PYTHONUNBUFFERED=1 \
    PATH=${PATH}:/root/.local/bin
RUN mkdir -p /root/.local/bin && pip install --no-cache-dir --upgrade "pip" && pip --version

COPY ./requirements/production.txt ${APP_HOME}/requirements/

RUN pip install --no-cache-dir --user -r "${APP_HOME}/requirements/production.txt" \
    && pip check \
    && find /root/.local/ -name '*.pyc' -delete \
    && find /root/.local/ -type d -name '__pycache__' -delete \
    # make sure that all directories and files in .local are also group accessible
    && find /root/.local -executable -print0 | xargs --null chmod g+x  \
    && find /root/.local -print0 | xargs --null chmod g+rw

######################### MAIN IMAGE ################################
# hadolint ignore=DL3006
FROM ${BASE_PYTHON_IMAGE} as main

ARG APP_UID
ARG APP_GID
ARG APP_USER_HOME_DIR=/home/pola-backend
ARG APP_HOME
ENV APP_UID=${APP_UID} \
    APP_GID=${APP_GID} \
    APP_USER_HOME_DIR=${APP_USER_HOME_DIR} \
    APP_HOME=${APP_HOME}

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

# Make sure noninteractive debian install is used and language variables set
ENV DEBIAN_FRONTEND=noninteractive LANGUAGE=C.UTF-8 LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    LC_CTYPE=C.UTF-8 LC_MESSAGES=C.UTF-8

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        apt-transport-https \
        apt-utils \
        ca-certificates \
        curl \
        dumb-init \
        locales \
        lsb-release \
        postgresql-client \
        sudo \
        # Required by encrypoint.sh
        netcat \
        # Required by Heroku-exec
        openssh-client \
        openssh-server \
        iproute2 \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && addgroup --gid "${APP_GID}" "pola-backend" \
    && adduser --quiet "pola-backend" --uid "${APP_UID}" \
        --gid "${APP_GID}" \
        --home "${APP_USER_HOME_DIR}" \
# Make app files belong to the root group and are accessible. This is to accomodate the guidelines from
# OpenShift https://docs.openshift.com/enterprise/3.0/creating_images/guidelines.html
    && mkdir -pv "${APP_HOME}" \
    && chown -R "pola-backend:root" "${APP_USER_HOME_DIR}" "${APP_HOME}" \
    && find "${APP_HOME}" -executable -print0 | xargs --null chmod g+x  \
    && find "${APP_HOME}" -print0 | xargs --null chmod g+rw

COPY --chown=pola-backend:root --from=build-py /root/.local "${APP_USER_HOME_DIR}/.local"
COPY --chown=pola-backend:root --from=build-js /app/pola/static/js/ "${APP_HOME}/pola/static/js/"
COPY --chown=pola-backend:root --from=build-js /app/pola/static/fonts/ "${APP_HOME}/pola/static/fonts/"
COPY --chown=pola-backend:root --from=build-js /app/pola/static/css/ "${APP_HOME}/pola/static/css/"

# Make /etc/passwd root-group-writeable so that user can be dynamically added by OpenShift
# hadolint ignore=DL4005
RUN chmod g=u /etc/passwd \
# Enable heroku-exec
# See: https://devcenter.heroku.com/articles/exec#using-with-docker
    && rm /bin/sh \
    && ln -s /bin/bash /bin/sh

COPY ./scripts/prod-docker-image/heroku-exec.sh /app/.profile.d/heroku-exec.sh

ENV PATH="${APP_USER_HOME_DIR}/.local/bin:${PATH}" \
    GUNICORN_CMD_ARGS="--worker-tmp-dir /dev/shm"

COPY --chown=pola-backend:root ./scripts/prod-docker-image/entrypoint.sh /entrypoint
COPY ./ ${APP_HOME}

WORKDIR ${APP_HOME}

EXPOSE 8080

RUN usermod -g 0 pola-backend -G "${APP_GID}"

USER ${APP_UID}

ARG RELEASE_SHA
ENV RELEASE_SHA=${RELEASE_SHA}

ENTRYPOINT ["/usr/bin/dumb-init", "--", "/entrypoint"]
CMD ["gunicorn", "pola.config.wsgi:application"]

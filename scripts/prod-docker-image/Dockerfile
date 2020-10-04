ARG APP_UID="50000"
ARG APP_GID="50000"

ARG APP_HOME=/opt/pola-backend

ARG PYTHON_VERSION="3.6"

FROM python:${PYTHON_VERSION}-slim-buster as build

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

ENV PYTHONUNBUFFERED 1
ENV PATH=${PATH}:/root/.local/bin
RUN mkdir -p /root/.local/bin

COPY ./requirements/ ${APP_HOME}/requirements/

RUN pip install --user -r "${APP_HOME}/requirements/production.txt" \
    && find /root/.local/ -name '*.pyc' -print0 | xargs -0 rm -r \
    && find /root/.local/ -type d -name '__pycache__' -print0 | xargs -0 rm -r

# make sure that all directories and files in .local are also group accessible
RUN find /root/.local -executable -print0 | xargs --null chmod g+x && \
    find /root/.local -print0 | xargs --null chmod g+rw

LABEL io.github.klubjagiellonski.distro="debian"
LABEL io.github.klubjagiellonski.distro.version="buster"
LABEL io.github.klubjagiellonski.module="pola"
LABEL io.github.klubjagiellonski.component="pola-backend"
LABEL io.github.klubjagiellonski.image="pola-backend"

######################### MAIN IMAGE #########################

FROM python:${PYTHON_VERSION}-slim-buster as main

ARG APP_UID
ARG APP_GID
ENV APP_UID=${APP_UID}
ENV APP_GID=${APP_GID}
ARG APP_USER_HOME_DIR=/home/pola-backend
ENV APP_USER_HOME_DIR=${APP_USER_HOME_DIR}
ARG APP_HOME
ENV APP_HOME=${APP_HOME}

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
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --gid "${APP_GID}" "pola-backend" && \
    adduser --quiet "pola-backend" --uid "${APP_UID}" \
        --gid "${APP_GID}" \
        --home "${APP_USER_HOME_DIR}"

# Make app files belong to the root group and are accessible. This is to accomodate the guidelines from
# OpenShift https://docs.openshift.com/enterprise/3.0/creating_images/guidelines.html
RUN mkdir -pv "${APP_HOME}"; \
    chown -R "pola-backend:root" "${APP_USER_HOME_DIR}" "${APP_HOME}"; \
    find "${APP_HOME}" -executable -print0 | xargs --null chmod g+x && \
    find "${APP_HOME}" -print0 | xargs --null chmod g+rw

COPY --chown=pola-backend:root --from=build /root/.local "${APP_USER_HOME_DIR}/.local"

# Make /etc/passwd root-group-writeable so that user can be dynamically added by OpenShift
RUN chmod g=u /etc/passwd

# Enable heroku-exec
# See: https://devcenter.heroku.com/articles/exec#using-with-docker
# hadolint ignore=DL4005
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
COPY ./scripts/prod-docker-image/heroku-exec.sh /app/.profile.d/heroku-exec.sh

ENV PATH="${APP_USER_HOME_DIR}/.local/bin:${PATH}"
ENV GUNICORN_CMD_ARGS="--worker-tmp-dir /dev/shm"

COPY ./scripts/prod-docker-image/entrypoint.sh /entrypoint
COPY ./ ${APP_HOME}

WORKDIR ${APP_HOME}

EXPOSE 8080

USER ${APP_UID}

ARG RELEASE_SHA
ENV RELEASE_SHA=${RELEASE_SHA}

LABEL io.github.klubjagiellonski.distro="debian"
LABEL io.github.klubjagiellonski.distro.version="buster"
LABEL io.github.klubjagiellonski.module="pola"
LABEL io.github.klubjagiellonski.component="pola-backend"
LABEL io.github.klubjagiellonski.image="pola-backend"

ENTRYPOINT ["/usr/bin/dumb-init", "--", "/entrypoint"]
CMD ["gunicorn", "pola.config.wsgi:application"]

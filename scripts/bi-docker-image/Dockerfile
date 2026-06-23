# syntax=docker/dockerfile:1.14.0
# check=error=true;experimental=all

ARG PYTHON_VERSION="3.13.14"
FROM python:${PYTHON_VERSION}-slim-trixie

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        git \
        lsb-release \
        make \
    && install -d /usr/share/postgresql-common/pgdg \
    && curl --fail -o /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc https://www.postgresql.org/media/keys/ACCC4CF8.asc \
    && echo "deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
        libpq5 \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /var/cache/* /tmp/* /var/tmp/*

ENV PYTHONUNBUFFERED=1
RUN mkdir /app
WORKDIR /app

COPY ./scripts/bi-docker-image/entrypoint.sh /entrypoint
ENTRYPOINT ["/entrypoint"]

COPY dependencies/constraints-bi.txt dependencies/requirements-bi.txt  /app/dependencies/

RUN pip install \
      --no-cache-dir \
      --requirement dependencies/requirements-bi.txt \
      --constraint dependencies/constraints-bi.txt && pip check

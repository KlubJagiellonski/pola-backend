ARG PYTHON_VERSION="3.6"
FROM python:${PYTHON_VERSION}-slim-buster

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
RUN mkdir /app
WORKDIR /app

COPY ./scripts/ci-docker-image/entrypoint.sh /entrypoint
ENTRYPOINT ["/entrypoint"]

ARG DJANGO_VERSION="2.0.2"
ENV DJANGO_VERSION=${DJANGO_VERSION}

RUN pip install --no-cache "django==${DJANGO_VERSION}"

COPY requirements/base.txt requirements/local.txt /app/requirements/

RUN pip install --no-cache -r requirements/local.txt

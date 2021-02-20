FROM python:3.8-slim-buster

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        software-properties-common \
        make \
        build-essential \
        ca-certificates \
        libpq-dev \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /var/cache/* /tmp/* /var/tmp/*

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app

COPY ./scripts/bi-docker-image/entrypoint.sh /entrypoint
ENTRYPOINT ["/entrypoint"]

COPY requirements/bi.txt /app/requirements/

RUN pip install --no-cache-dir -r requirements/bi.txt && pip check

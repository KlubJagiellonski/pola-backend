ARG PYTHON_VERSION="3.6"
FROM python:${PYTHON_VERSION}-buster

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ARG DJANGO_VERSION="2.0.2"
ENV DJANGO_VERSION=${DJANGO_VERSION}
RUN pip install "django==${DJANGO_VERSION}"
ADD requirements/base.txt requirements/local.txt /app/requirements/

RUN pip install -r requirements/local.txt


ADD . /app/

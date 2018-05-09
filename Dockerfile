FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD requirements/base.txt requirements/local.txt requirements/test.txt /app/requirements/
RUN pip install -r requirements/local.txt

ADD . /app/

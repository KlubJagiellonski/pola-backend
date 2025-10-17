# syntax=docker/dockerfile:1.14.0
# check=error=true;experimental=all

ARG PYTHON_VERSION="3.11"
FROM python:${PYTHON_VERSION}-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade "pip" && pip --version

COPY requirements.txt /app/

RUN pip install \
      --no-cache-dir \
      --requirement /app/requirements.txt && pip check

COPY . /app/

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]

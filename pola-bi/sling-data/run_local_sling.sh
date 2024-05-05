#!/usr/bin/env bash

set -euo pipefail

export MY_POSTGRES='postgresql://pola_app:pola_app@localhost:5432/pola_app?sslmode=disable'

sling conns set MY_BIGQUERY \
  type=bigquery \
  project=pola-bi-looker \
  dataset=pola_backend__local \
  gc_bucket=pola-app_pola-backend_postgres_csv-files \
  location=europe-west3

sling  "${@}"

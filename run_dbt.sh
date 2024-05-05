#!/usr/bin/env bash

set -euo pipefail


# Check if COMPOSE_FILE environment variable is set

if [ -z "${COMPOSE_FILE:-}" ]; then
  COMPOSE_FILE="docker-compose.yaml:docker-compose.dbt.yaml:docker-compose.dbt-local.yaml"
  export COMPOSE_FILE
fi

TMP_DIR=$(mktemp -d)
cleanup() {
    rm -rf "${TMP_DIR}"
}
trap cleanup EXIT HUP INT TERM

GCP_ACCOUNT=$(gcloud config get-value core/account)
if [ -z "${GCP_ACCOUNT:-}" ]; then
  echo "Your are not authenticated to gcloud sdk. Skipping passing credentials" >&2
  echo "To authenticate, please run 'gcloud auth login' " >&2
  GCP_CREDENTIAL_FILE=/dev/null
else
  if [ -z "${GCP_PROJECT:-}" ]; then
    GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project)
    echo "GCP_PROJECT is not set. Using the current project: ${GOOGLE_CLOUD_PROJECT}" >&2
  else
    GOOGLE_CLOUD_PROJECT="${GCP_PROJECT}"
    echo "GCP_PROJECT is set to ${GOOGLE_CLOUD_PROJECT}" >&2
  fi

  export GOOGLE_CLOUD_PROJECT

  GCP_CREDENTIAL_FILE="${TMP_DIR}/gcp-credentials.json"
  # Copy the credentials file to the temporary directory
  # Token refreshing SHOULD works, but it is not tested.

  jq -n \
    --arg access_token "$(gcloud auth print-access-token)" \
    --arg refresh_token "$(gcloud auth print-refresh-token)" \
    --arg gcp_client_id "$(gcloud config get auth/client_id)" \
    --arg gcp_client_secret "$(gcloud config get auth/client_secret)" \
    '{
    type: "authorized_user",
    token: $access_token,
    refresh_token: $refresh_token,
    client_id: $gcp_client_id,
    client_secret: $gcp_client_secret
  }' > "${GCP_CREDENTIAL_FILE}"
fi

docker-compose run --rm --no-deps --publish 8081:8081  \
  -e GOOGLE_CLOUD_PROJECT \
  -v "${TMP_DIR}:/host/${TMP_DIR}" \
  -e GOOGLE_APPLICATION_CREDENTIALS="/host/${GCP_CREDENTIAL_FILE}" \
  dbt -- "${@}"

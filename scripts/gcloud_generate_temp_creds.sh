#!/usr/bin/env bash

GCP_CREDENTIAL_FILE="$(mktemp -t gcp-credentials-XXXXXX).json"
# Copy the credentials file to the temporary directory
# Token refreshing SHOULD works, but it is not tested.

jq -n \
  --arg access_token "$(gcloud auth print-access-token)" \
  --arg refresh_token "$(gcloud auth print-refresh-token || true)" \
  --arg gcp_client_id "$(gcloud config get auth/client_id)" \
  --arg gcp_client_secret "$(gcloud config get auth/client_secret)" \
  '{
  type: "authorized_user",
  token: $access_token,
  refresh_token: $refresh_token,
  client_id: $gcp_client_id,
  client_secret: $gcp_client_secret
}' > "${GCP_CREDENTIAL_FILE}"

echo "${GCP_CREDENTIAL_FILE}"

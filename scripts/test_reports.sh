#!/bin/bash

PRODUCT_CODE="5908217666666"

# Create a temp directory
TMP_DIR=$(mktemp -d)
trap "rm -rf ${TMP_DIR}" EXIT

# Fetch example directory
curl --output "${TMP_DIR}/image.jpeg" 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Calico_tabby_cat_-_Savannah.jpg/1200px-Calico_tabby_cat_-_Savannah.jpg'

# Utilities
function aws() {
  set +x
  AWS_ACCESS_KEY_ID=$(heroku config:get --app pola-app POLA_APP_AWS_ACCESS_KEY_ID)
  AWS_SECRET_ACCESS_KEY=$(heroku config:get --app pola-app POLA_APP_AWS_SECRET_ACCESS_KEY)

  docker run --rm -e "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}" -e "AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}" amazon/aws-cli "${@}"
}

function main() {
  echo "Fetching product: $PRODUCT_CODE"
  curl -v "https://www.pola-app.pl/a/v3/get_by_code?device_id=TEST-DEVICE-ID&code=$PRODUCT_CODE" | tee "${TMP_DIR}/product-response.json" | jq .

  PRODUCT_ID=$(cat "${TMP_DIR}/product-response.json" | jq .product_id -r)
  read -r -d '' REPORT_JSON_DATA << EOM
  {
      "description": "TEST - KAMIL",
      "product_id": $PRODUCT_ID,
      "files_count": 1,
      "file_ext": "jpg",
      "mime_type": "image/jpeg"
  }
EOM

  echo $REPORT_JSON_DATA | jq .

  echo "Creating report"
  curl -L -v https://www.pola-app.pl/a/v3/create_report?device_id=TEST-DEVICE-ID -H "application/json" -X POST --data "${REPORT_JSON_DATA}" | tee "${TMP_DIR}/report-response.json" | jq
  SIGNED_URL=$(cat "${TMP_DIR}/report-response.json" | jq '.signed_requests[0]' -r)
  echo "SIGNED_URL=${SIGNED_URL}"
  echo "Upload file"
  curl -v -X PUT -T "${TMP_DIR}/image.jpeg"  -H 'Content-Type: image/jpeg' "${SIGNED_URL}"

  echo "Checking bucket content"
  BUCKET_NAME=$(echo "${SIGNED_URL}" | cut -d "/" -f 3 | cut -d "." -f 1)
  OBJECT_NAME=$(echo "${SIGNED_URL}" | cut -d "/" -f 4- | cut -d "?" -f 1)
  OBJECT_URI="s3://${BUCKET_NAME}/${OBJECT_NAME}"
  aws s3 ls "${OBJECT_URI}" && echo "Found: ${OBJECT_URI}" || echo "Not found: ${OBJECT_URI}"

}
main

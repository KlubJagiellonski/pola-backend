#!/usr/bin/env bash
set -euo pipefail

# Generate a simple SVG badge with total scans from BigQuery.
#
# Usage:
#   scripts/generate_scans_svg.sh <dataset_id> [<output_path>] [<table_id>]
#
# Env:
#   GCP_PROJECT_ID  - Google Cloud project ID (required)
#
# Example:
#   GCP_PROJECT_ID=pola-bi-looker \
#   scripts/generate_scans_svg.sh pola_backend__prod docs/badges/total_scans.svg

if [[ ${#} -lt 1 ]]; then
  echo "Usage: $0 <dataset_id> [<output_path>] [<table_id>]" >&2
  exit 2
fi

: "${GCP_PROJECT_ID:?GCP_PROJECT_ID is required in environment}"

DATASET_ID="$1"
OUTPUT_PATH="${2:-docs/badges/total_scans.svg}"
TABLE_ID="${3:-pola_query}"

# Run the query using Standard SQL and CSV output; take the last line (value row).
TOTAL_SCANS=$(bq query \
  --use_legacy_sql=false \
  --quiet \
  --format=csv \
  "SELECT COUNT(1) AS total_scans FROM \`${GCP_PROJECT_ID}.${DATASET_ID}.${TABLE_ID}\`")

# Extract the numeric value (skip header)
TOTAL_SCANS=$(echo "${TOTAL_SCANS}" | tail -n 1 | tr -d '\r\n ')

mkdir -p "$(dirname "${OUTPUT_PATH}")"

# Basic badge styling
LABEL="scans"
LABEL_COLOR="#555"      # dark grey
VALUE_COLOR="#4c1"      # green
FONT_FAMILY="DejaVu Sans,Verdana,Geneva,sans-serif"

# Fixed widths to keep things simple (px)
LABEL_WIDTH=60
VALUE_WIDTH=110
HEIGHT=20
TOTAL_WIDTH=$((LABEL_WIDTH + VALUE_WIDTH))

cat >"${OUTPUT_PATH}" <<SVG
<svg xmlns="http://www.w3.org/2000/svg" width="${TOTAL_WIDTH}" height="${HEIGHT}" role="img" aria-label="${LABEL}: ${TOTAL_SCANS}">
  <title>${LABEL}: ${TOTAL_SCANS}</title>
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#fff" stop-opacity=".7"/>
    <stop offset=".1" stop-opacity=".1"/>
    <stop offset=".9" stop-opacity=".3"/>
    <stop offset="1" stop-opacity=".5"/>
  </linearGradient>
  <mask id="m"><rect width="${TOTAL_WIDTH}" height="${HEIGHT}" rx="3" fill="#fff"/></mask>
  <g mask="url(#m)">
    <rect width="${LABEL_WIDTH}" height="${HEIGHT}" fill="${LABEL_COLOR}"/>
    <rect x="${LABEL_WIDTH}" width="${VALUE_WIDTH}" height="${HEIGHT}" fill="${VALUE_COLOR}"/>
    <rect width="${TOTAL_WIDTH}" height="${HEIGHT}" fill="url(#s)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="${FONT_FAMILY}" font-size="11">
    <text x="$((LABEL_WIDTH/2))" y="14" fill="#010101" fill-opacity=".3">${LABEL}</text>
    <text x="$((LABEL_WIDTH/2))" y="14">${LABEL}</text>
    <text x="$((LABEL_WIDTH + VALUE_WIDTH/2))" y="14" fill="#010101" fill-opacity=".3">${TOTAL_SCANS}</text>
    <text x="$((LABEL_WIDTH + VALUE_WIDTH/2))" y="14">${TOTAL_SCANS}</text>
  </g>
</svg>
SVG

echo "Wrote SVG to ${OUTPUT_PATH} with total_scans=${TOTAL_SCANS}"

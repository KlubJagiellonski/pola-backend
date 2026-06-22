#!/usr/bin/env bash
set -euo pipefail

# Generate a minimal SVG with the total scans number (large sans-serif on transparent background).
#
# Usage:
#   scripts/generate_scans_svg.sh <dataset_id> [<output_path>] [<table_id>]
#
# Env:
#   GCP_PROJECT_ID  - Google Cloud project ID (required)
#
# Example:
#   GCP_PROJECT_ID=pola-bi-looker \
#   scripts/generate_scans_svg.sh pola_backend__prod docs/total_scans.svg

if [[ ${#} -lt 1 ]]; then
  echo "Usage: $0 <dataset_id> [<output_path>] [<table_id>]" >&2
  exit 2
fi

: "${GCP_PROJECT_ID:?GCP_PROJECT_ID is required in environment}"

DATASET_ID="$1"
OUTPUT_PATH="${2:-docs/total_scans.svg}"
TABLE_ID="${3:-pola_query}"

# Ensure BigQuery CLI is available.
command -v bq >/dev/null 2>&1 || { echo "bq CLI not found (install Google Cloud SDK / bq component)" >&2; exit 1; }

# Run the query using Standard SQL and CSV output.
TOTAL_SCANS=$(bq query \
  --use_legacy_sql=false \
  --quiet \
  --format=csv \
  --project_id="${GCP_PROJECT_ID}" \
  "SELECT COUNT(1) AS total_scans FROM \`${GCP_PROJECT_ID}.${DATASET_ID}.${TABLE_ID}\`")

# Extract the numeric value (skip header) and validate it.
TOTAL_SCANS=$(echo "${TOTAL_SCANS}" | sed -n '2p' | tr -d '\r\n ')
if [[ ! "${TOTAL_SCANS}" =~ ^[0-9]+$ ]]; then
  echo "Unexpected BigQuery output for total scans: ${TOTAL_SCANS}" >&2
  exit 1
fi
mkdir -p "$(dirname "${OUTPUT_PATH}")"

# Minimal, large-number SVG styling (transparent background by default)
# You can tweak FONT_SIZE or FONT_FAMILY if desired.
FONT_SIZE=72                                  # px
FONT_FAMILY="system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif"
H_PADDING=16                                   # px left/right padding

# Rough per-digit width estimate as a percentage of font size (digits are typically ~0.6em wide)
CHAR_WIDTH_X100=62                             # 0.62 * font-size

NUM_LEN=${#TOTAL_SCANS}
TEXT_WIDTH=$(( NUM_LEN * FONT_SIZE * CHAR_WIDTH_X100 / 100 ))
WIDTH=$(( TEXT_WIDTH + 2 * H_PADDING ))
# Add some headroom so glyphs aren't clipped
HEIGHT=$(( FONT_SIZE + FONT_SIZE / 3 ))        # ~1.33 line-height

cat >"${OUTPUT_PATH}" <<SVG
<svg xmlns="http://www.w3.org/2000/svg" width="${WIDTH}" height="${HEIGHT}" viewBox="0 0 ${WIDTH} ${HEIGHT}" role="img" aria-label="total scans: ${TOTAL_SCANS}">
  <title>total scans: ${TOTAL_SCANS}</title>
  <text x="${H_PADDING}" y="${FONT_SIZE}" font-family="${FONT_FAMILY}" font-size="${FONT_SIZE}" fill="#000">${TOTAL_SCANS}</text>
  <!-- Transparent background by default (no rects). -->
</svg>
SVG

echo "Wrote SVG to ${OUTPUT_PATH} with total_scans=${TOTAL_SCANS}"

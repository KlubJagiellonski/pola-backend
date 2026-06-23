#!/usr/bin/env bash
# Run the prod image locally like Cloud Run: PORT=8080, entrypoint + gunicorn on 0.0.0.0:8080.
# Requires: prod image built (e.g. python scripts/manage_image.py build --image-type prod).
# Optional: start Postgres first with  docker compose up -d postgres

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

IMAGE="${1:-pola-backend_prod:latest}"

# Postgres reachable from host (default from docker-compose). Mac/Win: host.docker.internal. Linux: add --add-host=host.docker.internal:host-gateway or set DATABASE_URL to your host IP.
DATABASE_URL="${DATABASE_URL:-postgres://pola_app:pola_app@host.docker.internal:5432/pola_app}"

echo "Using image: $IMAGE"
echo "DATABASE_URL: ${DATABASE_URL}"
echo "Open http://localhost:8080 after startup."
echo ""

docker run --rm -it \
  -p 8080:8080 \
  -e PORT=8080 \
  -e DATABASE_URL="$DATABASE_URL" \
  -e DJANGO_SECRET_KEY="${DJANGO_SECRET_KEY:-dev-secret-key-change-in-production}" \
  -e IS_PRODUCTION=false \
  -e POLA_APP_GCS_PUBLIC_BUCKET_NAME=local-public \
  -e POLA_APP_GCS_BACKEND_BUCKET_NAME=local-backend \
  -e POLA_APP_GCS_AI_PICS_BUCKET_NAME=local-ai-pics \
  -e POLA_APP_GCS_WEB_BUCKET_NAME=local-web \
  -e POLA_APP_GCS_COMPANY_LOGOTYPE_BUCKET_NAME=local-logos \
  -e POLA_APP_GCS_PUBLIC_BASE_URL=http://localhost:8080 \
  -e DJANGO_DEFAULT_FROM_EMAIL="pola <noreply@localhost>" \
  -e AI_SHARED_SECRET="${AI_SHARED_SECRET:-local-ai-secret}" \
  "$IMAGE"

#!/usr/bin/env bash

set -euo pipefail

if [ -z "${BRANCH:-}" ]; then
  echo "BRANCH is not set"
  exit 1
fi

if [ -z "${S3_BUCKET:-}" ]; then
  echo "S3_BUCKET is not set"
  exit 1
fi

MANIFEST_TMP=$(mktemp)

if [[ -n "${DEBUG:-}" ]]; then
  echo "Manifest will be written to ${MANIFEST_TMP}"
else
  trap 'rm -f ${MANIFEST_TMP}' EXIT
fi

PATH_PREFIX="addon-templates/${BRANCH}"

# Caching is disabled on uploads since it may lead to inconsistent versions, is
# tougher to reason about, and we generally just don't need it for this scale.
function sync_templates() {
  aws s3 sync \
    templates/ \
    "s3://${S3_BUCKET}/${PATH_PREFIX}" \
    --cache-control "no-store, no-cache, must-revalidate, max-age=0" \
    --delete \
    --exact-timestamps \
    "$@"
}

# Upload YAML files as plain text so they render more easily in browser.
sync_templates --exclude "*" --include "*.yaml" --include "*.yml" --content-type "text/plain"
sync_templates --exclude "*.yaml" --exclude "*.yml" --include "*"

python3 .utils/generate-manifest-json.py > "$MANIFEST_TMP"

aws s3 cp \
  "$MANIFEST_TMP" \
  "s3://${S3_BUCKET}/${PATH_PREFIX}/manifest.json" \
  --content-type "application/json" \
  --cache-control "no-store, no-cache, must-revalidate, max-age=0"

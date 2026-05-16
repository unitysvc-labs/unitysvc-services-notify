#!/bin/bash
# Connectivity test for Slack notifications.
# Sends a test message directly to your Slack incoming webhook via the UnitySVC gateway.
# Slack webhooks return HTTP 200 with body "ok" on success.

set -e

: "${SERVICE_BASE_URL:?SERVICE_BASE_URL environment variable is required}"
: "${UNITYSVC_API_KEY:?UNITYSVC_API_KEY environment variable is required}"

http_code=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
  "${SERVICE_BASE_URL}" \
  -H "Authorization: Bearer ${UNITYSVC_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"text":"unitysvc connectivity test"}')

if [[ "$http_code" =~ ^2 ]]; then
  echo "connectivity ok"
  exit 0
else
  echo "connectivity failed (HTTP $http_code)"
  exit 1
fi

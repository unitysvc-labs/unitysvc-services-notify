#!/bin/bash
# Connectivity test for Discord notifications.
# Sends a test message directly to your Discord webhook URL via the UnitySVC gateway.
# Discord webhooks return 204 No Content on success.

set -e

: "${SERVICE_BASE_URL:?SERVICE_BASE_URL environment variable is required}"
: "${UNITYSVC_API_KEY:?UNITYSVC_API_KEY environment variable is required}"

http_code=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
  "${SERVICE_BASE_URL}" \
  -H "Authorization: Bearer ${UNITYSVC_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"content":"unitysvc connectivity test"}')

if [[ "$http_code" =~ ^2 ]]; then
  echo "connectivity ok"
  exit 0
else
  echo "connectivity failed (HTTP $http_code)"
  exit 1
fi

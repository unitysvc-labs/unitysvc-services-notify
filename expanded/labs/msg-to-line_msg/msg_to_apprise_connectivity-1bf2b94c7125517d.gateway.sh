#!/bin/bash
# Connectivity test for a UnitySVC Notify transformer (Apprise) service.
#   local_testing : POST the COMPOSED apprise body straight to the apprise-api
#                   (no gateway to compose it for us, no platform auth).
#   gateway       : POST the canonical envelope; the gateway composes the
#                   apprise body (adds "urls") and forwards it (Bearer auth).
# The apprise_url parameter holds the per-channel test URL, e.g. discord://demo/demotoken.
set -o pipefail

URL="${API_GATEWAY_BASE_URL}/labs/msg-to-line_msg"


status=$(curl -sS --max-time 10 \
    -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${UNITYSVC_API_KEY}" \
    -d '{"title":"connectivity check","body":"ping","from":"test@example.com"}' \
    -o /dev/null -w "%{http_code}" \
    "$URL" 2>/dev/null)


case "$status" in
  2??) echo "connectivity ok (HTTP $status)"; exit 0 ;;
  000) echo "connectivity failed: could not connect to $URL" >&2; exit 1 ;;
  *)   echo "connectivity failed: HTTP $status from $URL" >&2; exit 1 ;;
esac
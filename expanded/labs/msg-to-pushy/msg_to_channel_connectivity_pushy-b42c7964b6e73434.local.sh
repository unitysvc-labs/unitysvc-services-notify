#!/bin/bash
# Connectivity test for a UnitySVC Notify gateway-transformer channel (pushy).
#   local_testing : POST the channel-NATIVE pushy body (baked in) straight to
#                   a mock upstream (local_url).  No gateway to transform it, no
#                   platform auth.
#   gateway       : POST the canonical envelope to service_base_url@<channel>;
#                   the gateway transforms it into the pushy-native payload and
#                   forwards it (Bearer auth).
# The pushy-native body is baked into this variant — only the local_url (mock
# upstream) and channel (transformer selector) parameters are supplied.
set -o pipefail


URL="https://mock.unitysvc.dev/pushy/push?api_key=demo123"
status=$(curl -sS --max-time 10 \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"to": "device-or-topic", "notification": {"title": "connectivity check", "body": "ping"}, "data": {"message": "ping"}}' \
    -o /dev/null -w "%{http_code}" \
    "$URL" 2>/dev/null)


case "$status" in
  2??) echo "connectivity ok (HTTP $status)"; exit 0 ;;
  000) echo "connectivity failed: could not connect to $URL" >&2; exit 1 ;;
  *)   echo "connectivity failed: HTTP $status from $URL" >&2; exit 1 ;;
esac
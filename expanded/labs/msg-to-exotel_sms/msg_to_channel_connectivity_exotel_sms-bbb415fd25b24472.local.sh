#!/bin/bash
# Connectivity test for a UnitySVC Notify gateway-transformer channel (exotel-sms).
#   local_testing : POST the channel-NATIVE exotel-sms body (baked in) straight to
#                   a mock upstream (local_url).  No gateway to transform it, no
#                   platform auth.
#   gateway       : POST the canonical envelope to service_base_url@<channel>;
#                   the gateway transforms it into the exotel-sms-native payload and
#                   forwards it (Bearer auth).
# The exotel-sms-native body is baked into this variant — only the local_url (mock
# upstream) and channel (transformer selector) parameters are supplied.
set -o pipefail


URL="https://demo123sid:demo123token@mock.unitysvc.dev/exotel_sms/v1/Accounts/demo123sid/Sms/send"
status=$(curl -sS --max-time 10 \
    -X POST \
    -H "Content-Type: application/x-www-form-urlencoded" \
    --data-urlencode 'From=source' \
    --data-urlencode 'Body=connectivity check' \
    --data-urlencode 'EncodingType=plain' \
    --data-urlencode 'Priority=normal' \
    --data-urlencode 'To=+15551234567' \
    -o /dev/null -w "%{http_code}" \
    "$URL" 2>/dev/null)


case "$status" in
  2??) echo "connectivity ok (HTTP $status)"; exit 0 ;;
  000) echo "connectivity failed: could not connect to $URL" >&2; exit 1 ;;
  *)   echo "connectivity failed: HTTP $status from $URL" >&2; exit 1 ;;
esac
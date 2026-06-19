#!/usr/bin/env bash
# Validate `discord-relay` (byok channel) against mock.unitysvc.dev — no real Discord needed.
#
# Mirrors the rendered byok upstream from specs/labs/discord-relay.json:
#   ${ customer_secrets.DISCORD_WEBHOOK_BASE ?? https://discord.com/api/webhooks }
#     /${ customer_secrets.DISCORD_WEBHOOK_ID }/${ customer_secrets.DISCORD_WEBHOOK_TOKEN }
# For testing the seller sets a SELLER secret DISCORD_WEBHOOK_BASE=mock; the ops_customer's
# customer-secret lookup misses and falls back to that seller secret (route_mapping.py), so
# only test traffic hits the mock while production defaults to real Discord. Locally it comes
# from the DISCORD_WEBHOOK_BASE env var. The customer sends a NATIVE Discord webhook body; the
# gateway forwards it unchanged after composing this URL.
set -euo pipefail

DISCORD_WEBHOOK_BASE="${DISCORD_WEBHOOK_BASE:-https://mock.unitysvc.dev/discord/api/webhooks}"
DISCORD_WEBHOOK_ID="${DISCORD_WEBHOOK_ID:-demo}"
DISCORD_WEBHOOK_TOKEN="${DISCORD_WEBHOOK_TOKEN:-demotoken}"

URL="${DISCORD_WEBHOOK_BASE}/${DISCORD_WEBHOOK_ID}/${DISCORD_WEBHOOK_TOKEN}"
BODY='{"content":"connectivity check from UnitySVC discord-relay"}'

echo "POST native Discord body -> ${URL}"
status=$(curl -sS --max-time 10 -X POST "${URL}" \
  -H "Content-Type: application/json" -d "${BODY}" \
  -o /tmp/discord-relay-resp.json -w "%{http_code}")
echo "HTTP ${status}"
cat /tmp/discord-relay-resp.json 2>/dev/null; echo

case "${status}" in
  2??) echo "✓ discord-relay OK — mock accepted the native Discord body"; exit 0 ;;
  *)   echo "✗ discord-relay FAILED (HTTP ${status})"; exit 1 ;;
esac

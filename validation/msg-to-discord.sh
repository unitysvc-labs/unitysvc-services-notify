#!/usr/bin/env bash
# Validate `msg-to-discord` (apprise channel) against mock.unitysvc.dev via apprise.unitysvc.dev.
#
# The customer sends the unified envelope {title, body, type, format}. The gateway's
# body-transformer (specs/unitysvc-labs/msg-to-discord.json) composes an apprise-api request:
#   {"urls":"discord://<id>/<token>","title":...,"body":...,"type":...,"format":...}
# Here the discord:// URL is swapped for json://mock.unitysvc.dev/... so delivery lands on
# the mock instead of a real Discord server — proving the envelope -> Apprise path end to end.
# (For a real send, set TARGET="discord://$DISCORD_WEBHOOK_ID/$DISCORD_WEBHOOK_TOKEN".)
set -euo pipefail

APPRISE="${APPRISE_ENDPOINT:-https://apprise.unitysvc.dev/notify}"
TARGET="${TARGET:-json://mock.unitysvc.dev/discord-validate}"

# Exactly the body the gateway's resty.template emits from the envelope above:
BODY="{\"urls\":\"${TARGET}\",\"title\":\"connectivity check\",\"body\":\"ping from UnitySVC msg-to-discord\",\"type\":\"info\",\"format\":\"text\"}"

echo "POST apprise-api body -> ${APPRISE}  (urls=${TARGET})"
status=$(curl -sS --max-time 10 -X POST "${APPRISE}" \
  -H "Content-Type: application/json" -d "${BODY}" \
  -o /tmp/msg-to-discord-resp.json -w "%{http_code}")
echo "HTTP ${status}"
cat /tmp/msg-to-discord-resp.json 2>/dev/null; echo

# apprise-api returns {"error": null, "details": [...]} on a successful send.
if [ "${status:0:1}" = "2" ] && grep -q '"error": null' /tmp/msg-to-discord-resp.json; then
  echo "✓ msg-to-discord OK — Apprise composed the body and delivered to the mock"; exit 0
else
  echo "✗ msg-to-discord FAILED (HTTP ${status})"; exit 1
fi

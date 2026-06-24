import os
import sys

import httpx

# Code example for a UnitySVC Notify gateway-transformer channel (whatsapp-msg).
#   local_testing : POST the channel-NATIVE whatsapp-msg body (baked in) straight to
#                   a mock upstream (local_url).  No gateway to transform it, no
#                   platform auth.
#   gateway       : POST the canonical envelope to {BASE_URL}@<channel>; the
#                   gateway transforms it into the whatsapp-msg-native payload.
# The whatsapp-msg-native body is baked into this variant — only the local_url (mock
# upstream) and channel (transformer selector) parameters are supplied.
BASE_URL = "${APPRISE_BASE:-https://apprise.unitysvc.dev}/notify"


response = httpx.post(
    "https://mock.unitysvc.dev/whatsapp/v17.0/1234567890/messages",
    headers={"Content-Type": "application/json"},
    json={
        "messaging_product": "whatsapp",
        "to": "1234567890",
        "type": "text",
        "text": {
            "body": "Hello from UnitySVC",
        },
    },
)
if not (200 <= response.status_code < 300):
    print(f"failed (HTTP {response.status_code})", file=sys.stderr)
    sys.exit(1)

print(f"sent (HTTP {response.status_code})")
import os
import sys

import httpx

# Code example for a UnitySVC Notify gateway-transformer channel (d7networks-sms).
#   local_testing : POST the channel-NATIVE d7networks-sms body (baked in) straight to
#                   a mock upstream (local_url).  No gateway to transform it, no
#                   platform auth.
#   gateway       : POST the canonical envelope to {BASE_URL}@<channel>; the
#                   gateway transforms it into the d7networks-sms-native payload.
# The d7networks-sms-native body is baked into this variant — only the local_url (mock
# upstream) and channel (transformer selector) parameters are supplied.
BASE_URL = "${APPRISE_BASE:-https://apprise.unitysvc.dev}/notify"


response = httpx.post(
    "https://mock.unitysvc.dev/d7networks_sms/messages/v1/send",
    headers={"Content-Type": "application/json"},
    json={
        "message_globals": {
            "channel": "sms",
            "originator": "source",
        },
        "messages": [
            {
                "recipients": ["+15551234567"],
                "content": "Hello from UnitySVC",
                "data_coding": "auto",
            }
        ],
    },
)
if not (200 <= response.status_code < 300):
    print(f"failed (HTTP {response.status_code})", file=sys.stderr)
    sys.exit(1)

print(f"sent (HTTP {response.status_code})")
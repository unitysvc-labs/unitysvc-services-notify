import os
import sys

import httpx

# Code example for a UnitySVC Notify gateway-transformer channel (octopush-sms).
#   local_testing : POST the channel-NATIVE octopush-sms body (baked in) straight to
#                   a mock upstream (local_url).  No gateway to transform it, no
#                   platform auth.
#   gateway       : POST the canonical envelope to {BASE_URL}@<channel>; the
#                   gateway transforms it into the octopush-sms-native payload.
# The octopush-sms-native body is baked into this variant — only the local_url (mock
# upstream) and channel (transformer selector) parameters are supplied.
BASE_URL = "${APPRISE_BASE:-https://apprise.unitysvc.dev}/notify"


response = httpx.post(
    "https://mock.unitysvc.dev/octopush_sms/v1/public/sms-campaign/send",
    headers={"Content-Type": "application/json"},
    json={
        "recipients": [
            {
                "phone_number": "+15551234567"
            }
        ],
        "text": "connectivity check",
        "type": "sms_premium",
        "purpose": "alert",
        "sender": "src",
        "with_replies": False,
    },
)
if not (200 <= response.status_code < 300):
    print(f"failed (HTTP {response.status_code})", file=sys.stderr)
    sys.exit(1)

print(f"sent (HTTP {response.status_code})")
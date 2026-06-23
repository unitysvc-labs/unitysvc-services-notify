import os
import sys

import httpx

# Code example for a UnitySVC Notify gateway-transformer channel (msg91-sms).
#   local_testing : POST the channel-NATIVE msg91-sms body (baked in) straight to
#                   a mock upstream (local_url).  No gateway to transform it, no
#                   platform auth.
#   gateway       : POST the canonical envelope to {BASE_URL}@<channel>; the
#                   gateway transforms it into the msg91-sms-native payload.
# The msg91-sms-native body is baked into this variant — only the local_url (mock
# upstream) and channel (transformer selector) parameters are supplied.
BASE_URL = "${APPRISE_BASE:-https://apprise.unitysvc.dev}/notify"


response = httpx.post(
    "https://mock.unitysvc.dev/msg91_sms/api/v5/flow/",
    headers={"Content-Type": "application/json"},
    json={
        "template_id": "test_tmpl",
        "short_url": 0,
        "recipients": [
            {
                "mobiles": "15551234567",
                "body": "Hello from UnitySVC",
                "type": "info",
            }
        ],
    },
)
if not (200 <= response.status_code < 300):
    print(f"failed (HTTP {response.status_code})", file=sys.stderr)
    sys.exit(1)

print(f"sent (HTTP {response.status_code})")
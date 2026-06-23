import os
import sys

import httpx

# Code example for a UnitySVC Notify gateway-transformer channel (httpsms-sms).
#   local_testing : POST the channel-NATIVE httpsms-sms body (baked in) straight to
#                   a mock upstream (local_url).  No gateway to transform it, no
#                   platform auth.
#   gateway       : POST the canonical envelope to {BASE_URL}@<channel>; the
#                   gateway transforms it into the httpsms-sms-native payload.
# The httpsms-sms-native body is baked into this variant — only the local_url (mock
# upstream) and channel (transformer selector) parameters are supplied.
BASE_URL = "${APPRISE_BASE:-https://apprise.unitysvc.dev}/notify"


response = httpx.post(
    "https://mock.unitysvc.dev/httpsms_sms/v1/messages/send",
    headers={"Content-Type": "application/json"},
    json={
        "from": "+15551234567",
        "to": "+15551234567",
        "content": "Hello from UnitySVC",
    },
)
if not (200 <= response.status_code < 300):
    print(f"failed (HTTP {response.status_code})", file=sys.stderr)
    sys.exit(1)

print(f"sent (HTTP {response.status_code})")
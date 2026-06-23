import os
import sys

import httpx

# Code example for a UnitySVC Notify gateway-transformer channel (plivo-sms).
#   local_testing : POST the channel-NATIVE plivo-sms body (baked in) straight to
#                   a mock upstream (local_url).  No gateway to transform it, no
#                   platform auth.
#   gateway       : POST the canonical envelope to {BASE_URL}@<channel>; the
#                   gateway transforms it into the plivo-sms-native payload.
# The plivo-sms-native body is baked into this variant — only the local_url (mock
# upstream) and channel (transformer selector) parameters are supplied.
BASE_URL = "${APPRISE_BASE:-https://apprise.unitysvc.dev}/notify"


response = httpx.post(
    "https://demoauthid:demo123@mock.unitysvc.dev/plivo_sms/v1/Account/demoauthid/Message/",
    headers={"Content-Type": "application/json"},
    json={
        "src": "source",
        "dst": "+15551234567",
        "text": "Hello from UnitySVC",
    },
)
if not (200 <= response.status_code < 300):
    print(f"failed (HTTP {response.status_code})", file=sys.stderr)
    sys.exit(1)

print(f"sent (HTTP {response.status_code})")
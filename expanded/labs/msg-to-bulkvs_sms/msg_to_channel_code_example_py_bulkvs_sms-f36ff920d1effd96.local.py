import os
import sys

import httpx

# Code example for a UnitySVC Notify gateway-transformer channel (bulkvs-sms).
#   local_testing : POST the channel-NATIVE bulkvs-sms body (baked in) straight to
#                   a mock upstream (local_url).  No gateway to transform it, no
#                   platform auth.
#   gateway       : POST the canonical envelope to {BASE_URL}@<channel>; the
#                   gateway transforms it into the bulkvs-sms-native payload.
# The bulkvs-sms-native body is baked into this variant — only the local_url (mock
# upstream) and channel (transformer selector) parameters are supplied.
BASE_URL = "${APPRISE_BASE:-https://apprise.unitysvc.dev}/notify"


response = httpx.post(
    "https://demo123:demo123@mock.unitysvc.dev/bulkvs_sms/api/v1.0/messageSend",
    headers={"Content-Type": "application/json"},
    json={
        "From": "source",
        "To": "+15551234567",
        "Message": "Hello from UnitySVC",
    },
)
if not (200 <= response.status_code < 300):
    print(f"failed (HTTP {response.status_code})", file=sys.stderr)
    sys.exit(1)

print(f"sent (HTTP {response.status_code})")
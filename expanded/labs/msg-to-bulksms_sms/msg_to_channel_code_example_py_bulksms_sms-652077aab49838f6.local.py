import os
import sys

import httpx

# Code example for a UnitySVC Notify gateway-transformer channel (bulksms-sms).
#   local_testing : POST the channel-NATIVE bulksms-sms body (baked in) straight to
#                   a mock upstream (local_url).  No gateway to transform it, no
#                   platform auth.
#   gateway       : POST the canonical envelope to {BASE_URL}@<channel>; the
#                   gateway transforms it into the bulksms-sms-native payload.
# The bulksms-sms-native body is baked into this variant — only the local_url (mock
# upstream) and channel (transformer selector) parameters are supplied.
BASE_URL = "${APPRISE_BASE:-https://apprise.unitysvc.dev}/notify"


response = httpx.post(
    "https://demo123user:demo123@mock.unitysvc.dev/bulksms/v1/messages",
    headers={"Content-Type": "application/json"},
    json={
        "to": "+15551234567",
        "body": "Hello from UnitySVC",
        "routingGroup": "STANDARD",
        "encoding": "TEXT",
        "deliveryReports": "ERRORS",
    },
)
if not (200 <= response.status_code < 300):
    print(f"failed (HTTP {response.status_code})", file=sys.stderr)
    sys.exit(1)

print(f"sent (HTTP {response.status_code})")
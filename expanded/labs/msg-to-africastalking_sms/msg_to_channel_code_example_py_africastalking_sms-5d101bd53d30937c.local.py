import os
import sys

import httpx

# Code example for a UnitySVC Notify gateway-transformer channel (africastalking-sms).
#   local_testing : POST the channel-NATIVE africastalking-sms body (baked in) straight to
#                   a mock upstream (local_url).  No gateway to transform it, no
#                   platform auth.
#   gateway       : POST the canonical envelope to {BASE_URL}@<channel>; the
#                   gateway transforms it into the africastalking-sms-native payload.
# The africastalking-sms-native body is baked into this variant — only the local_url (mock
# upstream) and channel (transformer selector) parameters are supplied.
BASE_URL = "${APPRISE_BASE:-https://apprise.unitysvc.dev}/notify"


response = httpx.post(
    "https://mock.unitysvc.dev/africastalking_sms/version1/messaging",
    data={
        "username": "test_user",
        "to": "+15551234567",
        "from": "sender",
        "message": "Hello from UnitySVC",
    },
)
if not (200 <= response.status_code < 300):
    print(f"failed (HTTP {response.status_code})", file=sys.stderr)
    sys.exit(1)

print(f"sent (HTTP {response.status_code})")
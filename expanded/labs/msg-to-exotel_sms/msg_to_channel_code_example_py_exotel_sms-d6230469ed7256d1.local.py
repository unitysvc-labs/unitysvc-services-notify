import os
import sys

import httpx

# Code example for a UnitySVC Notify gateway-transformer channel (exotel-sms).
#   local_testing : POST the channel-NATIVE exotel-sms body (baked in) straight to
#                   a mock upstream (local_url).  No gateway to transform it, no
#                   platform auth.
#   gateway       : POST the canonical envelope to {BASE_URL}@<channel>; the
#                   gateway transforms it into the exotel-sms-native payload.
# The exotel-sms-native body is baked into this variant — only the local_url (mock
# upstream) and channel (transformer selector) parameters are supplied.
BASE_URL = "${APPRISE_BASE:-https://apprise.unitysvc.dev}/notify"


response = httpx.post(
    "https://demo123sid:demo123token@mock.unitysvc.dev/exotel_sms/v1/Accounts/demo123sid/Sms/send",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data={
        "From": "source",
        "Body": "Hello from UnitySVC",
        "EncodingType": "plain",
        "Priority": "normal",
        "To": "+15551234567",
    },
)
if not (200 <= response.status_code < 300):
    print(f"failed (HTTP {response.status_code})", file=sys.stderr)
    sys.exit(1)

print(f"sent (HTTP {response.status_code})")
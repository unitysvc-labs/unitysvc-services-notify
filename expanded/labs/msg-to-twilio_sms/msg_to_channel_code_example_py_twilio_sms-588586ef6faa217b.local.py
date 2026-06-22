import os
import sys

import httpx

# Code example for a UnitySVC Notify gateway-transformer channel (twilio-sms).
#   local_testing : POST the channel-NATIVE twilio-sms body (baked in) straight to
#                   a mock upstream (local_url).  No gateway to transform it, no
#                   platform auth.
#   gateway       : POST the canonical envelope to {BASE_URL}@<channel>; the
#                   gateway transforms it into the twilio-sms-native payload.
# The twilio-sms-native body is baked into this variant — only the local_url (mock
# upstream) and channel (transformer selector) parameters are supplied.
BASE_URL = "${APPRISE_BASE:-https://apprise.unitysvc.dev}/notify"


response = httpx.post(
    "https://ACdeadbeefdeadbeef:dkry5cjqx4bi@mock.unitysvc.dev/twilio/2010-04-01/Accounts/ACdeadbeefdeadbeef/Messages.json",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data={
        "From": "+15551234567",
        "To": "+15559876543",
        "Body": "connectivity check",
    },
)
if not (200 <= response.status_code < 300):
    print(f"failed (HTTP {response.status_code})", file=sys.stderr)
    sys.exit(1)

print(f"sent (HTTP {response.status_code})")
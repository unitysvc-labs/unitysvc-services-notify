import os
import sys

import httpx

# Code example for a UnitySVC Notify gateway-transformer channel (pushdeer).
#   local_testing : POST the channel-NATIVE pushdeer body (baked in) straight to
#                   a mock upstream (local_url).  No gateway to transform it, no
#                   platform auth.
#   gateway       : POST the canonical envelope to {BASE_URL}@<channel>; the
#                   gateway transforms it into the pushdeer-native payload.
# The pushdeer-native body is baked into this variant — only the local_url (mock
# upstream) and channel (transformer selector) parameters are supplied.
BASE_URL = "${APPRISE_BASE:-https://apprise.unitysvc.dev}/notify"


response = httpx.post(
    "https://mock.unitysvc.dev/pushdeer/message/push?pushkey=demo123",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data={
        "text": "Hello from UnitySVC",
        "type": "text",
        "desp": "Notification delivered via transformer.",
    },
)
if not (200 <= response.status_code < 300):
    print(f"failed (HTTP {response.status_code})", file=sys.stderr)
    sys.exit(1)

print(f"sent (HTTP {response.status_code})")
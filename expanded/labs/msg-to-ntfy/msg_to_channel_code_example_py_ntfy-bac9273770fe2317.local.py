import os
import sys

import httpx

# Code example for a UnitySVC Notify gateway-transformer channel (ntfy).
#   local_testing : POST the channel-NATIVE ntfy body (baked in) straight to
#                   a mock upstream (local_url).  No gateway to transform it, no
#                   platform auth.
#   gateway       : POST the canonical envelope to {BASE_URL}@<channel>; the
#                   gateway transforms it into the ntfy-native payload.
# The ntfy-native body is baked into this variant — only the local_url (mock
# upstream) and channel (transformer selector) parameters are supplied.
BASE_URL = "${APPRISE_BASE:-https://apprise.unitysvc.dev}/notify"


response = httpx.post(
    "https://mock.unitysvc.dev/ntfy/demo",
    headers={"Content-Type": "application/json"},
    json={
        "topic": "unitysvc",
        "title": "Hello from UnitySVC",
        "message": "Notification delivered via transformer.",
    },
)
if not (200 <= response.status_code < 300):
    print(f"failed (HTTP {response.status_code})", file=sys.stderr)
    sys.exit(1)

print(f"sent (HTTP {response.status_code})")
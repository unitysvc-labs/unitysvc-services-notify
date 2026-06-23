import os
import sys

import httpx

# Code example for a UnitySVC Notify gateway-transformer channel (matrix).
#   local_testing : POST the channel-NATIVE matrix body (baked in) straight to
#                   a mock upstream (local_url).  No gateway to transform it, no
#                   platform auth.
#   gateway       : POST the canonical envelope to {BASE_URL}@<channel>; the
#                   gateway transforms it into the matrix-native payload.
# The matrix-native body is baked into this variant — only the local_url (mock
# upstream) and channel (transformer selector) parameters are supplied.
BASE_URL = "${APPRISE_BASE:-https://apprise.unitysvc.dev}/notify"


response = httpx.post(
    "https://mock.unitysvc.dev/matrix/_matrix/client/v3/rooms/demo/send/m.room.message/1",
    headers={"Content-Type": "application/json"},
    json={
        "msgtype": "m.text",
        "body": "Hello from UnitySVC\nNotification delivered via transformer.",
    },
)
if not (200 <= response.status_code < 300):
    print(f"failed (HTTP {response.status_code})", file=sys.stderr)
    sys.exit(1)

print(f"sent (HTTP {response.status_code})")
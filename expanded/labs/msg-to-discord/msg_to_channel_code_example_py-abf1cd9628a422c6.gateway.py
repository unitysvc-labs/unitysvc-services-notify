import os
import sys

import httpx

# Code example for a UnitySVC Notify gateway-transformer channel.
#   local_testing : POST the channel-NATIVE body straight to a mock upstream
#                   (local_url).  No gateway to transform it, no platform auth.
#   gateway       : POST the canonical envelope to {BASE_URL}@<channel>; the
#                   gateway transforms it into the upstream-native payload.
# The native_body / local_url parameters hold the local-mode upstream test
# payload and URL; the channel parameter selects the transformer channel.
BASE_URL = "${API_GATEWAY_BASE_URL}/labs/msg-to-discord"


response = httpx.post(
    f"{BASE_URL}@gateway",
    headers={"Authorization": f"Bearer {k}"} if (k := os.environ.get("UNITYSVC_API_KEY")) else {},
    json={
        "title": "Hello from UnitySVC",
        "body": "Notification delivered via transformer.",
        "type": "info",
        "format": "text",
    },
)
response.raise_for_status()

print(f"sent (HTTP {response.status_code})")
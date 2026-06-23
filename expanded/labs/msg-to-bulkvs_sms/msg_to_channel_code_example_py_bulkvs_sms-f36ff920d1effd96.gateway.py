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
BASE_URL = "${API_GATEWAY_BASE_URL}/labs/msg-to-bulkvs_sms"


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
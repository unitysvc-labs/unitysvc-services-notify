import os
import sys

import httpx

# Code example for a UnitySVC Notify gateway-transformer channel (form-webhook).
#   local_testing : POST the channel-NATIVE form-webhook body (baked in) straight to
#                   a mock upstream (local_url).  No gateway to transform it, no
#                   platform auth.
#   gateway       : POST the canonical envelope to {BASE_URL}@<channel>; the
#                   gateway transforms it into the form-webhook-native payload.
# The form-webhook-native body is baked into this variant — only the local_url (mock
# upstream) and channel (transformer selector) parameters are supplied.
BASE_URL = "${APPRISE_BASE:-https://apprise.unitysvc.dev}/notify"


response = httpx.post(
    "https://mock.unitysvc.dev/form",
    data={
        "version": "1.0",
        "title": "Hello from UnitySVC",
        "message": "Notification delivered via transformer.",
        "type": "info",
    },
)
if not (200 <= response.status_code < 300):
    print(f"failed (HTTP {response.status_code})", file=sys.stderr)
    sys.exit(1)

print(f"sent (HTTP {response.status_code})")
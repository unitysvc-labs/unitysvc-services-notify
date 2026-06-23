import os
import sys

import httpx

# Code example for a UnitySVC Notify gateway-transformer channel (brevo-email).
#   local_testing : POST the channel-NATIVE brevo-email body (baked in) straight to
#                   a mock upstream (local_url).  No gateway to transform it, no
#                   platform auth.
#   gateway       : POST the canonical envelope to {BASE_URL}@<channel>; the
#                   gateway transforms it into the brevo-email-native payload.
# The brevo-email-native body is baked into this variant — only the local_url (mock
# upstream) and channel (transformer selector) parameters are supplied.
BASE_URL = "${APPRISE_BASE:-https://apprise.unitysvc.dev}/notify"


response = httpx.post(
    "https://mock.unitysvc.dev/brevo/v3/smtp/email",
    headers={"Content-Type": "application/json"},
    json={
        "sender": {"email": "test@example.com"},
        "to": [{"email": "test@example.com"}],
        "subject": "connectivity check",
        "textContent": "ping",
    },
)
if not (200 <= response.status_code < 300):
    print(f"failed (HTTP {response.status_code})", file=sys.stderr)
    sys.exit(1)

print(f"sent (HTTP {response.status_code})")
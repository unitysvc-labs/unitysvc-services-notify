import os
import sys

import httpx

# Code example for a UnitySVC Notify gateway-transformer channel (sendgrid-email).
#   local_testing : POST the channel-NATIVE sendgrid-email body (baked in) straight to
#                   a mock upstream (local_url).  No gateway to transform it, no
#                   platform auth.
#   gateway       : POST the canonical envelope to {BASE_URL}@<channel>; the
#                   gateway transforms it into the sendgrid-email-native payload.
# The sendgrid-email-native body is baked into this variant — only the local_url (mock
# upstream) and channel (transformer selector) parameters are supplied.
BASE_URL = "${APPRISE_BASE:-https://apprise.unitysvc.dev}/notify"


response = httpx.post(
    "https://mock.unitysvc.dev/sendgrid/v3/mail/send",
    headers={"Content-Type": "application/json"},
    json={
        "personalizations": [
            {
                "to": [
                    {
                        "email": "test@example.com"
                    }
                ]
            }
        ],
        "from": {
            "email": "test@example.com"
        },
        "subject": "Hello from UnitySVC",
        "content": [
            {
                "type": "text/plain",
                "value": "Notification delivered via transformer.",
            }
        ],
    },
)
if not (200 <= response.status_code < 300):
    print(f"failed (HTTP {response.status_code})", file=sys.stderr)
    sys.exit(1)

print(f"sent (HTTP {response.status_code})")
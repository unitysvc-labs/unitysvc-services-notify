import os
import sys

import httpx

# Code example for a UnitySVC Notify gateway-transformer channel (victorops).
#   local_testing : POST the channel-NATIVE victorops body (baked in) straight to
#                   a mock upstream (local_url).  No gateway to transform it, no
#                   platform auth.
#   gateway       : POST the canonical envelope to {BASE_URL}@<channel>; the
#                   gateway transforms it into the victorops-native payload.
# The victorops-native body is baked into this variant — only the local_url (mock
# upstream) and channel (transformer selector) parameters are supplied.
BASE_URL = "${APPRISE_BASE:-https://apprise.unitysvc.dev}/notify"


response = httpx.post(
    "https://mock.unitysvc.dev/victorops/integrations/generic/apikey123abc/alert/routingkey",
    headers={"Content-Type": "application/json"},
    json={
        "message_type": "CRITICAL",
        "entity_display_name": "Hello from UnitySVC",
        "state_message": "Notification delivered via transformer.",
    },
)
if not (200 <= response.status_code < 300):
    print(f"failed (HTTP {response.status_code})", file=sys.stderr)
    sys.exit(1)

print(f"sent (HTTP {response.status_code})")
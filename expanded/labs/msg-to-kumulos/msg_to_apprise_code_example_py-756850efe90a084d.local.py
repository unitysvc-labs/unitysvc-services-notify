import os

import httpx

# Code example for a UnitySVC Notify transformer (Apprise) service.
#   local_testing : POST the COMPOSED apprise body straight to the apprise-api.
#   gateway       : POST the canonical envelope; the gateway composes "urls".
# The apprise_url parameter holds the per-channel test URL, e.g. discord://demo/demotoken.
URL = "${APPRISE_BASE:-https://apprise.unitysvc.dev}/notify"


response = httpx.post(
    URL,
    json={
        "urls": "kumulos://12345678-1234-4123-8123-123456789abc/DKRY5CJQX4BIPW3AHOV29GNU18FMT07ELSZ6",
        "title": "Hello from UnitySVC",
        "body": "Notification delivered via transformer.",
        "type": "info",
        "format": "text",
    },
)

response.raise_for_status()
print(f"sent (HTTP {response.status_code})")
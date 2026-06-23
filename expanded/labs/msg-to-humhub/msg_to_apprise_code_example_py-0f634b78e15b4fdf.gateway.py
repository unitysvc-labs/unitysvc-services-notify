import os

import httpx

# Code example for a UnitySVC Notify transformer (Apprise) service.
#   local_testing : POST the COMPOSED apprise body straight to the apprise-api.
#   gateway       : POST the canonical envelope; the gateway composes "urls".
# The apprise_url parameter holds the per-channel test URL, e.g. discord://demo/demotoken.
URL = "${API_GATEWAY_BASE_URL}/labs/msg-to-humhub"


response = httpx.post(
    URL,
    headers={"Authorization": f"Bearer {k}"} if (k := os.environ.get("UNITYSVC_API_KEY")) else {},
    json={
        "title": "Hello from UnitySVC",
        "body": "Notification delivered via transformer.",
        "from": "user@example.com",
    },
)

response.raise_for_status()
print(f"sent (HTTP {response.status_code})")
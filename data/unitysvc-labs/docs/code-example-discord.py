import os
import requests

# Environment variables set by UnitySVC after enrollment
base_url = os.environ["SERVICE_BASE_URL"]
api_key = os.environ["UNITYSVC_API_KEY"]

# Send a message using Discord's webhook format
response = requests.post(
    base_url,
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    },
    json={"content": "Hello from UnitySVC!"},
)

print(response.status_code)

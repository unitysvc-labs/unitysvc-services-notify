"""Send a Discord notification via the unitysvc-py SDK with request logging.

Replaces failed_notify-discord-byok_Python_code_example_notify_gateway.py.
Uses the SDK's start/stop request-logging endpoints so the full
request+response JSON is captured and printed — useful for writing mock
service assertions.

Required env vars:
    UNITYSVC_API_KEY          svcpass_... key for your customer account
    UNITYSVC_API_URL          backend base URL, e.g. http://localhost:8000
    NOTIFY_DISCORD_SERVICE_ID UUID of the notify-discord-byok service

Optional env vars:
    MOCK_DISCORD_WEBHOOK_URL  where to point DISCORD_WEBHOOK_URL for testing
                              (default: http://localhost:8101/api/webhooks/mock/token)
    DISCORD_MESSAGE           message text to send (default: "Hello from unitysvc-py!")

Usage:
    export UNITYSVC_API_KEY=svcpass_...
    export UNITYSVC_API_URL=http://localhost:8000
    export NOTIFY_DISCORD_SERVICE_ID=<uuid>
    python notify_discord_sdk_example.py
"""

from __future__ import annotations

import json
import os
import sys

from unitysvc import Client


def main() -> None:
    api_key = os.environ.get("UNITYSVC_API_KEY", "")
    if not api_key:
        sys.exit("UNITYSVC_API_KEY is required")

    api_url = os.environ.get("UNITYSVC_API_URL", "http://localhost:8000")
    service_id = os.environ.get("NOTIFY_DISCORD_SERVICE_ID", "")
    if not service_id:
        sys.exit("NOTIFY_DISCORD_SERVICE_ID is required")

    mock_webhook = os.environ.get(
        "MOCK_DISCORD_WEBHOOK_URL",
        "http://localhost:8100/api/webhooks/mock/token",
    )
    message = os.environ.get("DISCORD_MESSAGE", "Hello from unitysvc-py!")

    client = Client(
        api_key=api_key,
        base_url=f"{api_url.rstrip('/')}/v1/customer",
    )

    # Point the customer's webhook secret at the mock server so the
    # notify worker calls the mock instead of real Discord.
    print(f"[1/5] Setting DISCORD_WEBHOOK_URL → {mock_webhook}")
    client.secrets.set("DISCORD_WEBHOOK_URL", mock_webhook)

    # Enable request logging so the gateway dispatch is persisted.
    print("[2/5] Starting request logging")
    client.request_logs.start()

    # Dispatch through the gateway; the notify worker calls the mock
    # webhook with {"content": message} and returns a SendResponse.
    print(f"[3/5] Dispatching notify to service {service_id}")
    resp = client.services.dispatch(
        service_id,
        path="/send",
        json={"message": message, "target": "", "format": "text"},
    )
    print(f"      status={resp.status_code}")
    try:
        print(f"      body={json.dumps(resp.json(), indent=2)}")
    except Exception:
        print(f"      body={resp.text!r}")

    # Stop logging before reading so we don't capture our own list call.
    print("[4/5] Stopping request logging")
    client.request_logs.stop()

    # Fetch the persisted log entries.  Each entry carries the full
    # upstream request+response; the upstream identity/credential fields
    # are redacted server-side.
    print("[5/5] Request logs:")
    logs = client.request_logs.list(service_id=service_id)  # type: ignore[call-arg]
    if not logs.data:
        print("      (no entries — logging may not have flushed yet; retry in a moment)")
        return

    for entry in logs.data:
        detail = client.request_logs.get(entry.id)
        print(json.dumps(detail.to_dict(), indent=2, default=str))


if __name__ == "__main__":
    main()

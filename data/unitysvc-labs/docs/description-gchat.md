# Google Chat Notifications (Bring Your Own Webhook)

Send messages to Google Chat spaces via the UnitySVC gateway using your own Google Chat webhook URL.

## Prerequisites

1. **Create an incoming webhook** in your Google Chat space: open the space → Manage webhooks → Add webhook.
2. Copy the full webhook URL (e.g. `https://chat.googleapis.com/v1/spaces/.../messages?key=...`).
3. **Enroll** using your webhook URL — stored as `GCHAT_WEBHOOK_URL` in your secrets.

## API

Send a message via `POST /send`:

```json
{
  "target": "",
  "message": "Hello from UnitySVC!",
  "format": "text"
}
```

| Field     | Type   | Required | Description                                                    |
|-----------|--------|----------|----------------------------------------------------------------|
| `target`  | string | no       | Leave empty — the webhook already targets a specific space     |
| `message` | string | yes      | Message text                                                   |
| `format`  | string | no       | `text` (default) or `card` (Google Chat card format JSON)      |

## Notes

- Google Chat webhooks send to a fixed space. To send to multiple spaces, enroll multiple times with different webhook URLs.
- For `format: "card"`, pass the Google Chat card JSON as a string in the `message` field.

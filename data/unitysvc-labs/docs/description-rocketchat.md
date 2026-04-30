# Rocket.Chat Notifications (Bring Your Own Rocket.Chat Webhook)

Send messages to Rocket.Chat channels using your own incoming webhook URL.

## Prerequisites

1. **Enable Incoming Webhooks** in your Rocket.Chat admin panel: Administration → Integrations → New Integration → Incoming.
2. **Configure the webhook**: set the channel, bot name, and optionally an icon.
3. **Copy the webhook URL** after saving.
4. **Enroll** using the webhook URL — stored as `ROCKETCHAT_WEBHOOK_URL` in your secrets.

## API

Send a message via `POST /send`:

```json
{
  "target": "",
  "message": "Hello from UnitySVC!",
  "format": "text"
}
```

| Field     | Type   | Required | Description                                        |
|-----------|--------|----------|----------------------------------------------------|
| `target`  | string | no      | Unused — the webhook URL is already scoped to a specific Rocket.Chat channel |
| `message` | string | yes      | Message text                                       |
| `format`  | string | no       | `text` (default)                                   |

## Notes

- Works with both Rocket.Chat Cloud and self-hosted instances.

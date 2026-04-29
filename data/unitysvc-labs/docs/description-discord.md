# Discord Notifications (Bring Your Own Webhook)

Send messages to Discord channels via the UnitySVC gateway using your own Discord webhook URL.

## Prerequisites

1. **Create a Webhook** in your Discord server: go to channel settings → Integrations → Webhooks → New Webhook.
2. Copy the full webhook URL (e.g. `https://discord.com/api/webhooks/...`).
3. **Enroll** using your webhook URL — stored as `DISCORD_WEBHOOK_URL` in your secrets.

## API

Send a message via `POST /send`:

```json
{
  "target": "",
  "message": "Hello from UnitySVC!",
  "format": "text"
}
```

| Field     | Type   | Required | Description                                                   |
|-----------|--------|----------|---------------------------------------------------------------|
| `target`  | string | no       | Leave empty — the webhook already targets a specific channel  |
| `message` | string | yes      | Message content (plain text or Discord markdown)              |
| `format`  | string | no       | `text` (default) or `markdown`                                |

## Notes

- Discord webhooks send to a fixed channel. To send to multiple channels, enroll multiple times with different webhook URLs.
- Discord supports markdown formatting natively — use `format: "markdown"` to enable it.

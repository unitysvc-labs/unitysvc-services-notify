# Feishu / Lark Notifications (Bring Your Own Feishu/Lark Bot Webhook)

Send messages to Feishu (Lark internationally) groups using your own incoming webhook.

## Prerequisites

1. **Open a Feishu/Lark group** and click **Settings → Bots → Add Bot → Custom Bot**.
2. **Copy the webhook URL** provided and optionally configure a signing secret.
3. **Enroll** using the webhook URL — stored as `FEISHU_WEBHOOK_URL` in your secrets.

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
| `target`  | string | no      | Unused — the webhook URL is already scoped to a specific group or bot |
| `message` | string | yes      | Message text                                       |
| `format`  | string | no       | `text` (default)                                   |

## Notes

- Feishu and Lark are the same application: Feishu is the name used in China, Lark is used internationally.

# Mattermost Notifications (Bring Your Own Webhook)

Send messages to Mattermost channels via the UnitySVC gateway using your own incoming webhook URL.

## Prerequisites

1. **Enable Incoming Webhooks** in your Mattermost instance (System Console → Integrations → Integration Management).
2. **Create an Incoming Webhook**:
   - Go to your team → **Integrations** → **Incoming Webhooks** → **Add Incoming Webhook**.
   - Select the target channel and click **Save**.
3. **Copy the webhook URL** and store it as `MATTERMOST_WEBHOOK_URL` during enrollment.

## API

Send a message via `POST /send`:

```json
{
  "target": "",
  "message": "Hello from UnitySVC!",
  "format": "text"
}
```

| Field     | Type   | Required | Description                                                      |
|-----------|--------|----------|------------------------------------------------------------------|
| `target`  | string | no       | Unused — the webhook URL is already scoped to a specific channel |
| `message` | string | yes      | Message text                                                     |
| `format`  | string | no       | `text` (default) or `markdown`                                   |

## Notes

- Works with both Mattermost Cloud and self-hosted instances.
- Each webhook URL is bound to one channel; create a separate enrollment per channel.

# Microsoft Teams Notifications (Bring Your Own Webhook)

Send messages to Microsoft Teams channels via the UnitySVC gateway using your own incoming webhook URL.

## Prerequisites

1. **Create an Incoming Webhook** in your Teams channel:
   - Open the channel → click **...** → **Connectors** → search for **Incoming Webhook** → **Configure**.
   - Give it a name, optionally upload an icon, then click **Create**.
2. **Copy the webhook URL** provided after creation.
3. **Enroll** using your webhook URL — stored as `TEAMS_WEBHOOK_URL` in your secrets.

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

- Each webhook URL is scoped to a single Teams channel; enroll once per channel.
- Teams Connectors (legacy Office 365 webhooks) will be retired; this service uses the current **Incoming Webhook** connector which remains supported.

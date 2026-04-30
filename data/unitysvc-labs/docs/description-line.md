# LINE Notifications (Bring Your Own Channel)

Send messages to LINE users and groups via the UnitySVC gateway using your own LINE Messaging API channel.

## Prerequisites

1. **Create a LINE Messaging API channel** in the [LINE Developers Console](https://developers.line.biz/console/).
2. **Copy the Channel Secret** and **Channel Access Token** (long-lived) from the channel settings.
3. **Enroll** using both credentials — stored as `LINE_CHANNEL_SECRET` and `LINE_CHANNEL_TOKEN` in your secrets.

## API

Send a message via `POST /send`:

```json
{
  "target": "<user_id or group_id>",
  "message": "Hello from UnitySVC!",
  "format": "text"
}
```

| Field     | Type   | Required | Description                                                     |
|-----------|--------|----------|-----------------------------------------------------------------|
| `target`  | string | yes      | LINE user ID (e.g. `Uxxxxxxxx`) or group ID (e.g. `Cxxxxxxxx`) |
| `message` | string | yes      | Message text                                                    |
| `format`  | string | no       | `text` (default)                                                |

## Getting User and Group IDs

- **User ID**: Webhook events sent to your channel include the `source.userId` field. Use the [LINE Messaging API SDK](https://github.com/line/line-bot-sdk-python) to capture it.
- **Group ID**: Add your bot to a group; webhook events include `source.groupId`.
- Your bot must follow the user (or be in the group) before it can send messages.

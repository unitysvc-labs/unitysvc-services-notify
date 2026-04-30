# Cisco Webex Notifications (Bring Your Own Webex Bot)

Send messages to Cisco Webex rooms and users using your own Webex bot.

## Prerequisites

1. **Create a Webex bot** at [developer.webex.com/my-apps/new/bot](https://developer.webex.com/my-apps/new/bot).
2. **Copy the bot access token** shown immediately after creation (it is only shown once).
3. **Add the bot** to the Webex room or space where you want to send messages.
4. **Enroll** using the bot token — stored as `WEBEX_BOT_TOKEN` in your secrets.

## API

Send a message via `POST /send`:

```json
{
  "target": "room:Y2lzY29zcGFyazovL3VzL1JPT00v",
  "message": "Hello from UnitySVC!",
  "format": "text"
}
```

| Field     | Type   | Required | Description                                        |
|-----------|--------|----------|----------------------------------------------------|
| `target`  | string | yes      | Room ID prefixed with `room:` or email address prefixed with `email:` (e.g. `email:user@example.com`) |
| `message` | string | yes      | Message text                                       |
| `format`  | string | no       | `text` (default)                                   |

## Notes

- The bot must be added to a room before it can send messages there.
- Room IDs can be found via the Webex API: `GET https://webexapis.com/v1/rooms`.

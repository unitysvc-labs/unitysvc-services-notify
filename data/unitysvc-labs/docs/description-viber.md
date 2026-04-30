# Viber Notifications (Bring Your Own Viber Bot)

Send messages to Viber users using your own Viber bot.

## Prerequisites

1. **Create a Viber bot** (Public Account or chatbot) via the [Viber Admin Panel](https://partners.viber.com/account/create-bot-account).
2. **Copy the auth token** shown after creation.
3. **Enroll** using the auth token — stored as `VIBER_AUTH_TOKEN` in your secrets.

## API

Send a message via `POST /send`:

```json
{
  "target": "01234567890A=",
  "message": "Hello from UnitySVC!",
  "format": "text"
}
```

| Field     | Type   | Required | Description                                        |
|-----------|--------|----------|----------------------------------------------------|
| `target`  | string | yes      | Viber user ID (obtained from webhook events when a user sends a message to your bot) |
| `message` | string | yes      | Message text                                       |
| `format`  | string | no       | `text` (default)                                   |

## Notes

- Users must initiate a conversation with your bot first (opt-in) before you can send them messages.
- Viber user IDs are obtained from incoming webhook events.

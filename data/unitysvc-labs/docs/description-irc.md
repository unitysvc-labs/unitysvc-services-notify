# IRC Notifications (Bring Your Own IRC Bot)

Send messages to IRC channels or users using your own registered IRC nickname.

## Prerequisites

1. **Register a nickname** on your target IRC network (e.g. `/msg NickServ REGISTER <password> <email>` on Libera.Chat).
2. **Note the IRC server**, your registered nickname, NickServ password, and the default channel.
3. **Enroll** using all four values — stored as `IRC_SERVER`, `IRC_NICK`, `IRC_PASSWORD`, and `IRC_CHANNEL`.

## API

Send a message via `POST /send`:

```json
{
  "target": "#channel-name",
  "message": "Hello from UnitySVC!",
  "format": "text"
}
```

| Field     | Type   | Required | Description                                        |
|-----------|--------|----------|----------------------------------------------------|
| `target`  | string | yes      | IRC channel (e.g. `#myproject`) or nickname for a private message |
| `message` | string | yes      | Message text                                       |
| `format`  | string | no       | `text` (default)                                   |

## Notes

- The bot connects to IRC using SASL PLAIN auth (NickServ). For networks without NickServ, leave IRC_PASSWORD empty.
- The `target` field in each request overrides the default channel enrollment var.

# Signal Notifications (Bring Your Own signal-cli Instance)

Send messages to Signal users using your own signal-cli REST API instance.

## Prerequisites

1. **Run signal-cli-rest-api** ([github.com/bbernhard/signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api)) on a server you control and register a phone number.
2. **Note your server URL** (e.g. `http://your-server:8080`) and configure an auth token.
3. **Enroll** using both values — stored as `SIGNAL_AUTH_TOKEN` and `SIGNAL_SERVER_URL` in your secrets.

## API

Send a message via `POST /send`:

```json
{
  "target": "+15551234567",
  "message": "Hello from UnitySVC!",
  "format": "text"
}
```

| Field     | Type   | Required | Description                                        |
|-----------|--------|----------|----------------------------------------------------|
| `target`  | string | yes      | Recipient's phone number in E.164 format |
| `message` | string | yes      | Message text                                       |
| `format`  | string | no       | `text` (default)                                   |

## Notes

- Signal's official clients use end-to-end encryption; this service relies on signal-cli which must be linked to an active Signal account.

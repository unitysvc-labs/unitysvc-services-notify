# Zalo Notifications (Bring Your Own Zalo Official Account)

Send messages to Zalo users using your own Zalo Official Account.

## Prerequisites

1. **Create a Zalo Official Account** at [oa.zalo.me](https://oa.zalo.me/) and get it verified.
2. **Generate an access token** from the Zalo Developer portal under your OA credentials.
3. **Enroll** using the access token — stored as `ZALO_ACCESS_TOKEN` in your secrets.

## API

Send a message via `POST /send`:

```json
{
  "target": "user:1234567890123456789",
  "message": "Hello from UnitySVC!",
  "format": "text"
}
```

| Field     | Type   | Required | Description                                        |
|-----------|--------|----------|----------------------------------------------------|
| `target`  | string | yes      | Zalo user ID prefixed with `user:` (e.g. `user:1234567890123456789`) |
| `message` | string | yes      | Message text                                       |
| `format`  | string | no       | `text` (default)                                   |

## Notes

- Zalo is the dominant messaging platform in Vietnam with 75M+ users. Users must follow your Official Account before you can message them.

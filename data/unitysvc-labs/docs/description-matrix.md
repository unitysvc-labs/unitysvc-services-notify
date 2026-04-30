# Matrix Notifications (Bring Your Own Account)

Send messages to Matrix rooms via the UnitySVC gateway using your own Matrix access token and homeserver.

## Prerequisites

1. **Have a Matrix account** on any homeserver (e.g. matrix.org, or self-hosted Synapse/Dendrite).
2. **Obtain an access token**:
   - Log in via Element → **Settings** → **Help & About** → scroll to **Access Token** and click to reveal.
   - Alternatively, call `POST /_matrix/client/v3/login` on your homeserver.
3. **Note your homeserver URL** (e.g. `https://matrix.org`).
4. **Enroll** using both values — stored as `MATRIX_ACCESS_TOKEN` and `MATRIX_HOMESERVER` in your secrets.

## API

Send a message via `POST /send`:

```json
{
  "target": "!roomid:homeserver.tld",
  "message": "Hello from UnitySVC!",
  "format": "text"
}
```

| Field     | Type   | Required | Description                                                      |
|-----------|--------|----------|------------------------------------------------------------------|
| `target`  | string | yes      | Matrix room ID (e.g. `!abc123:matrix.org`) or room alias (`#room:server`) |
| `message` | string | yes      | Message text                                                     |
| `format`  | string | no       | `text` (default) or `html`                                       |

## Getting the Room ID

In Element: open the room → **Settings** → **Advanced** → copy the **Internal room ID** (starts with `!`).
Your account must be a member of the room before it can send messages.

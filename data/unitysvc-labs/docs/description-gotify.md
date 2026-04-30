# Gotify Notifications (Bring Your Own Gotify Server)

Send push notifications to your self-hosted Gotify server.

## Prerequisites

1. **Deploy Gotify** ([gotify.net](https://gotify.net/)) on your own server using Docker or the binary.
2. **Create an application** in the Gotify web UI and copy the **app token**.
3. **Note your Gotify server URL** (e.g. `https://gotify.example.com`).
4. **Enroll** using both values — stored as `GOTIFY_APP_TOKEN` and `GOTIFY_SERVER_URL`.

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
| `target`  | string | no      | Unused — the app token is already scoped to a specific Gotify application |
| `message` | string | yes      | Message text                                       |
| `format`  | string | no       | `text` (default)                                   |

## Notes

- Gotify is a self-hosted, open-source push notification server. Subscribers use the Gotify Android app or any compatible client.

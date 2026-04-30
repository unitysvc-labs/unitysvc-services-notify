# Pushover Notifications (Bring Your Own Pushover Application)

Send push notifications to mobile devices using your own Pushover application.

## Prerequisites

1. **Create a Pushover account** at [pushover.net](https://pushover.net/) and install the app on your device.
2. **Register an application** at [pushover.net/apps/build](https://pushover.net/apps/build) to get an **API Token / App Token**.
3. **Copy your User Key** from the Pushover dashboard (top of the main page).
4. **Enroll** using both values — stored as `PUSHOVER_APP_TOKEN` and `PUSHOVER_USER_KEY`.

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
| `target`  | string | no      | Unused — the Pushover user key in enrollment vars identifies the recipient |
| `message` | string | yes      | Message text                                       |
| `format`  | string | no       | `text` (default)                                   |

## Notes

- Pushover is a one-time purchase ($5 per platform). After the free trial, a license is required for the iOS or Android app.

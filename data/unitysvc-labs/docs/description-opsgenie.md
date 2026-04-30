# Opsgenie Notifications (Bring Your Own Opsgenie Integration)

Create Opsgenie alerts using your own Opsgenie API integration key.

## Prerequisites

1. **Log in to Opsgenie** at [app.opsgenie.com](https://app.opsgenie.com/).
2. **Create an API integration**: Settings → Integrations → Add Integration → **API**.
3. **Copy the API Key** shown for the integration.
4. **Enroll** using the API key — stored as `OPSGENIE_API_KEY` in your secrets.

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
| `target`  | string | no      | Unused — the API key determines the team and integration target |
| `message` | string | yes      | Message text                                       |
| `format`  | string | no       | `text` (default)                                   |

## Notes

- Alerts are created via the [Opsgenie Alert API](https://docs.opsgenie.com/docs/alert-api). The `message` field maps to the alert message.

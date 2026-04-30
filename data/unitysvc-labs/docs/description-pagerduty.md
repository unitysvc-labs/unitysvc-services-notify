# PagerDuty Notifications (Bring Your Own PagerDuty Integration)

Trigger PagerDuty incidents and alerts using your own Events API v2 integration key.

## Prerequisites

1. **Create or open a PagerDuty service** at [app.pagerduty.com](https://app.pagerduty.com/).
2. **Add an integration**: open the service → Integrations → Add Integration → **Events API v2**.
3. **Copy the Integration Key** (also called routing key).
4. **Enroll** using the routing key — stored as `PAGERDUTY_ROUTING_KEY` in your secrets.

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
| `target`  | string | no      | Unused — the routing key identifies the service and on-call responders |
| `message` | string | yes      | Message text                                       |
| `format`  | string | no       | `text` (default)                                   |

## Notes

- Messages sent via this service trigger PagerDuty incidents. The `message` field is used as the incident description.
- Severity can optionally be passed via the `format` field using values: `critical`, `error`, `warning`, `info`.

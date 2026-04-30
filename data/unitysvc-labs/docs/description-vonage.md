# Vonage SMS Notifications (Bring Your Own Vonage Account)

Send SMS messages using your own Vonage (Nexmo) account.

## Prerequisites

1. **Create a Vonage account** at [vonage.com](https://www.vonage.com/) and obtain or verify a phone number.
2. **Copy your API Key and API Secret** from the [Vonage Dashboard](https://dashboard.nexmo.com/).
3. **Enroll** using all three values — stored as `VONAGE_API_KEY`, `VONAGE_API_SECRET`, and `VONAGE_FROM_NUMBER`.

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

- Vonage charges per message sent. See [Vonage pricing](https://www.vonage.com/communications-apis/sms/) for current SMS rates.

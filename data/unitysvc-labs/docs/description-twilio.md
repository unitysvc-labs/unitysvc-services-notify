# Twilio SMS Notifications (Bring Your Own Twilio Account)

Send SMS messages using your own Twilio account.

## Prerequisites

1. **Create a Twilio account** at [twilio.com](https://www.twilio.com/) and purchase or verify a phone number.
2. **Copy your Account SID and Auth Token** from the Twilio Console dashboard.
3. **Enroll** using all three values — stored as `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, and `TWILIO_FROM_NUMBER`.

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

- Twilio charges per message sent. See [Twilio pricing](https://www.twilio.com/en-us/sms/pricing) for current SMS rates in your country.

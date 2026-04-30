# WhatsApp Notifications (Bring Your Own Account)

Send messages to WhatsApp users via the UnitySVC gateway using your own WhatsApp Business Cloud API credentials.

## Prerequisites

1. **Create a Meta Developer account** at [developers.facebook.com](https://developers.facebook.com/) and set up a **WhatsApp Business** app.
2. **Add the WhatsApp product** to your app and complete Business Verification.
3. **Obtain credentials** from your app dashboard:
   - **Phone Number ID** — found under WhatsApp → API Setup → Phone Number ID.
   - **System User Access Token** — create a System User in Business Settings → System Users, assign it to your app with `whatsapp_business_messaging` permission, then generate a token.
4. **Enroll** using both values — stored as `WHATSAPP_PHONE_NUMBER_ID` and `WHATSAPP_ACCESS_TOKEN` in your secrets.

## API

Send a message via `POST /send`:

```json
{
  "target": "+15551234567",
  "message": "Hello from UnitySVC!",
  "format": "text"
}
```

| Field     | Type   | Required | Description                                              |
|-----------|--------|----------|----------------------------------------------------------|
| `target`  | string | yes      | Recipient's phone number in E.164 format (e.g. `+15551234567`) |
| `message` | string | yes      | Message text                                             |
| `format`  | string | no       | `text` (default)                                         |

## Notes

- The recipient must have an active WhatsApp account and must have opted in to receive messages from your business.
- WhatsApp Business Cloud API charges per conversation — see [Meta's pricing](https://developers.facebook.com/docs/whatsapp/pricing) for current rates.
- For production use, your Meta app must pass app review and complete business verification.

# KakaoTalk Notifications (Bring Your Own KakaoTalk Business Channel)

Send messages to KakaoTalk users using your own KakaoTalk Business Channel.

## Prerequisites

1. **Register a KakaoTalk Business Channel** at [business.kakao.com](https://business.kakao.com/).
2. **Set up the KakaoTalk Channel API** via the Kakao Developers console and create an app.
3. **Generate an access token** using your app's REST API key through the OAuth2 flow.
4. **Enroll** using the access token — stored as `KAKAO_ACCESS_TOKEN` in your secrets.

## API

Send a message via `POST /send`:

```json
{
  "target": "user:abc123def456",
  "message": "Hello from UnitySVC!",
  "format": "text"
}
```

| Field     | Type   | Required | Description                                        |
|-----------|--------|----------|----------------------------------------------------|
| `target`  | string | yes      | KakaoTalk user ID prefixed with `user:` (obtained from OAuth2 login flow) |
| `message` | string | yes      | Message text                                       |
| `format`  | string | no       | `text` (default)                                   |

## Notes

- KakaoTalk is the dominant messaging app in South Korea with 45M+ monthly active users.
- Users must have added your business channel as a friend before you can send them messages.

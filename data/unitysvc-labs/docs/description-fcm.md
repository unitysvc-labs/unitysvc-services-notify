# Firebase Cloud Messaging (FCM) Notifications (Bring Your Own Firebase Project)

Send push notifications to Android and web apps using your own Firebase Cloud Messaging (FCM) project.

## Prerequisites

1. **Create a Firebase project** at [console.firebase.google.com](https://console.firebase.google.com/).
2. **Add your Android or web app** to the project and integrate the Firebase SDK.
3. **Get your Server Key**: Project Settings → Cloud Messaging → Server Key (Legacy) or generate a service account key for v1 API.
4. **Enroll** using the server key — stored as `FCM_SERVER_KEY` in your secrets.

## API

Send a message via `POST /send`:

```json
{
  "target": "token:dxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "message": "Hello from UnitySVC!",
  "format": "text"
}
```

| Field     | Type   | Required | Description                                        |
|-----------|--------|----------|----------------------------------------------------|
| `target`  | string | yes      | Device registration token prefixed with `token:`, or topic prefixed with `topic:` (e.g. `topic:news`) |
| `message` | string | yes      | Message text                                       |
| `format`  | string | no       | `text` (default)                                   |

## Notes

- FCM is the standard push notification service for Android apps and Chrome. For iOS, FCM routes through APNs.
- Device registration tokens are issued when users install and open your app.

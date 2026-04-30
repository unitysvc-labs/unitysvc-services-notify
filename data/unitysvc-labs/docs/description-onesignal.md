# OneSignal Notifications (Bring Your Own OneSignal App)

Send web and mobile push notifications using your own OneSignal application.

## Prerequisites

1. **Create a OneSignal account** at [onesignal.com](https://onesignal.com/) and add a new app.
2. **Configure push platforms** (Web Push, FCM for Android, APNs for iOS) in app settings.
3. **Copy your App ID and REST API Key** from Settings → Keys & IDs.
4. **Enroll** using both values — stored as `ONESIGNAL_APP_ID` and `ONESIGNAL_API_KEY`.

## API

Send a message via `POST /send`:

```json
{
  "target": "player:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "message": "Hello from UnitySVC!",
  "format": "text"
}
```

| Field     | Type   | Required | Description                                        |
|-----------|--------|----------|----------------------------------------------------|
| `target`  | string | yes      | Player/device ID prefixed with `player:`, or `tag:<key>=<value>` to target by user segment |
| `message` | string | yes      | Message text                                       |
| `format`  | string | no       | `text` (default)                                   |

## Notes

- OneSignal supports web push, iOS, Android, and email. This service uses the push notification API.
- Player IDs are assigned when users subscribe to your app's notifications.

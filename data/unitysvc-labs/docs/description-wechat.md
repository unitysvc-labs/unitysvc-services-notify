# WeChat (WeCom) Notifications (Bring Your Own WeCom App)

Send messages to WeCom (Enterprise WeChat) users using your own WeCom application.

## Prerequisites

1. **Create a WeCom account** at [work.weixin.qq.com](https://work.weixin.qq.com/) and set up an organization.
2. **Create an application** (App Management → Create App). Note the **Agent ID**.
3. **Copy your Corp ID** from Settings → General, and the **Corp Secret** from your app's settings.
4. **Enroll** using all three values — stored as `WECHAT_CORP_ID`, `WECHAT_CORP_SECRET`, and `WECHAT_AGENT_ID`.

## API

Send a message via `POST /send`:

```json
{
  "target": "@user123",
  "message": "Hello from UnitySVC!",
  "format": "text"
}
```

| Field     | Type   | Required | Description                                        |
|-----------|--------|----------|----------------------------------------------------|
| `target`  | string | yes      | WeCom user account or `@all` to broadcast to the entire organization |
| `message` | string | yes      | Message text                                       |
| `format`  | string | no       | `text` (default)                                   |

## Notes

- WeCom (Enterprise WeChat) is distinct from WeChat public accounts and is designed for internal organizational messaging.

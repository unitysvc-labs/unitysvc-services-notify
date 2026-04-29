# Telegram Notifications (Bring Your Own Bot)

Send messages to Telegram chats, groups, and channels via the UnitySVC gateway using your own Telegram Bot.

## Prerequisites

1. **Create a Telegram Bot** via [@BotFather](https://t.me/BotFather) and copy the bot token.
2. **Get the chat ID** of the target chat, group, or channel where you want to send messages.
3. **Enroll** using your bot token — stored as `TELEGRAM_BOT_TOKEN` in your secrets.

## API

Send a message via `POST /send`:

```json
{
  "target": "<chat_id>",
  "message": "Hello from UnitySVC!",
  "format": "text"
}
```

| Field     | Type   | Required | Description                                             |
|-----------|--------|----------|---------------------------------------------------------|
| `target`  | string | yes      | Telegram chat ID (numeric) or `@username` for channels |
| `message` | string | yes      | Message text                                            |
| `format`  | string | no       | `text` (default) or `html` or `markdown`               |

## Getting the Chat ID

- **Private chat**: Start a conversation with your bot, then call `https://api.telegram.org/bot<TOKEN>/getUpdates` to find your chat ID.
- **Group**: Add your bot to the group; the chat ID appears in `getUpdates` as a negative integer.
- **Channel**: Use `@channel_username` as the target (bot must be an admin of the channel).

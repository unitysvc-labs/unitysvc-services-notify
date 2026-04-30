# Discord Notifications (Bring Your Own Bot)

Send messages to Discord channels and users via the UnitySVC gateway using your own Discord Bot.

## Prerequisites

1. **Create a Discord Application** at [discord.com/developers/applications](https://discord.com/developers/applications).
2. Go to **Bot** → **Add Bot** → **Reset Token** and copy the bot token.
3. Under **OAuth2 → URL Generator**, select `bot` scope + `Send Messages` permission, then invite the bot to your server.
4. **Enroll** using your bot token — stored as `DISCORD_BOT_TOKEN` in your secrets.

## API

Send a message via `POST /send`:

```json
{
  "target": "channel:987654321",
  "message": "Deployment complete!",
  "format": "text"
}
```

| Field     | Type   | Required | Description                                                           |
|-----------|--------|----------|-----------------------------------------------------------------------|
| `target`  | string | yes      | `channel:<channel_id>` or `user:<user_id>` (DM)                       |
| `message` | string | yes      | Message content (plain text or Discord markdown)                      |
| `format`  | string | no       | `text` (default) or `markdown`                                        |

## Getting Channel and User IDs

Enable **Developer Mode** in Discord (Settings → App Settings → Advanced), then right-click any channel or user to copy its ID.

## Notes

- The bot must be a member of the server and have **Send Messages** permission in the target channel.
- For DMs, use `user:<user_id>` — the user must have previously messaged your bot.

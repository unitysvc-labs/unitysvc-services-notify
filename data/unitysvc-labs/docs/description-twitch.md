# Twitch Notifications (Bring Your Own Twitch Bot)

Send messages to Twitch chat using your own Twitch bot account.

## Prerequisites

1. **Create a Twitch bot account** (a regular Twitch account used as a bot) and log in.
2. **Generate an OAuth token** at [twitchapps.com/tmi](https://twitchapps.com/tmi/) while logged in as the bot account.
3. **Note the Twitch channel** name (all lowercase) where the bot will send messages. The bot account must follow the channel.
4. **Enroll** using both values — stored as `TWITCH_BOT_TOKEN` and `TWITCH_CHANNEL`.

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
| `target`  | string | no      | Unused — the channel is set via the `TWITCH_CHANNEL` enrollment var (BYOK) or `twitch_channel` parameter (relay) |
| `message` | string | yes      | Message text                                       |
| `format`  | string | no       | `text` (default)                                   |

## Notes

- The bot must follow (join) the target channel before it can send messages.
- The OAuth token format is `oauth:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`.

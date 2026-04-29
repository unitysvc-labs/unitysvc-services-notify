# Slack Notifications (Bring Your Own Bot)

Send messages to Slack channels via the UnitySVC gateway using your own Slack Bot.

## Prerequisites

1. **Create a Slack App** at [api.slack.com/apps](https://api.slack.com/apps) with the `chat:write` OAuth scope.
2. Install the app to your workspace and copy the **Bot User OAuth Token** (starts with `xoxb-`).
3. **Invite the bot** to the target channel: `/invite @your-bot-name`.
4. Copy the **channel ID** from the channel settings (the alphanumeric ID, e.g. `C0123456789`).
5. **Enroll** with `SLACK_BOT_TOKEN` and `SLACK_CHANNEL_ID`.

## API

Send a message via `POST /send`:

```json
{
  "target": "C0123456789",
  "message": "Hello from UnitySVC!",
  "format": "text"
}
```

| Field     | Type   | Required | Description                                                                     |
|-----------|--------|----------|---------------------------------------------------------------------------------|
| `target`  | string | no       | Channel ID to override the enrolled `SLACK_CHANNEL_ID`; leave empty to use default |
| `message` | string | yes      | Message text                                                                    |
| `format`  | string | no       | `text` (default) or `markdown` (Slack mrkdwn)                                  |

## Notes

- The enrolled `SLACK_CHANNEL_ID` is the default target. Override it per-request with the `target` field.
- Slack uses its own markdown dialect ("mrkdwn") — use `format: "markdown"` to enable rich formatting.

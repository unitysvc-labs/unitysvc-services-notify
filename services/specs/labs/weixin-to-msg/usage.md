# WeChat to Messages — `weixin-to-msg`

Bring the messages a WeChat bot receives into a UnitySVC room. A [Kadxy weixin-ilink-gateway](https://github.com/Kadxy/weixin-ilink-gateway) logs a WeChat account in by QR code and long-polls WeChat (the iLink bot protocol) for the messages people send that account's bot. It emits each one as the raw iLink message object; given to this service, the gateway converts it into the platform `msg` envelope and posts it into your room through the room connector named in the URL. The gateway runs as the `kadxy/weixin-ilink-gateway` container service (one private instance per enrollment) or anywhere you host it.

## The message the gateway emits

The gateway emits the same object two ways: it POSTs it as JSON to every URL in its `WEBHOOK_URLS` setting as soon as it arrives (two attempts, one second apart, then dropped), and it lists it under `GET /messages/updates?after=<seq>` (`Authorization: Bearer <gateway API key>`, answer `{"ok": true, "count": N, "messages": [...]}`) from an in-memory buffer of the last 100 (a platform instance) or 1,000 messages, where `seq` is the cursor: pass the last `seq` you handled and only later messages come back. The object is WeChat's own, unmodified:

```json
{
  "seq": 12,
  "message_id": "7362938192837465123",
  "from_user_id": "o3Fx8w1LqXb9u2Zy@im.wechat",
  "to_user_id": "bot_7f3a1c@im.bot",
  "client_id": "",
  "create_time_ms": 1763280000000,
  "update_time_ms": 1763280000000,
  "session_id": "s_8c2e",
  "message_type": 1,
  "message_state": 2,
  "item_list": [
    {
      "type": 1,
      "msg_id": "7362938192837465123",
      "create_time_ms": 1763280000000,
      "is_completed": true,
      "text_item": { "text": "Hello from WeChat" }
    }
  ],
  "context_token": "ctx_…"
}
```

| Field | Meaning |
| --- | --- |
| `seq` | The gateway's cursor: increases with every message of the account |
| `message_id` | WeChat's id of the message, a string (it is a large integer) |
| `from_user_id` | The sender's iLink user id (`…@im.wechat`); WeChat gives no display name |
| `to_user_id` | The bot's iLink id (`…@im.bot`) |
| `message_type` | `1` a person's message, `2` the bot's own (the gateway's poller already leaves these out) |
| `message_state` | `2` finished |
| `item_list[].type` | `1` text (`text_item.text`), `2` image, `3` voice (`voice_item.text` is a transcript when WeChat made one), `4` file (`file_item.file_name`), `5` video; media items carry an encrypted CDN reference (`media.encrypt_query_param`, `media.aes_key`), not a URL |
| `item_list[].ref_msg` | A quoted message: its `title` is the quoted text |
| `context_token`, `session_id`, `client_id` | WeChat's reply-routing state, needed only to send back through the gateway |

## What the room receives

| `msg` field          | Source in the gateway message                                                                 |
| -------------------- | --------------------------------------------------------------------------------------------- |
| `body`               | the `item_list` items in order, one line each: a text item as written; `[image]`, `[video]`; a voice item's transcript, else `[voice]`; `[file: <file_name>]`; a quoted message as a `> <title>` line before its item |
| `format`             | always `text` (WeChat text is plain)                                                           |
| `type`               | `info`                                                                                        |
| `origin.service`     | `weixin`                                                                                      |
| `origin.external_id` | `message_id`, also the idempotency key, so a message read or delivered twice is posted once   |
| `origin.author`      | `from_user_id`, the sender's iLink user id                                                    |

Everything else (`seq`, `to_user_id`, `session_id`, `context_token`, timestamps) is dropped. Images, files, voice and video stay in WeChat's encrypted CDN: the room gets the placeholder, not the file. The message is posted as you (the connector's member) and shown in the room under the connector's name; the WeChat sender is stored as `origin_author`, readable through the API and SDK. A message whose first line starts with `!` is taken as a private room command, not posted as chat.

## Setup

1. **Pick the connector the messages come in through.** In UnitySVC open the room → **Configure** → **Notifications**. Under **Your notifications**, use a connector card (or **Add connector**). Set **Inbound** to **Through a converter service…** and type `labs/weixin-to-msg`. The card then shows its **Inbound URL**: `https://api.svcpass.com/webhook/<KEY>/labs/weixin-to-msg/<connector id>`.
2. **Have a gateway with a WeChat account logged in.** Enroll in `kadxy/weixin-ilink-gateway` (one instance per enrollment), note the instance's address and its generated API key from the enrollment's instance details, open `<address>/console` and scan the QR code with the WeChat account the bot should use. Or run the gateway yourself with `docker compose up` and your own `API_KEY`.
3. **Connect the gateway to the connector.**
   - **A platform instance** cannot push, so run the **Python reader** example: with `WEIXIN_GATEWAY_URL` and `WEIXIN_GATEWAY_API_KEY` set to the instance's address and key, `UNITYSVC_API_KEY` to your key and `WEIXIN_ROOM_CONNECTOR` to the connector id, `python reader.py --follow` polls `/messages/updates` every five seconds and forwards each message to the service, keeping the last `seq` in `.weixin-to-msg.cursor`. Run it where it can stay up (a cron entry running one pass a minute works too).
   - **A gateway you host** pushes on its own: set its `WEBHOOK_URLS` to the connector's Inbound URL and restart it. No reader needed.
4. **Talk.** Message the bot from WeChat. The message appears in the room under the connector's name.

Several WeChat accounts into several rooms: one gateway (or instance) and one connector each. Nothing else to configure: no secrets and no enrollment in this service.

## What is refused or dropped

- **The bot's own messages** (`message_type` 2) are answered `204` (header `X-UnitySVC-Rule: own-echo`) and nothing is posted, free of charge. The gateway's poller already leaves them out of its buffer and webhooks, so this only matters for a reader of your own that takes WeChat's `getupdates` stream whole; it keeps what the room sends back to WeChat from coming back.
- **A message with nothing to show** (no items, or over 32,000 characters of text) is answered `422` and nothing is posted.
- **Media** arrives as its placeholder; to fetch a file, use the gateway's `POST /media/download` with the item's CDN reference.

## How the URL works

A gateway's `WEBHOOK_URLS` push sets no headers, so the key rides in the URL: the platform's ingress turns `/webhook/<KEY>/labs/weixin-to-msg/<connector id>` into an ordinary keyed request to `/labs/weixin-to-msg/<connector id>`. A client that can set headers, such as the reader, calls that path directly with `Authorization: Bearer <key>` and the message as a JSON body; with no connector id the message lands in your own `me` room. Treat the Inbound URL as a secret: it carries a key that may post into the room.

## Sending back to WeChat

This service is one direction. The gateway's `POST /messages/send` (`{"to": "<from_user_id>", "items": [{"type": "text", "text": "…"}]}`, Bearer the gateway key) answers a person who has messaged the bot; the gateway caches the `context_token` it needs from their last message. A connector's outbound side (`Notify`) has no WeChat service yet.

## Troubleshooting

- **Nothing arrives in the room** — for a platform instance, is the reader running, and does it print `posted`? For a hosted gateway, is `WEBHOOK_URLS` the connector's Inbound URL, copied whole, and was the gateway restarted after setting it? Check `GET /status` on the gateway: `logged_in` must be `true` and `polling` `true`.
- **The reader prints HTTP 401 from the gateway** — `Not logged in`: open `/console` and scan the QR code again (a replaced or restarted platform instance loses its login); otherwise `WEIXIN_GATEWAY_API_KEY` is not the gateway's key.
- **401 from the service** — the URL is not a connector's Inbound URL, or its key was replaced: copy the current URL from Configure → Notifications. From the reader, `UNITYSVC_API_KEY` is not a key of the connector's account.
- **403 from the service** — the connector belongs to another account than the key's: copy the URL from the room's own Configure → Notifications page.
- **422 from the service** — the message had no items or more than 32,000 characters of text. Nothing is posted.
- **Old messages again after the reader moved** — the cursor is a file in the reader's working directory; carry `.weixin-to-msg.cursor` along or set `WEIXIN_CURSOR_FILE`. The room drops repeats of one message id, so a replay posts nothing twice.
- **Messages missing after the instance was replaced** — a platform instance keeps its buffer in memory: messages that arrived while no reader was running and the instance was replaced are gone. Keep the reader running, and log in again after a replacement.

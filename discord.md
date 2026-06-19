# Discord Notification Services — Design

This document describes the two Discord notification services so the design can be
reviewed and validated. Both are **multi-channel** services (one free channel + one
paid `plus` channel) authored via the `templates/` + per-channel param-file model.
Discord is the first channel; every other channel is added by writing two more param
files (see `specs/labs/`).

| Service | Template | Input you send | Free channel | Paid channel | Delivers to |
|---|---|---|---|---|---|
| `discord-relay` | `notify-relay` | a **native Discord webhook** body | `byok` | `plus` | `discord.com` (your webhook) |
| `msg-to-discord` | `msg-to-channel` | the **unified message envelope** | `apprise` | `apprise-plus` | `apprise.unitysvc.dev` → your webhook |

Pick `discord-relay` if you already speak Discord's webhook format; pick
`msg-to-discord` if you want one envelope that works the same across every channel.

---

## Credentials (both services)

Discord delivery uses an **Incoming Webhook** you create in your own server — no bot,
no OAuth. A webhook URL looks like:

```
https://discord.com/api/webhooks/<WEBHOOK_ID>/<WEBHOOK_TOKEN>
```

You store only the two **minimal copyable pieces** as UnitySVC customer secrets — never
the whole URL:

| Secret name | Value | Where to find it |
|---|---|---|
| `DISCORD_WEBHOOK_ID` | the numeric id segment | Discord → Server Settings → Integrations → Webhooks → *New Webhook* → Copy Webhook URL; the id is the second-to-last path segment |
| `DISCORD_WEBHOOK_TOKEN` | the token segment | the last path segment of the same URL |

The service composes the full upstream URL (relay) or the Apprise `discord://` URL
(`msg-to-discord`) from these at request time. You authenticate to the **gateway** with
your UnitySVC API key (`Authorization: Bearer $UNITYSVC_API_KEY`); the gateway swaps in
your Discord credentials before forwarding.

---

## `discord-relay` — native Discord passthrough

You send exactly what Discord's webhook API expects; the gateway forwards it unchanged
after composing your webhook URL from `DISCORD_WEBHOOK_ID` + `DISCORD_WEBHOOK_TOKEN`.

**Message format** — any native Discord webhook body, e.g.:

```json
{ "content": "Deployment complete ✅" }
```

or a richer embed:

```json
{ "embeds": [ { "title": "Deploy complete", "description": "v2 is live", "color": 3066993 } ] }
```

**Call it** (free `byok` channel, canonical path):

```bash
curl -X POST "$API_GATEWAY_BASE_URL/labs/discord-relay" \
  -H "Authorization: Bearer $UNITYSVC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"content":"Deployment complete ✅"}'
```

Upstream config (rendered from `specs/labs/discord-relay.json`):

```
byok.base_url = ${ customer_secrets.DISCORD_WEBHOOK_BASE ?? https://discord.com/api/webhooks }
                /${ customer_secrets.DISCORD_WEBHOOK_ID }/${ customer_secrets.DISCORD_WEBHOOK_TOKEN }
```

`DISCORD_WEBHOOK_BASE` is an **optional customer secret** that defaults to the real Discord
host. Production customers leave it unset (or point it at their own Discord-compatible
proxy); the ops/test customer sets it to `https://mock.unitysvc.dev/discord/api/webhooks`
so only their requests hit the mock (see *Validation* below). It is a *customer* secret —
not a seller one — precisely so testing and production can differ per customer rather than
globally.

---

## `msg-to-discord` — unified envelope via Apprise

You send the channel-agnostic **message envelope**; the gateway composes an Apprise
`discord://<id>/<token>` URL from your secrets and forwards an apprise-api request to
`apprise.unitysvc.dev`, which delivers to Discord.

**Message format** — the envelope (same shape for every `msg-to-*` channel):

```json
{
  "title":  "Deploy complete",
  "body":   "v2 is live",
  "type":   "info",     // info | success | warning | failure   (default: info)
  "format": "text"      // text | markdown | html               (default: text)
}
```

**Call it** (free `apprise` channel, canonical path):

```bash
curl -X POST "$API_GATEWAY_BASE_URL/labs/msg-to-discord" \
  -H "Authorization: Bearer $UNITYSVC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title":"Deploy complete","body":"v2 is live","type":"success","format":"text"}'
```

What the gateway POSTs to `apprise.unitysvc.dev/notify` (composed by the channel's
body-transformer):

```json
{ "urls": "discord://<DISCORD_WEBHOOK_ID>/<DISCORD_WEBHOOK_TOKEN>",
  "title": "Deploy complete", "body": "v2 is live", "type": "success", "format": "text" }
```

---

## The `plus` channel (paid, per-enrollment destinations)

The free channel uses one fixed pair of secrets (`DISCORD_WEBHOOK_ID` /
`DISCORD_WEBHOOK_TOKEN`) — one Discord destination. The **`plus`** channel (`plus` for
relay, `apprise-plus` for `msg-to-discord`) lets one customer bind **many** destinations,
each as a separate enrollment, by naming its secrets per enrollment:

- At enrollment you provide two parameters: `webhook_id_secret` and `webhook_token_secret`
  — the **names** of the customer secrets holding that destination's id and token.
- You get a unique enrollment code and call the platform's per-enrollment path
  `$API_GATEWAY_BASE_URL/e/<code>` for that destination — no extra access interface is
  declared on the service; `/e/<code>` is provided by the platform.
- Pricing: free channel **$0**, `plus` channel **$0.001 / message** (`list_price.type:"channel"`).

Example: store `STAGING_WEBHOOK_ID` / `STAGING_WEBHOOK_TOKEN` and `PROD_WEBHOOK_ID` /
`PROD_WEBHOOK_TOKEN`, enroll twice, and each enrollment routes to its own Discord channel.

---

## Validate against `mock.unitysvc.dev`

Both upstreams are reachable and used for credential-free validation — no real Discord
needed. The repo ships two runnable probes under `validation/` that mirror exactly what
the gateway does:

```bash
bash validation/discord-relay.sh      # native body  -> mock Discord webhook        -> 200
bash validation/msg-to-discord.sh     # envelope -> apprise body (json://mock) -> apprise.unitysvc.dev -> mock
```

- **`discord-relay.sh`** composes the byok upstream with `DISCORD_WEBHOOK_BASE` pointed at
  the mock (`https://mock.unitysvc.dev/discord/api/webhooks`) and POSTs a native Discord
  payload — proving the relay path end to end.
- **`msg-to-discord.sh`** builds the exact apprise-api body the gateway's body-transformer
  produces (with the `discord://…` URL swapped to `json://mock.unitysvc.dev/…` so delivery
  lands on the mock instead of a real Discord server) and POSTs it to
  `apprise.unitysvc.dev/notify` — proving the envelope → Apprise composition and delivery.

The gateway's body-transformer template was verified against the real `resty.template`
engine the gateway runs, so the composed apprise body matches production.

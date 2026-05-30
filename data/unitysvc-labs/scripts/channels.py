"""
Channel catalog for unitysvc-labs notification services.

Each entry defines one upstream notification channel.  The `update_services.py`
script expands each entry into 2–4 service definitions:

  {channel_id}-relay          free, customer stores webhook URL as a fixed-name secret
  {channel_id}-relay-multi    $0.001/use, customer provides webhook URL at enrollment
  msg-to-{channel_id}         free, SMTP→upstream transformer (has_transformer only)
  msg-to-{channel_id}-multi   $0.001/use, transformer, customer webhook (has_transformer only)

Field reference
---------------
channel_id      str   kebab-case service prefix (e.g. "discord")
display         str   human-readable channel name
tier            int   1=chat-webhooks, 2=mobile-push, 3=incident-ops, 4=email/SMS
body_type       str   upstream body shape; determines Lua transformer template
                      one of: discord | slack | telegram | msteams | matrix |
                               ryver | ntfy | gotify | json
has_transformer bool  True → also generate msg-to-* transformer service pair
webhook_path    str   default webhook_path for connectivity tests / code examples
                      (only meaningful for relay; transformer uses a fixed URI in offering)
chat_id_param   bool  True → telegram-family: requires chat_id enrollment param
tags            list  extra listing tags beyond [channel_id, "notification"]
"""

from __future__ import annotations

# ── Tier 1 – Chat / generic webhooks ──────────────────────────────────────────

TIER1: list[dict] = [
    dict(
        channel_id="discord",
        display="Discord",
        tier=1,
        body_type="discord",
        has_transformer=True,
        webhook_path="/api/webhooks/{id}/{token}",
        chat_id_param=False,
        tags=["chat", "gaming"],
    ),
    dict(
        channel_id="slack",
        display="Slack",
        tier=1,
        body_type="slack",
        has_transformer=True,
        webhook_path="/services/{a}/{b}/{c}",
        chat_id_param=False,
        tags=["chat", "workplace"],
    ),
    dict(
        channel_id="telegram",
        display="Telegram",
        tier=1,
        body_type="telegram",
        has_transformer=True,
        webhook_path="/bot{token}/sendMessage",
        chat_id_param=True,
        tags=["chat", "messaging"],
    ),
    dict(
        channel_id="msteams",
        display="Microsoft Teams",
        tier=1,
        body_type="msteams",
        has_transformer=True,
        # webhookb2 format (connector cards)
        webhook_path="/webhookb2/{rest}",
        chat_id_param=False,
        tags=["chat", "workplace", "microsoft"],
    ),
    dict(
        channel_id="mattermost",
        display="Mattermost",
        tier=1,
        body_type="slack",
        has_transformer=True,
        webhook_path="/hooks/{key}",
        chat_id_param=False,
        tags=["chat", "workplace", "self-hosted"],
    ),
    dict(
        channel_id="matrix",
        display="Matrix",
        tier=1,
        body_type="matrix",
        has_transformer=True,
        # room_id encoded as enrollment param; relay path uses token
        webhook_path="/_matrix/client/v3/rooms/{room}/send/m.room.message/{txn}",
        chat_id_param=False,
        tags=["chat", "open-protocol", "self-hosted"],
    ),
    dict(
        channel_id="rocketchat",
        display="Rocket.Chat",
        tier=1,
        body_type="slack",
        has_transformer=True,
        webhook_path="/hooks/{token}",
        chat_id_param=False,
        tags=["chat", "self-hosted"],
    ),
    dict(
        channel_id="gchat",
        display="Google Chat",
        tier=1,
        body_type="slack",
        has_transformer=True,
        webhook_path="/v1/spaces/{space}/messages",
        chat_id_param=False,
        tags=["chat", "workplace", "google"],
    ),
    dict(
        channel_id="zulip",
        display="Zulip",
        tier=1,
        # form-encoded API (type/to/content); no JSON body transformer
        body_type="json",
        has_transformer=False,
        webhook_path="/api/v1/messages",
        chat_id_param=False,
        tags=["chat", "self-hosted"],
    ),
    dict(
        channel_id="webex",
        display="Webex",
        tier=1,
        body_type="slack",
        has_transformer=True,
        webhook_path="/v1/webhooks/incoming/{token}",
        chat_id_param=False,
        tags=["chat", "workplace", "cisco"],
    ),
    dict(
        channel_id="flock",
        display="Flock",
        tier=1,
        body_type="slack",
        has_transformer=True,
        webhook_path="/hooks/sendMessage/{token}",
        chat_id_param=False,
        tags=["chat", "workplace"],
    ),
    dict(
        channel_id="ryver",
        display="Ryver",
        tier=1,
        body_type="ryver",
        has_transformer=True,
        webhook_path="/application/webhook/{token}",
        chat_id_param=False,
        tags=["chat", "workplace"],
    ),
    dict(
        channel_id="json",
        display="JSON Webhook",
        tier=1,
        body_type="json",
        has_transformer=True,
        webhook_path="",
        chat_id_param=False,
        tags=["webhook", "generic"],
    ),
]

# ── Tier 2 – Mobile / desktop push ────────────────────────────────────────────

TIER2: list[dict] = [
    dict(
        channel_id="ntfy",
        display="ntfy",
        tier=2,
        body_type="ntfy",
        has_transformer=True,
        webhook_path="/{topic}",
        chat_id_param=False,
        tags=["push", "self-hosted"],
    ),
    dict(
        channel_id="gotify",
        display="Gotify",
        tier=2,
        body_type="gotify",
        has_transformer=True,
        webhook_path="/message",
        chat_id_param=False,
        tags=["push", "self-hosted"],
    ),
    dict(
        channel_id="pushover",
        display="Pushover",
        tier=2,
        body_type="json",
        has_transformer=False,
        webhook_path="/1/messages.json",
        chat_id_param=False,
        tags=["push", "mobile"],
    ),
    dict(
        channel_id="pushbullet",
        display="Pushbullet",
        tier=2,
        body_type="json",
        has_transformer=False,
        webhook_path="/v2/pushes",
        chat_id_param=False,
        tags=["push", "mobile"],
    ),
    dict(
        channel_id="bark",
        display="Bark",
        tier=2,
        body_type="json",
        has_transformer=False,
        webhook_path="/push",
        chat_id_param=False,
        tags=["push", "ios"],
    ),
    dict(
        channel_id="join",
        display="Join",
        tier=2,
        body_type="json",
        has_transformer=False,
        webhook_path="/_ah/api/messaging/v1/sendPush",
        chat_id_param=False,
        tags=["push", "android"],
    ),
    dict(
        channel_id="prowl",
        display="Prowl",
        tier=2,
        body_type="json",
        has_transformer=False,
        webhook_path="/publicapi/add",
        chat_id_param=False,
        tags=["push", "ios"],
    ),
    dict(
        channel_id="pushjet",
        display="Pushjet",
        tier=2,
        body_type="json",
        has_transformer=False,
        webhook_path="/message",
        chat_id_param=False,
        tags=["push", "self-hosted"],
    ),
    dict(
        channel_id="simplepush",
        display="SimplePush",
        tier=2,
        body_type="json",
        has_transformer=False,
        webhook_path="/send",
        chat_id_param=False,
        tags=["push"],
    ),
    dict(
        channel_id="notica",
        display="Notica",
        tier=2,
        body_type="json",
        has_transformer=False,
        webhook_path="/{token}",
        chat_id_param=False,
        tags=["push"],
    ),
    dict(
        channel_id="notifico",
        display="Notifico",
        tier=2,
        body_type="slack",
        has_transformer=False,
        webhook_path="/h/{project}/{hook}",
        chat_id_param=False,
        tags=["push", "irc", "chat"],
    ),
    dict(
        channel_id="serverchan",
        display="ServerChan",
        tier=2,
        body_type="json",
        has_transformer=False,
        webhook_path="/{token}.send",
        chat_id_param=False,
        tags=["push", "wechat"],
    ),
    dict(
        channel_id="wxpusher",
        display="WxPusher",
        tier=2,
        body_type="json",
        has_transformer=False,
        webhook_path="/api/send/message",
        chat_id_param=False,
        tags=["push", "wechat"],
    ),
    dict(
        channel_id="fcm",
        display="Firebase Cloud Messaging",
        tier=2,
        body_type="json",
        has_transformer=False,
        webhook_path="/v1/projects/{project}/messages:send",
        chat_id_param=False,
        tags=["push", "firebase", "google", "mobile"],
    ),
    dict(
        channel_id="onesignal",
        display="OneSignal",
        tier=2,
        body_type="json",
        has_transformer=False,
        webhook_path="/api/v1/notifications",
        chat_id_param=False,
        tags=["push", "mobile"],
    ),
]

# ── Tier 3 – Incident / ops alerting ──────────────────────────────────────────

TIER3: list[dict] = [
    dict(
        channel_id="pagerduty",
        display="PagerDuty",
        tier=3,
        body_type="json",
        has_transformer=False,
        webhook_path="/v2/enqueue",
        chat_id_param=False,
        tags=["incident", "ops", "alerting"],
    ),
    dict(
        channel_id="opsgenie",
        display="Opsgenie",
        tier=3,
        body_type="json",
        has_transformer=False,
        webhook_path="/v2/alerts",
        chat_id_param=False,
        tags=["incident", "ops", "alerting"],
    ),
    dict(
        channel_id="pagertree",
        display="PagerTree",
        tier=3,
        body_type="json",
        has_transformer=False,
        webhook_path="/integration/{token}",
        chat_id_param=False,
        tags=["incident", "ops", "alerting"],
    ),
    dict(
        channel_id="spikesh",
        display="Spike.sh",
        tier=3,
        body_type="json",
        has_transformer=False,
        webhook_path="/v1/notify",
        chat_id_param=False,
        tags=["incident", "ops", "alerting"],
    ),
    dict(
        channel_id="signl4",
        display="SIGNL4",
        tier=3,
        body_type="json",
        has_transformer=False,
        webhook_path="/webhook/{token}",
        chat_id_param=False,
        tags=["incident", "ops", "alerting", "mobile"],
    ),
    dict(
        channel_id="victorops",
        display="VictorOps",
        tier=3,
        body_type="json",
        has_transformer=False,
        webhook_path="/integrations/generic/{api_id}/alert/{routing_key}",
        chat_id_param=False,
        tags=["incident", "ops", "alerting"],
    ),
    dict(
        channel_id="jira",
        display="Jira",
        tier=3,
        body_type="json",
        has_transformer=False,
        webhook_path="/rest/api/2/issue",
        chat_id_param=False,
        tags=["incident", "issue-tracking", "atlassian"],
    ),
]

# ── Tier 4 – Transactional email APIs ─────────────────────────────────────────

TIER4_EMAIL: list[dict] = [
    dict(
        channel_id="mailgun",
        display="Mailgun",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="/v3/{domain}/messages",
        chat_id_param=False,
        tags=["email", "transactional"],
    ),
    dict(
        channel_id="sendgrid",
        display="SendGrid",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="/v3/mail/send",
        chat_id_param=False,
        tags=["email", "transactional"],
    ),
    dict(
        channel_id="ses",
        display="Amazon SES",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="/v2/email/outbound-emails",
        chat_id_param=False,
        tags=["email", "transactional", "aws"],
    ),
    dict(
        channel_id="brevo",
        display="Brevo",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="/v3/smtp/email",
        chat_id_param=False,
        tags=["email", "transactional"],
    ),
    dict(
        channel_id="postmark",
        display="Postmark",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="/email",
        chat_id_param=False,
        tags=["email", "transactional"],
    ),
    dict(
        channel_id="resend",
        display="Resend",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="/emails",
        chat_id_param=False,
        tags=["email", "transactional"],
    ),
    dict(
        channel_id="sparkpost",
        display="SparkPost",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="/api/v1/transmissions",
        chat_id_param=False,
        tags=["email", "transactional"],
    ),
    dict(
        channel_id="smtp2go",
        display="SMTP2GO",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="/v3/email/send",
        chat_id_param=False,
        tags=["email", "transactional"],
    ),
    dict(
        channel_id="o365",
        display="Office 365",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="/v1.0/users/{user}/sendMail",
        chat_id_param=False,
        tags=["email", "transactional", "microsoft"],
    ),
]

# ── Tier 4 – SMS / messaging APIs ─────────────────────────────────────────────

TIER4_SMS: list[dict] = [
    dict(
        channel_id="twilio",
        display="Twilio",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="/2010-04-01/Accounts/{sid}/Messages.json",
        chat_id_param=False,
        tags=["sms", "messaging"],
    ),
    dict(
        channel_id="sns",
        display="Amazon SNS",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="/",
        chat_id_param=False,
        tags=["messaging", "aws", "push"],
    ),
    dict(
        channel_id="messagebird",
        display="MessageBird",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="/messages",
        chat_id_param=False,
        tags=["sms", "messaging"],
    ),
    dict(
        channel_id="clicksend",
        display="ClickSend",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="/v3/sms/send",
        chat_id_param=False,
        tags=["sms", "messaging"],
    ),
    dict(
        channel_id="bulksms",
        display="BulkSMS",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="/v1/messages",
        chat_id_param=False,
        tags=["sms", "messaging"],
    ),
    dict(
        channel_id="threema",
        display="Threema",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="/send_simple",
        chat_id_param=False,
        tags=["sms", "messaging", "encrypted"],
    ),
    dict(
        channel_id="whatsapp",
        display="WhatsApp",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="/v17.0/{phone_id}/messages",
        chat_id_param=False,
        tags=["messaging", "meta"],
    ),
    dict(
        channel_id="signal",
        display="Signal",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="/v2/send",
        chat_id_param=False,
        tags=["messaging", "encrypted"],
    ),
    dict(
        channel_id="line",
        display="LINE",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="/v2/bot/message/push",
        chat_id_param=False,
        tags=["messaging", "asia"],
    ),
    dict(
        channel_id="viber",
        display="Viber",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="/pa/send_message",
        chat_id_param=False,
        tags=["messaging"],
    ),
    dict(
        channel_id="groupme",
        display="GroupMe",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="/v3/bots/post",
        chat_id_param=False,
        tags=["messaging", "chat"],
    ),
    dict(
        channel_id="kakaotalk",
        display="KakaoTalk",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="",
        chat_id_param=False,
        tags=["messaging", "asia"],
    ),
    dict(
        channel_id="wechat",
        display="WeChat Work",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="",
        chat_id_param=False,
        tags=["messaging", "workplace", "china"],
    ),
    dict(
        channel_id="feishu",
        display="Feishu / Lark",
        tier=4,
        body_type="json",
        has_transformer=False,
        webhook_path="",
        chat_id_param=False,
        tags=["chat", "workplace", "china"],
    ),
]

# ── Combined catalog ───────────────────────────────────────────────────────────

ALL_CHANNELS: list[dict] = TIER1 + TIER2 + TIER3 + TIER4_EMAIL + TIER4_SMS

# Channels that get transformer service pair (msg-to-*)
TRANSFORMER_CHANNELS = [ch for ch in ALL_CHANNELS if ch["has_transformer"]]

# Body-type → Lua template string
# _body is the decoded canonical envelope: {title, body, from}
# Uses resty.template syntax: {* expr *} for raw output, {{ expr }} for escaped.
# _escape_json() produces a JSON-safe double-quoted string (including the quotes).
BODY_TYPE_TEMPLATES: dict[str, str] = {
    "discord": (
        '{"embeds":[{"title":{* _escape_json(_body.title) *},'
        '"description":{* _escape_json(_body.body) *},'
        '"footer":{"text":{* _escape_json("from ".._body.from) *}}}]}'
    ),
    "slack": (
        '{"text":{* _escape_json(_body.title..": ".._body.body) *},'
        '"username":{* _escape_json(_body.from) *}}'
    ),
    "telegram": (
        # chat_id is injected from enrollment_vars at service definition time
        '{"chat_id":{* _escape_json(enrollment_vars.chat_id) *},'
        '"text":{* _escape_json(_body.title.."\n\n".._body.body) *}}'
    ),
    "msteams": (
        '{"@type":"MessageCard","@context":"http://schema.org/extensions",'
        '"themeColor":"0076D7",'
        '"summary":{* _escape_json(_body.title) *},'
        '"sections":[{"activityTitle":{* _escape_json(_body.title) *},'
        '"activitySubtitle":{* _escape_json(_body.from) *},'
        '"activityText":{* _escape_json(_body.body) *}}]}'
    ),
    "matrix": (
        '{"msgtype":"m.text",'
        '"body":{* _escape_json(_body.title.."\n\n".._body.body) *}}'
    ),
    "ryver": (
        '{"body":{* _escape_json(_body.body) *}}'
    ),
    "ntfy": (
        '{"message":{* _escape_json(_body.body) *},'
        '"title":{* _escape_json(_body.title) *}}'
    ),
    "gotify": (
        '{"message":{* _escape_json(_body.body) *},'
        '"title":{* _escape_json(_body.title) *},'
        '"priority":5}'
    ),
    "json": (
        '{"message":{* _escape_json(_body.body) *},'
        '"title":{* _escape_json(_body.title) *},'
        '"from":{* _escape_json(_body.from) *}}'
    ),
}

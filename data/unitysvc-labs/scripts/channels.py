"""
Channel catalog for unitysvc-labs notification services.

Each entry defines one upstream notification channel.  The `update_services.py`
script expands each entry into 2-4 service definitions:

  {channel_id}-relay          free, customer stores webhook URL as a fixed-name secret
  {channel_id}-relay-multi    $0.001/use, customer provides webhook URL via params+secrets
  msg-to-{channel_id}         free, SMTP->upstream transformer (has_transformer only)
  msg-to-{channel_id}-multi   $0.001/use, transformer, customer provides creds at enrollment

Field reference
---------------
channel_id        str        kebab-case service prefix (e.g. "discord")
display           str        human-readable channel name
tier              int        1=chat-webhooks, 2=mobile-push, 3=incident-ops, 4=email/SMS
body_type         str        upstream body shape; determines Lua transformer template
                             one of: discord | slack | telegram | msteams | matrix |
                                      ryver | ntfy | gotify | bark | json |
                                      pushover (fixed) | pushover_multi |
                                      resend_email | postmark_email | sendgrid_email |
                                      brevo_email | smtp2go_email |
                                      messagebird_sms | whatsapp_msg | line_msg |
                                      groupme_msg | wechat_work | feishu_msg
has_transformer   bool       True -> also generate msg-to-* transformer service pair
fixed_base_url    str|None   When set, the transformer uses this hardcoded base URL
                             instead of a customer-secret-backed URL.  Use for APIs
                             where the endpoint is fixed and only the body credentials
                             vary per customer (e.g. Pushover, Bark).
webhook_path      str        default path for connectivity tests / fixed-variant URI
auth_header       dict|None  Authorization header injected into proxy_rewrite headers.
                             dict has keys: name (header name), prefix (value prefix).
                             None if auth is embedded in the body or URL.
                             Examples:
                               dict(name="Authorization", prefix="Bearer ")
                               dict(name="X-Postmark-Server-Token", prefix="")
                               dict(name="api-key", prefix="")
credential_params list[dict] Extra body-level credential params for transformer services.
                             Each dict: {param, default_secret, title, description,
                             ui_description}.  Empty for webhook-style channels.
                             For multi: resolved via ${ customer_secrets.{{ params.X }} }
                             For fixed: resolved via ${ service_secrets.DEFAULT_SECRET }
tags              list       extra listing tags beyond [channel_id, "notification"]
"""

from __future__ import annotations

# -- Tier 1 -- Chat / generic webhooks -----------------------------------------

TIER1: list[dict] = [
    dict(
        channel_id="discord",
        display="Discord",
        tier=1,
        body_type="discord",
        has_transformer=True,
        fixed_base_url=None,
        webhook_path="/api/webhooks/{id}/{token}",
        auth_header=None,
        credential_params=[],
        tags=["chat", "gaming"],
    ),
    dict(
        channel_id="slack",
        display="Slack",
        tier=1,
        body_type="slack",
        has_transformer=True,
        fixed_base_url=None,
        webhook_path="/services/{a}/{b}/{c}",
        auth_header=None,
        credential_params=[],
        tags=["chat", "workplace"],
    ),
    dict(
        channel_id="telegram",
        display="Telegram",
        tier=1,
        body_type="telegram",
        has_transformer=True,
        fixed_base_url=None,
        webhook_path="/bot{token}/sendMessage",
        auth_header=None,
        credential_params=[
            dict(
                param="chat_id_secret",
                default_secret="TELEGRAM_CHAT_ID",
                title="Chat ID Secret Name",
                description="Name of the customer secret containing the Telegram chat or channel ID",
                ui_description="Enter the name of the customer secret that holds your Telegram chat or channel ID",
            ),
        ],
        tags=["chat", "messaging"],
    ),
    dict(
        channel_id="msteams",
        display="Microsoft Teams",
        tier=1,
        body_type="msteams",
        has_transformer=True,
        fixed_base_url=None,
        # webhookb2 format (connector cards)
        webhook_path="/webhookb2/{rest}",
        auth_header=None,
        credential_params=[],
        tags=["chat", "workplace", "microsoft"],
    ),
    dict(
        channel_id="mattermost",
        display="Mattermost",
        tier=1,
        body_type="slack",
        has_transformer=True,
        fixed_base_url=None,
        webhook_path="/hooks/{key}",
        auth_header=None,
        credential_params=[],
        tags=["chat", "workplace", "self-hosted"],
    ),
    dict(
        channel_id="matrix",
        display="Matrix",
        tier=1,
        body_type="matrix",
        has_transformer=True,
        fixed_base_url=None,
        webhook_path="/_matrix/client/v3/rooms/{room}/send/m.room.message/{txn}",
        auth_header=None,
        credential_params=[],
        tags=["chat", "open-protocol", "self-hosted"],
    ),
    dict(
        channel_id="rocketchat",
        display="Rocket.Chat",
        tier=1,
        body_type="slack",
        has_transformer=True,
        fixed_base_url=None,
        webhook_path="/hooks/{token}",
        auth_header=None,
        credential_params=[],
        tags=["chat", "self-hosted"],
    ),
    dict(
        channel_id="gchat",
        display="Google Chat",
        tier=1,
        body_type="slack",
        has_transformer=True,
        fixed_base_url=None,
        webhook_path="/v1/spaces/{space}/messages",
        auth_header=None,
        credential_params=[],
        tags=["chat", "workplace", "google"],
    ),
    dict(
        channel_id="zulip",
        display="Zulip",
        tier=1,
        # form-encoded API (type/to/content); no JSON body transformer
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/api/v1/messages",
        auth_header=None,
        credential_params=[],
        tags=["chat", "self-hosted"],
    ),
    dict(
        channel_id="webex",
        display="Webex",
        tier=1,
        body_type="slack",
        has_transformer=True,
        fixed_base_url=None,
        webhook_path="/v1/webhooks/incoming/{token}",
        auth_header=None,
        credential_params=[],
        tags=["chat", "workplace", "cisco"],
    ),
    dict(
        channel_id="flock",
        display="Flock",
        tier=1,
        body_type="slack",
        has_transformer=True,
        fixed_base_url=None,
        webhook_path="/hooks/sendMessage/{token}",
        auth_header=None,
        credential_params=[],
        tags=["chat", "workplace"],
    ),
    dict(
        channel_id="ryver",
        display="Ryver",
        tier=1,
        body_type="ryver",
        has_transformer=True,
        fixed_base_url=None,
        webhook_path="/application/webhook/{token}",
        auth_header=None,
        credential_params=[],
        tags=["chat", "workplace"],
    ),
    dict(
        channel_id="json",
        display="JSON Webhook",
        tier=1,
        body_type="json",
        has_transformer=True,
        fixed_base_url=None,
        webhook_path="",
        auth_header=None,
        credential_params=[],
        tags=["webhook", "generic"],
    ),
]

# -- Tier 2 -- Mobile / desktop push -------------------------------------------

TIER2: list[dict] = [
    dict(
        channel_id="ntfy",
        display="ntfy",
        tier=2,
        body_type="ntfy",
        has_transformer=True,
        fixed_base_url=None,
        webhook_path="/{topic}",
        auth_header=None,
        credential_params=[],
        tags=["push", "self-hosted"],
    ),
    dict(
        channel_id="gotify",
        display="Gotify",
        tier=2,
        body_type="gotify",
        has_transformer=True,
        fixed_base_url=None,
        webhook_path="/message",
        auth_header=None,
        credential_params=[],
        tags=["push", "self-hosted"],
    ),
    dict(
        channel_id="pushover",
        display="Pushover",
        tier=2,
        # Fixed variant uses service_secrets; multi uses customer_secrets via params.
        # Separate body_type keys handle the two cases (see BODY_TYPE_TEMPLATES below).
        body_type="pushover",
        has_transformer=True,
        fixed_base_url="https://api.pushover.net",
        webhook_path="/1/messages.json",
        auth_header=None,
        credential_params=[
            dict(
                param="token_secret",
                default_secret="PUSHOVER_TOKEN",
                title="App Token Secret Name",
                description=(
                    "Name of the customer secret containing your Pushover "
                    "application token"
                ),
                ui_description=(
                    "Enter the name of the customer secret that holds your "
                    "Pushover app token"
                ),
            ),
            dict(
                param="user_secret",
                default_secret="PUSHOVER_USER",
                title="User Key Secret Name",
                description=(
                    "Name of the customer secret containing your Pushover user key"
                ),
                ui_description=(
                    "Enter the name of the customer secret that holds your "
                    "Pushover user key"
                ),
            ),
        ],
        tags=["push", "mobile"],
    ),
    dict(
        channel_id="bark",
        display="Bark",
        tier=2,
        body_type="bark",
        has_transformer=True,
        # Base URL is conventionally https://api.day.app but can be self-hosted.
        # Device key goes in the URL path -- customers supply both via secrets.
        fixed_base_url=None,
        webhook_path="/{device_key}",
        auth_header=None,
        credential_params=[],
        tags=["push", "ios"],
    ),
    dict(
        channel_id="pushbullet",
        display="Pushbullet",
        tier=2,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/v2/pushes",
        auth_header=None,
        credential_params=[],
        tags=["push", "mobile"],
    ),
    dict(
        channel_id="join",
        display="Join",
        tier=2,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/_ah/api/messaging/v1/sendPush",
        auth_header=None,
        credential_params=[],
        tags=["push", "android"],
    ),
    dict(
        channel_id="prowl",
        display="Prowl",
        tier=2,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/publicapi/add",
        auth_header=None,
        credential_params=[],
        tags=["push", "ios"],
    ),
    dict(
        channel_id="pushjet",
        display="Pushjet",
        tier=2,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/message",
        auth_header=None,
        credential_params=[],
        tags=["push", "self-hosted"],
    ),
    dict(
        channel_id="simplepush",
        display="SimplePush",
        tier=2,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/send",
        auth_header=None,
        credential_params=[],
        tags=["push"],
    ),
    dict(
        channel_id="notica",
        display="Notica",
        tier=2,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/{token}",
        auth_header=None,
        credential_params=[],
        tags=["push"],
    ),
    dict(
        channel_id="notifico",
        display="Notifico",
        tier=2,
        body_type="slack",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/h/{project}/{hook}",
        auth_header=None,
        credential_params=[],
        tags=["push", "irc", "chat"],
    ),
    dict(
        channel_id="serverchan",
        display="ServerChan",
        tier=2,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/{token}.send",
        auth_header=None,
        credential_params=[],
        tags=["push", "wechat"],
    ),
    dict(
        channel_id="wxpusher",
        display="WxPusher",
        tier=2,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/api/send/message",
        auth_header=None,
        credential_params=[],
        tags=["push", "wechat"],
    ),
    dict(
        channel_id="fcm",
        display="Firebase Cloud Messaging",
        tier=2,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/v1/projects/{project}/messages:send",
        auth_header=None,
        credential_params=[],
        tags=["push", "firebase", "google", "mobile"],
    ),
    dict(
        channel_id="onesignal",
        display="OneSignal",
        tier=2,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/api/v1/notifications",
        auth_header=None,
        credential_params=[],
        tags=["push", "mobile"],
    ),
]

# -- Tier 3 -- Incident / ops alerting -----------------------------------------

TIER3: list[dict] = [
    dict(
        channel_id="pagerduty",
        display="PagerDuty",
        tier=3,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/v2/enqueue",
        auth_header=None,
        credential_params=[],
        tags=["incident", "ops", "alerting"],
    ),
    dict(
        channel_id="opsgenie",
        display="Opsgenie",
        tier=3,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/v2/alerts",
        auth_header=None,
        credential_params=[],
        tags=["incident", "ops", "alerting"],
    ),
    dict(
        channel_id="pagertree",
        display="PagerTree",
        tier=3,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/integration/{token}",
        auth_header=None,
        credential_params=[],
        tags=["incident", "ops", "alerting"],
    ),
    dict(
        channel_id="spikesh",
        display="Spike.sh",
        tier=3,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/v1/notify",
        auth_header=None,
        credential_params=[],
        tags=["incident", "ops", "alerting"],
    ),
    dict(
        channel_id="signl4",
        display="SIGNL4",
        tier=3,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/webhook/{token}",
        auth_header=None,
        credential_params=[],
        tags=["incident", "ops", "alerting", "mobile"],
    ),
    dict(
        channel_id="victorops",
        display="VictorOps",
        tier=3,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/integrations/generic/{api_id}/alert/{routing_key}",
        auth_header=None,
        credential_params=[],
        tags=["incident", "ops", "alerting"],
    ),
    dict(
        channel_id="jira",
        display="Jira",
        tier=3,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/rest/api/2/issue",
        auth_header=None,
        credential_params=[],
        tags=["incident", "issue-tracking", "atlassian"],
    ),
]

# -- Tier 4 -- Transactional email APIs ----------------------------------------

def _email_credential_params(cid: str, display: str) -> list[dict]:
    """Standard credential params for email transformer channels."""
    return [
        dict(
            param="api_key_secret",
            default_secret=f"{cid}_API_KEY",
            title="API Key Secret Name",
            description=f"Name of the customer secret containing your {display} API key",
            ui_description=f"Enter the name of the customer secret holding your {display} API key",
        ),
        dict(
            param="from_email_secret",
            default_secret=f"{cid}_FROM_EMAIL",
            title="From Address Secret Name",
            description="Name of the customer secret containing the sender email address",
            ui_description="Enter the name of the customer secret holding the sender email address",
        ),
        dict(
            param="to_email_secret",
            default_secret=f"{cid}_TO_EMAIL",
            title="To Address Secret Name",
            description="Name of the customer secret containing the recipient email address",
            ui_description="Enter the name of the customer secret holding the recipient email address",
        ),
    ]


TIER4_EMAIL: list[dict] = [
    dict(
        channel_id="mailgun",
        display="Mailgun",
        tier=4,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/v3/{domain}/messages",
        auth_header=None,
        credential_params=[],
        tags=["email", "transactional"],
    ),
    dict(
        channel_id="sendgrid",
        display="SendGrid",
        tier=4,
        body_type="sendgrid_email",
        has_transformer=True,
        fixed_base_url="https://api.sendgrid.com",
        webhook_path="/v3/mail/send",
        auth_header=dict(name="Authorization", prefix="Bearer "),
        credential_params=_email_credential_params("SENDGRID", "SendGrid"),
        tags=["email", "transactional"],
    ),
    dict(
        channel_id="ses",
        display="Amazon SES",
        tier=4,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/v2/email/outbound-emails",
        auth_header=None,
        credential_params=[],
        tags=["email", "transactional", "aws"],
    ),
    dict(
        channel_id="brevo",
        display="Brevo",
        tier=4,
        body_type="brevo_email",
        has_transformer=True,
        fixed_base_url="https://api.brevo.com",
        webhook_path="/v3/smtp/email",
        auth_header=dict(name="api-key", prefix=""),
        credential_params=_email_credential_params("BREVO", "Brevo"),
        tags=["email", "transactional"],
    ),
    dict(
        channel_id="postmark",
        display="Postmark",
        tier=4,
        body_type="postmark_email",
        has_transformer=True,
        fixed_base_url="https://api.postmarkapp.com",
        webhook_path="/email",
        auth_header=dict(name="X-Postmark-Server-Token", prefix=""),
        credential_params=_email_credential_params("POSTMARK", "Postmark"),
        tags=["email", "transactional"],
    ),
    dict(
        channel_id="resend",
        display="Resend",
        tier=4,
        body_type="resend_email",
        has_transformer=True,
        fixed_base_url="https://api.resend.com",
        webhook_path="/emails",
        auth_header=dict(name="Authorization", prefix="Bearer "),
        credential_params=_email_credential_params("RESEND", "Resend"),
        tags=["email", "transactional"],
    ),
    dict(
        channel_id="sparkpost",
        display="SparkPost",
        tier=4,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/api/v1/transmissions",
        auth_header=None,
        credential_params=[],
        tags=["email", "transactional"],
    ),
    dict(
        channel_id="smtp2go",
        display="SMTP2GO",
        tier=4,
        body_type="smtp2go_email",
        has_transformer=True,
        fixed_base_url="https://api.smtp2go.com",
        webhook_path="/v3/email/send",
        auth_header=None,  # API key is in the request body
        credential_params=_email_credential_params("SMTP2GO", "SMTP2GO"),
        tags=["email", "transactional"],
    ),
    dict(
        channel_id="o365",
        display="Office 365",
        tier=4,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/v1.0/users/{user}/sendMail",
        auth_header=None,
        credential_params=[],
        tags=["email", "transactional", "microsoft"],
    ),
]

# -- Tier 4 -- SMS / messaging APIs --------------------------------------------

TIER4_SMS: list[dict] = [
    dict(
        channel_id="twilio",
        display="Twilio",
        tier=4,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/2010-04-01/Accounts/{sid}/Messages.json",
        auth_header=None,
        credential_params=[],
        tags=["sms", "messaging"],
    ),
    dict(
        channel_id="sns",
        display="Amazon SNS",
        tier=4,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/",
        auth_header=None,
        credential_params=[],
        tags=["messaging", "aws", "push"],
    ),
    dict(
        channel_id="messagebird",
        display="MessageBird",
        tier=4,
        body_type="messagebird_sms",
        has_transformer=True,
        fixed_base_url="https://rest.messagebird.com",
        webhook_path="/v2/send",
        auth_header=dict(name="Authorization", prefix="AccessKey "),
        credential_params=[
            dict(
                param="api_key_secret",
                default_secret="MESSAGEBIRD_API_KEY",
                title="API Key Secret Name",
                description="Name of the customer secret containing your MessageBird API key",
                ui_description="Enter the name of the customer secret holding your MessageBird API key",
            ),
            dict(
                param="from_id_secret",
                default_secret="MESSAGEBIRD_ORIGINATOR",
                title="Originator Secret Name",
                description="Name of the customer secret containing the sender ID or phone number",
                ui_description="Enter the name of the customer secret holding the sender ID or phone number",
            ),
            dict(
                param="to_phone_secret",
                default_secret="MESSAGEBIRD_TO_PHONE",
                title="Recipient Phone Secret Name",
                description="Name of the customer secret containing the recipient phone number",
                ui_description="Enter the name of the customer secret holding the recipient phone number",
            ),
        ],
        tags=["sms", "messaging"],
    ),
    dict(
        channel_id="clicksend",
        display="ClickSend",
        tier=4,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/v3/sms/send",
        auth_header=None,
        credential_params=[],
        tags=["sms", "messaging"],
    ),
    dict(
        channel_id="bulksms",
        display="BulkSMS",
        tier=4,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/v1/messages",
        auth_header=None,
        credential_params=[],
        tags=["sms", "messaging"],
    ),
    dict(
        channel_id="threema",
        display="Threema",
        tier=4,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/send_simple",
        auth_header=None,
        credential_params=[],
        tags=["sms", "messaging", "encrypted"],
    ),
    dict(
        channel_id="whatsapp",
        display="WhatsApp",
        tier=4,
        body_type="whatsapp_msg",
        has_transformer=True,
        fixed_base_url=None,
        webhook_path="/v17.0/{phone_number_id}/messages",
        auth_header=dict(name="Authorization", prefix="Bearer "),
        credential_params=[
            dict(
                param="api_key_secret",
                default_secret="WHATSAPP_ACCESS_TOKEN",
                title="Access Token Secret Name",
                description="Name of the customer secret containing your WhatsApp Cloud API access token",
                ui_description="Enter the name of the customer secret holding your WhatsApp Cloud API access token",
            ),
            dict(
                param="to_phone_secret",
                default_secret="WHATSAPP_TO_PHONE",
                title="Recipient Phone Secret Name",
                description="Name of the customer secret containing the recipient phone number",
                ui_description="Enter the name of the customer secret holding the recipient phone number",
            ),
        ],
        tags=["messaging", "meta"],
    ),
    dict(
        channel_id="signal",
        display="Signal",
        tier=4,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/v2/send",
        auth_header=None,
        credential_params=[],
        tags=["messaging", "encrypted"],
    ),
    dict(
        channel_id="line",
        display="LINE",
        tier=4,
        body_type="line_msg",
        has_transformer=True,
        fixed_base_url="https://api.line.me",
        webhook_path="/v2/bot/message/push",
        auth_header=dict(name="Authorization", prefix="Bearer "),
        credential_params=[
            dict(
                param="api_key_secret",
                default_secret="LINE_CHANNEL_ACCESS_TOKEN",
                title="Channel Access Token Secret Name",
                description="Name of the customer secret containing your LINE Channel Access Token",
                ui_description="Enter the name of the customer secret holding your LINE Channel Access Token",
            ),
            dict(
                param="to_id_secret",
                default_secret="LINE_TO_ID",
                title="Recipient ID Secret Name",
                description="Name of the customer secret containing the target user or group ID",
                ui_description="Enter the name of the customer secret holding the target user or group ID",
            ),
        ],
        tags=["messaging", "asia"],
    ),
    dict(
        channel_id="viber",
        display="Viber",
        tier=4,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="/pa/send_message",
        auth_header=None,
        credential_params=[],
        tags=["messaging"],
    ),
    dict(
        channel_id="groupme",
        display="GroupMe",
        tier=4,
        body_type="groupme_msg",
        has_transformer=True,
        fixed_base_url="https://api.groupme.com",
        webhook_path="/v3/bots/post",
        auth_header=None,  # bot_id is in the request body
        credential_params=[
            dict(
                param="bot_id_secret",
                default_secret="GROUPME_BOT_ID",
                title="Bot ID Secret Name",
                description="Name of the customer secret containing the GroupMe bot ID",
                ui_description="Enter the name of the customer secret holding the GroupMe bot ID",
            ),
        ],
        tags=["messaging", "chat"],
    ),
    dict(
        channel_id="kakaotalk",
        display="KakaoTalk",
        tier=4,
        body_type="json",
        has_transformer=False,
        fixed_base_url=None,
        webhook_path="",
        auth_header=None,
        credential_params=[],
        tags=["messaging", "asia"],
    ),
    dict(
        channel_id="wechat",
        display="WeChat Work",
        tier=4,
        body_type="wechat_work",
        has_transformer=True,
        fixed_base_url=None,
        webhook_path="/cgi-bin/webhook/send",
        auth_header=None,  # auth key is in the webhook URL
        credential_params=[],
        tags=["messaging", "workplace", "china"],
    ),
    dict(
        channel_id="feishu",
        display="Feishu / Lark",
        tier=4,
        body_type="feishu_msg",
        has_transformer=True,
        fixed_base_url=None,
        webhook_path="/open-apis/bot/v2/hook/{key}",
        auth_header=None,  # auth key is in the webhook URL
        credential_params=[],
        tags=["chat", "workplace", "china"],
    ),
]

# -- Combined catalog ----------------------------------------------------------

ALL_CHANNELS: list[dict] = TIER1 + TIER2 + TIER3 + TIER4_EMAIL + TIER4_SMS

# Channels that get transformer service pair (msg-to-*)
TRANSFORMER_CHANNELS = [ch for ch in ALL_CHANNELS if ch["has_transformer"]]

# Body-type -> Lua template string
# _body is the decoded canonical envelope: {title, body, from}
# Uses resty.template syntax: {* expr *} for raw output, {{ expr }} for escaped.
# _escape_json() produces a JSON-safe double-quoted string (including the quotes).
#
# For credential-injecting body types:
#   "fixed" variant  -> ${ service_secrets.NAME }   (operator-managed)
#   "multi" variant  -> ${ customer_secrets.{{ params.NAME }} }  (per-enrollment)
# The _multi suffix selects the multi variant when present; fallback to base key.
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
    # telegram fixed (msg-to-telegram): operator-managed service secrets.
    "telegram": (
        '{"chat_id":${ service_secrets.TELEGRAM_CHAT_ID },'
        '"text":{* _escape_json(_body.title.."\\n\\n".._body.body) *}}'
    ),
    # telegram multi (msg-to-telegram-multi): per-enrollment customer secrets.
    "telegram_multi": (
        '{"chat_id":${ customer_secrets.{{ params.chat_id_secret }} },'
        '"text":{* _escape_json(_body.title.."\\n\\n".._body.body) *}}'
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
    # Bark: device key in URL path (webhook_path_secret); body is title+body only.
    "bark": (
        '{"title":{* _escape_json(_body.title) *},'
        '"body":{* _escape_json(_body.body) *}}'
    ),
    # Pushover fixed (msg-to-pushover): operator-managed service secrets.
    "pushover": (
        '{"token":${ service_secrets.PUSHOVER_TOKEN },'
        '"user":${ service_secrets.PUSHOVER_USER },'
        '"message":{* _escape_json(_body.title.."\n\n".._body.body) *},'
        '"title":{* _escape_json(_body.title) *}}'
    ),
    # Pushover multi (msg-to-pushover-multi): per-enrollment customer secrets.
    # {{ params.X }} is expanded by Jinja2 at enrollment time (before gateway
    # processes the offering), then ${ customer_secrets.NAME } is resolved at
    # request time.
    "pushover_multi": (
        '{"token":${ customer_secrets.{{ params.token_secret }} },'
        '"user":${ customer_secrets.{{ params.user_secret }} },'
        '"message":{* _escape_json(_body.title.."\n\n".._body.body) *},'
        '"title":{* _escape_json(_body.title) *}}'
    ),
    "json": (
        '{"message":{* _escape_json(_body.body) *},'
        '"title":{* _escape_json(_body.title) *},'
        '"from":{* _escape_json(_body.from) *}}'
    ),
    # -- Email body types --
    # Fixed variants use service_secrets; multi variants use customer_secrets via params.
    "resend_email": (
        '{"from":${ service_secrets.EMAIL_FROM },'
        '"to":[${ service_secrets.EMAIL_TO }],'
        '"subject":{* _escape_json(_body.title) *},'
        '"text":{* _escape_json(_body.body) *}}'
    ),
    "resend_email_multi": (
        '{"from":${ customer_secrets.{{ params.from_email_secret }} },'
        '"to":[${ customer_secrets.{{ params.to_email_secret }} }],'
        '"subject":{* _escape_json(_body.title) *},'
        '"text":{* _escape_json(_body.body) *}}'
    ),
    "postmark_email": (
        '{"From":${ service_secrets.EMAIL_FROM },'
        '"To":${ service_secrets.EMAIL_TO },'
        '"Subject":{* _escape_json(_body.title) *},'
        '"TextBody":{* _escape_json(_body.body) *}}'
    ),
    "postmark_email_multi": (
        '{"From":${ customer_secrets.{{ params.from_email_secret }} },'
        '"To":${ customer_secrets.{{ params.to_email_secret }} },'
        '"Subject":{* _escape_json(_body.title) *},'
        '"TextBody":{* _escape_json(_body.body) *}}'
    ),
    "sendgrid_email": (
        '{"personalizations":[{"to":[{"email":${ service_secrets.EMAIL_TO }}]}],'
        '"from":{"email":${ service_secrets.EMAIL_FROM }},'
        '"subject":{* _escape_json(_body.title) *},'
        '"content":[{"type":"text/plain","value":{* _escape_json(_body.body) *}}]}'
    ),
    "sendgrid_email_multi": (
        '{"personalizations":[{"to":[{"email":${ customer_secrets.{{ params.to_email_secret }} }}]}],'
        '"from":{"email":${ customer_secrets.{{ params.from_email_secret }} }},'
        '"subject":{* _escape_json(_body.title) *},'
        '"content":[{"type":"text/plain","value":{* _escape_json(_body.body) *}}]}'
    ),
    "brevo_email": (
        '{"sender":{"email":${ service_secrets.EMAIL_FROM }},'
        '"to":[{"email":${ service_secrets.EMAIL_TO }}],'
        '"subject":{* _escape_json(_body.title) *},'
        '"textContent":{* _escape_json(_body.body) *}}'
    ),
    "brevo_email_multi": (
        '{"sender":{"email":${ customer_secrets.{{ params.from_email_secret }} }},'
        '"to":[{"email":${ customer_secrets.{{ params.to_email_secret }} }}],'
        '"subject":{* _escape_json(_body.title) *},'
        '"textContent":{* _escape_json(_body.body) *}}'
    ),
    # smtp2go: api_key in body (auth_header=None)
    "smtp2go_email": (
        '{"api_key":${ service_secrets.API_KEY },'
        '"sender":${ service_secrets.EMAIL_FROM },'
        '"to":[${ service_secrets.EMAIL_TO }],'
        '"subject":{* _escape_json(_body.title) *},'
        '"text_body":{* _escape_json(_body.body) *}}'
    ),
    "smtp2go_email_multi": (
        '{"api_key":${ customer_secrets.{{ params.api_key_secret }} },'
        '"sender":${ customer_secrets.{{ params.from_email_secret }} },'
        '"to":[${ customer_secrets.{{ params.to_email_secret }} }],'
        '"subject":{* _escape_json(_body.title) *},'
        '"text_body":{* _escape_json(_body.body) *}}'
    ),
    # -- SMS / messaging body types --
    "messagebird_sms": (
        '{"originator":${ service_secrets.FROM_ID },'
        '"recipients":[${ service_secrets.TO_PHONE }],'
        '"body":{* _escape_json(_body.body) *}}'
    ),
    "messagebird_sms_multi": (
        '{"originator":${ customer_secrets.{{ params.from_id_secret }} },'
        '"recipients":[${ customer_secrets.{{ params.to_phone_secret }} }],'
        '"body":{* _escape_json(_body.body) *}}'
    ),
    "whatsapp_msg": (
        '{"messaging_product":"whatsapp","recipient_type":"individual",'
        '"to":${ service_secrets.TO_PHONE },'
        '"type":"text","text":{"preview_url":false,"body":{* _escape_json(_body.body) *}}}'
    ),
    "whatsapp_msg_multi": (
        '{"messaging_product":"whatsapp","recipient_type":"individual",'
        '"to":${ customer_secrets.{{ params.to_phone_secret }} },'
        '"type":"text","text":{"preview_url":false,"body":{* _escape_json(_body.body) *}}}'
    ),
    "line_msg": (
        '{"to":${ service_secrets.TO_ID },'
        '"messages":[{"type":"text","text":{* _escape_json(_body.title.."\\n\\n".._body.body) *}}]}'
    ),
    "line_msg_multi": (
        '{"to":${ customer_secrets.{{ params.to_id_secret }} },'
        '"messages":[{"type":"text","text":{* _escape_json(_body.title.."\\n\\n".._body.body) *}}]}'
    ),
    "groupme_msg": (
        '{"bot_id":${ service_secrets.BOT_ID },'
        '"text":{* _escape_json(_body.title..": ".._body.body) *}}'
    ),
    "groupme_msg_multi": (
        '{"bot_id":${ customer_secrets.{{ params.bot_id_secret }} },'
        '"text":{* _escape_json(_body.title..": ".._body.body) *}}'
    ),
    # Webhook-style (auth in URL, no body credentials) -- same template for fixed and multi
    "wechat_work": (
        '{"msgtype":"text","text":{"content":{* _escape_json(_body.title.."\\n\\n".._body.body) *}}}'
    ),
    "feishu_msg": (
        '{"msg_type":"text","content":{"text":{* _escape_json(_body.title.."\\n\\n".._body.body) *}}}'
    ),
}

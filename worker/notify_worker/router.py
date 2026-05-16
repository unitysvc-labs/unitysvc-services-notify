from notify_worker.channels.base import ChannelHandler
from notify_worker.channels.discord import DiscordHandler
from notify_worker.channels.slack import SlackHandler
from notify_worker.channels.apprise_handler import (
    TelegramHandler, GotifyHandler, GchatHandler, TeamsHandler,
    PushoverHandler, MattermostHandler, RocketchatHandler, LineHandler,
    TwilioHandler, VonageHandler, OpsgenieHandler, PagerdutyHandler,
    OnesignalHandler, WebexHandler, ViberHandler, MatrixHandler, FeishuHandler,
    KakaotalkHandler, WechatHandler, WhatsappHandler, ZaloHandler, FcmHandler,
    IrcHandler, SignalHandler, TwitchHandler, NostrHandler,
)

_REGISTRY: dict[str, ChannelHandler] = {
    "discord":    DiscordHandler(),
    "slack":      SlackHandler(),
    "telegram":   TelegramHandler(),
    "gotify":     GotifyHandler(),
    "gchat":      GchatHandler(),
    "teams":      TeamsHandler(),
    "pushover":   PushoverHandler(),
    "mattermost": MattermostHandler(),
    "rocketchat": RocketchatHandler(),
    "line":       LineHandler(),
    "twilio":     TwilioHandler(),
    "vonage":     VonageHandler(),
    "opsgenie":   OpsgenieHandler(),
    "pagerduty":  PagerdutyHandler(),
    "onesignal":  OnesignalHandler(),
    "webex":      WebexHandler(),
    "viber":      ViberHandler(),
    "matrix":     MatrixHandler(),
    "feishu":     FeishuHandler(),
    "kakaotalk":  KakaotalkHandler(),
    "wechat":     WechatHandler(),
    "whatsapp":   WhatsappHandler(),
    "zalo":       ZaloHandler(),
    "fcm":        FcmHandler(),
    "irc":        IrcHandler(),
    "signal":     SignalHandler(),
    "twitch":     TwitchHandler(),
    "nostr":      NostrHandler(),
}


def get_handler(channel: str) -> ChannelHandler:
    handler = _REGISTRY.get(channel.lower())
    if not handler:
        raise ValueError(f"Unknown channel: {channel!r}. Supported: {sorted(_REGISTRY)}")
    return handler

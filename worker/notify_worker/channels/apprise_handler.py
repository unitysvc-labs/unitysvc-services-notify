"""
Generic Apprise-backed handler for channels that accept a single URL/token.
Each channel subclass only needs to implement `build_apprise_url`.
"""
import apprise
from notify_worker.channels.base import ChannelHandler
from notify_worker.models import SendRequest


class AppriseHandler(ChannelHandler):
    def build_apprise_url(self, credential: str, target: str) -> str:
        raise NotImplementedError

    async def send(self, credential: str, req: SendRequest) -> str:
        url = self.build_apprise_url(credential, req.target)
        a = apprise.Apprise()
        a.add(url)
        title = ""
        body = req.message
        ok = await a.async_notify(body=body, title=title)
        if not ok:
            raise RuntimeError("apprise failed to deliver notification")
        return "delivered via apprise"


# ── Concrete channel implementations ──────────────────────────────────────────

class SlackHandler(AppriseHandler):
    """credential: Slack bot token (xoxb-...)  target: channel name e.g. #general"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        ch = target.lstrip("#") if target else "general"
        return f"slack://{credential}/#{ch}"


class TelegramHandler(AppriseHandler):
    """credential: bot token  target: chat_id"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        return f"tgram://{credential}/{target}/"


class GotifyHandler(AppriseHandler):
    """credential: app token  target: server URL e.g. https://gotify.example.com"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        from urllib.parse import urlparse
        p = urlparse(target)
        scheme = "gotifys" if p.scheme == "https" else "gotify"
        return f"{scheme}://{p.netloc}/{credential}/"


class GchatHandler(AppriseHandler):
    """credential: full Google Chat webhook URL"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        return f"gchat://{credential}"


class TeamsHandler(AppriseHandler):
    """credential: full MS Teams webhook URL"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        return credential  # Apprise accepts the raw teams URL


class PushoverHandler(AppriseHandler):
    """credential: user_key/app_token  e.g. 'USER_KEY/APP_TOKEN'"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        user_key, app_token = credential.split("/", 1)
        return f"pover://{user_key}@{app_token}/"


class MattermostHandler(AppriseHandler):
    """credential: full Mattermost incoming webhook URL"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        return credential


class RocketchatHandler(AppriseHandler):
    """credential: full Rocket.Chat webhook URL"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        return credential


class LineHandler(AppriseHandler):
    """credential: LINE Notify access token"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        return f"line://{credential}/"


class TwilioHandler(AppriseHandler):
    """credential: 'account_sid:auth_token:from_number'  target: to_number"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        parts = credential.split(":")
        sid, token, from_no = parts[0], parts[1], parts[2]
        return f"twilio://{sid}:{token}@{from_no}/{target}/"


class VonageHandler(AppriseHandler):
    """credential: 'api_key:api_secret:from_number'  target: to_number"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        parts = credential.split(":")
        key, secret, from_no = parts[0], parts[1], parts[2]
        return f"nexmo://{key}:{secret}/{from_no}/{target}/"


class OpsgenieHandler(AppriseHandler):
    """credential: OpsGenie API key"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        return f"opsgenie://{credential}/"


class PagerdutyHandler(AppriseHandler):
    """credential: PagerDuty integration key"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        return f"pagerduty://{credential}@events.pagerduty.com/"


class OnesignalHandler(AppriseHandler):
    """credential: 'app_id:api_key'"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        app_id, api_key = credential.split(":", 1)
        return f"onesignal://{api_key}/{app_id}/"


class WebexHandler(AppriseHandler):
    """credential: Webex bot token  target: room ID"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        return f"webex://{credential}/{target}/"


class ViberHandler(AppriseHandler):
    """credential: Viber bot token  target: receiver ID"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        return f"viber://{credential}/{target}/"


class MatrixHandler(AppriseHandler):
    """credential: 'user:password@homeserver'  target: room alias e.g. #room:server"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        return f"matrix://{credential}/{target}/"


class FeishuHandler(AppriseHandler):
    """credential: Feishu/Lark webhook URL"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        return credential


class KakaotalkHandler(AppriseHandler):
    """credential: KakaoTalk access token"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        return f"kakao://{credential}/"


class WechatHandler(AppriseHandler):
    """credential: 'corp_id:corp_secret:agent_id'  target: to_user"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        parts = credential.split(":")
        corp_id, corp_secret, agent_id = parts[0], parts[1], parts[2]
        to = target or "@all"
        return f"wxwork://{corp_id}:{corp_secret}/{agent_id}/{to}/"


class WhatsappHandler(AppriseHandler):
    """credential: Meta Cloud API token  target: phone number"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        return f"whatsapp://{credential}/{target}/"


class ZaloHandler(AppriseHandler):
    """credential: Zalo OA access token  target: user ID"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        # Apprise does not natively support Zalo; use raw HTTP fallback
        raise NotImplementedError("Zalo not supported via apprise — use direct handler")


class FcmHandler(AppriseHandler):
    """credential: FCM server key  target: device token or topic"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        return f"fcm://{credential}/{target}/"


class IrcHandler(AppriseHandler):
    """credential: 'nick:password@host:port'  target: #channel"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        ch = target.lstrip("#")
        return f"irc://{credential}/#{ch}"


class SignalHandler(AppriseHandler):
    """credential: Signal CLI REST API base URL  target: recipient number"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        return f"signals://{credential}/{target}/"


class TwitchHandler(AppriseHandler):
    """credential: 'client_id:client_secret:access_token'  target: channel"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        parts = credential.split(":")
        client_id, client_secret, token = parts[0], parts[1], parts[2]
        return f"twitch://{client_id}:{client_secret}:{token}/{target}/"


class NostrHandler(AppriseHandler):
    """credential: private key (nsec or hex)  target: relay URL"""
    def build_apprise_url(self, credential: str, target: str) -> str:
        relay = target or "wss://relay.damus.io"
        return f"nostr://{credential}@{relay}/"

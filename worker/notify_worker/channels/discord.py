import httpx
from notify_worker.channels.base import ChannelHandler
from notify_worker.models import SendRequest


class DiscordHandler(ChannelHandler):
    """
    credential: full Discord webhook URL
      e.g. https://discord.com/api/webhooks/{id}/{token}
    target: ignored (channel is encoded in the webhook URL)
    """

    async def send(self, credential: str, req: SendRequest) -> str:
        payload: dict = {"content": req.message}
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(credential, json=payload)
        resp.raise_for_status()
        return f"delivered to discord webhook (HTTP {resp.status_code})"

import httpx
from notify_worker.channels.base import ChannelHandler
from notify_worker.models import SendRequest


class SlackHandler(ChannelHandler):
    """
    credential: Slack incoming webhook URL
      e.g. https://hooks.slack.com/services/T.../B.../...
    target: ignored (channel is bound to the webhook)
    """

    async def send(self, credential: str, req: SendRequest) -> str:
        payload = {"text": req.message}
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(credential, json=payload)
        resp.raise_for_status()
        return f"delivered to slack webhook (HTTP {resp.status_code})"

from pydantic import BaseModel
from typing import Literal


class SendRequest(BaseModel):
    message: str
    title: str = ""          # subject line for channels that have one (email)
    target: str = ""
    format: Literal["text", "html", "markdown"] = "text"
    # gateway injects routing_key into body
    channel: str | None = None
    routing_key: dict | None = None

    @property
    def resolved_channel(self) -> str | None:
        if self.channel:
            return self.channel
        if self.routing_key:
            return self.routing_key.get("channel")
        return None


class SendResponse(BaseModel):
    ok: bool
    channel: str
    detail: str = ""

from abc import ABC, abstractmethod
from notify_worker.models import SendRequest


class ChannelHandler(ABC):
    @abstractmethod
    async def send(self, credential: str, req: SendRequest) -> str:
        """Send notification. Returns a detail string on success, raises on failure."""
        ...

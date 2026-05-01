import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from notify_worker.models import SendRequest, SendResponse
from notify_worker.router import get_handler

logger = logging.getLogger("notify_worker")
app = FastAPI(title="Notify Worker", version="1.0.0")


def _extract_credential(request: Request) -> str:
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth[len("Bearer "):]
    raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")


def _extract_channel(channel_path: str | None, body: SendRequest) -> str:
    # Priority: URL path segment > body.channel > body.routing_key.channel
    if channel_path:
        return channel_path
    resolved = body.resolved_channel
    if resolved:
        return resolved
    raise HTTPException(status_code=400, detail="Channel not specified — provide it in the URL path (/notify/{channel}/send) or in the request body as 'channel'")


@app.post("/notify/{channel}/send", response_model=SendResponse)
async def send_with_channel(channel: str, request: Request, body: SendRequest):
    credential = _extract_credential(request)
    return await _dispatch(channel, credential, body)


@app.post("/send", response_model=SendResponse)
async def send(request: Request, body: SendRequest):
    credential = _extract_credential(request)
    channel = _extract_channel(None, body)
    return await _dispatch(channel, credential, body)


async def _dispatch(channel: str, credential: str, body: SendRequest) -> SendResponse:
    try:
        handler = get_handler(channel)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        detail = await handler.send(credential, body)
        logger.info("channel=%s ok: %s", channel, detail)
        return SendResponse(ok=True, channel=channel, detail=detail)
    except Exception as e:
        logger.error("channel=%s error: %s", channel, e)
        raise HTTPException(status_code=502, detail=f"Delivery failed: {e}")


@app.get("/health")
async def health():
    return {"ok": True}

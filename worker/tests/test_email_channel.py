"""Unit tests for the platform email channel (unitysvc#1525).

Verifies the Mailgun call shape (from/to/subject/text|html), recipient
validation, and the unconfigured-worker error — without hitting Mailgun.
"""

import httpx
import pytest

from notify_worker.channels.email import EmailHandler
from notify_worker.models import SendRequest

# Bind the real client before any test monkeypatches httpx.AsyncClient.
_REAL_ASYNC_CLIENT = httpx.AsyncClient

MAILGUN_ENV = {
    "MAILGUN_API_KEY": "key-test",
    "MAILGUN_DOMAIN": "svcpass.com",
    "NOTIFY_EMAIL_FROM": "UnitySVC <noreply@svcpass.com>",
}


def _mock_transport(capture):
    def handler(request: httpx.Request) -> httpx.Response:
        capture["url"] = str(request.url)
        capture["auth"] = request.headers.get("authorization")
        capture["body"] = request.content.decode()
        return httpx.Response(200, json={"id": "<queued@mailgun>"})

    return httpx.MockTransport(handler)


@pytest.mark.asyncio
async def test_sends_text_email_with_defaults(monkeypatch):
    for k, v in MAILGUN_ENV.items():
        monkeypatch.setenv(k, v)
    cap: dict = {}
    monkeypatch.setattr(
        httpx, "AsyncClient",
        lambda **kw: _REAL_ASYNC_CLIENT(transport=_mock_transport(cap), **{k: v for k, v in kw.items() if k != "transport"}),
    )

    req = SendRequest(message="disk is full", format="text")
    detail = await EmailHandler().send("ops@customer.com", req)

    assert "svcpass.com/messages" in cap["url"]
    assert cap["auth"] is not None  # basic auth api:key
    assert "to=ops%40customer.com" in cap["body"]
    assert "from=" in cap["body"]
    assert "subject=UnitySVC+Notification" in cap["body"]  # default subject
    assert "text=disk+is+full" in cap["body"]
    assert "queued to ops@customer.com" in detail


@pytest.mark.asyncio
async def test_html_and_custom_subject(monkeypatch):
    for k, v in MAILGUN_ENV.items():
        monkeypatch.setenv(k, v)
    cap: dict = {}
    monkeypatch.setattr(
        httpx, "AsyncClient",
        lambda **kw: _REAL_ASYNC_CLIENT(transport=_mock_transport(cap), **{k: v for k, v in kw.items() if k != "transport"}),
    )

    req = SendRequest(message="<b>down</b>", title="ALERT: uptime", format="html")
    await EmailHandler().send("ops@customer.com", req)
    assert "subject=ALERT%3A+uptime" in cap["body"]
    assert "html=%3Cb%3Edown%3C%2Fb%3E" in cap["body"]
    assert "text=" not in cap["body"]  # html, not text


@pytest.mark.asyncio
async def test_invalid_recipient_rejected(monkeypatch):
    for k, v in MAILGUN_ENV.items():
        monkeypatch.setenv(k, v)
    with pytest.raises(ValueError, match="not a valid email"):
        await EmailHandler().send("not-an-email", SendRequest(message="x"))


@pytest.mark.asyncio
async def test_unconfigured_worker_errors(monkeypatch):
    monkeypatch.delenv("MAILGUN_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="MAILGUN_API_KEY unset"):
        await EmailHandler().send("ops@customer.com", SendRequest(message="x"))

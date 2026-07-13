"""Platform email channel — send from noreply@svcpass.com via Mailgun.

Unlike the Apprise channels, email delivery does NOT ask the customer for an
SMTP server (unitysvc#1525): most customers have none, and OAuth-signup emails
are often non-deliverable. Instead the PLATFORM sends the mail from a domain we
own (svcpass.com) through Mailgun. The ``credential`` here is therefore the
RECIPIENT address (from the customer's ``UNITYSVC_NOTIFY_EMAIL`` secret on the
default channel, or a per-request param on the ``-plus`` channel), not an
upstream secret — mirroring how the Discord handler treats the webhook URL as
the destination.

Worker deployment env (NOT customer secrets — platform-owned):
  MAILGUN_API_KEY     required to actually send (absent → 502 with a clear msg)
  MAILGUN_DOMAIN      the sending domain (default: svcpass.com)
  MAILGUN_BASE        API base (default: https://api.mailgun.net/v3)
  NOTIFY_EMAIL_FROM   From header (default: UnitySVC <noreply@svcpass.com>)
"""

import os
import re

import httpx

from notify_worker.channels.base import ChannelHandler
from notify_worker.models import SendRequest

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_DEFAULT_SUBJECT = "UnitySVC Notification"


class EmailHandler(ChannelHandler):
    """
    credential: recipient email address.
    req.title:  subject line (defaults to "UnitySVC Notification").
    req.message: body; sent as HTML when req.format == "html", else plain text.
    """

    async def send(self, credential: str, req: SendRequest) -> str:
        recipient = (credential or "").strip()
        if not _EMAIL_RE.match(recipient):
            raise ValueError(f"recipient is not a valid email address: {recipient!r}")

        api_key = os.environ.get("MAILGUN_API_KEY")
        if not api_key:
            raise RuntimeError(
                "email channel not configured: MAILGUN_API_KEY unset on the worker"
            )
        domain = os.environ.get("MAILGUN_DOMAIN", "svcpass.com")
        base = os.environ.get("MAILGUN_BASE", "https://api.mailgun.net/v3").rstrip("/")
        sender = os.environ.get("NOTIFY_EMAIL_FROM", "UnitySVC <noreply@svcpass.com>")

        data = {
            "from": sender,
            "to": recipient,
            "subject": (req.title or "").strip() or _DEFAULT_SUBJECT,
        }
        # Mailgun keys the content type off the field name.
        data["html" if req.format == "html" else "text"] = req.message

        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                f"{base}/{domain}/messages",
                auth=("api", api_key),
                data=data,
            )
        resp.raise_for_status()
        return f"email queued to {recipient} via Mailgun (HTTP {resp.status_code})"

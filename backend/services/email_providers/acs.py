"""
Azure Communication Services (Email) provider.

Uses the async azure-communication-email SDK. Requires a verified sender domain on the ACS resource.
"""
from __future__ import annotations

import logging
import re
from typing import Any, Mapping, MutableMapping, Optional

from azure.communication.email.aio import EmailClient
from azure.core.exceptions import HttpResponseError

from .mailhog import EmailProvider, TransientEmailError, PermanentEmailError

logger = logging.getLogger(__name__)


def _plain_text_from_html(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:100_000] if text else " "


class ACSEmailProvider(EmailProvider):
    """
    Send transactional email via Azure Communication Services Email API.

    Environment: AZURE_COMMUNICATION_CONNECTION_STRING (or ACS_CONNECTION_STRING).
    Sender must match an address/domain verified on the ACS resource.
    """

    def __init__(self, connection_string: str) -> None:
        if not connection_string or not connection_string.strip():
            raise ValueError(
                "ACS email requires AZURE_COMMUNICATION_CONNECTION_STRING (or ACS_CONNECTION_STRING)"
            )
        self._conn = connection_string.strip()
        self._client: Optional[EmailClient] = None

    async def _get_client(self) -> EmailClient:
        if self._client is None:
            self._client = EmailClient.from_connection_string(self._conn)
        return self._client

    async def close(self) -> None:
        if self._client is not None:
            await self._client.close()
            self._client = None

    async def send(
        self,
        to: str,
        subject: str,
        html_body: str,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
    ) -> bool:
        from_email = (from_email or "").strip()
        from_name = (from_name or "").strip()
        if not from_email:
            raise PermanentEmailError("ACS email requires a configured from_email (EMAIL_FROM)")
        subject = subject or "(no subject)"
        plain = _plain_text_from_html(html_body)

        message: MutableMapping[str, Any] = {
            "senderAddress": from_email,
            "content": {
                "subject": subject,
                "html": html_body,
                "plainText": plain,
            },
            "recipients": {
                "to": [{"address": to, **({"displayName": from_name} if from_name else {})}],
            },
        }

        client = await self._get_client()
        try:
            poller = await client.begin_send(message)
            result: Mapping[str, Any] = await poller.result()
        except HttpResponseError as e:
            status = getattr(e, "status_code", None) or 0
            if status in (401, 403):
                raise PermanentEmailError(f"ACS email auth/forbidden ({status}): {e}") from e
            if status == 400:
                raise PermanentEmailError(f"ACS email invalid request ({status}): {e}") from e
            if status == 429:
                raise TransientEmailError(f"ACS email rate limited: {e}") from e
            if status >= 500:
                raise TransientEmailError(f"ACS email server error ({status}): {e}") from e
            raise TransientEmailError(f"ACS email HTTP error ({status}): {e}") from e
        except TransientEmailError:
            raise
        except PermanentEmailError:
            raise
        except Exception as e:
            raise TransientEmailError(f"ACS email unexpected error: {e}") from e

        raw_status = (result.get("status") if isinstance(result, Mapping) else None) or ""
        status_upper = str(raw_status).strip().upper()
        if status_upper == "FAILED":
            err = result.get("error") if isinstance(result, Mapping) else None
            msg = ""
            if isinstance(err, Mapping):
                msg = str(err.get("message") or err.get("code") or err)
            raise PermanentEmailError(f"ACS email send failed: {msg or raw_status}")
        if status_upper and status_upper not in {"SUCCEEDED", "RUNNING"}:
            logger.warning("ACS email LRO status=%s raw=%s", raw_status, result)

        return True

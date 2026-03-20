"""
Outbound HTTP request logger.

Writes provider (e.g. OpenAI) outbound calls to log.ApiRequest so they are
visible in the same diagnostics stream as inbound middleware request logs.
"""

from __future__ import annotations

import json
import time
import uuid
from typing import Any, Optional
from urllib.parse import urlparse

from common.config_service import ConfigurationService
from common.constants import (
    DEFAULT_LOGGING_CAPTURE_PAYLOADS,
    DEFAULT_LOGGING_MAX_PAYLOAD_SIZE_KB,
)
from common.database import SessionLocal
from common.request_context import get_current_request_context
from middleware.request_logger import log_api_request

_CONFIG_CACHE: dict[str, Any] = {}
_CONFIG_CACHE_TIMESTAMP: Optional[float] = None
_CONFIG_CACHE_TTL_SECONDS = 300


def _get_logging_config() -> dict[str, Any]:
    global _CONFIG_CACHE, _CONFIG_CACHE_TIMESTAMP
    if (
        _CONFIG_CACHE_TIMESTAMP is not None
        and (time.time() - _CONFIG_CACHE_TIMESTAMP) < _CONFIG_CACHE_TTL_SECONDS
    ):
        return _CONFIG_CACHE

    db = None
    try:
        db = SessionLocal()
        config_service = ConfigurationService(db)
        _CONFIG_CACHE = {
            "capture_payloads": config_service.get_logging_capture_payloads(),
            "max_payload_size_kb": config_service.get_logging_max_payload_size_kb(),
        }
        _CONFIG_CACHE_TIMESTAMP = time.time()
        return _CONFIG_CACHE
    except Exception:
        return {
            "capture_payloads": DEFAULT_LOGGING_CAPTURE_PAYLOADS,
            "max_payload_size_kb": DEFAULT_LOGGING_MAX_PAYLOAD_SIZE_KB,
        }
    finally:
        if db is not None:
            db.close()


def _serialize_payload(payload: Any, max_payload_chars: int) -> Optional[str]:
    if payload is None:
        return None
    try:
        # Keep payload logs valid JSON even when truncated, so downstream
        # tooling (and humans) can parse/read them reliably.
        if isinstance(payload, str):
            content = payload
            if len(content) <= max_payload_chars:
                return json.dumps({"text": content}, ensure_ascii=True)
            return json.dumps(
                {
                    "truncated": True,
                    "original_size_chars": len(content),
                    "preview": content[:max_payload_chars],
                },
                ensure_ascii=True,
            )

        content = json.dumps(payload, ensure_ascii=True)
        if len(content) <= max_payload_chars:
            return content
        return json.dumps(
            {
                "truncated": True,
                "original_size_chars": len(content),
                "preview": content[:max_payload_chars],
            },
            ensure_ascii=True,
        )
    except Exception:
        return None


def _build_outbound_path(provider: str, url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path or "/"
    safe_provider = provider.strip().lower() or "unknown"
    return f"/outbound/{safe_provider}{path}"


def log_outbound_http_request(
    *,
    provider: str,
    method: str,
    url: str,
    status_code: int,
    duration_ms: int,
    request_payload: Any = None,
    response_payload: Any = None,
) -> None:
    """
    Persist outbound HTTP call metadata to log.ApiRequest.
    """
    context = get_current_request_context()
    logging_config = _get_logging_config()
    capture_payloads = bool(logging_config.get("capture_payloads", True))
    max_payload_size_kb = int(
        logging_config.get("max_payload_size_kb", DEFAULT_LOGGING_MAX_PAYLOAD_SIZE_KB)
    )
    max_payload_chars = max(1024, max_payload_size_kb * 1024)
    request_id = (
        f"{context.request_id}:outbound:{uuid.uuid4()}" if context else str(uuid.uuid4())
    )

    headers = {
        "direction": "outbound",
        "provider": provider,
        "url": url,
    }

    log_api_request(
        {
            "request_id": request_id,
            "method": method.upper(),
            "path": _build_outbound_path(provider, url),
            "query_params": None,
            "status_code": status_code,
            "duration_ms": max(0, int(duration_ms)),
            "user_id": context.user_id if context else None,
            "company_id": context.company_id if context else None,
            "ip_address": context.ip_address if context else None,
            "user_agent": context.user_agent if context else "backend-outbound-httpx",
            "request_payload": (
                _serialize_payload(request_payload, max_payload_chars)
                if capture_payloads
                else None
            ),
            "response_payload": (
                _serialize_payload(response_payload, max_payload_chars)
                if capture_payloads
                else None
            ),
            "headers": json.dumps(headers, ensure_ascii=True),
        }
    )


def timed_log_outbound_http_request(
    *,
    provider: str,
    method: str,
    url: str,
    started_at_monotonic: float,
    status_code: int,
    request_payload: Any = None,
    response_payload: Any = None,
) -> None:
    duration_ms = int((time.monotonic() - started_at_monotonic) * 1000)
    log_outbound_http_request(
        provider=provider,
        method=method,
        url=url,
        status_code=status_code,
        duration_ms=duration_ms,
        request_payload=request_payload,
        response_payload=response_payload,
    )


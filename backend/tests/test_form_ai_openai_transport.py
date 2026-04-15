"""Unit tests for OpenAI transport resolution and SSE accumulation (Story 6.2 form-ai)."""

import json

import pytest

from modules.form_ai import service


def test_resolve_auto_defaults_to_sync_when_env_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FORM_AI_OPENAI_TRANSPORT", raising=False)
    assert service._resolve_openai_transport("auto") == "sync"


def test_resolve_auto_reads_stream_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FORM_AI_OPENAI_TRANSPORT", "stream")
    assert service._resolve_openai_transport("auto") == "stream"


def test_resolve_explicit_overrides_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FORM_AI_OPENAI_TRANSPORT", "stream")
    assert service._resolve_openai_transport("sync") == "sync"
    assert service._resolve_openai_transport("stream") == "stream"


def test_consume_responses_sse_concatenates_deltas() -> None:
    event = {"type": "response.output_text.delta", "delta": '{"a":1}'}
    lines = [
        f"data: {json.dumps(event)}".encode("utf-8"),
        b"data: [DONE]\n",
    ]
    text = service._consume_openai_responses_sse_to_text(lines)
    assert text == '{"a":1}'


def test_consume_chat_completions_sse_concatenates_content() -> None:
    lines = [
        b'data: {"choices":[{"delta":{"content":"hello"}}]}',
        b'data: {"choices":[{"delta":{"content":" world"}}]}',
        b"data: [DONE]\n",
    ]
    assert service._consume_chat_completions_sse_to_text(lines).strip() == "hello world"

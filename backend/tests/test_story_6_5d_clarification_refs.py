"""Story 6.5d: clarification ref resolution unit tests."""
from __future__ import annotations

from unittest.mock import MagicMock

from modules.reference import clarification


class _Row:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def test_resolve_clarification_context_uses_request_override():
    db = MagicMock()
    db.execute.return_value.fetchall.side_effect = [
        [
            _Row(
                Code="AU",
                DisplayName="Australia",
                FlagEmoji="🇦🇺",
                Description="",
                ClarificationSummary="E1 AU",
            ),
            _Row(
                Code="US",
                DisplayName="United States",
                FlagEmoji="🇺🇸",
                Description="",
                ClarificationSummary="E1 US",
            ),
        ],
        [
            _Row(
                Code="EVENT_REGISTRATION",
                DisplayName="Event Registration",
                PromptHint="purpose hint",
            ),
        ],
        [
            _Row(
                Code="ATTENDEE",
                DisplayName="Attendee",
                PromptHint="respondent hint",
            ),
        ],
    ]
    db.execute.return_value.fetchone.return_value = None

    ctx = clarification.resolve_clarification_context(
        db,
        company_id=1,
        form_id=None,
        audience_locale_code="US",
        form_purpose_code="EVENT_REGISTRATION",
        respondent_type_code="ATTENDEE",
    )
    assert ctx.audience_locale_code == "US"
    assert ctx.e1_summary == "E1 US"
    assert ctx.e2_hint == "purpose hint"
    assert ctx.e3_hint == "respondent hint"

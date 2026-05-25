"""Clarification ref resolution (Story 6.5d Track B)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass(frozen=True)
class ClarificationItem:
    code: str
    displayName: str
    description: Optional[str] = None
    flagEmoji: Optional[str] = None
    promptHint: Optional[str] = None
    clarificationSummary: Optional[str] = None


@dataclass(frozen=True)
class ClarificationListResponse:
    items: List[ClarificationItem]
    defaultCode: str
    resolvedDefault: ClarificationItem


@dataclass(frozen=True)
class ResolvedClarificationContext:
    audience_locale_code: str
    form_purpose_code: str
    respondent_type_code: str
    e1_summary: str
    e2_hint: str
    e3_hint: str


def _coerce_form_id(runtime_context: Optional[Dict[str, Any]]) -> Optional[int]:
    if not runtime_context:
        return None
    raw = runtime_context.get("formId")
    if raw is None:
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def _load_company_defaults(
    db: Session, company_id: Optional[int]
) -> Dict[str, Optional[str]]:
    if company_id is None:
        return {}
    row = db.execute(
        text(
            """
            SELECT TOP 1
                [DefaultAudienceLocaleCode],
                [DefaultFormPurposeCode],
                [DefaultRespondentTypeCode]
            FROM [dbo].[Company]
            WHERE [CompanyID] = :company_id AND [IsDeleted] = 0
            """
        ),
        {"company_id": company_id},
    ).fetchone()
    if row is None:
        return {}
    return {
        "audienceLocale": row.DefaultAudienceLocaleCode,
        "formPurpose": row.DefaultFormPurposeCode,
        "respondentType": row.DefaultRespondentTypeCode,
    }


def _load_form_snapshot(
    db: Session, form_id: Optional[int]
) -> Dict[str, Optional[str]]:
    if form_id is None:
        return {}
    row = db.execute(
        text(
            """
            SELECT TOP 1
                [AudienceLocaleCode],
                [FormPurposeCode],
                [RespondentTypeCode]
            FROM [dbo].[Form]
            WHERE [FormID] = :form_id AND [IsDeleted] = 0
            """
        ),
        {"form_id": form_id},
    ).fetchone()
    if row is None:
        return {}
    return {
        "audienceLocale": row.AudienceLocaleCode,
        "formPurpose": row.FormPurposeCode,
        "respondentType": row.RespondentTypeCode,
    }


def _resolve_code(
    *,
    request_value: Optional[str],
    form_value: Optional[str],
    company_value: Optional[str],
    fallback: str,
) -> tuple[str, str]:
    if request_value:
        return request_value, "request"
    if form_value:
        return form_value, "form"
    if company_value:
        return company_value, "company"
    return fallback, "fallback"


def list_audience_locales(
    db: Session,
    *,
    company_id: Optional[int] = None,
    form_id: Optional[int] = None,
    request_code: Optional[str] = None,
) -> ClarificationListResponse:
    rows = db.execute(
        text(
            """
            SELECT [Code], [DisplayName], [FlagEmoji], [Description], [ClarificationSummary]
            FROM [ref].[AudienceLocale]
            WHERE [IsActive] = 1
            ORDER BY [SortOrder], [DisplayName]
            """
        )
    ).fetchall()
    items = [
        ClarificationItem(
            code=r.Code,
            displayName=r.DisplayName,
            description=r.Description,
            flagEmoji=r.FlagEmoji,
            clarificationSummary=r.ClarificationSummary,
        )
        for r in rows
    ]
    company_defaults = _load_company_defaults(db, company_id)
    form_snapshot = _load_form_snapshot(db, form_id)
    resolved_code, _ = _resolve_code(
        request_value=request_code,
        form_value=form_snapshot.get("audienceLocale"),
        company_value=company_defaults.get("audienceLocale"),
        fallback="AU",
    )
    resolved = next((i for i in items if i.code == resolved_code), items[0])
    return ClarificationListResponse(
        items=items,
        defaultCode=resolved.code,
        resolvedDefault=resolved,
    )


def list_form_purposes(
    db: Session,
    *,
    company_id: Optional[int] = None,
    form_id: Optional[int] = None,
    request_code: Optional[str] = None,
) -> ClarificationListResponse:
    rows = db.execute(
        text(
            """
            SELECT [Code], [DisplayName], [PromptHint]
            FROM [ref].[FormPurpose]
            WHERE [IsActive] = 1
            ORDER BY [SortOrder], [DisplayName]
            """
        )
    ).fetchall()
    items = [
        ClarificationItem(
            code=r.Code,
            displayName=r.DisplayName,
            promptHint=r.PromptHint,
        )
        for r in rows
    ]
    company_defaults = _load_company_defaults(db, company_id)
    form_snapshot = _load_form_snapshot(db, form_id)
    resolved_code, _ = _resolve_code(
        request_value=request_code,
        form_value=form_snapshot.get("formPurpose"),
        company_value=company_defaults.get("formPurpose"),
        fallback="EVENT_REGISTRATION",
    )
    resolved = next((i for i in items if i.code == resolved_code), items[0])
    return ClarificationListResponse(
        items=items,
        defaultCode=resolved.code,
        resolvedDefault=resolved,
    )


def list_respondent_types(
    db: Session,
    *,
    company_id: Optional[int] = None,
    form_id: Optional[int] = None,
    request_code: Optional[str] = None,
) -> ClarificationListResponse:
    rows = db.execute(
        text(
            """
            SELECT [Code], [DisplayName], [PromptHint]
            FROM [ref].[RespondentType]
            WHERE [IsActive] = 1
            ORDER BY [SortOrder], [DisplayName]
            """
        )
    ).fetchall()
    items = [
        ClarificationItem(
            code=r.Code,
            displayName=r.DisplayName,
            promptHint=r.PromptHint,
        )
        for r in rows
    ]
    company_defaults = _load_company_defaults(db, company_id)
    form_snapshot = _load_form_snapshot(db, form_id)
    resolved_code, _ = _resolve_code(
        request_value=request_code,
        form_value=form_snapshot.get("respondentType"),
        company_value=company_defaults.get("respondentType"),
        fallback="ATTENDEE",
    )
    resolved = next((i for i in items if i.code == resolved_code), items[0])
    return ClarificationListResponse(
        items=items,
        defaultCode=resolved.code,
        resolvedDefault=resolved,
    )


def resolve_clarification_context(
    db: Session,
    *,
    company_id: Optional[int],
    form_id: Optional[int],
    audience_locale_code: Optional[str],
    form_purpose_code: Optional[str],
    respondent_type_code: Optional[str],
) -> ResolvedClarificationContext:
    locales = list_audience_locales(
        db,
        company_id=company_id,
        form_id=form_id,
        request_code=audience_locale_code,
    )
    purposes = list_form_purposes(
        db,
        company_id=company_id,
        form_id=form_id,
        request_code=form_purpose_code,
    )
    respondents = list_respondent_types(
        db,
        company_id=company_id,
        form_id=form_id,
        request_code=respondent_type_code,
    )
    locale = locales.resolvedDefault
    purpose = purposes.resolvedDefault
    respondent = respondents.resolvedDefault
    return ResolvedClarificationContext(
        audience_locale_code=locale.code,
        form_purpose_code=purpose.code,
        respondent_type_code=respondent.code,
        e1_summary=locale.clarificationSummary or "",
        e2_hint=purpose.promptHint or "",
        e3_hint=respondent.promptHint or "",
    )

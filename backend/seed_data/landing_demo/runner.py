"""
Idempotent seed for landing-page demo event + eight published forms.

Used by scripts/seed_landing_demo_forms.py (local review) and migration 096 (test env).
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.company import Company
from models.event import Event
from models.form import Form
from models.form_public_link import FormPublicLink
from models.ref.country import Country
from models.ref.event_status import EventStatus
from models.ref.event_type import EventType
from models.ref.form_approval_status import FormApprovalStatus
from models.ref.form_status import FormStatus
from modules.events.service import create_event
from modules.forms.publish_service import publish_form
from modules.forms.service import create_form
from modules.forms.version_service import FormVersionService
from seed_data.landing_demo.forms import (
    DEMO_EVENT_DESCRIPTION,
    DEMO_EVENT_NAME,
    LANDING_DEMO_FORMS,
    LandingDemoFormSpec,
)

COMPANY_NAME = "Signal Platforms"
DEFAULT_USER_ID = 1


@dataclass
class SeedResult:
    company_id: int
    event_id: int
    event_created: bool
    forms: list[dict[str, Any]]


def _resolve_company(db: Session, company_name: str) -> Company:
    company = db.execute(
        select(Company).where(
            Company.CompanyName == company_name,
            Company.IsDeleted == False,  # noqa: E712
        )
    ).scalars().first()
    if not company:
        raise ValueError(f"Company not found: {company_name!r}")
    return company


def _resolve_ref_ids(db: Session) -> dict[str, int]:
    draft_form = db.execute(select(FormStatus).where(FormStatus.StatusCode == "DRAFT")).scalars().first()
    no_approval = db.execute(
        select(FormApprovalStatus).where(FormApprovalStatus.ApprovalStatusCode == "NO_APPROVAL")
    ).scalars().first()
    published_event = db.execute(
        select(EventStatus).where(EventStatus.StatusCode == "PUBLISHED")
    ).scalars().first()
    expo_type = db.execute(select(EventType).where(EventType.TypeCode == "EXPO")).scalars().first()
    au = db.execute(select(Country).where(Country.CountryCode == "AU")).scalars().first()

    missing = []
    if not draft_form:
        missing.append("FormStatus DRAFT")
    if not no_approval:
        missing.append("FormApprovalStatus NO_APPROVAL")
    if not published_event:
        missing.append("EventStatus PUBLISHED")
    if not expo_type:
        missing.append("EventType EXPO")
    if not au:
        missing.append("Country AU")
    if missing:
        raise ValueError("Missing reference data: " + ", ".join(missing))

    return {
        "form_status_draft": draft_form.FormStatusID,
        "form_approval_no_approval": no_approval.FormApprovalStatusID,
        "event_status_published": published_event.EventStatusID,
        "event_type_expo": expo_type.EventTypeID,
        "country_au": au.CountryID,
    }


async def _get_or_create_demo_event(
    db: Session,
    *,
    user_id: int,
    company_id: int,
    refs: dict[str, int],
) -> tuple[Event, bool]:
    existing = db.execute(
        select(Event).where(
            Event.CompanyID == company_id,
            Event.Name == DEMO_EVENT_NAME,
            Event.IsDeleted == False,  # noqa: E712
        )
    ).scalars().first()
    if existing:
        return existing, False

    start = datetime.utcnow() + timedelta(days=90)
    end = start + timedelta(days=2)
    event_data = {
        "name": DEMO_EVENT_NAME,
        "description": DEMO_EVENT_DESCRIPTION,
        "short_description": "Public demo forms for EventLead landing page.",
        "start_datetime": start,
        "end_datetime": end,
        "timezone_identifier": "Australia/Brisbane",
        "venue_name": "Demo Showcase Hall",
        "city": "Brisbane",
        "state": "QLD",
        "country_id": refs["country_au"],
        "event_type_id": refs["event_type_expo"],
        "event_status_id": refs["event_status_published"],
        "is_public": False,
        "is_shared_with_platform": False,
        "expected_attendees": 500,
        "tags": "landing-page,demo,public-examples",
    }
    event = await create_event(db, user_id, company_id, event_data)
    return event, True


async def _get_or_create_form(
    db: Session,
    *,
    user_id: int,
    company_id: int,
    event_id: int,
    spec: LandingDemoFormSpec,
    refs: dict[str, int],
    publish: bool,
    update_existing_definitions: bool,
) -> dict[str, Any]:
    from sqlalchemy import desc

    from models.form_version import FormVersion

    existing = db.execute(
        select(Form).where(
            Form.CompanyID == company_id,
            Form.EventID == event_id,
            Form.FormName == spec.form_name,
            Form.IsDeleted == False,  # noqa: E712
        )
    ).scalars().first()

    created = False
    definition = spec.builder()
    version_service = FormVersionService(db)

    if existing:
        form_id = existing.FormID
        if update_existing_definitions:
            draft = db.execute(
                select(FormVersion)
                .where(FormVersion.FormID == form_id, FormVersion.Status == "DRAFT")
                .order_by(desc(FormVersion.VersionNumber))
                .limit(1)
            ).scalars().first()
            if draft:
                await version_service.update_version(
                    form_id,
                    draft.VersionNumber,
                    user_id,
                    definition,
                    comment=f"Landing demo refresh ({spec.slug})",
                )
            else:
                await version_service.create_version(
                    form_id,
                    user_id,
                    definition,
                    comment=f"Landing demo seed refresh ({spec.slug})",
                )
            if publish:
                publish_form(db, form_id, user_id)
    else:
        form_data = {
            "form_name": spec.form_name,
            "form_description": spec.form_description,
            "event_id": event_id,
            "form_status_id": refs["form_status_draft"],
            "form_approval_status_id": refs["form_approval_no_approval"],
            "is_public": True,
            "deployment_cost": 0,
        }
        form = await create_form(db, user_id, company_id, form_data)
        form_id = form.FormID
        created = True
        await version_service.create_version(
            form_id,
            user_id,
            definition,
            comment=f"Landing demo seed ({spec.slug})",
        )
        if publish:
            publish_form(db, form_id, user_id)

    link = db.execute(
        select(FormPublicLink).where(
            FormPublicLink.FormID == form_id,
            FormPublicLink.LinkType == "PRODUCTION",
            FormPublicLink.IsActive == True,  # noqa: E712
        )
    ).scalars().first()
    token = link.Token if link else None
    base = os.environ.get("PUBLIC_FORM_BASE_URL", "http://localhost:3000")
    public_url = f"{base.rstrip('/')}/forms/{token}" if token else None

    return {
        "slug": spec.slug,
        "form_id": form_id,
        "form_name": spec.form_name,
        "created": created,
        "public_token": token,
        "public_url": public_url,
    }


async def seed_landing_demo(
    db: Session,
    *,
    user_id: int = DEFAULT_USER_ID,
    company_name: str = COMPANY_NAME,
    publish: bool = True,
    update_existing_definitions: bool = False,
    skip_if_complete: bool = True,
) -> SeedResult:
    """
    Create demo event and eight forms under Signal Platforms.

    When skip_if_complete=True and all eight forms already exist on the event, only
    returns metadata (no definition updates) unless update_existing_definitions=True.
    """
    company = _resolve_company(db, company_name)
    refs = _resolve_ref_ids(db)
    event, event_created = await _get_or_create_demo_event(
        db, user_id=user_id, company_id=company.CompanyID, refs=refs
    )

    existing_forms = db.execute(
        select(Form.FormName).where(
            Form.EventID == event.EventID,
            Form.CompanyID == company.CompanyID,
            Form.IsDeleted == False,  # noqa: E712
        )
    ).scalars().all()
    expected_names = {s.form_name for s in LANDING_DEMO_FORMS}
    have_all = expected_names.issubset(set(existing_forms))

    form_results: list[dict[str, Any]] = []
    if skip_if_complete and have_all and not update_existing_definitions:
        for spec in LANDING_DEMO_FORMS:
            form = db.execute(
                select(Form).where(
                    Form.EventID == event.EventID,
                    Form.FormName == spec.form_name,
                    Form.IsDeleted == False,  # noqa: E712
                )
            ).scalars().first()
            link = None
            if form and publish:
                link = db.execute(
                    select(FormPublicLink).where(
                        FormPublicLink.FormID == form.FormID,
                        FormPublicLink.LinkType == "PRODUCTION",
                        FormPublicLink.IsActive == True,  # noqa: E712
                    )
                ).scalars().first()
            base = os.environ.get("PUBLIC_FORM_BASE_URL", "http://localhost:3000")
            token = link.Token if link else None
            form_results.append(
                {
                    "slug": spec.slug,
                    "form_id": form.FormID if form else None,
                    "form_name": spec.form_name,
                    "created": False,
                    "public_token": token,
                    "public_url": f"{base.rstrip('/')}/forms/{token}" if token else None,
                }
            )
    else:
        for spec in LANDING_DEMO_FORMS:
            row = await _get_or_create_form(
                db,
                user_id=user_id,
                company_id=company.CompanyID,
                event_id=event.EventID,
                spec=spec,
                refs=refs,
                publish=publish,
                update_existing_definitions=update_existing_definitions,
            )
            form_results.append(row)

    return SeedResult(
        company_id=company.CompanyID,
        event_id=event.EventID,
        event_created=event_created,
        forms=form_results,
    )


def write_manifest(result: SeedResult, output_path: Path) -> None:
    payload = {
        "company_id": result.company_id,
        "event_id": result.event_id,
        "event_name": DEMO_EVENT_NAME,
        "event_created": result.event_created,
        "forms": result.forms,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

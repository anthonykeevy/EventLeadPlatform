"""Story 6.5e: Landing demo event (PUBLISHED) + eight DRAFT form shells with AI prompts.

Creates under Signal Platforms (CompanyID 1):
- Event: EventLead Public Demo Showcase 2026 (PUBLISHED)
- Eight form headers (DRAFT, NO_APPROVAL) linked to the event
- FormVersion v1: empty canvas + aiAgentSettings.lastPrompt per LANDING-PAGE-SAFE-EXAMPLE-FORMS.md

Forms are intentionally NOT published. Anthony builds via Form Builder, adds backgrounds,
tests, then publishes; published URLs are wired to the landing page separately.

Idempotent: safe to re-run if event/forms already exist (skips existing rows).

Revision ID: 096
Revises: 095
Create Date: 2026-06-03
"""

from __future__ import annotations

import json

from alembic import op
from sqlalchemy import text

from schemas.form_definition import FormDefinition
from seed_data.landing_demo.definition_shell import build_blank_definition_with_prompt
from seed_data.landing_demo.prompts import (
    COMPANY_ID,
    DEMO_EVENT_DESCRIPTION,
    DEMO_EVENT_NAME,
    DEMO_EVENT_SHORT,
    DEMO_TAG,
    LANDING_DEMO_FORM_ROWS,
    SEED_USER_ID,
)

revision = "096"
down_revision = "095"
branch_labels = None
depends_on = None

VERSION_COMMENT = "Story 6.5e landing demo shell — empty canvas; AI prompt pre-loaded for Form Builder"


def _validate_shell_definitions() -> None:
    for row in LANDING_DEMO_FORM_ROWS:
        raw = json.loads(build_blank_definition_with_prompt(0, row.ai_prompt))
        FormDefinition.model_validate(raw)


def upgrade() -> None:
    _validate_shell_definitions()
    conn = op.get_bind()

    company = conn.execute(
        text(
            """
            SELECT CompanyID, CompanyName
            FROM dbo.[Company]
            WHERE CompanyID = :cid AND IsDeleted = 0
            """
        ),
        {"cid": COMPANY_ID},
    ).fetchone()
    if not company:
        raise RuntimeError(
            f"096: CompanyID {COMPANY_ID} not found. Run migration 073 (Signal Platforms seed) first."
        )

    refs = conn.execute(
        text(
            """
            SELECT
                (SELECT TOP 1 EventStatusID FROM ref.EventStatus WHERE StatusCode = N'PUBLISHED') AS EventPublished,
                (SELECT TOP 1 EventTypeID FROM ref.EventType WHERE TypeCode = N'EXPO') AS EventTypeExpo,
                (SELECT TOP 1 CountryID FROM ref.Country WHERE CountryCode = N'AU') AS CountryAu,
                (SELECT TOP 1 FormStatusID FROM ref.FormStatus WHERE StatusCode = N'DRAFT') AS FormDraft,
                (SELECT TOP 1 FormApprovalStatusID FROM ref.FormApprovalStatus WHERE ApprovalStatusCode = N'NO_APPROVAL') AS FormNoApproval,
                (SELECT TOP 1 EventCompanyRoleID FROM ref.EventCompanyRole WHERE RoleCode = N'event_owner') AS EventOwnerRole
            """
        )
    ).fetchone()

    missing = [
        name
        for name, val in [
            ("EventStatus PUBLISHED", refs.EventPublished),
            ("EventType EXPO", refs.EventTypeExpo),
            ("Country AU", refs.CountryAu),
            ("FormStatus DRAFT", refs.FormDraft),
            ("FormApprovalStatus NO_APPROVAL", refs.FormNoApproval),
            ("EventCompanyRole event_owner", refs.EventOwnerRole),
        ]
        if val is None
    ]
    if missing:
        raise RuntimeError("096: Missing reference data: " + ", ".join(missing))

    event_row = conn.execute(
        text(
            """
            SELECT EventID FROM dbo.[Event]
            WHERE CompanyID = :cid AND Name = :name AND IsDeleted = 0
            """
        ),
        {"cid": COMPANY_ID, "name": DEMO_EVENT_NAME},
    ).fetchone()

    if event_row:
        event_id = int(event_row.EventID)
    else:
        insert_event = conn.execute(
            text(
                """
                INSERT INTO dbo.[Event] (
                    Name, Description, ShortDescription, CompanyID, CreatedBy,
                    StartDateTime, EndDateTime, TimezoneIdentifier,
                    VenueName, City, State, CountryID, EventTypeID, Tags,
                    IsPublic, IsSharedWithPlatform, IsPublicReviewRequired,
                    PublicReviewStatusID, EventStatusID, IsRecurring,
                    ExpectedAttendees, FormsCreated, TotalSubmissions,
                    CreatedDate, IsDeleted
                )
                OUTPUT INSERTED.EventID
                VALUES (
                    :name, :description, :short_desc, :company_id, :user_id,
                    DATEADD(day, 90, GETUTCDATE()),
                    DATEADD(day, 92, GETUTCDATE()),
                    N'Australia/Brisbane',
                    N'Demo Showcase Hall', N'Brisbane', N'QLD', :country_id, :event_type_id,
                    :tags,
                    0, 0, 0,
                    NULL, :event_status_id, 0,
                    500, 0, 0,
                    GETUTCDATE(), 0
                )
                """
            ),
            {
                "name": DEMO_EVENT_NAME,
                "description": DEMO_EVENT_DESCRIPTION,
                "short_desc": DEMO_EVENT_SHORT,
                "company_id": COMPANY_ID,
                "user_id": SEED_USER_ID,
                "country_id": refs.CountryAu,
                "event_type_id": refs.EventTypeExpo,
                "tags": DEMO_TAG,
                "event_status_id": refs.EventPublished,
            },
        )
        event_id = int(insert_event.scalar_one())

        conn.execute(
            text(
                """
                IF NOT EXISTS (
                    SELECT 1 FROM dbo.EventCompany
                    WHERE EventID = :event_id AND CompanyID = :company_id
                      AND IsActive = 1 AND IsDeleted = 0
                )
                INSERT INTO dbo.EventCompany (
                    EventID, CompanyID, EventCompanyRoleID, IsActive, CreatedBy, CreatedDate, IsDeleted
                )
                VALUES (
                    :event_id, :company_id, :role_id, 1, :user_id, GETUTCDATE(), 0
                )
                """
            ),
            {
                "event_id": event_id,
                "company_id": COMPANY_ID,
                "role_id": refs.EventOwnerRole,
                "user_id": SEED_USER_ID,
            },
        )

    forms_created = 0
    for row in LANDING_DEMO_FORM_ROWS:
        existing_form = conn.execute(
            text(
                """
                SELECT FormID FROM dbo.[Form]
                WHERE CompanyID = :company_id AND EventID = :event_id
                  AND FormName = :form_name AND IsDeleted = 0
                """
            ),
            {
                "company_id": COMPANY_ID,
                "event_id": event_id,
                "form_name": row.form_name,
            },
        ).fetchone()

        if existing_form:
            form_id = int(existing_form.FormID)
        else:
            ins = conn.execute(
                text(
                    """
                    INSERT INTO dbo.[Form] (
                        FormName, FormDescription, CompanyID, EventID,
                        FormStatusID, FormApprovalStatusID, IsPublic, DeploymentCost,
                        TotalSubmissions, DemoLeadsCollected, ProductionLeadsCollected,
                        UnpublishMode, CreatedBy, CreatedDate, IsDeleted
                    )
                    OUTPUT INSERTED.FormID
                    VALUES (
                        :form_name, :form_description, :company_id, :event_id,
                        :form_status_id, :approval_status_id, 0, 0,
                        0, 0, 0,
                        N'MANUAL', :user_id, GETUTCDATE(), 0
                    )
                    """
                ),
                {
                    "form_name": row.form_name,
                    "form_description": row.form_description,
                    "company_id": COMPANY_ID,
                    "event_id": event_id,
                    "form_status_id": refs.FormDraft,
                    "approval_status_id": refs.FormNoApproval,
                    "user_id": SEED_USER_ID,
                },
            )
            form_id = int(ins.scalar_one())
            forms_created += 1

        has_version = conn.execute(
            text(
                "SELECT 1 FROM dbo.FormVersion WHERE FormID = :form_id AND VersionNumber = 1"
            ),
            {"form_id": form_id},
        ).fetchone()

        if not has_version:
            definition_json = build_blank_definition_with_prompt(form_id, row.ai_prompt)
            conn.execute(
                text(
                    """
                    INSERT INTO dbo.FormVersion (
                        FormID, VersionNumber, DefinitionJSON, VersionComment,
                        Status, IsActive, CreatedBy, CreatedDate
                    )
                    VALUES (
                        :form_id, 1, :definition_json, :version_comment,
                        N'DRAFT', 0, :user_id, GETUTCDATE()
                    )
                    """
                ),
                {
                    "form_id": form_id,
                    "definition_json": definition_json,
                    "version_comment": VERSION_COMMENT,
                    "user_id": SEED_USER_ID,
                },
            )
        else:
            # Refresh prompt on existing shell if definition has no components (idempotent tune)
            conn.execute(
                text(
                    """
                    UPDATE dbo.FormVersion
                    SET DefinitionJSON = :definition_json,
                        VersionComment = :version_comment
                    WHERE FormID = :form_id AND VersionNumber = 1
                      AND Status = N'DRAFT'
                      AND DefinitionJSON NOT LIKE N'%"components":[{%'
                    """
                ),
                {
                    "form_id": form_id,
                    "definition_json": build_blank_definition_with_prompt(form_id, row.ai_prompt),
                    "version_comment": VERSION_COMMENT,
                },
            )

    conn.execute(
        text(
            """
            UPDATE dbo.[Event]
            SET FormsCreated = (
                SELECT COUNT(*) FROM dbo.[Form] f
                WHERE f.EventID = :event_id AND f.IsDeleted = 0
            ),
                UpdatedDate = GETUTCDATE(),
                UpdatedBy = :user_id
            WHERE EventID = :event_id
            """
        ),
        {"event_id": event_id, "user_id": SEED_USER_ID},
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
            UPDATE fv SET fv.Status = N'ARCHIVED', fv.IsActive = 0
            FROM dbo.FormVersion fv
            INNER JOIN dbo.[Form] f ON f.FormID = fv.FormID
            INNER JOIN dbo.[Event] e ON e.EventID = f.EventID
            WHERE e.Name = :event_name AND e.CompanyID = :company_id
              AND fv.VersionComment = :version_comment;

            UPDATE f SET f.IsDeleted = 1, f.DeletedDate = GETUTCDATE(), f.DeletedBy = :user_id
            FROM dbo.[Form] f
            INNER JOIN dbo.[Event] e ON e.EventID = f.EventID
            WHERE e.Name = :event_name AND e.CompanyID = :company_id
              AND f.IsDeleted = 0;

            UPDATE ec SET ec.IsDeleted = 1, ec.DeletedDate = GETUTCDATE(), ec.DeletedBy = :user_id
            FROM dbo.EventCompany ec
            INNER JOIN dbo.[Event] e ON e.EventID = ec.EventID
            WHERE e.Name = :event_name AND e.CompanyID = :company_id AND ec.IsDeleted = 0;

            UPDATE e SET e.IsDeleted = 1, e.DeletedDate = GETUTCDATE(), e.DeletedBy = :user_id
            FROM dbo.[Event] e
            WHERE e.Name = :event_name AND e.CompanyID = :company_id AND e.IsDeleted = 0;
            """
        ),
        {
            "event_name": DEMO_EVENT_NAME,
            "company_id": COMPANY_ID,
            "version_comment": VERSION_COMMENT,
            "user_id": SEED_USER_ID,
        },
    )

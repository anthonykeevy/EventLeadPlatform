"""
Form Readiness Service (Story 5.5)
Test threshold checking and publish readiness.
"""
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from models.form import Form
from models.form_submission import FormSubmission
from models.form_test_run import FormTestRun
from models.form_version import FormVersion
from models.company_form_test_config import CompanyFormTestConfig


def get_company_test_config(db: Session, company_id: int) -> tuple[bool, int, bool]:
    """
    Get test threshold config for company.
    Returns (enabled, threshold_value, require_publish_approval). Default (False, 3, False) if not configured.
    """
    row = db.execute(
        select(CompanyFormTestConfig).where(CompanyFormTestConfig.CompanyID == company_id)
    ).scalars().first()

    if not row:
        return False, 3, False
    return (
        bool(row.TestThresholdEnabled),
        int(row.TestThresholdValue or 3),
        bool(getattr(row, "RequirePublishApproval", False)),
    )


def get_test_run_count(db: Session, form_id: int) -> int:
    """
    Count test runs for form: preview submissions + explicit FormTestRun records.
    """
    preview_count = db.execute(
        select(func.count(FormSubmission.FormSubmissionID)).where(
            FormSubmission.FormID == form_id,
            FormSubmission.IsPreview == True,  # noqa: E712
            FormSubmission.IsDeleted == False,  # noqa: E712
        )
    ).scalar() or 0

    explicit_count = db.execute(
        select(func.count(FormTestRun.FormTestRunID)).where(FormTestRun.FormID == form_id)
    ).scalar() or 0

    return int(preview_count) + int(explicit_count)


def check_publish_readiness(
    db: Session,
    form_id: int,
    company_id: int,
) -> dict:
    """
    Check if form meets test threshold for publish.
    Returns dict with canPublish, testRunCount, testThresholdRequired, testRunsNeeded, message.
    """
    enabled, threshold, _ = get_company_test_config(db, company_id)
    count = get_test_run_count(db, form_id)

    if not enabled:
        return {
            "canPublish": True,
            "testRunCount": count,
            "testThresholdRequired": 0,
            "testRunsNeeded": 0,
            "message": "Ready to publish",
        }

    if count >= threshold:
        return {
            "canPublish": True,
            "testRunCount": count,
            "testThresholdRequired": threshold,
            "testRunsNeeded": 0,
            "message": "Ready to publish",
        }

    needed = threshold - count
    return {
        "canPublish": False,
        "testRunCount": count,
        "testThresholdRequired": threshold,
        "testRunsNeeded": needed,
        "message": f"{needed} more test run(s) needed",
    }


def record_test_run(
    db: Session,
    form_id: int,
    user_id: int,
    company_id: int,
) -> None:
    """Record explicit 'Record test run' for form. Gets latest version."""
    form = db.execute(
        select(Form).where(Form.FormID == form_id, Form.IsDeleted == False)
    ).scalar_one_or_none()

    if not form:
        raise ValueError(f"Form not found: {form_id}")

    if form.CompanyID != company_id:
        raise ValueError("Form does not belong to your company")

    version = db.execute(
        select(FormVersion)
        .where(FormVersion.FormID == form_id)
        .order_by(FormVersion.VersionNumber.desc())
    ).scalars().first()

    if not version:
        raise ValueError(f"No form version found for form {form_id}")

    run = FormTestRun(
        FormID=form_id,
        FormVersionID=version.FormVersionID,
        CompanyID=company_id,
        RecordedBy=user_id,
    )
    db.add(run)

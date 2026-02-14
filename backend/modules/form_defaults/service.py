"""
Form Defaults Service — CRUD + Merge Resolver (Story 5.2)
"""
import json
import copy
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from models.global_form_defaults import GlobalFormDefaults
from models.global_form_defaults_version import GlobalFormDefaultsVersion
from models.company_form_defaults import CompanyFormDefaults
from models.company_form_defaults_version import CompanyFormDefaultsVersion
from models.ref.form_defaults_schema_version import FormDefaultsSchemaVersion


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge: override recursively overrides base.
    Nested dicts are merged recursively; lists and scalars are replaced.
    """
    result = copy.deepcopy(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def get_global_defaults(db: Session) -> Optional[GlobalFormDefaults]:
    """Get current active global defaults (single row with IsActive=1)."""
    return db.execute(
        select(GlobalFormDefaults).where(GlobalFormDefaults.IsActive == True)
    ).scalar_one_or_none()


def get_company_defaults(db: Session, company_id: int) -> Optional[CompanyFormDefaults]:
    """Get current effective company defaults (IsActive=1, IsDeleted=0)."""
    return db.execute(
        select(CompanyFormDefaults).where(
            and_(
                CompanyFormDefaults.CompanyID == company_id,
                CompanyFormDefaults.IsActive == True,
                CompanyFormDefaults.IsDeleted == False,
            )
        )
    ).scalar_one_or_none()


def resolve_merged_defaults(db: Session, company_id: int) -> Dict[str, Any]:
    """
    Merge resolver: Global deep-merged with Company overrides.
    Returns merged defaults (theme, globalStyles, canvasSettings, defaultGridLayoutsByComponent).
    """
    global_row = get_global_defaults(db)
    if not global_row:
        raise ValueError("Global form defaults not found. Run migration 039.")

    base = json.loads(global_row.DefaultsJSON)
    company_row = get_company_defaults(db, company_id)
    if not company_row:
        return base

    override = json.loads(company_row.DefaultsJSON)
    return deep_merge(base, override)


def update_global_defaults(
    db: Session,
    defaults: Dict[str, Any],
    user_id: int,
    change_summary: Optional[str] = None,
) -> GlobalFormDefaults:
    """
    Update global defaults. Inserts into Version table, updates main row.
    Requires: only one IsActive row (enforced by DB).
    """
    row = get_global_defaults(db)
    if not row:
        raise ValueError("Global form defaults not found. Run migration 039.")

    defaults_json = json.dumps(defaults)
    version_num = row.VersionNumber + 1

    # Insert version history
    version_row = GlobalFormDefaultsVersion(
        FormDefaultsSchemaVersionID=row.FormDefaultsSchemaVersionID,
        VersionNumber=version_num,
        DefaultsJSON=defaults_json,
        ChangeSummary=change_summary,
        CreatedBy=user_id,
    )
    db.add(version_row)
    db.flush()

    # Update main row
    row.VersionNumber = version_num
    row.DefaultsJSON = defaults_json
    row.UpdatedBy = user_id
    db.commit()
    db.refresh(row)
    return row


def update_company_defaults(
    db: Session,
    company_id: int,
    defaults: Dict[str, Any],
    user_id: int,
    change_summary: Optional[str] = None,
) -> CompanyFormDefaults:
    """
    Create or update company defaults. Inserts into Version table.
    Creates row if none exists.
    """
    schema_version_row = db.execute(
        select(FormDefaultsSchemaVersion).where(FormDefaultsSchemaVersion.SchemaVersion == 1)
    ).scalar_one_or_none()
    if not schema_version_row:
        raise ValueError("Form defaults schema version 1 not found.")

    defaults_json = json.dumps(defaults)
    row = get_company_defaults(db, company_id)

    if row:
        version_num = row.VersionNumber + 1
        version_row = CompanyFormDefaultsVersion(
            CompanyID=company_id,
            FormDefaultsSchemaVersionID=schema_version_row.FormDefaultsSchemaVersionID,
            VersionNumber=version_num,
            DefaultsJSON=defaults_json,
            ChangeSummary=change_summary,
            CreatedBy=user_id,
        )
        db.add(version_row)
        db.flush()
        row.VersionNumber = version_num
        row.DefaultsJSON = defaults_json
        row.UpdatedBy = user_id
    else:
        version_row = CompanyFormDefaultsVersion(
            CompanyID=company_id,
            FormDefaultsSchemaVersionID=schema_version_row.FormDefaultsSchemaVersionID,
            VersionNumber=1,
            DefaultsJSON=defaults_json,
            ChangeSummary=change_summary,
            CreatedBy=user_id,
        )
        db.add(version_row)
        db.flush()
        row = CompanyFormDefaults(
            CompanyID=company_id,
            FormDefaultsSchemaVersionID=schema_version_row.FormDefaultsSchemaVersionID,
            VersionNumber=1,
            DefaultsJSON=defaults_json,
            IsActive=True,
            IsDeleted=False,
            CreatedBy=user_id,
            UpdatedBy=user_id,
        )
        db.add(row)

    db.commit()
    db.refresh(row)
    return row


def get_global_history(db: Session, limit: int = 50) -> List[Tuple[int, str, Optional[str], str, Optional[int]]]:
    """Get global defaults version history. Returns list of (VersionNumber, DefaultsJSON, ChangeSummary, CreatedDate, CreatedBy)."""
    rows = db.execute(
        select(
            GlobalFormDefaultsVersion.VersionNumber,
            GlobalFormDefaultsVersion.DefaultsJSON,
            GlobalFormDefaultsVersion.ChangeSummary,
            GlobalFormDefaultsVersion.CreatedDate,
            GlobalFormDefaultsVersion.CreatedBy,
        )
        .order_by(GlobalFormDefaultsVersion.VersionNumber.desc())
        .limit(limit)
    ).all()
    return rows


def get_company_history(db: Session, company_id: int, limit: int = 50) -> List[Tuple[int, str, Optional[str], str, Optional[int]]]:
    """Get company defaults version history."""
    rows = db.execute(
        select(
            CompanyFormDefaultsVersion.VersionNumber,
            CompanyFormDefaultsVersion.DefaultsJSON,
            CompanyFormDefaultsVersion.ChangeSummary,
            CompanyFormDefaultsVersion.CreatedDate,
            CompanyFormDefaultsVersion.CreatedBy,
        )
        .where(CompanyFormDefaultsVersion.CompanyID == company_id)
        .order_by(CompanyFormDefaultsVersion.VersionNumber.desc())
        .limit(limit)
    ).all()
    return rows

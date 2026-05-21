"""
Form Builder Init Service (Story 5.2 T03)
Resolves context, merges defaults, loads components, builds definition skeleton.
"""
import copy
import json
import uuid
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import select

from models.event import Event
from models.company import Company
from modules.form_builder.component_catalog import resolve_allowed_components
from modules.form_defaults.service import resolve_merged_defaults


def resolve_country_id(db: Session, company_id: int, event_id: int) -> Optional[int]:
    """
    Resolve CountryID from EventID. Fallback to Company.CountryID if Event.CountryID is null.
    Returns None if both are null; raises ValueError if Event not found or company mismatch.
    """
    event = db.execute(
        select(Event).where(
            Event.EventID == event_id,
            Event.CompanyID == company_id,
        )
    ).scalar_one_or_none()
    if not event:
        raise ValueError("Event not found or company mismatch")
    if event.CountryID is not None:
        return event.CountryID
    company = db.execute(
        select(Company).where(Company.CompanyID == company_id)
    ).scalar_one_or_none()
    if not company:
        raise ValueError("Company not found")
    return company.CountryID if company.CountryID is not None else None


def get_allowed_components(
    db: Session,
    company_id: int,
    country_id: Optional[int],
) -> List[Dict[str, Any]]:
    """Thin wrapper over :func:`resolve_allowed_components` for init API shape."""
    catalog = resolve_allowed_components(db, company_id, country_id)
    return [component.to_init_dict() for component in catalog.components]


def filter_default_grid_layouts_by_components(
    merged_defaults: Dict[str, Any],
    allowed_codes: List[str],
) -> Dict[str, Any]:
    """
    Filter defaultGridLayoutsByComponent to only include allowed component codes.
    """
    dgl = merged_defaults.get("globalStyles", {}).get("defaultGridLayoutsByComponent")
    if not dgl or not isinstance(dgl, dict):
        return {}
    return {k: v for k, v in dgl.items() if k in allowed_codes}


def build_init_payload(
    db: Session,
    company_id: int,
    event_id: int,
) -> Dict[str, Any]:
    """
    Build full init payload: context, merged defaults, components, definitionJSON skeleton.
    Raises ValueError for invalid companyId/eventId.
    """
    country_id = resolve_country_id(db, company_id, event_id)
    merged = resolve_merged_defaults(db, company_id)
    components = get_allowed_components(db, company_id, country_id)
    allowed_codes = [c["componentCode"] for c in components]

    dgl = filter_default_grid_layouts_by_components(merged, allowed_codes)
    defaults = {
        "theme": merged.get("theme"),
        "globalStyles": copy.deepcopy(merged.get("globalStyles") or {}),
        "canvasSettings": merged.get("canvasSettings"),
        "defaultGridLayoutsByComponent": dgl,
    }
    if "defaultGridLayoutsByComponent" in defaults["globalStyles"]:
        defaults["globalStyles"]["defaultGridLayoutsByComponent"] = dgl

    page_id = f"page-{uuid.uuid4().hex[:8]}"
    definition_skeleton = {
        "schemaVersion": "1.0",
        "theme": None,
        "globalStyles": None,
        "canvasSettings": None,
        "pages": [{"id": page_id, "title": "Page 1", "components": []}],
        "logic": {"rules": []},
    }

    return {
        "schemaVersion": 1,
        "context": {
            "companyId": company_id,
            "eventId": event_id,
            "countryId": country_id,
        },
        "defaults": defaults,
        "components": components,
        "definitionJSON": definition_skeleton,
    }

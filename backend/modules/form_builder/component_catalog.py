"""Authoritative component catalog resolver (Story 6.5c).

Single source of truth for which component types exist for a given
``CompanyID`` + ``CountryID``. Consumed by form-builder init, Form AI
Blocks A/F/I, and the semantic validator.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import text
from sqlalchemy.orm import Session

from modules.form_ai.compiler import ALWAYS_FULL_WIDTH_TYPES

# Width-class vocabulary aligned with migration 057 snapshot baseline.
_WIDTH_CLASSES_BY_TYPE: Dict[str, List[str]] = {
    "text": ["compact", "half", "full"],
    "first-name": ["half", "full"],
    "last-name": ["half", "full"],
    "email": ["compact", "half", "full"],
    "phone": ["compact", "half", "full"],
    "number": ["compact", "half", "full"],
    "date": ["compact", "half", "full"],
    "address": ["full"],
    "address-lookup-au": ["full"],
    "url": ["half", "full"],
    "textarea": ["half", "full"],
    "dropdown": ["compact", "half", "full"],
    "select": ["compact", "half", "full"],
    "checkbox": ["half", "full"],
    "radio": ["half", "full"],
    "rating": ["half", "full"],
    "file-upload": ["full"],
    "terms": ["full"],
    "submit-button": ["compact", "half"],
    "header": ["full"],
    "paragraph": ["full"],
    "divider": ["full"],
}

_DEFAULT_WIDTH_CLASSES = ["compact", "half", "full"]


def width_classes_for(component_code: str) -> List[str]:
    """Return allowed widthIntent hints for a component type."""
    if component_code in ALWAYS_FULL_WIDTH_TYPES:
        return ["full"]
    return list(_WIDTH_CLASSES_BY_TYPE.get(component_code, _DEFAULT_WIDTH_CLASSES))


@dataclass(frozen=True)
class ResolvedComponent:
    """One row from the resolved catalog."""

    component_code: str
    display_name: str
    category: Optional[str]
    sort_order: int
    properties_schema: Optional[Dict[str, Any]]
    structure: Optional[Dict[str, Any]]
    default_grid_layout_vertical: Optional[Dict[str, Any]]
    default_grid_layout_horizontal: Optional[Dict[str, Any]]
    validation_config: Optional[Dict[str, Any]]

    @property
    def width_classes(self) -> List[str]:
        return width_classes_for(self.component_code)

    def to_init_dict(self) -> Dict[str, Any]:
        return {
            "componentCode": self.component_code,
            "displayName": self.display_name,
            "category": self.category,
            "sortOrder": self.sort_order,
            "propertiesSchema": self.properties_schema,
            "structure": self.structure,
            "defaultGridLayoutVertical": self.default_grid_layout_vertical,
            "defaultGridLayoutHorizontal": self.default_grid_layout_horizontal,
            "validationConfig": self.validation_config,
        }


@dataclass(frozen=True)
class ResolvedComponentCatalog:
    """Resolved catalog for a company + country context."""

    company_id: int
    country_id: Optional[int]
    components: Tuple[ResolvedComponent, ...]

    @property
    def component_codes(self) -> Tuple[str, ...]:
        return tuple(c.component_code for c in self.components)

    def to_capability_json(self) -> Dict[str, Any]:
        """Shape consumed by Block F renderer and semantic validator."""
        return {
            "components": [
                {"type": c.component_code, "widthClasses": c.width_classes}
                for c in self.components
            ],
            "resolvedCountryId": self.country_id,
            "resolvedCompanyId": self.company_id,
            "catalogVersion": "FormBuilderComponent-active-rows",
        }

    def catalog_hash(self) -> str:
        payload = json.dumps(self.to_capability_json(), sort_keys=True, ensure_ascii=True)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def format_allowed_types_fragment(self) -> str:
        codes = ", ".join(self.component_codes)
        return (
            "ALLOWED componentType values for this request (do NOT invent others): "
            f"{codes}\n"
        )


_CATALOG_QUERY = text(
    """
    SELECT
        fbc.ComponentCode,
        fbc.DisplayName,
        ct.Category,
        fbc.SortOrder,
        fbc.PropertiesSchemaJSON,
        fbc.StructureJSON,
        fbc.DefaultGridLayoutVerticalJSON,
        fbc.DefaultGridLayoutHorizontalJSON,
        fbc.ValidationConfigJSON
    FROM [dbo].[FormBuilderComponent] fbc
    JOIN [ref].[ComponentType] ct ON fbc.ComponentTypeID = ct.ComponentTypeID
    JOIN [ref].[ComponentScope] cs ON fbc.ComponentScopeID = cs.ComponentScopeID
    WHERE fbc.IsActive = 1 AND fbc.IsDeleted = 0
    AND (
        (cs.ScopeCode = 'Global' AND fbc.CountryID IS NULL AND fbc.CompanyID IS NULL)
        OR (cs.ScopeCode = 'Country' AND fbc.CountryID = :country_id AND :country_id IS NOT NULL)
        OR (cs.ScopeCode = 'Company' AND fbc.CompanyID = :company_id)
    )
    AND (
        :requires_offline_capable = 0
        OR ISNULL(ct.RequiresNetwork, 0) = 0
    )
    ORDER BY fbc.SortOrder, fbc.DisplayName
    """
)


def resolve_allowed_components(
    db: Session,
    company_id: int,
    country_id: Optional[int],
    *,
    requires_offline_capable: bool = False,
) -> ResolvedComponentCatalog:
    """Load components: Global ∪ Country(country_id) ∪ Company(company_id).

    When ``requires_offline_capable`` is true, exclude rows whose
    ``ref.ComponentType.RequiresNetwork`` is set (Story 6.5d EDF offline rule).
    """
    rows = db.execute(
        _CATALOG_QUERY,
        {
            "company_id": company_id,
            "country_id": country_id,
            "requires_offline_capable": 1 if requires_offline_capable else 0,
        },
    ).fetchall()

    components: List[ResolvedComponent] = []
    for row in rows:
        components.append(
            ResolvedComponent(
                component_code=row.ComponentCode,
                display_name=row.DisplayName,
                category=row.Category,
                sort_order=row.SortOrder or 0,
                properties_schema=(
                    json.loads(row.PropertiesSchemaJSON)
                    if row.PropertiesSchemaJSON
                    else None
                ),
                structure=(
                    json.loads(row.StructureJSON) if row.StructureJSON else None
                ),
                default_grid_layout_vertical=(
                    json.loads(row.DefaultGridLayoutVerticalJSON)
                    if row.DefaultGridLayoutVerticalJSON
                    else None
                ),
                default_grid_layout_horizontal=(
                    json.loads(row.DefaultGridLayoutHorizontalJSON)
                    if row.DefaultGridLayoutHorizontalJSON
                    else None
                ),
                validation_config=(
                    json.loads(row.ValidationConfigJSON)
                    if row.ValidationConfigJSON
                    else None
                ),
            )
        )

    return ResolvedComponentCatalog(
        company_id=company_id,
        country_id=country_id,
        components=tuple(components),
    )

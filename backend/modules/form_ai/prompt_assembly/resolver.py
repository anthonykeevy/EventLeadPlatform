"""Resolver for the Story 6.5b Prompt Assembly Registry.

Picks the active ``PromptAssemblyRegistryVersion`` for a given registry
code and, for each of its ``PromptSection`` rows, the winning
``PromptSectionVariant`` to use for the request.

Variant selection rule (6.5b in-scope):
  * Match ``VariantCode == axis_value`` for the section's runtime axis
    (Block C: ``brand_posture``; all other in-scope sections have only
    a ``DEFAULT`` variant).
  * Fall back to ``IsDefault = 1`` when no axis match is found
    (this covers cases like ``brand_posture = None``, an unrecognised
    posture string, or future audit hardening).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Mapping, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.config.prompt_assembly_registry import PromptAssemblyRegistry
from models.config.prompt_assembly_registry_version import (
    PromptAssemblyRegistryVersion,
)
from models.config.prompt_section import PromptSection
from models.config.prompt_section_variant import PromptSectionVariant


REGISTRY_CODE_FORM_AI_V1 = "FORM_AI_V1"

# In-scope axis mapping for 6.5b. Section axes added in 6.5c / 6.5d
# (locale -> D, clarification -> E) plug into the same shape.
_SECTION_AXIS = {
    "C": "brand_posture",
    "E1": "audience_locale",
    "E2": "form_purpose",
    "E3": "respondent_type",
}


@dataclass(frozen=True)
class ResolvedSection:
    """One row from the resolved assembly: section + winning variant."""

    section_code: str  # e.g. 'A', 'B', 'C', 'G', 'I'
    section_id: int
    sort_order: int
    data_structure_type: str  # 'Prose' | 'Json' | 'Snapshot' | 'Refs'
    heading: Optional[str]
    variant_id: int
    variant_code: str
    snippet: str


@dataclass(frozen=True)
class ResolvedAssembly:
    """Result of resolving an active registry version for a request."""

    registry_code: str
    registry_id: int
    registry_version_id: int
    version_number: int
    sections: List[ResolvedSection]

    @property
    def variant_ids(self) -> Dict[str, int]:
        """Per-section variant ID map keyed by SectionCode (audit payload)."""
        return {s.section_code: s.variant_id for s in self.sections}


def _resolve_active_version(
    db: Session, registry_code: str
) -> Optional[Mapping]:
    """Pick the highest active ``PromptAssemblyRegistryVersion`` for a registry.

    Uses the SQLAlchemy ORM expression API so the same query runs on
    SQL Server (production / Test) and SQLite (CI fixture in
    ``test_story_6_5b_registry_resolver.py``) without dialect drift.
    """
    stmt = (
        select(
            PromptAssemblyRegistry.PromptAssemblyRegistryID.label("RegistryID"),
            PromptAssemblyRegistryVersion.PromptAssemblyRegistryVersionID.label(
                "VersionID"
            ),
            PromptAssemblyRegistryVersion.VersionNumber.label("VersionNumber"),
        )
        .join(
            PromptAssemblyRegistryVersion,
            PromptAssemblyRegistryVersion.PromptAssemblyRegistryID
            == PromptAssemblyRegistry.PromptAssemblyRegistryID,
        )
        .where(
            PromptAssemblyRegistry.Code == registry_code,
            PromptAssemblyRegistry.IsDeleted == False,  # noqa: E712
            PromptAssemblyRegistry.IsActive == True,  # noqa: E712
            PromptAssemblyRegistryVersion.IsActive == True,  # noqa: E712
            PromptAssemblyRegistryVersion.IsDeleted == False,  # noqa: E712
        )
        .order_by(
            PromptAssemblyRegistryVersion.VersionNumber.desc(),
            PromptAssemblyRegistryVersion.PromptAssemblyRegistryVersionID.desc(),
        )
        .limit(1)
    )
    return db.execute(stmt).mappings().first()


def _load_sections_with_variants(db: Session, version_id: int) -> List[Mapping]:
    """Load every active section + variant under a version.

    Returns one row per (section, variant). Section rows with no active
    variant are still returned (variant fields NULL) so the caller can
    raise a clean error. Same dialect-portability trade-off as
    ``_resolve_active_version``.
    """
    stmt = (
        select(
            PromptSection.PromptSectionID.label("SectionID"),
            PromptSection.SectionCode.label("SectionCode"),
            PromptSection.SortOrder.label("SortOrder"),
            PromptSection.DataStructureType.label("DataStructureType"),
            PromptSection.Heading.label("Heading"),
            PromptSection.IsRequired.label("IsRequired"),
            PromptSectionVariant.PromptSectionVariantID.label("VariantID"),
            PromptSectionVariant.VariantCode.label("VariantCode"),
            PromptSectionVariant.IsDefault.label("IsDefault"),
            PromptSectionVariant.PromptSnippet.label("PromptSnippet"),
        )
        .join(
            PromptSectionVariant,
            (
                PromptSectionVariant.PromptSectionID
                == PromptSection.PromptSectionID
            )
            & (PromptSectionVariant.IsDeleted == False),  # noqa: E712
            isouter=True,
        )
        .where(
            PromptSection.PromptAssemblyRegistryVersionID == version_id,
            PromptSection.IsDeleted == False,  # noqa: E712
        )
        .order_by(
            PromptSection.SortOrder.asc(),
            PromptSection.PromptSectionID.asc(),
            PromptSectionVariant.PromptSectionVariantID.asc(),
        )
    )
    return list(db.execute(stmt).mappings())


def _pick_variant(
    section_code: str,
    section_id: int,
    section_rows: List[Mapping],
    *,
    brand_posture: Optional[str],
    audience_locale: Optional[str],
    form_purpose: Optional[str] = None,
    respondent_type: Optional[str] = None,
) -> Optional[Mapping]:
    """Pick the winning variant row for a section.

    Selection precedence:
      1. Variant whose VariantCode == runtime axis value (e.g.
         brand_posture for Block C).
      2. Variant marked IsDefault = 1.
      3. None - caller raises if section is required.
    """
    axis = _SECTION_AXIS.get(section_code)
    axis_value: Optional[str] = None
    if axis == "brand_posture" and brand_posture:
        axis_value = brand_posture
    elif axis == "audience_locale" and audience_locale:
        axis_value = audience_locale
    elif axis == "form_purpose" and form_purpose:
        axis_value = form_purpose
    elif axis == "respondent_type" and respondent_type:
        axis_value = respondent_type

    if axis_value:
        for row in section_rows:
            if row["VariantCode"] == axis_value:
                return row

    for row in section_rows:
        if row.get("IsDefault"):
            return row

    return None


def resolve_prompt_assembly(
    db: Session,
    registry_code: str,
    *,
    brand_posture: Optional[str] = None,
    audience_locale: Optional[str] = None,
    form_purpose: Optional[str] = None,
    respondent_type: Optional[str] = None,
) -> ResolvedAssembly:
    """Resolve the active assembly for a registry code.

    Args:
      db: Active SQLAlchemy session bound to the same DB the migrations
        were applied against.
      registry_code: e.g. ``FORM_AI_V1``.
      brand_posture: One of ``local`` / ``heritage`` / ``neutral`` /
        ``transcreate``. Used to pick Block C variant. If ``None`` or
        unrecognised, falls back to the section's IsDefault variant.
        Heritage-without-origin handling is the caller's
        responsibility (existing service.py behaviour collapses
        heritage-without-origin to local; pass ``brand_posture='local'``
        in that case).
      audience_locale: Reserved for 6.5c (Block D registry cutover).
        Currently accepted but ignored by the in-scope resolver.

    Returns:
      ResolvedAssembly with sections in SortOrder.

    Raises:
      LookupError when the registry / active version cannot be found.
      RuntimeError when a required section has no winning variant.
    """
    active = _resolve_active_version(db, registry_code)
    if active is None:
        raise LookupError(
            f"Prompt assembly registry not found or inactive: {registry_code!r}"
        )

    rows = _load_sections_with_variants(db, int(active["VersionID"]))

    # Group variants by section, preserving order from the SQL query.
    section_groups: Dict[int, List[Mapping]] = {}
    section_meta: Dict[int, Mapping] = {}
    for row in rows:
        section_id = int(row["SectionID"])
        if section_id not in section_meta:
            section_meta[section_id] = row
            section_groups[section_id] = []
        if row["VariantID"] is not None:
            section_groups[section_id].append(row)

    # Sort the sections by (SortOrder, SectionID) to mirror SQL ORDER BY.
    sorted_section_ids = sorted(
        section_meta.keys(),
        key=lambda sid: (int(section_meta[sid]["SortOrder"]), sid),
    )

    sections: List[ResolvedSection] = []
    for section_id in sorted_section_ids:
        meta = section_meta[section_id]
        section_code = str(meta["SectionCode"])
        variants = section_groups[section_id]
        winner = _pick_variant(
            section_code,
            section_id,
            variants,
            brand_posture=brand_posture,
            audience_locale=audience_locale,
            form_purpose=form_purpose,
            respondent_type=respondent_type,
        )
        if winner is None:
            if bool(meta["IsRequired"]):
                raise RuntimeError(
                    f"No active variant resolved for required PromptSection "
                    f"(SectionCode={section_code!r}, SectionID={section_id}). "
                    "Ensure migrations 079, 080, and 081 have been applied."
                )
            continue
        sections.append(
            ResolvedSection(
                section_code=section_code,
                section_id=section_id,
                sort_order=int(meta["SortOrder"]),
                data_structure_type=str(meta["DataStructureType"]),
                heading=(str(meta["Heading"]) if meta["Heading"] is not None else None),
                variant_id=int(winner["VariantID"]),
                variant_code=str(winner["VariantCode"]),
                snippet=str(winner["PromptSnippet"]),
            )
        )

    return ResolvedAssembly(
        registry_code=registry_code,
        registry_id=int(active["RegistryID"]),
        registry_version_id=int(active["VersionID"]),
        version_number=int(active["VersionNumber"]),
        sections=sections,
    )

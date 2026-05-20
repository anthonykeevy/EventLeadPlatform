"""Story 6.5b - resolver behaviour tests.

These tests build a minimal in-memory FORM_AI_V1 fixture (one section A
plus a Block C with all four brand-posture variants) directly via the
SQLAlchemy ORM and exercise ``resolve_prompt_assembly`` against an
**isolated SQLite in-memory engine** (so the suite stays runnable
before Tony executes migrations 078-082 on LocalDB / Test, and so CI
doesn't need a live SQL Server). Coverage:

  * Active version selection (only ``IsActive=1`` versions are returned).
  * SortOrder is preserved across resolved sections.
  * Block C variant selection by ``brand_posture`` (each of the four
    canonical postures picks the matching variant).
  * Fallback to ``IsDefault=1`` when no axis match is found.
  * Multi-version registries pick the highest ``VersionNumber`` row.
"""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from common.database import Base
from models.config.prompt_assembly_registry import PromptAssemblyRegistry
from models.config.prompt_assembly_registry_version import (
    PromptAssemblyRegistryVersion,
)
from models.config.prompt_section import PromptSection
from models.config.prompt_section_variant import PromptSectionVariant
from modules.form_ai.prompt_assembly.resolver import (
    REGISTRY_CODE_FORM_AI_V1,
    resolve_prompt_assembly,
)


@pytest.fixture(scope="function")
def registry_db():
    """Isolated SQLite in-memory engine with the registry schema seeded.

    Doesn't depend on ``conftest.test_db`` because that fixture binds
    against LocalDB / Azure SQL when ``DATABASE_URL`` is set, and the
    Story 6.5b registry tables only exist after Tony runs migrations
    078-082 there. SQLite gives us schema parity via SQLAlchemy ORM
    metadata for the resolver-shape tests.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def _attach_schemas(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        for schema in ("ref", "dbo", "config", "audit", "log", "cache"):
            cursor.execute(f"ATTACH DATABASE ':memory:' AS \"{schema}\"")
        cursor.close()
        # Models use ``func.getutcdate()`` (MSSQL builtin) as the
        # server-side default for ``CreatedUtc``. Stub it on SQLite so
        # ORM inserts on the registry tables don't blow up at flush time.
        from datetime import datetime as _dt

        dbapi_conn.create_function(
            "getutcdate", 0, lambda: _dt.utcnow().isoformat(sep=" ", timespec="seconds")
        )

    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


# SQLite + BigInteger PKs don't autoincrement (only ``INTEGER PRIMARY
# KEY`` does on SQLite). The fixture below assigns IDs explicitly via
# these counters so the test seeding stays portable. Production uses
# MSSQL ``BIGINT IDENTITY`` so this divergence is fixture-only.
_ID_COUNTERS = {
    "registry": 0,
    "version": 0,
    "section": 0,
    "variant": 0,
}


def _next_id(kind: str) -> int:
    _ID_COUNTERS[kind] += 1
    return _ID_COUNTERS[kind]


@pytest.fixture(autouse=True)
def _reset_id_counters():
    for key in _ID_COUNTERS:
        _ID_COUNTERS[key] = 0
    yield


# Markers used to distinguish variants without coupling tests to the real
# Story 6.5b prose (those are pinned in test_story_6_5b_equivalence.py).
_BLOCK_A_TEXT = "BLOCK_A__test_text"
_BLOCK_C_LOCAL = "BLOCK_C__local_marker"
_BLOCK_C_HERITAGE = "BLOCK_C__heritage_marker {heritageOrigin}"
_BLOCK_C_NEUTRAL = "BLOCK_C__neutral_marker"
_BLOCK_C_TRANSCREATE = "BLOCK_C__transcreate_marker"


def _seed_registry(
    session,
    *,
    registry_code: str = REGISTRY_CODE_FORM_AI_V1,
    version_active: bool = True,
    version_number: int = 1,
) -> PromptAssemblyRegistryVersion:
    """Seed a single FORM_AI_V1 registry version with Block A + Block C.

    Block A: required, single DEFAULT variant.
    Block C: required, four variants (local/heritage/neutral/transcreate)
    with ``local`` as IsDefault.
    """
    registry = PromptAssemblyRegistry(
        PromptAssemblyRegistryID=_next_id("registry"),
        Code=registry_code,
        Description="Story 6.5b resolver test fixture",
        IsActive=True,
    )
    session.add(registry)
    session.flush()

    version = PromptAssemblyRegistryVersion(
        PromptAssemblyRegistryVersionID=_next_id("version"),
        PromptAssemblyRegistryID=registry.PromptAssemblyRegistryID,
        VersionNumber=version_number,
        IsActive=version_active,
    )
    session.add(version)
    session.flush()

    section_a = PromptSection(
        PromptSectionID=_next_id("section"),
        PromptAssemblyRegistryVersionID=version.PromptAssemblyRegistryVersionID,
        SectionCode="A",
        DisplayName="Role contract",
        SortOrder=10,
        IsRequired=True,
        DataStructureType="Prose",
        Heading=None,
    )
    section_c = PromptSection(
        PromptSectionID=_next_id("section"),
        PromptAssemblyRegistryVersionID=version.PromptAssemblyRegistryVersionID,
        SectionCode="C",
        DisplayName="Brand posture",
        SortOrder=50,
        IsRequired=True,
        DataStructureType="Prose",
        Heading=None,
    )
    session.add_all([section_a, section_c])
    session.flush()

    session.add(
        PromptSectionVariant(
            PromptSectionVariantID=_next_id("variant"),
            PromptSectionID=section_a.PromptSectionID,
            VariantCode="DEFAULT",
            DisplayName="Block A default",
            IsDefault=True,
            PromptSnippet=_BLOCK_A_TEXT,
        )
    )
    session.add_all(
        [
            PromptSectionVariant(
                PromptSectionVariantID=_next_id("variant"),
                PromptSectionID=section_c.PromptSectionID,
                VariantCode="local",
                DisplayName="Block C local",
                IsDefault=True,
                PromptSnippet=_BLOCK_C_LOCAL,
            ),
            PromptSectionVariant(
                PromptSectionVariantID=_next_id("variant"),
                PromptSectionID=section_c.PromptSectionID,
                VariantCode="heritage",
                DisplayName="Block C heritage",
                IsDefault=False,
                PromptSnippet=_BLOCK_C_HERITAGE,
            ),
            PromptSectionVariant(
                PromptSectionVariantID=_next_id("variant"),
                PromptSectionID=section_c.PromptSectionID,
                VariantCode="neutral",
                DisplayName="Block C neutral",
                IsDefault=False,
                PromptSnippet=_BLOCK_C_NEUTRAL,
            ),
            PromptSectionVariant(
                PromptSectionVariantID=_next_id("variant"),
                PromptSectionID=section_c.PromptSectionID,
                VariantCode="transcreate",
                DisplayName="Block C transcreate",
                IsDefault=False,
                PromptSnippet=_BLOCK_C_TRANSCREATE,
            ),
        ]
    )
    session.commit()
    return version


def test_resolver_active_version_returns_sections_in_sort_order(registry_db):
    _seed_registry(registry_db)

    resolved = resolve_prompt_assembly(registry_db, REGISTRY_CODE_FORM_AI_V1)

    section_codes = [s.section_code for s in resolved.sections]
    sort_orders = [s.sort_order for s in resolved.sections]
    assert section_codes == ["A", "C"], section_codes
    assert sort_orders == sorted(sort_orders), sort_orders


def test_resolver_block_c_picks_variant_by_brand_posture(registry_db):
    _seed_registry(registry_db)

    cases = {
        "local": _BLOCK_C_LOCAL,
        "heritage": _BLOCK_C_HERITAGE,
        "neutral": _BLOCK_C_NEUTRAL,
        "transcreate": _BLOCK_C_TRANSCREATE,
    }
    for posture, expected_snippet in cases.items():
        resolved = resolve_prompt_assembly(
            registry_db,
            REGISTRY_CODE_FORM_AI_V1,
            brand_posture=posture,
        )
        block_c = next(s for s in resolved.sections if s.section_code == "C")
        assert block_c.variant_code == posture, (posture, block_c.variant_code)
        assert block_c.snippet == expected_snippet


def test_resolver_block_c_falls_back_to_is_default_when_no_axis_match(registry_db):
    _seed_registry(registry_db)

    resolved = resolve_prompt_assembly(
        registry_db,
        REGISTRY_CODE_FORM_AI_V1,
        brand_posture="unknown_posture_value",
    )
    block_c = next(s for s in resolved.sections if s.section_code == "C")
    assert block_c.variant_code == "local"
    assert block_c.snippet == _BLOCK_C_LOCAL


def test_resolver_block_c_falls_back_to_is_default_when_brand_posture_none(registry_db):
    _seed_registry(registry_db)

    resolved = resolve_prompt_assembly(
        registry_db,
        REGISTRY_CODE_FORM_AI_V1,
        brand_posture=None,
    )
    block_c = next(s for s in resolved.sections if s.section_code == "C")
    assert block_c.variant_code == "local"


def test_resolver_returns_audit_ids(registry_db):
    version = _seed_registry(registry_db)

    resolved = resolve_prompt_assembly(
        registry_db,
        REGISTRY_CODE_FORM_AI_V1,
        brand_posture="heritage",
    )
    assert resolved.registry_code == REGISTRY_CODE_FORM_AI_V1
    assert resolved.registry_version_id == version.PromptAssemblyRegistryVersionID
    assert resolved.version_number == version.VersionNumber
    variant_ids = resolved.variant_ids
    assert set(variant_ids.keys()) == {"A", "C"}
    assert all(isinstance(v, int) and v > 0 for v in variant_ids.values())


def test_resolver_raises_lookup_error_when_registry_inactive(registry_db):
    _seed_registry(registry_db, registry_code="DOES_NOT_EXIST", version_active=False)

    with pytest.raises(LookupError):
        resolve_prompt_assembly(registry_db, REGISTRY_CODE_FORM_AI_V1)


def test_resolver_picks_highest_active_version(registry_db):
    """When multiple versions exist, the active one (highest VersionNumber)
    wins."""
    registry = PromptAssemblyRegistry(
        PromptAssemblyRegistryID=_next_id("registry"),
        Code=REGISTRY_CODE_FORM_AI_V1,
        Description="multi-version fixture",
        IsActive=True,
    )
    registry_db.add(registry)
    registry_db.flush()

    inactive_v1 = PromptAssemblyRegistryVersion(
        PromptAssemblyRegistryVersionID=_next_id("version"),
        PromptAssemblyRegistryID=registry.PromptAssemblyRegistryID,
        VersionNumber=1,
        IsActive=False,
    )
    active_v2 = PromptAssemblyRegistryVersion(
        PromptAssemblyRegistryVersionID=_next_id("version"),
        PromptAssemblyRegistryID=registry.PromptAssemblyRegistryID,
        VersionNumber=2,
        IsActive=True,
    )
    registry_db.add_all([inactive_v1, active_v2])
    registry_db.flush()

    for version, marker in ((inactive_v1, "v1_marker"), (active_v2, "v2_marker")):
        section = PromptSection(
            PromptSectionID=_next_id("section"),
            PromptAssemblyRegistryVersionID=version.PromptAssemblyRegistryVersionID,
            SectionCode="A",
            DisplayName="Role contract",
            SortOrder=10,
            IsRequired=True,
            DataStructureType="Prose",
        )
        registry_db.add(section)
        registry_db.flush()
        registry_db.add(
            PromptSectionVariant(
                PromptSectionVariantID=_next_id("variant"),
                PromptSectionID=section.PromptSectionID,
                VariantCode="DEFAULT",
                IsDefault=True,
                PromptSnippet=marker,
            )
        )
    registry_db.commit()

    resolved = resolve_prompt_assembly(registry_db, REGISTRY_CODE_FORM_AI_V1)
    assert resolved.version_number == 2
    block_a = next(s for s in resolved.sections if s.section_code == "A")
    assert block_a.snippet == "v2_marker"

"""Story 6.5b - migration static-shape sanity checks.

These tests don't run alembic. They verify that each of the five new
migration files (073-077) has:

  * a ``revision`` and ``down_revision`` constant,
  * an ``upgrade()`` and ``downgrade()`` callable,
  * a non-trivial ``downgrade()`` body (not just ``pass``),
  * a chain that links to the expected previous revision,

so a botched migration template never reaches the migration handoff
doc Tony executes.
"""

from __future__ import annotations

import importlib.util
import inspect
import textwrap
from pathlib import Path

import pytest


_MIGRATIONS_DIR = Path(__file__).resolve().parents[1] / "migrations" / "versions"

# (filename, expected revision, expected down_revision)
# Story 6.5b migrations chain off the existing head revision "074"
# (074_seed_platform_owner_onboarding_complete.py). Files were
# renumbered from 073-077 to 078-082 when the SM noticed the original
# numeric collision with the platform-owner seed migrations.
_EXPECTED_CHAIN = [
    (
        "078_story_6_5b_prompt_assembly_registry_schema.py",
        "078",
        "074",
    ),
    (
        "079_story_6_5b_seed_form_ai_v1_profile.py",
        "079",
        "078",
    ),
    (
        "080_story_6_5b_seed_variants_a_b_c_i.py",
        "080",
        "079",
    ),
    (
        "081_story_6_5b_seed_block_g_context_pack.py",
        "081",
        "080",
    ),
    (
        "082_story_6_5b_generation_run_assembly_audit.py",
        "082",
        "081",
    ),
]


def _load_migration(name: str):
    path = _MIGRATIONS_DIR / name
    assert path.exists(), f"migration file missing: {name}"
    spec = importlib.util.spec_from_file_location(
        f"_test_migration_{path.stem}", path
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("filename,expected_revision,expected_down", _EXPECTED_CHAIN)
def test_migration_has_revision_and_down_revision(
    filename: str,
    expected_revision: str,
    expected_down: str | None,
) -> None:
    module = _load_migration(filename)

    revision = getattr(module, "revision", None)
    down_revision = getattr(module, "down_revision", None)
    assert isinstance(revision, str) and revision, (
        f"{filename}: ``revision`` must be a non-empty str."
    )
    assert revision == expected_revision, (
        f"{filename}: ``revision`` = {revision!r}, expected "
        f"{expected_revision!r}."
    )
    assert down_revision is not None and str(down_revision), (
        f"{filename}: ``down_revision`` must be set so alembic can chain."
    )
    if expected_down is not None:
        assert down_revision == expected_down, (
            f"{filename}: ``down_revision`` = {down_revision!r}, expected "
            f"{expected_down!r}."
        )


@pytest.mark.parametrize("filename,expected_revision,expected_down", _EXPECTED_CHAIN)
def test_migration_has_callable_upgrade_and_downgrade(
    filename: str,
    expected_revision: str,
    expected_down: str | None,
) -> None:
    module = _load_migration(filename)

    upgrade = getattr(module, "upgrade", None)
    downgrade = getattr(module, "downgrade", None)
    assert callable(upgrade), f"{filename}: missing ``upgrade()``."
    assert callable(downgrade), f"{filename}: missing ``downgrade()``."


@pytest.mark.parametrize("filename,expected_revision,expected_down", _EXPECTED_CHAIN)
def test_migration_downgrade_is_not_a_no_op(
    filename: str,
    expected_revision: str,
    expected_down: str | None,
) -> None:
    """Story 6.5b migrations all need working rollbacks: 073 drops tables,
    074-076 delete seeded rows, 077 drops audit columns + FK. A
    ``pass``/empty/comment-only body is never correct."""
    module = _load_migration(filename)

    downgrade = getattr(module, "downgrade")
    body = textwrap.dedent(inspect.getsource(downgrade))
    body_lines = [
        line.strip()
        for line in body.splitlines()
        if line.strip()
        and not line.strip().startswith("#")
        and not line.strip().startswith('"""')
        and not line.strip().startswith("'''")
    ]
    body_lines = [l for l in body_lines if not l.startswith("def ")]

    assert body_lines, f"{filename}: ``downgrade()`` body is empty."
    if len(body_lines) == 1 and body_lines[0] == "pass":
        pytest.fail(
            f"{filename}: ``downgrade()`` is a single ``pass`` - migrations "
            "must be reversible."
        )


def test_migration_chain_links_in_order():
    """Story 6.5b migrations must form a strict 073->074->075->076->077
    chain so ``alembic upgrade head`` runs them in order."""
    chain = []
    for filename, _expected_rev, _expected_down in _EXPECTED_CHAIN:
        module = _load_migration(filename)
        chain.append((module.revision, module.down_revision))

    for i in range(1, len(chain)):
        rev, down = chain[i]
        prev_rev, _ = chain[i - 1]
        assert down == prev_rev, (
            f"chain break at {chain[i]}: expected down_revision={prev_rev!r}, "
            f"got {down!r}."
        )

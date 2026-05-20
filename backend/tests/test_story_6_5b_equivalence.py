"""Story 6.5b - prompt-assembly equivalence tests.

These tests pin the in-code source-of-truth for the registry seed
(``canonical_seeds.py``) and assert that ``_build_initial_messages``
keeps producing the legacy literal blocks A / B / C / G / I when given
a synthetic ``RenderedAssembly`` carrying the canonical seeds. The
byte-for-byte AC-19 sign-off lives in
``backend/scripts/story_6_5b_prompt_equivalence_diff.py``; this test is
the **fast** structural guardrail that runs in CI on every commit and
catches whitespace / phrase drift.

Coverage:

  * Stable per-block marker phrases reach the assembled system message
    (one assertion per A/B/C/G/I block).
  * Block C heritage variant substitutes ``{heritageOrigin}`` correctly
    when called via the registry path.
  * No code path reads ``docs/stories/STORY-6.2-AI-CONTEXT-PACK.md`` from
    disk during prompt assembly (file-read monkeypatch).
  * Migration 075 / 076 prose matches ``canonical_seeds.py`` byte-for-byte
    (the AC-19 hash gate).
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path

import pytest

from modules.form_ai import service
from modules.form_ai.prompt_assembly import (
    REGISTRY_CODE_FORM_AI_V1,
    RenderedAssembly,
)
from modules.form_ai.prompt_assembly import canonical_seeds as seeds


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_migration(path: Path):
    """Import a migration module by file path (Alembic versions don't share
    a parent package, so importlib gets us a clean module without
    hijacking sys.path)."""
    spec = importlib.util.spec_from_file_location(
        f"_test_migration_{path.stem}", path
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _migrations_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "migrations" / "versions"


def _build_canonical_assembly(
    *,
    brand_posture: str = "local",
    heritage_origin: str = "",
) -> RenderedAssembly:
    """Build a RenderedAssembly using canonical seeds (mirrors the no-DB
    fallback). The ``brand_posture`` selects which Block C variant the
    fixture exposes."""
    block_c_variants = {
        "local": seeds.BLOCK_C_LOCAL,
        "heritage": seeds.BLOCK_C_HERITAGE.format(heritageOrigin=heritage_origin),
        "neutral": seeds.BLOCK_C_NEUTRAL,
        "transcreate": seeds.BLOCK_C_TRANSCREATE,
    }
    block_c = block_c_variants.get(brand_posture, seeds.BLOCK_C_LOCAL)
    block_g = (
        "## Story 6.2 AI Context Pack\n\n"
        "(Block G fixture - real prose lives in migration 081.)\n"
    )
    return RenderedAssembly(
        registry_code=REGISTRY_CODE_FORM_AI_V1,
        registry_version_id=1,
        version_number=1,
        sections={
            "A": seeds.BLOCK_A_DEFAULT,
            "B": seeds.BLOCK_B_DEFAULT,
            "C": block_c,
            "G": block_g,
            "I": seeds.BLOCK_I_DEFAULT,
        },
        variant_ids={"A": 1, "B": 2, "C": 3, "G": 4, "I": 5},
    )


# ---------------------------------------------------------------------------
# Stable marker phrases per block (sample 4-6 per AC-19 §step 7)
# ---------------------------------------------------------------------------


_BLOCK_A_MARKERS = [
    "You generate an EventLead semantic form plan for Story 6.3.1.",
    "Output a single JSON object only. No markdown or prose.",
    "Return FormSemanticPlan only;",
    "do not output any coordinates",
]

_BLOCK_B_MARKERS = [
    "CONSENT & LEGAL ACKNOWLEDGEMENTS",
    "Marketing consent",
    "company-managed terms",
]

_BLOCK_I_MARKERS = [
    "REQUIRED ROOT KEYS",
    'semanticPlanVersion: must be the string "1.0"',
    "EACH COMPONENT (object):",
    'widthIntent: one of "compact" | "half" | "full"',
    "validationIntent: an OBJECT (not an array)",
    "Use only Story 6.2/6.3.1 supported component catalog",
]

_BLOCK_C_LOCAL_MARKERS = [
    "Brand posture: local.",
    "Match copy voice to the resolved audience locale.",
]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_assembly_carries_block_a_marker_phrases():
    rendered = _build_canonical_assembly()

    messages = service._build_initial_messages(
        prompt="dummy",
        runtime_context=None,
        rendered_assembly=rendered,
    )
    system_body = messages[0]["content"]
    for marker in _BLOCK_A_MARKERS:
        assert marker in system_body, marker


def test_assembly_carries_block_b_marker_phrases():
    rendered = _build_canonical_assembly()

    messages = service._build_initial_messages(
        prompt="dummy",
        runtime_context=None,
        rendered_assembly=rendered,
    )
    system_body = messages[0]["content"]
    for marker in _BLOCK_B_MARKERS:
        assert marker in system_body, marker


def test_assembly_carries_block_i_marker_phrases():
    rendered = _build_canonical_assembly()

    messages = service._build_initial_messages(
        prompt="dummy",
        runtime_context=None,
        rendered_assembly=rendered,
    )
    system_body = messages[0]["content"]
    for marker in _BLOCK_I_MARKERS:
        assert marker in system_body, marker


def test_assembly_carries_block_c_local_marker_phrases():
    rendered = _build_canonical_assembly(brand_posture="local")

    messages = service._build_initial_messages(
        prompt="dummy",
        runtime_context=None,
        brand_posture="local",
        rendered_assembly=rendered,
    )
    system_body = messages[0]["content"]
    for marker in _BLOCK_C_LOCAL_MARKERS:
        assert marker in system_body, marker


def test_assembly_substitutes_heritage_origin_in_block_c():
    rendered = _build_canonical_assembly(
        brand_posture="heritage",
        heritage_origin="Australia",
    )

    messages = service._build_initial_messages(
        prompt="dummy",
        runtime_context=None,
        brand_posture="heritage",
        brand_heritage_origin="Australia",
        rendered_assembly=rendered,
    )
    system_body = messages[0]["content"]
    assert "{heritageOrigin}" not in system_body
    assert "Australia brand heritage" in system_body


def test_assembly_does_not_read_context_pack_from_disk(monkeypatch):
    """Closes R6: the assembled prompt must not open the on-disk
    ``STORY-6.2-AI-CONTEXT-PACK.md`` file at any point."""
    forbidden_pattern = re.compile(r"STORY-6\.2-AI-CONTEXT-PACK\.md")
    real_open = Path.open

    def _guard(self: Path, *args, **kwargs):
        if forbidden_pattern.search(str(self)):
            raise AssertionError(
                f"Story 6.5b regression: prompt assembly opened {self} "
                "from disk. Block G must come from the registry."
            )
        return real_open(self, *args, **kwargs)

    monkeypatch.setattr(Path, "open", _guard, raising=True)

    rendered = _build_canonical_assembly()
    messages = service._build_initial_messages(
        prompt="dummy",
        runtime_context=None,
        rendered_assembly=rendered,
    )
    assert "## Story 6.2 AI Context Pack" in messages[0]["content"]


def test_canonical_seeds_match_migration_075_byte_for_byte():
    """Migration 075 inlines Block A / B / I / C-* prose as Python literals
    (Alembic migrations must be self-contained). This test is the
    AC-19 fingerprint guardrail: any drift between the canonical seeds
    and the migration literals fails fast in CI before reaching UAT."""
    migration_path = _migrations_dir() / "080_story_6_5b_seed_variants_a_b_c_i.py"
    module = _load_migration(migration_path)

    expected_constants = {
        "BLOCK_A_DEFAULT": seeds.BLOCK_A_DEFAULT,
        "BLOCK_B_DEFAULT": seeds.BLOCK_B_DEFAULT,
        "BLOCK_I_DEFAULT": seeds.BLOCK_I_DEFAULT,
        "BLOCK_C_LOCAL": seeds.BLOCK_C_LOCAL,
        "BLOCK_C_HERITAGE": seeds.BLOCK_C_HERITAGE,
        "BLOCK_C_NEUTRAL": seeds.BLOCK_C_NEUTRAL,
        "BLOCK_C_TRANSCREATE": seeds.BLOCK_C_TRANSCREATE,
    }
    for name, expected in expected_constants.items():
        actual = getattr(module, name, None)
        assert actual is not None, f"migration 080 missing constant {name!r}"
        assert actual == expected, (
            f"migration 080 {name} drift: "
            f"sha256(canonical)={hashlib.sha256(expected.encode()).hexdigest()} "
            f"vs sha256(migration)={hashlib.sha256(actual.encode()).hexdigest()}"
        )


def test_block_g_migration_081_does_not_read_context_pack_at_runtime():
    """Migration 081 must inline Block G prose as a Python literal rather
    than reading ``STORY-6.2-AI-CONTEXT-PACK.md`` at upgrade time. The
    file-read at migration *generation* time is fine; the migration
    *body* must be self-contained so older Alembic checkouts and
    deploy targets that don't ship the docs folder still upgrade
    cleanly. Closes R6.

    The check inspects only **executable** lines (Python source minus
    comments and docstrings) so that "how the content was derived"
    notes in module-level comments are still allowed.
    """
    import ast

    migration_path = _migrations_dir() / "081_story_6_5b_seed_block_g_context_pack.py"
    source = migration_path.read_text(encoding="utf-8")

    tree = ast.parse(source)
    string_constants: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            string_constants.append(node.value)

    # ``ast.unparse`` re-emits the AST without comments; for the
    # forbidden-call check that's what we want. We still allow the
    # forbidden tokens *inside* string constants (the inlined prose
    # itself reproduces JSON examples and the trim-marker phrase from
    # the source markdown).
    code_only = ast.unparse(tree)

    forbidden_calls = (
        "Path(__file__)",
        "open(",
        ".read_text(",
    )
    for needle in forbidden_calls:
        if needle in code_only:
            # Confirm it's not just inside a string constant (inlined
            # prose from the original markdown could legitimately mention
            # ``open()`` etc.).
            in_string_only = all(
                needle in s for s in string_constants if needle in s
            ) and any(needle in s for s in string_constants)
            if not in_string_only:
                pytest.fail(
                    f"migration 081 still calls {needle!r} at upgrade time - "
                    "Block G must be an inlined Python literal so the "
                    "migration is self-contained."
                )

    # Belt-and-braces: filename references inside file-handle-style calls
    # only. ``STORY-6.2-AI-CONTEXT-PACK.md`` is allowed to appear inside
    # the seeded ``Description`` SQL literal (audit trail) and inside
    # comments; what's forbidden is a file open / read_text / Path build
    # at runtime that re-introduces R6.
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func_repr = ast.unparse(node.func) if hasattr(ast, "unparse") else ""
            if func_repr in {"open", "Path", "pathlib.Path"}:
                args_repr = ast.unparse(node)
                if "STORY-6.2-AI-CONTEXT-PACK.md" in args_repr:
                    pytest.fail(
                        "migration 081 opens STORY-6.2-AI-CONTEXT-PACK.md at "
                        f"upgrade time: {args_repr!r}"
                    )

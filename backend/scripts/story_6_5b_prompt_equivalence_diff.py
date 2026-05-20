"""Story 6.5b - prompt-equivalence diff helper (AC-19 gate artefact).

Runs **post-Story-6.5b** ``_build_initial_messages`` (registry path) and
**pre-Story-6.5b** ``_build_initial_messages`` (literal path, kept inline
in this script as ``_build_initial_messages_legacy``) for the same set
of inputs and emits a per-block (A..I) diff report. The report is the
artefact Tony signs off on before flipping PR #104 from Draft to Ready.

Usage::

    python backend/scripts/story_6_5b_prompt_equivalence_diff.py \\
        --postures local heritage neutral transcreate \\
        --output docs/stories/STORY-6.5b-PROMPT-EQUIVALENCE-DIFF.md

Default invocation runs all four canonical brand postures with
``audience_locale='AU'`` and a synthetic prompt; the report is written to
``docs/stories/STORY-6.5b-PROMPT-EQUIVALENCE-DIFF.md``.

The script does **not** require a live database. It uses the
canonical-seed fallback (``modules.form_ai.prompt_assembly.canonical_seeds``)
and the migration-inlined Block G prose
(``backend/migrations/versions/081_story_6_5b_seed_block_g_context_pack.py::BLOCK_G_DEFAULT_TRIMMED``).

Verdicts per block:
  * IDENTICAL    -> bytes match.
  * WHITESPACE   -> only whitespace differs (newline count, trailing
                    spaces).
  * CONTENT      -> a real character-level delta. The block fails the
                    AC-19 gate.
"""

from __future__ import annotations

import argparse
import difflib
import importlib.util
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPO_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from modules.form_ai import service  # noqa: E402
from modules.form_ai.prompt_assembly import (  # noqa: E402
    REGISTRY_CODE_FORM_AI_V1,
    RenderedAssembly,
)
from modules.form_ai.prompt_assembly import canonical_seeds as seeds  # noqa: E402


# ---------------------------------------------------------------------------
# Legacy ``_build_initial_messages`` (pre-Story-6.5b) - inlined here so the
# diff script doesn't depend on git history. The legacy function lived at
# ``backend/modules/form_ai/service.py`` before commit ``cb339ed``. Block G
# was sourced from ``_load_context_pack()`` -> on-disk MD file; this helper
# instead injects a caller-supplied ``context_pack`` so the diff is
# deterministic.
# ---------------------------------------------------------------------------


_LEGACY_BLOCK_A = (
    "Output a single JSON object only. No markdown or prose.\n"
    "Return FormSemanticPlan only; do not output any coordinates, "
    "pixel widths, x/y positions, style blocks, or final DefinitionJSON.\n"
)


_LEGACY_BLOCK_I = (
    "REQUIRED ROOT KEYS (exact, case-sensitive):\n"
    '  - semanticPlanVersion: must be the string "1.0" (do NOT use the story number).\n'
    "  - formId: short slug or id (string).\n"
    "  - title: form title (string).\n"
    "  - components: array of component intents (see below).\n"
    "Do NOT add any other root keys.\n"
    "\n"
    "EACH COMPONENT (object):\n"
    "  - componentType (required), label, placeholder, helpText, section, rowGroup,\n"
    '  - widthIntent: one of "compact" | "half" | "full".\n'
    "    This is a HINT, not a final width. The deterministic compiler picks\n"
    "    the actual pixel width from a per-type tier table and may shrink the\n"
    "    component further (or wrap it onto its own row) so the layout fits\n"
    '    the canvas. Treat widthIntent as a maximum cap: use "compact" when\n'
    '    the field\'s content is short (e.g. zip, age, state code), "full"\n'
    "    only when you genuinely want the field to span the row.\n"
    "    Use rowGroup to indicate which fields you'd like packed side-by-side;\n"
    "    the compiler decides whether they actually fit.\n"
    "  - options: array of {label,value} for dropdown/radio,\n"
    "  - validationIntent: an OBJECT (not an array) with any of these boolean/number keys:\n"
    "      required, email, phone, url, minLength, maxLength, min, max, pattern.\n"
    '    Example: "validationIntent": { "required": true, "email": true }.\n'
    '    NEVER emit validationIntent as a list of strings (e.g. ["required","email"]).\n'
    "\n"
    "Use only Story 6.2/6.3.1 supported component catalog and single-page constraints.\n\n"
)


def _legacy_render_brand_posture_block(
    posture: Optional[str],
    origin: Optional[str],
) -> str:
    """Mirror of pre-6.5b ``service.py::_render_brand_posture_block`` (commit
    cb339ed). Heritage-without-origin and unrecognised postures collapse
    to ``local`` (matches ``service.py`` fallback)."""
    norm = (posture or "").strip().lower() or None
    origin_clean = (origin or "").strip()
    if norm == "heritage" and origin_clean:
        return (
            "Brand posture: heritage. Audience locale still controls field shape "
            f"and compliance; copy voice may lightly reflect {origin_clean} brand heritage."
        )
    if norm == "neutral":
        return "Brand posture: neutral. Use market-neutral voice; audience locale still controls field shape and compliance."
    if norm == "transcreate":
        return "Brand posture: transcreate. Adapt copy idiomatically for the audience locale while preserving the user's intent."
    return "Brand posture: local. Match copy voice to the resolved audience locale."


def _build_initial_messages_legacy(
    *,
    prompt: str,
    context_pack: str,
    runtime_context: Optional[Dict] = None,
    capability_snapshot_json: Optional[Dict] = None,
    audience_locale: Optional[str] = "AU",
    brand_posture: Optional[str] = None,
    brand_heritage_origin: Optional[str] = None,
    db_session=None,
) -> List[Dict[str, str]]:
    """Pre-6.5b ``service._build_initial_messages``, inlined.

    Calls the still-current helpers for D / F / runtime-context / locale
    blocks (those didn't change in 6.5b); reproduces the literal Block A,
    Block B (via ``_active_consent_guidance_block``), Block C, Block G
    (trimmed via ``_trim_context_pack_for_prompt``), and Block I content
    that ``_build_initial_messages`` *used to* concatenate inline.
    """
    runtime_context_block = service._build_runtime_context_block(runtime_context)
    capability_block = service._build_capability_prompt_block(capability_snapshot_json)
    locale_block = service._assemble_locale_block(audience_locale or "AU", brand_posture, db_session)
    brand_posture_block = _legacy_render_brand_posture_block(brand_posture, brand_heritage_origin)
    prompt_context_pack = service._trim_context_pack_for_prompt(context_pack)

    layout_mode = service.resolve_layout_mode(runtime_context)
    layout_mode_block = (
        service._HORIZONTAL_STACKED_LAYOUT_NUDGE
        if layout_mode == service.LAYOUT_MODE_HORIZONTAL_STACKED
        else ""
    )

    system_body = (
        _LEGACY_BLOCK_A
        + "\n"
        + service._active_consent_guidance_block()
        + (layout_mode_block + "\n" if layout_mode_block else "")
        + "\n"
        + _LEGACY_BLOCK_I
        + (capability_block + "\n\n" if capability_block else "")
        + f"{prompt_context_pack}"
        + "\n\n## LOCALE AND BRAND POSTURE\n"
        + locale_block
        + "\n"
        + brand_posture_block
        + ("\n\n" + runtime_context_block if runtime_context_block else "")
    )
    return [
        {"role": "system", "content": system_body},
        {
            "role": "user",
            "content": (
                "Generate a semantic plan for this request.\n"
                f"Prompt: {prompt}\n"
                "Return only valid JSON."
            ),
        },
    ]


# ---------------------------------------------------------------------------
# Block-by-block extraction
# ---------------------------------------------------------------------------


# Stable header phrases that uniquely identify each block in the legacy
# system body. Used to slice both the legacy and new outputs into per-block
# pieces. Order matches the *current emission order* in
# ``_build_initial_messages``.
_BLOCK_MARKERS: List[Tuple[str, str]] = [
    ("A", "Output a single JSON object only. No markdown or prose."),
    ("B", "## CONSENT & LEGAL ACKNOWLEDGEMENTS"),
    ("I", "REQUIRED ROOT KEYS (exact, case-sensitive):"),
    # Block G seeded prose starts with the trimmed STORY-6.2 H1 (migration 081).
    ("G", "# STORY-6.2 AI Context Pack"),
    ("D_HEADER", "## LOCALE AND BRAND POSTURE"),
    ("C", "Brand posture:"),
]


def _slice_blocks(system_body: str) -> Dict[str, str]:
    """Slice a system body into per-block strings using marker phrases.

    Returns a dict ``{section_code: text}`` covering A/B/I/G/D_HEADER/C.
    The caller can compare same-keyed entries between OLD and NEW.
    """
    indices: Dict[str, int] = {}
    for code, marker in _BLOCK_MARKERS:
        idx = system_body.find(marker)
        if idx >= 0:
            indices[code] = idx

    ordered = sorted(indices.items(), key=lambda kv: kv[1])
    blocks: Dict[str, str] = {}
    for i, (code, start) in enumerate(ordered):
        end = ordered[i + 1][1] if i + 1 < len(ordered) else len(system_body)
        blocks[code] = system_body[start:end]
    return blocks


# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------


def _verdict(old: str, new: str) -> str:
    if old == new:
        return "IDENTICAL"
    if old.replace(" ", "").replace("\n", "") == new.replace(" ", "").replace("\n", ""):
        return "WHITESPACE"
    return "CONTENT"


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------


def _git_head_sha() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL,
        )
        return out.decode().strip()
    except Exception:  # pragma: no cover
        return "unknown"


_SOURCE_CHANGE_LINE: Dict[str, str] = {
    "A": "A: Python literal in `service._build_initial_messages` → `config.PromptSectionVariant` (Block A / ROLE_CONTRACT).",
    "B": "B: `service._active_consent_guidance_block()` → `config.PromptSectionVariant` (Block B / SAFETY).",
    "C": "C: `BRAND_POSTURE_PROMPTS` dict / `_render_brand_posture_block` → four `PromptSectionVariant` rows (Block C).",
    "G": "G: on-disk `STORY-6.2-AI-CONTEXT-PACK.md` via `_load_context_pack()` → `PromptSectionVariant` (Block G / FEW_SHOT, migration 081).",
    "I": "I: Python literal tail in `service._build_initial_messages` → `config.PromptSectionVariant` (Block I / JSON_OUTPUT).",
    "D_HEADER": "D: unchanged this story — `_assemble_locale_block` (not registry-migrated in 6.5b).",
}


def _format_block_panel(code: str, old: str, new: str, verdict: str) -> str:
    icon = {
        "IDENTICAL": "OK",
        "WHITESPACE": "WS",
        "CONTENT": "FAIL",
    }.get(verdict, "??")

    old_stripped = old.rstrip("\n")
    new_stripped = new.rstrip("\n")
    old_len = len(old_stripped)
    new_len = len(new_stripped)

    body_lines: List[str] = [
        f"### Block {code} — verdict: {verdict} [{icon}]",
        "",
        f"**Source change:** {_SOURCE_CHANGE_LINE.get(code, code)}",
        "",
    ]

    if verdict == "IDENTICAL":
        body_lines.append(
            "Bytes are identical between OLD (pre-6.5b literal path) and NEW (post-6.5b registry path)."
        )
    elif verdict == "WHITESPACE":
        body_lines.append(
            "Only whitespace differs between OLD and NEW (newline count / trailing spaces)."
        )
    else:
        body_lines.append("**CONTENT delta** — must be resolved before AC-19 sign-off.")

    body_lines.extend(
        [
            "",
            f"#### OLD (pre-6.5b) — {old_len:,} chars",
            "",
            "```text",
            old_stripped or "(empty — block marker not found in legacy system message)",
            "```",
            "",
            f"#### NEW (post-6.5b registry) — {new_len:,} chars",
            "",
            "```text",
            new_stripped or "(empty — block marker not found in registry system message)",
            "```",
            "",
        ]
    )

    if verdict not in ("IDENTICAL",) and old_stripped and new_stripped:
        diff = "\n".join(
            difflib.unified_diff(
                old_stripped.splitlines(),
                new_stripped.splitlines(),
                fromfile=f"OLD/Block-{code}",
                tofile=f"NEW/Block-{code}",
                lineterm="",
            )
        )
        if diff:
            body_lines.extend(
                [
                    "#### Unified diff",
                    "",
                    "```diff",
                    diff,
                    "```",
                    "",
                ]
            )

    return "\n".join(body_lines)


def _build_rendered_assembly_for(
    *,
    brand_posture: str,
    heritage_origin: str,
    block_g: str,
) -> RenderedAssembly:
    """Build a registry-shape RenderedAssembly using canonical seeds + the
    migration-inlined Block G prose."""
    block_c_variants = {
        "local": seeds.BLOCK_C_LOCAL,
        "heritage": seeds.BLOCK_C_HERITAGE.format(heritageOrigin=heritage_origin),
        "neutral": seeds.BLOCK_C_NEUTRAL,
        "transcreate": seeds.BLOCK_C_TRANSCREATE,
    }
    block_c = block_c_variants.get(brand_posture, seeds.BLOCK_C_LOCAL)
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


def _load_block_g_from_migration() -> str:
    """Import the inlined ``BLOCK_G_DEFAULT_TRIMMED`` constant from the
    seed migration. Avoids reading the markdown file and keeps the diff
    deterministic relative to what's actually committed to the registry
    after Tony runs alembic upgrade head."""
    migration_path = (
        BACKEND_ROOT
        / "migrations"
        / "versions"
        / "081_story_6_5b_seed_block_g_context_pack.py"
    )
    spec = importlib.util.spec_from_file_location(
        "_diff_migration_081", migration_path
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    constant = getattr(module, "BLOCK_G_DEFAULT_TRIMMED", None)
    if not isinstance(constant, str) or not constant.strip():
        raise SystemExit(
            "Migration 081 does not expose a non-empty BLOCK_G_DEFAULT_TRIMMED "
            "constant. Cannot run the equivalence diff."
        )
    return constant


def _legacy_block_g_input() -> str:
    """The pre-6.5b path read ``STORY-6.2-AI-CONTEXT-PACK.md`` from disk
    and trimmed it. The registry now stores that trimmed prose verbatim
    in ``PromptSectionVariant.PromptSnippet`` (migration 081). Re-using
    the migration-inlined trimmed prose here mirrors what the OLD code
    *would have* assembled if the file read had succeeded."""
    return _load_block_g_from_migration()


def run_diff(
    *,
    postures: Iterable[str],
    heritage_origin: str,
    audience_locale: str,
    user_prompt: str,
) -> List[Mapping]:
    """Returns one entry per posture: ``{posture, blocks: {code: verdict}}``."""
    block_g = _load_block_g_from_migration()
    legacy_block_g_input = _legacy_block_g_input()

    rows: List[Mapping] = []
    for posture in postures:
        rendered = _build_rendered_assembly_for(
            brand_posture=posture,
            heritage_origin=heritage_origin,
            block_g=block_g,
        )

        new_messages = service._build_initial_messages(
            prompt=user_prompt,
            runtime_context=None,
            audience_locale=audience_locale,
            brand_posture=posture,
            brand_heritage_origin=heritage_origin if posture == "heritage" else None,
            rendered_assembly=rendered,
        )
        old_messages = _build_initial_messages_legacy(
            prompt=user_prompt,
            context_pack=legacy_block_g_input,
            runtime_context=None,
            audience_locale=audience_locale,
            brand_posture=posture,
            brand_heritage_origin=heritage_origin if posture == "heritage" else None,
            db_session=None,
        )

        new_body = new_messages[0]["content"]
        old_body = old_messages[0]["content"]

        new_blocks = _slice_blocks(new_body)
        old_blocks = _slice_blocks(old_body)

        block_results: Dict[str, Mapping] = {}
        for code, _marker in _BLOCK_MARKERS:
            old_chunk = old_blocks.get(code, "")
            new_chunk = new_blocks.get(code, "")
            verdict = _verdict(old_chunk, new_chunk)
            block_results[code] = {
                "old": old_chunk,
                "new": new_chunk,
                "verdict": verdict,
            }

        rows.append(
            {
                "posture": posture,
                "audience_locale": audience_locale,
                "heritage_origin": heritage_origin if posture == "heritage" else None,
                "user_prompt": user_prompt,
                "blocks": block_results,
                "old_full": old_body,
                "new_full": new_body,
            }
        )
    return rows


def render_report(
    rows: List[Mapping],
    *,
    output_path: Path,
    head_sha: str,
) -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    lines: List[str] = [
        "# Story 6.5b - Prompt Equivalence Diff (AC-19 gate artefact)",
        "",
        f"- Commit: `{head_sha}`",
        f"- Generated: {timestamp}",
        f"- Postures covered: {', '.join(r['posture'] for r in rows)}",
        f"- Audience locale: {rows[0]['audience_locale']}",
        f"- User prompt: `{rows[0]['user_prompt']}`",
        "",
        "## How to read this report",
        "",
        "For each brand posture below, every in-scope block (A, B, C, G, I) shows **two**",
        "fenced panels:",
        "",
        "- **OLD (pre-6.5b)** — system message slice from the legacy literal / file-read path",
        "  (inlined in this script as `_build_initial_messages_legacy`).",
        "- **NEW (post-6.5b)** — same slice from `_build_initial_messages` using the registry",
        "  (`RenderedAssembly` built from `canonical_seeds` + migration-081 Block G prose).",
        "",
        "Character counts are shown in each heading. When verdict is `IDENTICAL`, both panels",
        "contain the same bytes; they are still listed separately so you can review evidence.",
        "",
        "## Summary",
        "",
        "| Posture | A | B | I | G | C |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        cells = [row["posture"]]
        for code in ("A", "B", "I", "G", "C"):
            verdict = row["blocks"].get(code, {}).get("verdict", "MISSING")
            cells.append(verdict)
        lines.append("| " + " | ".join(cells) + " |")

    failures = [
        (r["posture"], code)
        for r in rows
        for code, payload in r["blocks"].items()
        if payload["verdict"] == "CONTENT" and code != "D_HEADER"
    ]
    overall = "PASS" if not failures else "FAIL"
    lines.extend(
        [
            "",
            f"## Top-level verdict: {overall}",
            "",
        ]
    )
    if failures:
        lines.append("Failing (Block, Posture) pairs:")
        lines.extend(f"  - Block {code} for posture `{posture}`" for posture, code in failures)
        lines.append("")

    lines.extend(
        [
            "## Tony sign-off",
            "",
            "- [ ] All in-scope blocks (A, B, C, G, I) report `IDENTICAL` "
            "or `WHITESPACE` for every covered posture.",
            "- [ ] No `CONTENT` deltas remain in the in-scope blocks.",
            "- [ ] D_HEADER is allowed to differ only when `_assemble_locale_block` "
            "output is content-aware (this is expected; Block D moves into the "
            "registry in Story 6.5c).",
            "",
        ]
    )

    for row in rows:
        lines.extend(
            [
                f"## Posture: `{row['posture']}`",
                "",
                "Inputs:",
                f"- audience_locale = `{row['audience_locale']}`",
                f"- brand_heritage_origin = `{row['heritage_origin'] or '(none)'}`",
                f"- user_prompt = `{row['user_prompt']}`",
                "",
            ]
        )
        for code, _marker in _BLOCK_MARKERS:
            payload = row["blocks"].get(code, {})
            old = payload.get("old", "")
            new = payload.get("new", "")
            verdict = payload.get("verdict", "MISSING")
            lines.append(_format_block_panel(code, old, new, verdict))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "--postures",
        nargs="+",
        default=["local", "heritage", "neutral", "transcreate"],
        help="Brand postures to diff (default: all four).",
    )
    parser.add_argument(
        "--heritage-origin",
        default="Australia",
        help="Heritage origin string used when posture=heritage.",
    )
    parser.add_argument(
        "--audience-locale",
        default="AU",
        help="Audience locale code (default: AU).",
    )
    parser.add_argument(
        "--user-prompt",
        default="Build a contact form for an AU tech conference.",
        help="Synthetic user prompt for the diff (default: AU tech conference).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT
        / "docs"
        / "stories"
        / "STORY-6.5b-PROMPT-EQUIVALENCE-DIFF.md",
        help="Where to write the report markdown file.",
    )
    args = parser.parse_args()

    rows = run_diff(
        postures=args.postures,
        heritage_origin=args.heritage_origin,
        audience_locale=args.audience_locale,
        user_prompt=args.user_prompt,
    )
    render_report(rows, output_path=args.output, head_sha=_git_head_sha())

    failures = [
        (r["posture"], code)
        for r in rows
        for code, payload in r["blocks"].items()
        if payload["verdict"] == "CONTENT" and code != "D_HEADER"
    ]
    print(f"Wrote {args.output}")
    if failures:
        print(f"AC-19 verdict: FAIL ({len(failures)} CONTENT deltas)")
        return 1
    print("AC-19 verdict: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

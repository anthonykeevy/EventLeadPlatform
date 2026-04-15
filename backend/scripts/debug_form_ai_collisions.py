"""
Print base vs visual collision pairs for a DefinitionJSON (Story 6.2 form-ai).

Usage (from repo root):
  python backend/scripts/debug_form_ai_collisions.py path/to/file.json

Accepts:
  - Raw definition (pages, canvasSettings, ...)
  - API response shape with definitionJSON and optional runtimeContext
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

# backend/ (parent of scripts/)
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from modules.form_ai.service import (  # noqa: E402
    _build_correction_message,
    _collect_visual_boundary_violations,
    _collect_visual_collisions,
    _enrich_collision_feedback_lines,
    _merge_visual_boundaries,
    _merge_visual_collisions,
)
from modules.form_validate.service import validate_definition_payload  # noqa: E402


def _load_definition(raw: Dict[str, Any]) -> Tuple[Dict[str, Any], Optional[Dict[str, Any]]]:
    if "definitionJSON" in raw and isinstance(raw["definitionJSON"], dict):
        return raw["definitionJSON"], raw.get("runtimeContext")
    if "definition" in raw and isinstance(raw["definition"], dict):
        return raw["definition"], raw.get("runtimeContext")
    if "pages" in raw:
        return raw, None
    raise ValueError("Expected definitionJSON, definition, or pages at top level")


def _print_pairs(title: str, collisions: list) -> None:
    print(f"\n=== {title} ({len(collisions)} pairs) ===")
    for c in collisions:
        print(
            f"  {c.componentAId} <-> {c.componentBId}  "
            f"area={c.overlapArea:.1f}  page={c.pageId}"
        )


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python backend/scripts/debug_form_ai_collisions.py <file.json>", file=sys.stderr)
        sys.exit(1)
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    data = json.loads(text)

    definition, rt_ctx = _load_definition(data)

    base = validate_definition_payload({"definition": definition})
    visual_c = _collect_visual_collisions(definition, rt_ctx)
    merged = _merge_visual_collisions(base, visual_c)
    vb = _collect_visual_boundary_violations(definition, rt_ctx)
    merged2 = _merge_visual_boundaries(merged, vb)

    print("=== Counts ===")
    print(f"Base (form_validate) collisions: {len(base.collisions)}")
    print(f"Visual (form_ai inflated geometry) collisions: {len(visual_c)}")
    print(f"Merged collisions (deduped pairs): {len(merged.collisions)}")
    print(f"Boundary (visual) violations: {len(vb)}")
    print(f"Merged valid: {merged2.valid}  errorCount: {merged2.summary.errorCount}")

    base_keys = {(c.componentAId, c.componentBId) for c in base.collisions}
    base_keys |= {(b, a) for a, b in base_keys}
    visual_only = [c for c in visual_c if (c.componentAId, c.componentBId) not in base_keys]

    _print_pairs("Base validation collisions", list(base.collisions))
    _print_pairs("Visual pairs not in base (extra from inflated boxes)", visual_only)
    _print_pairs("Merged (final)", list(merged.collisions))

    print("\n=== Enriched lines (as sent to model) ===")
    lines = _enrich_collision_feedback_lines(definition, rt_ctx, list(merged.collisions))
    for line in lines:
        print(line)

    print("\n=== Full correction message (Collisions section) ===")
    msg = _build_correction_message(merged2, definition, rt_ctx)
    if "Collisions:" in msg:
        start = msg.index("Collisions:")
        print(msg[start:])
    else:
        print("(no Collisions section)")


if __name__ == "__main__":
    main()

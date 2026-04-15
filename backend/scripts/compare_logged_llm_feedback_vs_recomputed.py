"""
Compare correction feedback actually sent to OpenAI (log.ApiRequest) with what
the current form_ai code would generate from the same candidate + runtime context.

Usage (from backend/, venv active):
  python scripts/compare_logged_llm_feedback_vs_recomputed.py [RequestID_prefix]

Default RequestID: 903afb9d-36c5-40ab-a6f2-feaa8ad34596 (trim if your DB stores full GUID)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modules.form_ai.service import (  # noqa: E402
    _build_correction_message,
    _collect_visual_boundary_violations,
    _collect_visual_collisions,
    _merge_guardrail_errors,
    _merge_visual_boundaries,
    _merge_visual_collisions,
    _validate_single_page_guardrail,
)
from modules.form_validate.service import validate_definition_payload  # noqa: E402
from common.database import engine  # noqa: E402


def _iter_openai_blocks(payload: str) -> list[dict]:
    if not payload or not payload.strip():
        return []
    try:
        outer = json.loads(payload)
    except json.JSONDecodeError:
        return []
    blocks = outer.get("input")
    if blocks is None and isinstance(outer, list):
        blocks = outer
    if not isinstance(blocks, list):
        return []
    return [b for b in blocks if isinstance(b, dict)]


def _block_text(block: dict) -> str:
    parts: list[str] = []
    for part in block.get("content") or []:
        if not isinstance(part, dict):
            continue
        t = part.get("text")
        if isinstance(t, str):
            parts.append(t)
    return "\n".join(parts)


def _parse_json_from_assistant_text(txt: str) -> dict | None:
    if '"pages"' not in txt or "schemaVersion" not in txt:
        return None
    try:
        return json.loads(txt)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]*\}", txt)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                return None
    return None


def _find_failing_candidate_before_correction(blocks: list[dict]) -> dict | None:
    """
    OpenAI request input is ordered. The failing candidate is the last assistant
    message *before* the last user message that contains the correction preamble.
    """
    last_corr_idx: int | None = None
    for i in range(len(blocks) - 1, -1, -1):
        b = blocks[i]
        if b.get("role") != "user":
            continue
        t = _block_text(b)
        if "Your previous JSON failed validation" in t or "Collisions:" in t:
            last_corr_idx = i
            break
    if last_corr_idx is None:
        return None
    for j in range(last_corr_idx - 1, -1, -1):
        b = blocks[j]
        if b.get("role") != "assistant":
            continue
        cand = _parse_json_from_assistant_text(_block_text(b))
        if cand:
            return cand
    return None


def _extract_user_correction_text(blocks: list[dict]) -> str | None:
    """Last user message that looks like form_ai correction."""
    for block in reversed(blocks):
        if block.get("role") != "user":
            continue
        txt = _block_text(block)
        if "Your previous JSON failed validation" in txt or "Collisions:" in txt:
            return txt
    return None


def _full_validation(candidate: dict, runtime_context: dict | None):
    v = validate_definition_payload({"definition": candidate})
    v = _merge_guardrail_errors(v, _validate_single_page_guardrail(candidate))
    v = _merge_visual_boundaries(
        v, _collect_visual_boundary_violations(candidate, runtime_context)
    )
    v = _merge_visual_collisions(
        v, _collect_visual_collisions(candidate, runtime_context)
    )
    return v


def main() -> None:
    prefix = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "903afb9d-36c5-40ab-a6f2-feaa8ad34596"
    )
    runtime_context = {
        "canvas": {"width": 1920, "height": 980},
        "componentFootprints": [
            {"componentType": "textarea", "width": 720, "height": 209},
            {"componentType": "first-name", "width": 560, "height": 110},
            {"componentType": "text", "width": 560, "height": 110},
        ],
    }

    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
            SELECT ApiRequestID, RequestID, Path, RequestPayload
            FROM log.ApiRequest
            WHERE RequestID LIKE :pat AND Path LIKE '/outbound/openai%'
            ORDER BY ApiRequestID ASC
            """
            ),
            {"pat": prefix + "%"},
        ).fetchall()

    print(f"Found {len(rows)} outbound OpenAI row(s) for RequestID LIKE {prefix!r}\n")
    print("=" * 100)

    for api_id, req_id, path, payload in rows:
        blocks = _iter_openai_blocks(payload or "")
        logged_correction = _extract_user_correction_text(blocks)

        print(f"ApiRequestID={api_id} Path={path}")
        if logged_correction:
            print("\n--- LOGGED user correction message (excerpt) ---")
            print(logged_correction[:4000])
            if len(logged_correction) > 4000:
                print(f"\n... [{len(logged_correction) - 4000} more chars]")
        else:
            print("\n(No user correction message in this payload — likely first attempt.)")

        candidate = _find_failing_candidate_before_correction(blocks)
        if candidate:
            v = _full_validation(candidate, runtime_context)
            recomputed = _build_correction_message(v, candidate, runtime_context)
            print("\n--- RECOMPUTED _build_correction_message (current code, sample runtime_context) ---")
            print(recomputed[:4000])
            if len(recomputed) > 4000:
                print(f"\n... [{len(recomputed) - 4000} more chars]")

            print("\n--- RECOMPUTED validation summary ---")
            print(
                f"  valid={v.valid} schema={len(v.schemaErrors)} "
                f"boundary={len(v.boundaryViolations)} collisions={len(v.collisions)}"
            )
            for c in v.collisions:
                print(
                    f"    collision: {c.componentAId} / {c.componentBId} area={c.overlapArea}"
                )

            if logged_correction and recomputed.strip() != logged_correction.strip():
                print("\n--- DIFF: logged vs recomputed (first 2000 chars) ---")
                a, b = logged_correction, recomputed
                for i, (ca, cb) in enumerate(zip(a, b)):
                    if ca != cb:
                        print(f"First mismatch at char {i}: logged={ca!r} recomputed={cb!r}")
                        print("Logged context:", repr(a[max(0, i - 80) : i + 120]))
                        print("Recomp context:", repr(b[max(0, i - 80) : i + 120]))
                        break
                else:
                    if len(a) != len(b):
                        print(f"Length differ: logged={len(a)} recomputed={len(b)}")
                    else:
                        print("(Strings equal after strip? checking...)")
        else:
            print(
                "\n(Could not find failing candidate: assistant JSON before correction user message.)"
            )

        print("\n" + "=" * 100 + "\n")


if __name__ == "__main__":
    main()

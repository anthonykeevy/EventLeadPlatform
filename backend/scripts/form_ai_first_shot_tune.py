"""
First-shot tuning workflow (CLI): same user prompt; vary only the system addendum.

Process (manual + this tool):
  To mirror “Generate from Draft” on the server for Form 403: use `--save-definition`, then
  `scripts/push_form_draft_definition.py` (updates latest DRAFT `FormVersion.DefinitionJSON`).
  1) Run with baseline (no addendum) — measures raw first reply.
  2) Review printed scores (layout + goal).
  3) Edit a small addendum file; record what you changed (git or changelog).
  4) Re-run with --addendum-file (user prompt unchanged).
  5) Compare scores vs baseline.
  6–7) Loop: one change at a time; use --repeat to sample LLM variance.

Examples:

  # Baseline — first model response only (no validator corrections)
  python backend/scripts/form_ai_first_shot_tune.py --user-prompt "Build a ..."

  # With instruction addendum (system message only)
  python backend/scripts/form_ai_first_shot_tune.py --user-prompt "..." \\
    --addendum-file docs/experiments/addendum-v1.md \\
    --changelog-jsonl tmp/first-shot-changelog.jsonl --experiment-id exp-2026-03-31-a

  # Same addendum 3× to see variance
  python backend/scripts/form_ai_first_shot_tune.py --user-prompt "..." \\
    --addendum-file addendum.md --repeat 3
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPO_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from modules.form_ai.first_shot_scoring import (  # noqa: E402
    addendum_fingerprint,
    combined_score,
    score_goal_coverage,
    score_layout,
)
from modules.form_ai.service import generate_form_definition  # noqa: E402


def _run_once(
    user_prompt: str,
    addendum: str | None,
    model: str | None,
    runtime_path: Path | None,
    openai_transport: str,
    layout_weight: float,
) -> Dict[str, Any]:
    runtime = None
    if runtime_path is not None:
        runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
        if not isinstance(runtime, dict):
            raise ValueError("runtime JSON must be an object")

    result = generate_form_definition(
        user_prompt,
        model_override=model,
        runtime_context=runtime,
        openai_transport=openai_transport,
        max_system_correction_attempts=0,
        system_prompt_addendum=addendum,
    )
    if not result.trace.attempts:
        raise RuntimeError("Expected at least one trace attempt")

    first = result.trace.attempts[0].validation
    layout = score_layout(
        first.collisionCount,
        first.boundaryViolationCount,
        first.schemaErrorCount,
    )
    definition = result.definitionJSON
    if definition is None:
        goal, goal_checks = 0.0, [{"id": "definition", "ok": False, "detail": "no JSON"}]
    else:
        goal, goal_checks = score_goal_coverage(definition, user_prompt)

    comb = combined_score(layout, goal, layout_weight=layout_weight)

    return {
        "status": result.status,
        "terminalReason": result.trace.terminalReason,
        "valid": first.valid,
        "collisionCount": first.collisionCount,
        "boundaryViolationCount": first.boundaryViolationCount,
        "schemaErrorCount": first.schemaErrorCount,
        "layoutScore": round(layout, 2),
        "goalScore": round(goal, 2),
        "combinedScore": round(comb, 2),
        "goalChecks": goal_checks,
        "trace": result.trace.model_dump(),
        "definitionJSON": definition,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate first LLM response only (no corrections); optional system addendum."
    )
    parser.add_argument("--user-prompt", required=True, help="Fixed user request (unchanged across experiments).")
    parser.add_argument(
        "--addendum-file",
        type=Path,
        default=None,
        help="Text appended to the system message (not the user prompt).",
    )
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--runtime-json", type=Path, default=None)
    parser.add_argument(
        "--repeat",
        type=int,
        default=1,
        help="Run the same configuration this many times (variance check). Default 1.",
    )
    parser.add_argument(
        "--layout-weight",
        type=float,
        default=0.5,
        help="Weight for layout vs goal in combined score (0–1). Default 0.5.",
    )
    parser.add_argument(
        "--openai-transport",
        choices=("auto", "sync", "stream"),
        default="auto",
    )
    parser.add_argument("--experiment-id", type=str, default="local")
    parser.add_argument(
        "--changelog-jsonl",
        type=Path,
        default=None,
        help="Append one JSON line per repeat with scores and addendum fingerprint.",
    )
    parser.add_argument(
        "--save-definition",
        type=Path,
        default=None,
        help=(
            "Write the returned definitionJSON (first-shot draft) to this path as UTF-8 JSON. "
            "When --repeat > 1, each run overwrites the file (last run wins). "
            "Use repeat=1 on your best addendum, or copy the file after the winning iteration."
        ),
    )
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    addendum: str | None = None
    addendum_path: str | None = None
    if args.addendum_file is not None:
        addendum = args.addendum_file.read_text(encoding="utf-8")
        if not addendum.strip():
            addendum = None
        addendum_path = str(args.addendum_file.resolve())

    load_dotenv(REPO_ROOT / "backend" / ".env")

    repeats = max(1, int(args.repeat))
    combined_scores: List[float] = []
    rows: List[Dict[str, Any]] = []

    for r in range(1, repeats + 1):
        if not args.quiet:
            print(f"\n=== Run {r}/{repeats} ===", flush=True)
        row_core = _run_once(
            args.user_prompt.strip(),
            addendum,
            args.model,
            args.runtime_json,
            args.openai_transport,
            layout_weight=args.layout_weight,
        )
        combined_scores.append(float(row_core["combinedScore"]))
        rows.append(row_core)

        if not args.quiet:
            print(
                f"status={row_core['status']} terminal={row_core['terminalReason']} "
                f"valid={row_core['valid']}"
            )
            print(
                f"collisions={row_core['collisionCount']} boundaries={row_core['boundaryViolationCount']} "
                f"schema={row_core['schemaErrorCount']}"
            )
            print(
                f"scores: layout={row_core['layoutScore']} goal={row_core['goalScore']} "
                f"combined={row_core['combinedScore']}"
            )
            for chk in row_core["goalChecks"]:
                ok = chk.get("ok")
                cid = chk.get("id")
                print(f"  goal check [{cid}]: {'ok' if ok else 'MISS'}")

        if args.changelog_jsonl:
            fp = addendum_fingerprint(addendum or "")
            log = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "experimentId": args.experiment_id,
                "repeatIndex": r,
                "userPromptChars": len(args.user_prompt),
                "addendumPath": addendum_path,
                "addendumFingerprint": fp,
                "layoutScore": row_core["layoutScore"],
                "goalScore": row_core["goalScore"],
                "combinedScore": row_core["combinedScore"],
                "layoutWeight": args.layout_weight,
                "collisionCount": row_core["collisionCount"],
                "boundaryViolationCount": row_core["boundaryViolationCount"],
                "valid": row_core["valid"],
                "terminalReason": row_core["terminalReason"],
            }
            args.changelog_jsonl.parent.mkdir(parents=True, exist_ok=True)
            with args.changelog_jsonl.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(log, ensure_ascii=False) + "\n")

        if args.save_definition is not None:
            defn = row_core.get("definitionJSON")
            if isinstance(defn, dict):
                args.save_definition.parent.mkdir(parents=True, exist_ok=True)
                args.save_definition.write_text(
                    json.dumps(defn, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
                if not args.quiet:
                    print(f"Wrote definitionJSON to {args.save_definition.resolve()}", flush=True)

    if repeats > 1 and not args.quiet:
        print("\n--- Repeat summary (combined score) ---")
        print(
            f"min={min(combined_scores):.2f} max={max(combined_scores):.2f} "
            f"mean={statistics.mean(combined_scores):.2f}"
        )
        if len(combined_scores) > 1:
            print(f"stdev={statistics.stdev(combined_scores):.2f}")


if __name__ == "__main__":
    main()

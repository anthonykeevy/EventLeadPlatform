"""
Run the same form-AI prompt repeatedly (CLI), recording validation traces.

Each iteration is one call to ``generate_form_definition`` — that already includes
the Story 6.2 **internal** loop (initial model response + up to 3 correction passes).
Use ``--loops`` for how many **independent** generations to run (e.g. compare
stochastic outcomes or prompt/context variants).

Usage (from repo root, with OPENAI_API_KEY in backend/.env):

  python backend/scripts/form_ai_prompt_loop.py --prompt "Build a contact form..." --loops 5

  python backend/scripts/form_ai_prompt_loop.py --prompt-file my-prompt.txt --loops 3 \\
    --model gpt-5-mini --runtime-json runtime-context.json --output-jsonl runs.jsonl

Feedback strategy (collision text, hints) is determined by server code; to compare
different approaches, use different branches/env or extend the service — this CLI
only **measures** outcomes per run.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPO_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from modules.form_ai.schemas import FormAiGenerateResponse  # noqa: E402
from modules.form_ai.service import generate_form_definition  # noqa: E402


def _load_runtime(path: Optional[Path]) -> Optional[Dict[str, Any]]:
    if path is None:
        return None
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("runtime JSON must be an object at the root")
    return data


def _serialize_run(
    loop_index: int,
    prompt: str,
    result: FormAiGenerateResponse,
    elapsed_ms: float,
    *,
    include_definition: bool,
) -> Dict[str, Any]:
    tr = result.trace
    row: Dict[str, Any] = {
        "loopIndex": loop_index,
        "prompt": prompt,
        "status": result.status,
        "userMessage": result.userMessage,
        "draftHasValidationIssues": result.draftHasValidationIssues,
        "elapsedMs": round(elapsed_ms, 1),
        "terminalReason": tr.terminalReason,
        "attemptCount": tr.attemptCount,
        "systemCorrectionAttemptsUsed": tr.systemCorrectionAttemptsUsed,
        "maxSystemCorrectionAttempts": tr.maxSystemCorrectionAttempts,
        "resolvedOpenaiTransport": tr.resolvedOpenaiTransport,
        "attempts": [
            {
                "attemptNumber": a.attemptNumber,
                "phase": a.phase,
                "valid": a.validation.valid,
                "collisionCount": a.validation.collisionCount,
                "boundaryViolationCount": a.validation.boundaryViolationCount,
                "schemaErrorCount": a.validation.schemaErrorCount,
                "errorCount": a.validation.errorCount,
                "collisionDeltaFromPrevious": a.collisionDeltaFromPrevious,
                "collisionTrendVsPrevious": a.collisionTrendVsPrevious,
                "correctionIssued": a.correctionIssued,
                "notes": a.notes,
            }
            for a in tr.attempts
        ],
    }
    if tr.validationSummary is not None:
        row["validationSummary"] = tr.validationSummary.model_dump()
    if include_definition and result.definitionJSON is not None:
        row["definitionJSON"] = result.definitionJSON
    return row


def _print_human_summary(rows: List[Dict[str, Any]]) -> None:
    print("")
    print("--- Summary ---")
    n = len(rows)
    completed = sum(1 for r in rows if r["status"] == "completed")
    print(f"Loops: {n}  completed: {completed}  failed: {n - completed}")
    if n:
        retries = [r["systemCorrectionAttemptsUsed"] for r in rows]
        attempts = [r["attemptCount"] for r in rows]
        print(
            f"Retries used (min/avg/max): {min(retries)} / "
            f"{sum(retries) / n:.2f} / {max(retries)}"
        )
        print(
            f"Server attempts (min/avg/max): {min(attempts)} / "
            f"{sum(attempts) / n:.2f} / {max(attempts)}"
        )
        ms = [r["elapsedMs"] for r in rows]
        print(f"Elapsed ms (min/avg/max): {min(ms):.0f} / {sum(ms) / n:.0f} / {max(ms):.0f}")
    reasons: Dict[str, int] = {}
    for r in rows:
        tr = str(r["terminalReason"])
        reasons[tr] = reasons.get(tr, 0) + 1
    print("Terminal reasons:", dict(sorted(reasons.items(), key=lambda x: (-x[1], x[0]))))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run form-AI generate in a loop and record validation traces (CLI)."
    )
    parser.add_argument("--prompt", type=str, help="Single prompt string.")
    parser.add_argument(
        "--prompt-file",
        type=Path,
        help="Path to UTF-8 file containing the prompt (alternative to --prompt).",
    )
    parser.add_argument(
        "--loops",
        type=int,
        default=1,
        help="How many independent generate calls to run (default: 1).",
    )
    parser.add_argument("--model", type=str, default=None, help="Override OPENAI_MODEL for this run.")
    parser.add_argument(
        "--runtime-json",
        type=Path,
        default=None,
        help="Optional JSON file for runtimeContext (canvas, componentFootprints, etc.).",
    )
    parser.add_argument(
        "--openai-transport",
        choices=("auto", "sync", "stream"),
        default="auto",
        help="Outbound OpenAI transport (default: auto).",
    )
    parser.add_argument(
        "--output-jsonl",
        type=Path,
        default=None,
        help="Append one JSON object per loop for downstream analysis.",
    )
    parser.add_argument(
        "--include-definition",
        action="store_true",
        help="Include definitionJSON in JSONL rows (large).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Less console output (still writes JSONL if set).",
    )
    args = parser.parse_args()

    if args.prompt and args.prompt_file:
        parser.error("Use either --prompt or --prompt-file, not both.")
    if not args.prompt and not args.prompt_file:
        parser.error("Provide --prompt or --prompt-file.")

    prompt = args.prompt.strip() if args.prompt else ""
    if args.prompt_file:
        prompt = args.prompt_file.read_text(encoding="utf-8").strip()
    if len(prompt) < 3:
        parser.error("Prompt must be at least 3 characters.")

    loops = max(1, int(args.loops))

    load_dotenv(REPO_ROOT / "backend" / ".env")
    runtime = _load_runtime(args.runtime_json)

    rows: List[Dict[str, Any]] = []
    for i in range(1, loops + 1):
        if not args.quiet:
            print(f"\n[loop {i}/{loops}] generating...", flush=True)
        t0 = time.perf_counter()
        result = generate_form_definition(
            prompt,
            model_override=args.model,
            runtime_context=runtime,
            openai_transport=args.openai_transport,
        )
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        row = _serialize_run(
            i,
            prompt,
            result,
            elapsed_ms,
            include_definition=args.include_definition,
        )
        rows.append(row)

        if not args.quiet:
            print(
                f"  status={result.status} terminal={result.trace.terminalReason} "
                f"attempts={result.trace.attemptCount} retries_used="
                f"{result.trace.systemCorrectionAttemptsUsed} elapsed_ms={elapsed_ms:.0f}"
            )
            for a in result.trace.attempts:
                trend = a.collisionTrendVsPrevious or "-"
                delta = a.collisionDeltaFromPrevious
                delta_s = "" if delta is None else str(delta)
                print(
                    f"    attempt {a.attemptNumber} ({a.phase}): valid={a.validation.valid} "
                    f"collisions={a.validation.collisionCount} boundaries="
                    f"{a.validation.boundaryViolationCount} "
                    f"collision_delta={delta_s} trend={trend}"
                )

        if args.output_jsonl:
            args.output_jsonl.parent.mkdir(parents=True, exist_ok=True)
            with args.output_jsonl.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    if not args.quiet:
        _print_human_summary(rows)

    if args.output_jsonl and not args.quiet:
        print(f"\nAppended {len(rows)} line(s) to {args.output_jsonl}")


if __name__ == "__main__":
    main()

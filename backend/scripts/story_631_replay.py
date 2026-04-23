"""Story 6.3.1 — Replay LLM semantic plans through the current compiler.

Purpose
-------
Iterating on the deterministic compiler (column-aligned grid, width tiers,
canvas-grow policy, etc.) is faster when you can re-run the *same* LLM
output through the new compile path without paying for another OpenAI call.

This script reads ``dbo.GenerationArtifact`` rows of type
``semantic-plan-attempt`` for one or more recent ``GenerationRun`` records,
re-compiles each plan against a chosen canvas (desktop / tablet / mobile, or
explicit width/height), and writes the resulting DefinitionJSON to disk so
you can either:

  - eyeball the JSON directly, or
  - load it into the Form Builder via the dev-only "Load DefinitionJSON
    from file" button (gated on ``VITE_ENABLE_DEV_LOGS=true``) for human
    visual feedback.

Usage examples
--------------
List the 20 most recent generation runs:

    python backend/scripts/story_631_replay.py --list

Replay the latest run on the desktop canvas (default):

    python backend/scripts/story_631_replay.py --latest

Replay a specific run on a mobile canvas, write under custom output dir:

    python backend/scripts/story_631_replay.py --run-id 4521 --device mobile \
        --out replay-output/run-4521-mobile

Replay every run from the last 24h on all 3 device canvases:

    python backend/scripts/story_631_replay.py --since-hours 24 --all-devices

Output
------
For each (run, attempt, device) tuple we emit:

  <out>/<run_id>__attempt-<n>__<device>.definition.json     -- the form definition
  <out>/<run_id>__attempt-<n>__<device>.compile-summary.json -- compileSummary

Plus a final ``replay-summary.json`` listing every file with its run/prompt
metadata so you can correlate.

The script is **read-only** against the database — it inserts nothing.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.database import SessionLocal  # noqa: E402
from sqlalchemy import text  # noqa: E402

from modules.form_ai.compiler import (  # noqa: E402
    DEFAULT_CANVAS_HEIGHT,
    DEFAULT_CANVAS_WIDTH,
    compile_semantic_plan_to_definition,
)
from modules.form_ai.schemas import FormSemanticPlan  # noqa: E402
from modules.form_ai.service import (  # noqa: E402
    _filter_unrequested_headings_from_plan,
    _normalize_display_component_props,
    _post_process_generated_definition,
    _resolve_runtime_governance_versions,
)


# Mirror of the frontend ``DEVICE_DIMENSIONS`` so replays match what the user
# would see in the Form Builder when previewing each device.
DEVICE_CANVAS = {
    "desktop": (1920, 980),
    "tablet": (768, 1024),
    "mobile": (375, 667),
}


@dataclass
class ReplayPlan:
    run_id: int
    request_id: str
    attempt_number: int
    phase: str
    semantic_plan: Dict[str, Any]
    created_date: datetime
    form_id: Optional[int]
    company_id: Optional[int]
    status: str
    terminal_reason: Optional[str]


def _device_canvas(device: str) -> Tuple[int, int]:
    if device not in DEVICE_CANVAS:
        raise SystemExit(
            f"unknown device {device!r}; expected one of {sorted(DEVICE_CANVAS)}"
        )
    return DEVICE_CANVAS[device]


def list_recent_runs(session, limit: int = 20) -> List[Dict[str, Any]]:
    rows = session.execute(
        text(
            """
            SELECT TOP (:limit)
                gr.GenerationRunID,
                gr.RequestID,
                gr.FormID,
                gr.CompanyID,
                gr.Status,
                gr.TerminalReason,
                gr.AttemptCount,
                gr.CreatedDate,
                (SELECT COUNT(*) FROM dbo.GenerationArtifact ga
                  WHERE ga.GenerationRunID = gr.GenerationRunID
                    AND ga.ArtifactType = 'semantic-plan-attempt') AS SemanticPlanCount
            FROM dbo.GenerationRun gr
            ORDER BY gr.CreatedDate DESC
            """
        ),
        {"limit": int(limit)},
    ).all()
    return [
        {
            "GenerationRunID": r.GenerationRunID,
            "RequestID": r.RequestID,
            "FormID": r.FormID,
            "CompanyID": r.CompanyID,
            "Status": r.Status,
            "TerminalReason": r.TerminalReason,
            "AttemptCount": r.AttemptCount,
            "CreatedDate": r.CreatedDate,
            "SemanticPlanCount": r.SemanticPlanCount,
        }
        for r in rows
    ]


def fetch_replay_plans(
    session,
    *,
    run_ids: Optional[List[int]] = None,
    since_hours: Optional[float] = None,
    only_latest: bool = False,
) -> List[ReplayPlan]:
    """Pull ``semantic-plan-attempt`` artifacts joined to their run row.

    Filters are inclusive of each other: ``run_ids`` AND ``since_hours``.
    ``only_latest`` overrides both and selects only the most recent run.
    """
    where_clauses: List[str] = ["ga.ArtifactType = 'semantic-plan-attempt'"]
    params: Dict[str, Any] = {}
    if only_latest:
        latest = session.execute(
            text(
                """
                SELECT TOP 1 gr.GenerationRunID FROM dbo.GenerationRun gr
                  WHERE EXISTS (
                    SELECT 1 FROM dbo.GenerationArtifact ga
                     WHERE ga.GenerationRunID = gr.GenerationRunID
                       AND ga.ArtifactType = 'semantic-plan-attempt'
                  )
                  ORDER BY gr.CreatedDate DESC
                """
            )
        ).first()
        if latest is None:
            return []
        run_ids = [int(latest.GenerationRunID)]

    if run_ids:
        placeholders = ",".join(f":run_{i}" for i, _ in enumerate(run_ids))
        where_clauses.append(f"gr.GenerationRunID IN ({placeholders})")
        for i, rid in enumerate(run_ids):
            params[f"run_{i}"] = int(rid)

    if since_hours is not None:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=float(since_hours))
        where_clauses.append("gr.CreatedDate >= :cutoff")
        # SQL Server stores DATETIME without tz; strip tzinfo for parameter binding.
        params["cutoff"] = cutoff.replace(tzinfo=None)

    where_sql = " AND ".join(where_clauses)

    rows = session.execute(
        text(
            f"""
            SELECT
                gr.GenerationRunID,
                gr.RequestID,
                gr.FormID,
                gr.CompanyID,
                gr.Status,
                gr.TerminalReason,
                gr.CreatedDate,
                ga.SequenceNumber AS AttemptNumber,
                ga.ArtifactJson
            FROM dbo.GenerationArtifact ga
            JOIN dbo.GenerationRun gr ON gr.GenerationRunID = ga.GenerationRunID
            WHERE {where_sql}
            ORDER BY gr.CreatedDate DESC, ga.SequenceNumber ASC
            """
        ),
        params,
    ).all()

    plans: List[ReplayPlan] = []
    for r in rows:
        try:
            payload = json.loads(r.ArtifactJson)
        except (TypeError, ValueError) as exc:
            print(
                f"  ! skipping run {r.GenerationRunID} attempt {r.AttemptNumber}: "
                f"artifact JSON unreadable ({exc})"
            )
            continue
        semantic_plan = payload.get("semanticPlan")
        if not isinstance(semantic_plan, dict):
            continue
        plans.append(
            ReplayPlan(
                run_id=int(r.GenerationRunID),
                request_id=str(r.RequestID),
                attempt_number=int(payload.get("attemptNumber", r.AttemptNumber or 1)),
                phase=str(payload.get("phase", "unknown")),
                semantic_plan=semantic_plan,
                created_date=r.CreatedDate,
                form_id=int(r.FormID) if r.FormID is not None else None,
                company_id=int(r.CompanyID) if r.CompanyID is not None else None,
                status=str(r.Status),
                terminal_reason=str(r.TerminalReason) if r.TerminalReason else None,
            )
        )
    return plans


def compile_one(
    plan: ReplayPlan,
    *,
    canvas_width: int,
    canvas_height: int,
    prompt: str = "",
    governance: Optional[Dict[str, Any]] = None,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Compile a single replay plan and run the same post-process the live
    ``/api/form-ai/generate`` endpoint runs.

    Story 6.3.1 UAT round 5 (run 40) — replay output now matches the live
    endpoint byte-for-byte by:

      1. Loading the same active governance row set (capability policy, width
         policy, capability snapshot, validation contracts) from the DB. Without
         this, ``validation_contracts=None`` causes the compiler to silently
         drop every ``required``/``email``/``maxLength`` rule, and the saved
         JSON shows e.g. ``Email`` without the required asterisk even though
         the live endpoint preserved it. See ``_normalize_validation_intent`` —
         no contracts == no rules.

      2. Pre-filtering courtesy headers (``_filter_unrequested_headings_from_plan``)
         the same way ``run_form_ai_generation`` does, so the compiler doesn't
         lay out a header that the post-compile filter is going to drop and
         the canvas doesn't get a ghost top gap.

      3. Running ``_normalize_display_component_props`` + ``_post_process_generated_definition``.
         In ``deterministic-grid`` mode those only filter placeholder headings
         and rewrite ``props.tabOrder``; destructive geometry transforms stay
         gated off.

    ``governance`` defaults to ``None`` (built-in compiler defaults). Pass the
    output of ``_resolve_runtime_governance_versions(session)`` to mirror the
    live endpoint's resolved governance set.

    A ``prompt`` argument is accepted because the heading-filter step inspects
    the prompt for "header"/"title"/"intro" markers; replays don't have the
    original prompt, so we default to empty (which is the strictest case and
    safest for visual fidelity — placeholder/courtesy headings are dropped).
    """
    semantic = FormSemanticPlan.model_validate(plan.semantic_plan)
    plan_for_compile, _ = _filter_unrequested_headings_from_plan(semantic, prompt)
    runtime_context = {
        "canvas": {
            "width": canvas_width,
            "height": canvas_height,
            "gridSize": 8,
        },
    }
    governance = governance or {}
    definition, compile_summary = compile_semantic_plan_to_definition(
        plan_for_compile,
        runtime_context=runtime_context,
        capability_policy_json=governance.get("capabilityPolicyJson"),
        width_policy_json=governance.get("widthClassPolicyJson"),
        capability_snapshot_json=governance.get("componentCapabilitySnapshotJson"),
        validation_contracts=governance.get("validationContracts"),
    )
    definition = _normalize_display_component_props(definition)
    compiler_mode = (
        str(compile_summary.get("compilerMode", "deterministic-grid"))
        if isinstance(compile_summary, dict)
        else "deterministic-grid"
    )
    definition, post_processing_applied = _post_process_generated_definition(
        definition,
        prompt,
        runtime_context,
        compiler_mode=compiler_mode,
    )
    if isinstance(compile_summary, dict):
        compile_summary["postProcessingApplied"] = post_processing_applied
        compile_summary["governanceResolutionSource"] = (
            governance.get("governanceResolutionSource", "no-governance-loaded")
            if governance
            else "no-governance-loaded"
        )
    return definition, compile_summary


def write_outputs(
    out_dir: Path,
    plan: ReplayPlan,
    device: str,
    definition: Dict[str, Any],
    compile_summary: Dict[str, Any],
) -> Tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    base = f"{plan.run_id}__attempt-{plan.attempt_number}__{device}"
    def_path = out_dir / f"{base}.definition.json"
    sum_path = out_dir / f"{base}.compile-summary.json"
    def_path.write_text(json.dumps(definition, indent=2), encoding="utf-8")
    sum_path.write_text(json.dumps(compile_summary, indent=2, default=str), encoding="utf-8")
    return def_path, sum_path


def render_run_table(runs: Iterable[Dict[str, Any]]) -> None:
    print(
        f"{'RunID':>8}  {'CreatedDate':<23}  {'Status':<14}  "
        f"{'TerminalReason':<24}  {'#sem':>4}  {'FormID':>6}  RequestID"
    )
    print("-" * 110)
    for r in runs:
        print(
            f"{r['GenerationRunID']:>8}  "
            f"{str(r['CreatedDate']):<23}  "
            f"{str(r['Status']):<14}  "
            f"{str(r['TerminalReason'] or '-'):<24}  "
            f"{r['SemanticPlanCount']:>4}  "
            f"{(r['FormID'] if r['FormID'] is not None else '-'):>6}  "
            f"{r['RequestID']}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])

    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--list", action="store_true", help="List the most recent generation runs and exit.")
    selection.add_argument("--latest", action="store_true", help="Replay only the most recent run.")
    selection.add_argument("--run-id", type=int, action="append", help="Replay a specific run ID. Repeat for multiple.")

    parser.add_argument("--since-hours", type=float, help="Replay every run created in the last N hours.")
    parser.add_argument("--list-limit", type=int, default=20, help="How many runs to show with --list (default 20).")

    canvas_group = parser.add_argument_group("Canvas")
    canvas_group.add_argument("--device", choices=sorted(DEVICE_CANVAS), help="Use this device's canvas (1920x980 desktop / 768x1024 tablet / 375x667 mobile).")
    canvas_group.add_argument("--all-devices", action="store_true", help="Replay each plan against all 3 devices.")
    canvas_group.add_argument("--width", type=int, help="Custom canvas width (overrides --device).")
    canvas_group.add_argument("--height", type=int, help="Custom canvas height (overrides --device).")

    parser.add_argument("--out", default="replay-output", help="Output directory (created if missing).")
    parser.add_argument(
        "--no-governance",
        action="store_true",
        help=(
            "Skip loading active governance from the DB. The compiler will use "
            "its built-in defaults, which means validation rules (required, "
            "email, maxLength, ...) are dropped. Only useful when iterating on "
            "compiler defaults in isolation; live endpoint behaviour will not "
            "match."
        ),
    )

    args = parser.parse_args()

    session = SessionLocal()
    try:
        if args.list:
            runs = list_recent_runs(session, limit=args.list_limit)
            if not runs:
                print("No generation runs found.")
                return 0
            render_run_table(runs)
            return 0

        plans = fetch_replay_plans(
            session,
            run_ids=args.run_id,
            since_hours=args.since_hours,
            only_latest=args.latest,
        )
        if not plans:
            print("No semantic-plan-attempt artifacts matched the filters.")
            return 0

        # Decide canvas matrix.
        if args.all_devices:
            canvases: List[Tuple[str, int, int]] = [
                (name, w, h) for name, (w, h) in DEVICE_CANVAS.items()
            ]
        elif args.width and args.height:
            canvases = [("custom", args.width, args.height)]
        elif args.device:
            w, h = _device_canvas(args.device)
            canvases = [(args.device, w, h)]
        else:
            canvases = [("desktop", DEFAULT_CANVAS_WIDTH, DEFAULT_CANVAS_HEIGHT)]

        out_root = Path(args.out)
        summary_rows: List[Dict[str, Any]] = []
        ok = 0
        failed = 0

        # Load governance once — same call the live endpoint makes — so every
        # replayed plan compiles against the same active capability policy /
        # width policy / validation contracts the live flow would have used.
        # Without this, validation rules (required, email, maxLength) get
        # silently dropped and the saved JSON diverges from the live API output.
        if args.no_governance:
            governance: Optional[Dict[str, Any]] = None
            print("[info] --no-governance set: compiling with built-in defaults; "
                  "validation rules will not appear in output JSON.")
        else:
            governance = _resolve_runtime_governance_versions(session)
            print(
                f"[info] governance resolved from DB: "
                f"capabilityPolicy={governance.get('capabilityPolicyVersionRef')}, "
                f"widthPolicy={governance.get('widthClassPolicyVersionRef')}, "
                f"validationContracts={'yes' if governance.get('validationContracts') else 'no'}"
            )

        for plan in plans:
            for device_name, cw, ch in canvases:
                try:
                    definition, compile_summary = compile_one(
                        plan,
                        canvas_width=cw,
                        canvas_height=ch,
                        governance=governance,
                    )
                    def_path, sum_path = write_outputs(
                        out_root, plan, device_name, definition, compile_summary
                    )
                    ok += 1
                    summary_rows.append({
                        "runId": plan.run_id,
                        "requestId": plan.request_id,
                        "attemptNumber": plan.attempt_number,
                        "phase": plan.phase,
                        "device": device_name,
                        "canvas": {"width": cw, "height": ch},
                        "outputs": {
                            "definition": str(def_path.as_posix()),
                            "compileSummary": str(sum_path.as_posix()),
                        },
                        "originalRunStatus": plan.status,
                        "originalTerminalReason": plan.terminal_reason,
                        "compiledCanvasHeight": compile_summary.get("stageDiagnostics") and definition["canvasSettings"]["height"],
                        "canvasHeightGrew": compile_summary.get("canvasHeightGrew"),
                        "componentCount": compile_summary.get("outputComponentCount"),
                        "rowSolverDecisions": len(compile_summary.get("rowSolverDecisions") or []),
                        "rowGroupSplits": len(compile_summary.get("rowGroupSplits") or []),
                    })
                    print(
                        f"[OK] run={plan.run_id} attempt={plan.attempt_number} "
                        f"device={device_name} canvas={cw}x{ch} -> "
                        f"{def_path.name}"
                    )
                except Exception as exc:  # noqa: BLE001 — surface every compile error
                    failed += 1
                    print(
                        f"[ERR] run={plan.run_id} attempt={plan.attempt_number} "
                        f"device={device_name}: {type(exc).__name__}: {exc}"
                    )
                    summary_rows.append({
                        "runId": plan.run_id,
                        "attemptNumber": plan.attempt_number,
                        "device": device_name,
                        "error": f"{type(exc).__name__}: {exc}",
                    })

        out_root.mkdir(parents=True, exist_ok=True)
        (out_root / "replay-summary.json").write_text(
            json.dumps(summary_rows, indent=2, default=str), encoding="utf-8"
        )
        print(
            f"\nReplay complete: {ok} ok, {failed} failed. Summary written to "
            f"{out_root / 'replay-summary.json'}"
        )
        return 0 if failed == 0 else 1
    finally:
        session.close()


if __name__ == "__main__":
    raise SystemExit(main())

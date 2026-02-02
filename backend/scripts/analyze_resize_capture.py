"""
Analyze resize.capture frontend events and group by handle + phase.

Outputs a markdown report highlighting:
- initial (start.afterGrab) sizes of component + objects
- per-5px sample deltas vs expected handle direction
- wrap events / unexpected sign changes

Usage:
  python backend/scripts/analyze_resize_capture.py --component-id text-... --hours 2 --out docs/analysis/resize-capture-report.md
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from sqlalchemy import text


def _sign(x: float, eps: float = 0.5) -> int:
    if x > eps:
        return 1
    if x < -eps:
        return -1
    return 0


HANDLE_AXES: Dict[str, Tuple[int, int]] = {
    # resizeX, resizeY (matches ResizeHandles.tsx)
    "n": (0, -1),
    "s": (0, 1),
    "e": (1, 0),
    "w": (-1, 0),
    "ne": (1, -1),
    "se": (1, 1),
    "nw": (-1, -1),
    "sw": (-1, 1),
}


def _get(d: Dict[str, Any], path: List[str]) -> Any:
    cur: Any = d
    for p in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(p)
    return cur


def _rect_key(rect: Optional[Dict[str, Any]], key: str) -> Optional[float]:
    if not isinstance(rect, dict):
        return None
    v = rect.get(key)
    return float(v) if isinstance(v, (int, float)) else None


def _fmt_num(v: Optional[float]) -> str:
    if v is None:
        return "—"
    if abs(v - round(v)) < 1e-6:
        return str(int(round(v)))
    return f"{v:.2f}"


@dataclass(frozen=True)
class ObjSize:
    width: Optional[float]
    height: Optional[float]
    is_wrapped: Optional[bool]


@dataclass(frozen=True)
class SnapshotSizes:
    bounds_w: Optional[float]
    bounds_h: Optional[float]
    smart_w: Optional[float]
    smart_h: Optional[float]
    objects: Dict[str, ObjSize]


def extract_sizes(payload: Dict[str, Any]) -> SnapshotSizes:
    snap = payload.get("snapshot") or {}
    bounds = snap.get("bounds")
    smart = snap.get("smartBorderBounds")

    obj_metrics = snap.get("objectMetrics") or {}
    objects: Dict[str, ObjSize] = {}
    if isinstance(obj_metrics, dict):
        for obj_id, m in obj_metrics.items():
            if not isinstance(m, dict):
                continue
            rect = m.get("rect")
            objects[str(obj_id)] = ObjSize(
                width=_rect_key(rect, "width"),
                height=_rect_key(rect, "height"),
                is_wrapped=m.get("isTextWrapped") if isinstance(m.get("isTextWrapped"), bool) else None,
            )

    return SnapshotSizes(
        bounds_w=_rect_key(bounds, "width"),
        bounds_h=_rect_key(bounds, "height"),
        smart_w=_rect_key(smart, "width"),
        smart_h=_rect_key(smart, "height"),
        objects=objects,
    )


def load_events(component_id: str, hours: int) -> List[Dict[str, Any]]:
    # Make backend imports work when running from repo root.
    backend_dir = Path(__file__).resolve().parents[1]
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))

    # Use the same engine the app uses.
    from common.database import engine  # type: ignore

    # CreatedDate is typically stored in server local time; use a wide window.
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
                SELECT TOP 2000
                    EventType,
                    ComponentID,
                    ComponentType,
                    Payload,
                    SessionID,
                    ClientTimestamp,
                    CreatedDate
                FROM log.FrontendEvent
                WHERE EventType = 'resize.capture'
                  AND ComponentID = :component_id
                  AND CreatedDate >= :cutoff
                ORDER BY CreatedDate ASC
                """
            ),
            {"component_id": component_id, "cutoff": cutoff},
        ).fetchall()

    out: List[Dict[str, Any]] = []
    for r in rows:
        payload_str = r._mapping.get("Payload")
        try:
            payload = json.loads(payload_str) if payload_str else None
        except Exception:
            payload = None
        if not isinstance(payload, dict):
            continue
        out.append(
            {
                "componentId": r._mapping.get("ComponentID"),
                "componentType": r._mapping.get("ComponentType"),
                "sessionId": r._mapping.get("SessionID"),
                "createdDate": r._mapping.get("CreatedDate"),
                "clientTs": r._mapping.get("ClientTimestamp"),
                "payload": payload,
            }
        )
    return out


def group_by_run(events: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    runs: Dict[str, List[Dict[str, Any]]] = {}
    for e in events:
        p = e["payload"]
        run_id = p.get("captureRunId")
        if not isinstance(run_id, str):
            continue
        runs.setdefault(run_id, []).append(e)
    return runs


def build_report(component_id: str, events: List[Dict[str, Any]]) -> str:
    runs = group_by_run(events)

    # Build per-handle runs in chronological order
    run_items: List[Tuple[datetime, str, str]] = []
    for run_id, es in runs.items():
        # Any event will do for handle
        handle = None
        ts = None
        for e in es:
            p = e["payload"]
            if handle is None and isinstance(p.get("handle"), str):
                handle = p["handle"]
            if ts is None and isinstance(e.get("createdDate"), datetime):
                ts = e["createdDate"]
        if not handle or handle not in HANDLE_AXES:
            continue
        run_items.append((ts or datetime.min.replace(tzinfo=timezone.utc), handle, run_id))
    run_items.sort(key=lambda t: t[0])

    # Index by handle
    by_handle: Dict[str, List[str]] = {}
    for _, h, run_id in run_items:
        by_handle.setdefault(h, []).append(run_id)

    lines: List[str] = []
    lines.append(f"# Resize capture report\n")
    lines.append(f"- Component: `{component_id}`")
    lines.append(f"- Events analyzed: **{len(events)}**")
    lines.append(f"- Runs (captureRunId): **{len(runs)}**\n")

    def summarize_sizes(s: SnapshotSizes) -> str:
        obj_parts = []
        for obj_id in sorted(s.objects.keys()):
            o = s.objects[obj_id]
            wrap = ""
            if o.is_wrapped is True:
                wrap = " (wrapped)"
            obj_parts.append(f"`{obj_id}`={_fmt_num(o.width)}×{_fmt_num(o.height)}{wrap}")
        objs = ", ".join(obj_parts) if obj_parts else "—"
        return (
            f"bounds={_fmt_num(s.bounds_w)}×{_fmt_num(s.bounds_h)}, "
            f"smart={_fmt_num(s.smart_w)}×{_fmt_num(s.smart_h)}, "
            f"objects: {objs}"
        )

    # Detect mismatches within a run using sample deltas.
    for handle in ["n", "s", "w", "e", "ne", "se", "nw", "sw"]:
        run_ids = by_handle.get(handle, [])
        if not run_ids:
            continue

        rx, ry = HANDLE_AXES[handle]
        lines.append(f"## Handle `{handle}`\n")
        lines.append(f"- Expected axes: resizeX={rx}, resizeY={ry}\n")

        for run_id in run_ids:
            es = runs[run_id]
            es_sorted = sorted(es, key=lambda e: (e["payload"].get("phase") != "start.beforeGrab", e["payload"].get("sampleIndex") or 0))

            # Map phases
            phase_map: Dict[str, Dict[str, Any]] = {}
            samples: List[Dict[str, Any]] = []
            for e in es_sorted:
                p = e["payload"]
                phase = p.get("phase")
                if isinstance(phase, str):
                    if phase == "sample":
                        samples.append(e)
                    else:
                        phase_map[phase] = e

            start_after = phase_map.get("start.afterGrab") or phase_map.get("start.beforeGrab")
            after_drop = phase_map.get("afterDrop")

            if not start_after:
                continue

            start_sizes = extract_sizes(start_after["payload"])
            end_sizes = extract_sizes(after_drop["payload"]) if after_drop else None

            lines.append(f"### Run `{run_id}`")
            lines.append(f"- Start(afterGrab): {summarize_sizes(start_sizes)}")
            if end_sizes:
                lines.append(f"- End(afterDrop): {summarize_sizes(end_sizes)}")

            # Compute end delta summary vs expected (sign only)
            if end_sizes and start_sizes.bounds_w is not None and end_sizes.bounds_w is not None:
                dw = end_sizes.bounds_w - start_sizes.bounds_w
                lines.append(f"- Δbounds.width: {_fmt_num(dw)}")
            if end_sizes and "input" in start_sizes.objects and "input" in end_sizes.objects:
                ih0 = start_sizes.objects["input"].height
                ih1 = end_sizes.objects["input"].height
                if ih0 is not None and ih1 is not None:
                    dih = ih1 - ih0
                    lines.append(f"- Δinput.height: {_fmt_num(dih)}")

            # Sample mismatch detection
            sample_rows = sorted(
                [s for s in samples if isinstance(s["payload"].get("sampleIndex"), int)],
                key=lambda e: int(e["payload"].get("sampleIndex")),
            )
            mismatches: List[str] = []
            wrap_flips: List[str] = []

            prev_sizes: Optional[SnapshotSizes] = None
            prev_wrap: Optional[bool] = None

            for e in sample_rows:
                p = e["payload"]
                idx = p.get("sampleIndex")
                mouse = p.get("mouse") or {}
                dprev = (mouse.get("deltaFromPrev") if isinstance(mouse, dict) else None) or {}
                dx_prev = dprev.get("x") if isinstance(dprev, dict) else None
                dy_prev = dprev.get("y") if isinstance(dprev, dict) else None
                if not isinstance(idx, int):
                    continue

                cur_sizes = extract_sizes(p)
                if prev_sizes is None:
                    prev_sizes = cur_sizes
                    prev_wrap = cur_sizes.objects.get("input").is_wrapped if "input" in cur_sizes.objects else None
                    continue

                # Width sign check
                if isinstance(dx_prev, (int, float)) and rx != 0:
                    expected_w = dx_prev * rx
                    if prev_sizes.bounds_w is not None and cur_sizes.bounds_w is not None:
                        actual_dw = cur_sizes.bounds_w - prev_sizes.bounds_w
                        if _sign(expected_w) != 0 and _sign(actual_dw) != 0 and _sign(expected_w) != _sign(actual_dw):
                            mismatches.append(
                                f"sample#{idx}: expected Δw sign({_sign(expected_w)}) from mouseΔx={dx_prev} but got Δbounds.w={_fmt_num(actual_dw)}"
                            )

                # Height sign check using input height if present
                if isinstance(dy_prev, (int, float)) and ry != 0:
                    expected_h = dy_prev * ry
                    in0 = prev_sizes.objects.get("input")
                    in1 = cur_sizes.objects.get("input")
                    if in0 and in1 and in0.height is not None and in1.height is not None:
                        actual_dh = in1.height - in0.height
                        if _sign(expected_h) != 0 and _sign(actual_dh) != 0 and _sign(expected_h) != _sign(actual_dh):
                            mismatches.append(
                                f"sample#{idx}: expected Δh sign({_sign(expected_h)}) from mouseΔy={dy_prev} but got Δinput.h={_fmt_num(actual_dh)}"
                            )

                # Wrap flips on input
                cur_wrap = cur_sizes.objects.get("input").is_wrapped if "input" in cur_sizes.objects else None
                if prev_wrap is False and cur_wrap is True:
                    wrap_flips.append(f"sample#{idx}: input became wrapped")
                prev_wrap = cur_wrap

                prev_sizes = cur_sizes

            if mismatches:
                lines.append(f"- **Mismatches (direction)**: {len(mismatches)}")
                for m in mismatches[:10]:
                    lines.append(f"  - {m}")
                if len(mismatches) > 10:
                    lines.append(f"  - ... {len(mismatches) - 10} more")
            else:
                lines.append(f"- **Mismatches (direction)**: 0")

            if wrap_flips:
                lines.append(f"- **Wrap events**: {len(wrap_flips)}")
                for w in wrap_flips[:10]:
                    lines.append(f"  - {w}")
            else:
                lines.append(f"- **Wrap events**: 0")

            lines.append("")  # spacer

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--component-id", required=True)
    parser.add_argument("--hours", type=int, default=2)
    parser.add_argument("--out", default="docs/analysis/resize-capture-report.md")
    args = parser.parse_args()

    events = load_events(args.component_id, args.hours)
    report = build_report(args.component_id, events)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    print(f"Wrote report: {out_path} ({len(report):,} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


#!/usr/bin/env python3
"""
Quick check script to see if corner handle resize issues have improved.

This script queries the database for the most recent resize captures and
checks if corner handles are now persisting size changes.
"""

import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).resolve().parents[1] / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from common.database import engine
from sqlalchemy import text
from datetime import datetime, timedelta, timezone
import json

def check_recent_resizes(component_id: str, hours: int = 1):
    """Check recent resize captures for a component"""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT TOP 100
                    FrontendEventID,
                    CreatedDate,
                    Payload
                FROM log.FrontendEvent
                WHERE EventType = 'resize.capture'
                  AND ComponentID = :component_id
                  AND CreatedDate >= :cutoff
                ORDER BY CreatedDate DESC
            """),
            {"component_id": component_id, "cutoff": cutoff}
        ).fetchall()
    
    if not rows:
        print(f"No resize captures found for {component_id} in the last {hours} hour(s)")
        return
    
    # Group by captureRunId
    runs = {}
    for row in rows:
        payload_str = row._mapping.get("Payload")
        try:
            payload = json.loads(payload_str) if payload_str else {}
        except:
            continue
        
        run_id = payload.get("captureRunId")
        if not run_id:
            continue
        
        if run_id not in runs:
            runs[run_id] = {
                "handle": payload.get("handle"),
                "phases": {},
                "created": row._mapping.get("CreatedDate")
            }
        
        phase = payload.get("phase")
        if phase:
            runs[run_id]["phases"][phase] = payload
    
    print(f"\nFound {len(runs)} resize runs in the last {hours} hour(s)\n")
    
    # Analyze each run
    corner_handles = ['ne', 'se', 'nw', 'sw']
    edge_handles = ['n', 's', 'w', 'e']
    
    corner_runs = {k: v for k, v in runs.items() if v["handle"] in corner_handles}
    edge_runs = {k: v for k, v in runs.items() if v["handle"] in edge_handles}
    
    print(f"Corner handle runs: {len(corner_runs)}")
    print(f"Edge handle runs: {len(edge_runs)}\n")
    
    # Check corner handles for improvements
    print("=" * 60)
    print("CORNER HANDLE ANALYSIS")
    print("=" * 60)
    
    for run_id, run_data in sorted(corner_runs.items(), key=lambda x: x[1]["created"], reverse=True):
        handle = run_data["handle"]
        phases = run_data["phases"]
        
        start_after = phases.get("start.afterGrab")
        after_drop = phases.get("afterDrop")
        
        if not start_after or not after_drop:
            print(f"\n{handle.upper()} ({run_id[:20]}...): Missing phases")
            continue
        
        # Extract sizes
        def get_size(payload, path):
            val = payload
            for p in path:
                val = val.get(p) if isinstance(val, dict) else None
                if val is None:
                    return None
            return float(val) if isinstance(val, (int, float)) else None
        
        start_bounds_w = get_size(start_after, ["snapshot", "bounds", "width"])
        start_bounds_h = get_size(start_after, ["snapshot", "bounds", "height"])
        start_input_h = get_size(start_after, ["snapshot", "objectMetrics", "input", "rect", "height"])
        
        end_bounds_w = get_size(after_drop, ["snapshot", "bounds", "width"])
        end_bounds_h = get_size(after_drop, ["snapshot", "bounds", "height"])
        end_input_h = get_size(after_drop, ["snapshot", "objectMetrics", "input", "rect", "height"])
        
        delta_w = (end_bounds_w - start_bounds_w) if (end_bounds_w and start_bounds_w) else None
        delta_h = (end_input_h - start_input_h) if (end_input_h and start_input_h) else None
        
        status_w = "✓" if delta_w and abs(delta_w) > 0.5 else "✗"
        status_h = "✓" if delta_h and abs(delta_h) > 0.5 else "✗"
        
        print(f"\n{handle.upper()} ({run_id[:20]}...):")
        print(f"  Width:  {start_bounds_w:.1f} -> {end_bounds_w:.1f} (d{delta_w:+.1f}) {status_w}")
        print(f"  Height: {start_input_h:.1f} -> {end_input_h:.1f} (d{delta_h:+.1f}) {status_h}")
        
        if delta_w and abs(delta_w) > 0.5 and delta_h and abs(delta_h) > 0.5:
            print(f"  ✅ IMPROVED: Both width and height persisted!")
        elif delta_w and abs(delta_w) > 0.5:
            print(f"  ⚠️  PARTIAL: Only width persisted")
        elif delta_h and abs(delta_h) > 0.5:
            print(f"  ⚠️  PARTIAL: Only height persisted")
        else:
            print(f"  ❌ NO CHANGE: Neither width nor height persisted")
    
    print("\n" + "=" * 60)
    print("Run the full analysis script for detailed mismatch detection:")
    print(f"  python backend/scripts/analyze_resize_capture.py --component-id {component_id} --hours {hours}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--component-id", default="text-1768866112931-605", help="Component ID to check")
    parser.add_argument("--hours", type=int, default=1, help="Hours to look back")
    args = parser.parse_args()
    
    check_recent_resizes(args.component_id, args.hours)

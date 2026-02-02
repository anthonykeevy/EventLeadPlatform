"""
Compare recent fieldshell.resize.commit events (click vs drag).
"""
import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from common.database import SessionLocal
from models.log.frontend_event import FrontendEvent


def load_json(value):
    if not value:
        return {}
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return {}


def get_snapshot(event):
    payload = load_json(event.Payload)
    metrics = load_json(event.MetricsJson)
    before = metrics.get("before") or payload.get("componentBefore") or {}
    after = metrics.get("after") or payload.get("componentAfter") or {}
    return before, after


def pick_widths(snapshot):
    metrics = snapshot.get("objectMetrics") or {}
    widths = {}
    for key, value in metrics.items():
        rect = value.get("rect") or {}
        if "width" in rect:
            widths[key] = round(rect["width"], 2)
    return widths


def summarize_snapshot(label, snapshot):
    dims = snapshot.get("dimensions") or {}
    bounds = snapshot.get("bounds") or {}
    props = snapshot.get("props") or {}
    grid = snapshot.get("gridMetrics") or {}
    return {
        "label": label,
        "dimensions.width": dims.get("width"),
        "bounds.width": round(bounds.get("width"), 3) if bounds.get("width") is not None else None,
        "grid.containerWidth": grid.get("containerWidth"),
        "grid.columnGapPx": grid.get("columnGapPx"),
        "objectWidths": pick_widths(snapshot),
        "labelWidthOverride": props.get("labelWidthOverride"),
        "inputWidthOverride": props.get("inputWidthOverride"),
        "helpWidthOverride": props.get("helpWidthOverride"),
    }


def main():
    component_id = None
    if len(sys.argv) > 1:
        component_id = sys.argv[1]

    db = SessionLocal()
    try:
        query = db.query(FrontendEvent).filter(FrontendEvent.EventType == "fieldshell.resize.commit")
        if component_id:
            query = query.filter(FrontendEvent.ComponentID == component_id)
        events = query.order_by(FrontendEvent.CreatedDate.desc()).limit(5).all()
        if not events:
            print("No fieldshell.resize.commit found.")
            return

        for event in events:
            before, after = get_snapshot(event)
            before_summary = summarize_snapshot("BEFORE", before)
            after_summary = summarize_snapshot("AFTER", after)
            print(f"\nCommit: {event.CreatedDate} component={event.ComponentID}")
            for summary in (before_summary, after_summary):
                print(f"  {summary['label']}")
                print(f"    dimensions.width: {summary['dimensions.width']}")
                print(f"    bounds.width: {summary['bounds.width']}")
                print(f"    grid.containerWidth: {summary['grid.containerWidth']}")
                print(f"    grid.columnGapPx: {summary['grid.columnGapPx']}")
                print(f"    objectWidths: {summary['objectWidths']}")
                print(f"    overrides: label={summary['labelWidthOverride']} input={summary['inputWidthOverride']} help={summary['helpWidthOverride']}")
    finally:
        db.close()


if __name__ == "__main__":
    main()

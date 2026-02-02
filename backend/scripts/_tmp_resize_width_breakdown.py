"""
Extract width breakdown from latest fieldshell.resize.commit metrics.
"""
import json
import sys
from pathlib import Path

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


def pick_object_metrics(snapshot):
    metrics = snapshot.get("objectMetrics") or {}
    widths = {}
    for key, value in metrics.items():
        rect = value.get("rect") or {}
        if "width" in rect:
            widths[key] = rect["width"]
    return widths


def pick_grid_metrics(snapshot):
    return snapshot.get("gridMetrics") or {}


def print_snapshot(label, snapshot):
    dims = snapshot.get("dimensions") or {}
    bounds = snapshot.get("bounds") or {}
    grid = pick_grid_metrics(snapshot)
    widths = pick_object_metrics(snapshot)
    props = snapshot.get("props") or {}
    canvas_metrics = snapshot.get("canvasMetrics") or {}
    canvas_bounds = snapshot.get("canvasBounds") or {}

    print(f"{label}:")
    print(f"  dimensions.width: {dims.get('width')}")
    print(f"  bounds.width: {bounds.get('width')}")
    print(f"  grid.containerWidth: {grid.get('containerWidth')}")
    print(f"  grid.columnGap: {grid.get('columnGap')}")
    print(f"  grid.columnGapPx: {grid.get('columnGapPx')}")
    print(f"  grid.paddingLeft/right: {grid.get('paddingLeft')} / {grid.get('paddingRight')}")
    print(f"  grid.borderLeft/right: {grid.get('borderLeft')} / {grid.get('borderRight')}")
    print(f"  objectWidths (rect): {widths}")
    print(f"  canvas.scale: {canvas_metrics.get('canvasScale')}")
    print(f"  canvas.screenToCanvasRatio: {canvas_metrics.get('screenToCanvasRatio')}")
    print(f"  canvas.bounds.width: {canvas_bounds.get('width')}")
    print(f"  props.labelWidthOverride: {props.get('labelWidthOverride')}")
    print(f"  props.inputWidthOverride: {props.get('inputWidthOverride')}")
    print(f"  props.helpWidthOverride: {props.get('helpWidthOverride')}")
    print("")


def main():
    component_id = None
    if len(sys.argv) > 1:
        component_id = sys.argv[1]

    db = SessionLocal()
    try:
        query = db.query(FrontendEvent).filter(FrontendEvent.EventType == "fieldshell.resize.commit")
        if component_id:
            query = query.filter(FrontendEvent.ComponentID == component_id)
        event = query.order_by(FrontendEvent.CreatedDate.desc()).first()
        if not event:
            print("No fieldshell.resize.commit found.")
            return

        before, after = get_snapshot(event)
        print(f"Commit event: {event.CreatedDate} component={event.ComponentID}")
        print_snapshot("BEFORE", before)
        print_snapshot("AFTER", after)
    finally:
        db.close()


if __name__ == "__main__":
    main()

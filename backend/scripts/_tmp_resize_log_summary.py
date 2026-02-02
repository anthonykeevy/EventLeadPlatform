"""
Summarize recent resize logs with before/after metrics.
"""
import json
import sys
from datetime import timedelta
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


def pick_widths(snapshot: dict) -> dict:
    object_widths = snapshot.get("objectWidths") or {}
    if object_widths:
        return {key: int(round(val)) for key, val in object_widths.items()}
    metrics = snapshot.get("objectMetrics") or {}
    widths = {}
    for key, value in metrics.items():
        rect = value.get("rect") or {}
        if "width" in rect:
            widths[key] = int(round(rect["width"]))
    return widths


def extract_snapshot_width(snapshot: dict) -> str:
    dimensions = snapshot.get("dimensions") or {}
    return str(dimensions.get("width") or "")


def main():
    limit = 200
    component_id = None
    for arg in sys.argv[1:]:
        if arg.startswith("--limit="):
            limit = int(arg.split("=", 1)[1])
        elif component_id is None:
            component_id = arg

    db = SessionLocal()
    try:
        base_query = db.query(FrontendEvent)
        if component_id:
            base_query = base_query.filter(FrontendEvent.ComponentID == component_id)

        commit_event = (
            base_query.filter(FrontendEvent.EventType == "fieldshell.resize.commit")
            .order_by(FrontendEvent.CreatedDate.desc())
            .first()
        )
        if not commit_event:
            print("No fieldshell.resize.commit events found.")
            return

        window_start = commit_event.CreatedDate - timedelta(seconds=10)
        window_end = commit_event.CreatedDate + timedelta(seconds=2)

        events = (
            db.query(FrontendEvent)
            .filter(FrontendEvent.SessionID == commit_event.SessionID)
            .filter(FrontendEvent.CreatedDate >= window_start)
            .filter(FrontendEvent.CreatedDate <= window_end)
            .order_by(FrontendEvent.CreatedDate.asc())
            .limit(limit)
            .all()
        )

        print(f"Component: {commit_event.ComponentID}")
        print(f"Session: {commit_event.SessionID}")
        print(f"Window: {window_start} -> {window_end}")
        print("")

        include_prefixes = (
            "resize.handle.",
            "fieldshell.resize.",
            "resize.preview.",
            "resize.commit.",
            "resize.width.",
            "resize.grid.",
        )
        for event in events:
            if not event.EventType.startswith(include_prefixes):
                continue
            payload = load_json(event.Payload)
            payload_component = None
            if payload.get("componentId"):
                payload_component = payload.get("componentId")
            elif payload.get("component") and isinstance(payload.get("component"), dict):
                payload_component = payload.get("component", {}).get("id")
            component_label = payload_component or event.ComponentID or "unknown"
            print(f"[{event.CreatedDate}] {event.EventType} component={component_label}")
            if event.EventType.startswith("resize.handle."):
                delta_width = payload.get("deltaWidth")
                has_preview = payload.get("hasPreview")
                current_width = payload.get("currentWidthPx")
                next_width = payload.get("nextWidth")
                print(f"  handle={payload.get('handle')}, deltaWidth={delta_width}, currentWidthPx={current_width}, nextWidth={next_width}, hasPreview={has_preview}")
            if event.EventType == "fieldshell.resize.preview":
                preview = payload.get("previewProps") or {}
                print(f"  previewWidth={preview.get('width')}, displayWidth={preview.get('displayWidth')}, deltaWidth={payload.get('deltaWidth')}")
            if event.EventType == "fieldshell.resize.commit":
                metrics = load_json(event.MetricsJson)
                before = (metrics.get("before") or payload.get("componentBefore") or {})
                after = (metrics.get("after") or payload.get("componentAfter") or {})
                before_width = extract_snapshot_width(before)
                after_width = extract_snapshot_width(after)
                before_obj = pick_widths(before)
                after_obj = pick_widths(after)
                print(f"  BEFORE width={before_width} objectWidths={before_obj}")
                print(f"  AFTER  width={after_width} objectWidths={after_obj}")
            print("")
    finally:
        db.close()


if __name__ == "__main__":
    main()

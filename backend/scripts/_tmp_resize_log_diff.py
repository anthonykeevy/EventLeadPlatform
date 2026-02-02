"""
Detailed before/after diff for latest fieldshell.resize.commit.
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


def diff_values(path, before, after, changes):
    if isinstance(before, dict) and isinstance(after, dict):
        keys = sorted(set(before.keys()) | set(after.keys()))
        for key in keys:
            diff_values(path + [key], before.get(key), after.get(key), changes)
        return
    if isinstance(before, list) and isinstance(after, list):
        max_len = max(len(before), len(after))
        for idx in range(max_len):
            b = before[idx] if idx < len(before) else None
            a = after[idx] if idx < len(after) else None
            diff_values(path + [f"[{idx}]"], b, a, changes)
        return
    if before != after:
        changes.append((".".join(path), before, after))


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

        payload = load_json(event.Payload)
        metrics = load_json(event.MetricsJson)
        before = metrics.get("before") or payload.get("componentBefore") or {}
        after = metrics.get("after") or payload.get("componentAfter") or {}

        changes = []
        diff_values(["root"], before, after, changes)

        print(f"Commit event: {event.CreatedDate} component={event.ComponentID}")
        print(f"Total changes: {len(changes)}")
        print("")
        for path, b, a in changes:
            print(f"{path}:")
            print(f"  before: {b}")
            print(f"  after:  {a}")
            print("")
    finally:
        db.close()


if __name__ == "__main__":
    main()

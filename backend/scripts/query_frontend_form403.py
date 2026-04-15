"""One-off: query log.FrontendEvent for builder session related to form 403."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
try:
    from common.database import engine
except ImportError:
    from sqlalchemy import create_engine

    engine = create_engine(os.environ["DATABASE_URL"])

# Match builder route for form id 403 (not HTTP 403 / unrelated "403" in URLs)
SQL = """
SELECT TOP 150
    FrontendEventID,
    EventType,
    Level,
    ComponentID,
    PageURL,
    ClientTimestamp,
    CreatedDate,
    CAST(Payload AS NVARCHAR(MAX)) AS Payload
FROM log.FrontendEvent
WHERE PageURL LIKE N'%/forms/403/%'
   OR PageURL LIKE N'%forms%403%builder%'
   OR CAST(Payload AS NVARCHAR(MAX)) LIKE N'%\"formId\":\"403\"%'
   OR CAST(Payload AS NVARCHAR(MAX)) LIKE N'%formId\": \"403\"%'
ORDER BY CreatedDate DESC
"""


def main() -> None:
    with engine.connect() as conn:
        rows = conn.execute(text(SQL)).fetchall()
    print(f"rows: {len(rows)}")
    print("\n=== All matching rows (summary) ===\n")
    for r in rows:
        eid, et, lvl, cid, url, cts, cr, payload = r
        pl = (payload or "")[:200]
        print(f"{eid} | {et} | {lvl} | {cid}")
        print(f"  url: {url}")
        print(f"  created: {cr}")
        print(f"  payload preview: {pl!r}")
        print()

    collisionish = []
    for r in rows:
        eid, et, lvl, cid, url, cts, cr, payload = r
        pl = payload or ""
        if any(
            k in (et or "").lower()
            for k in ("collision", "smartborder", "overlap", "boundary")
        ):
            collisionish.append(r)
        elif any(
            k in pl.lower()
            for k in ("collision", "smartborder", "overlap", "rect", "bounds")
        ):
            collisionish.append(r)

    print(f"\n=== Collision / smartborder / bounds related: {len(collisionish)} ===\n")
    for r in collisionish[:50]:
        eid, et, lvl, cid, url, cts, cr, payload = r
        print(f"--- {eid} | {et} | {lvl} | comp={cid}")
        print(f"    url: {url}")
        print(f"    created: {cr}")
        try:
            obj = json.loads(payload) if payload else {}
            # compact high-signal keys
            keys = list(obj.keys())[:20]
            print(f"    payload keys: {keys}")
            if "collisionDetails" in str(obj):
                print(f"    (has collisionDetails in payload)")
            if "objectMetrics" in str(obj) or "canvasRect" in str(obj):
                print(f"    (has geometry metrics)")
            snippet = json.dumps(obj, indent=2)[:2500]
            print(snippet)
        except json.JSONDecodeError:
            print((payload or "")[:1500])
        print()


if __name__ == "__main__":
    main()

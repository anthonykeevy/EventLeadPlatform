"""List recent log.FrontendEvent rows whose EventType mentions collision or smartborder."""

from __future__ import annotations

import sys
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.database import engine  # noqa: E402


def main() -> None:
    seen: set[int] = set()
    with engine.connect() as conn:
        for pattern in ("%collision%", "%smartborder%", "%fieldshell.collision%"):
            rows = conn.execute(
                text(
                    """
                SELECT TOP 40 FrontendEventID, EventType, Level, PageURL, CreatedDate
                FROM log.FrontendEvent
                WHERE EventType LIKE :pat
                ORDER BY CreatedDate DESC
                """
                ),
                {"pat": pattern},
            ).fetchall()
            print(f"\n=== EventType LIKE {pattern!r} -> {len(rows)} rows ===")
            for r in rows:
                eid = r[0]
                if eid in seen:
                    continue
                seen.add(eid)
                # SELECT: 0=FrontendEventID, 1=EventType, 2=Level, 3=PageURL, 4=CreatedDate
                print(f"{r[4]} | {r[1]} | {(r[3] or '')[:120]}")


if __name__ == "__main__":
    main()

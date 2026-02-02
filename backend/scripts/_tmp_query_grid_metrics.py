import json
import sys
from sqlalchemy import text

sys.path.insert(0, str(__file__).rsplit("\\", 2)[0])

from common.database import engine

QUERY = """
SELECT TOP 5 Payload, CreatedDate
FROM log.FrontendEvent
WHERE EventType = 'smartborder.calculate.gridObjects'
ORDER BY CreatedDate DESC
"""


def main() -> None:
    with engine.connect() as conn:
        rows = conn.execute(text(QUERY)).mappings().all()
    for row in rows:
        payload = json.loads(row["Payload"] or "{}")
        metrics = payload.get("gridObjectMetrics", [])
        simplified = [
            (m.get("id"), m.get("width"), m.get("height"))
            for m in metrics
        ]
        print(row["CreatedDate"], simplified)


if __name__ == "__main__":
    main()

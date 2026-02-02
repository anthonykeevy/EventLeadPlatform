import sys
sys.path.insert(0, 'C:\\Users\\tonyk\\OneDrive\\Projects\\EventLeadPlatform\\backend')

from common.database import SessionLocal
from models.log import FrontendEvent
import json

db = SessionLocal()
events = db.query(FrontendEvent).order_by(FrontendEvent.id.desc()).limit(200).all()

print("ID|Timestamp|EventType|Payload")
print("-" * 80)
for e in reversed(events):
    payload_str = json.dumps(e.payload) if e.payload else "null"
    print(f"{e.id}|{e.timestamp}|{e.event_type}|{payload_str}")

db.close()

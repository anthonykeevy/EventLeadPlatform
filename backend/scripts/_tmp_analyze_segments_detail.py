import sys
sys.path.insert(0, 'C:\\Users\\tonyk\\OneDrive\\Projects\\EventLeadPlatform\\backend')

from common.database import SessionLocal
from models.log import FrontendEvent
import json

db = SessionLocal()

# Get smartborder.path.calculated events (which have full segment details)
events = db.query(FrontendEvent).filter(
    FrontendEvent.EventType == 'smartborder.path.calculated'
).order_by(FrontendEvent.CreatedDate.desc()).limit(20).all()

print("=" * 100)
print("FULL SEGMENT DETAILS - Most Recent Events")
print("=" * 100)

for idx, event in enumerate(reversed(events[:5])):  # Show last 5
    payload = json.loads(event.Payload) if event.Payload else {}
    
    print(f"\n{'='*100}")
    print(f"Event #{idx+1} - Timestamp: {event.CreatedDate}")
    print(f"Component: {payload.get('componentId', 'unknown')}")
    print(f"{'='*100}")
    
    segments = payload.get('segments', [])
    for i, seg in enumerate(segments):
        source = seg.get('source', {})
        print(f"\nSegment {i+1}: {source.get('dataGridObject', 'unknown')}")
        print(f"  yStart: {seg.get('yStart')}")
        print(f"  yEnd: {seg.get('yEnd')}")
        print(f"  xLeft: {seg.get('xLeft')}")
        print(f"  xRight: {seg.get('xRight')}")
        print(f"  Height: {seg.get('yEnd', 0) - seg.get('yStart', 0):.2f}px")
        print(f"  Width: {seg.get('xRight', 0) - seg.get('xLeft', 0):.2f}px")
        print(f"  Source tag: {source.get('tag')}")

db.close()

import sys
sys.path.insert(0, 'C:\\Users\\tonyk\\OneDrive\\Projects\\EventLeadPlatform\\backend')

from common.database import SessionLocal
from models.log import FrontendEvent
import json

db = SessionLocal()

# Get the path.calculated event with full segment details
events = db.query(FrontendEvent).filter(
    FrontendEvent.EventType == 'smartborder.path.calculated'
).order_by(FrontendEvent.CreatedDate.desc()).limit(5).all()

print("=" * 100)
print("ALL SEGMENTS IN LATEST SMARTBORDER PATH")
print("=" * 100)

if events:
    event = events[0]
    payload = json.loads(event.Payload) if event.Payload else {}
    
    print(f"\nTimestamp: {event.CreatedDate}")
    print(f"Component: {payload.get('componentId')}")
    
    segments = payload.get('segments', [])
    print(f"\nTotal Segments: {len(segments)}")
    
    for i, seg in enumerate(segments):
        source = seg.get('source', {})
        obj_id = source.get('dataGridObject', 'unknown')
        
        yStart = seg.get('yStart', 0)
        yEnd = seg.get('yEnd', 0)
        height = yEnd - yStart
        
        print(f"\nSegment {i+1}: {obj_id}")
        print(f"  yStart: {yStart:.2f}")
        print(f"  yEnd: {yEnd:.2f}")
        print(f"  Height: {height:.2f}px")
        print(f"  Tag: {source.get('tag', 'unknown')}")

    # Show the overall bounds
    print("\n" + "=" * 100)
    print("OVERALL BOUNDS:")
    bounds = payload.get('bounds', {})
    print(f"  Min Y: {bounds.get('minY', 0):.2f}")
    print(f"  Max Y: {bounds.get('maxY', 0):.2f}")
    print(f"  Total Height: {bounds.get('maxY', 0) - bounds.get('minY', 0):.2f}px")

db.close()

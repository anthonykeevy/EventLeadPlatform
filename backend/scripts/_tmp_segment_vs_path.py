import sys
sys.path.insert(0, 'C:\\Users\\tonyk\\OneDrive\\Projects\\EventLeadPlatform\\backend')

from common.database import SessionLocal
from models.log import FrontendEvent
import json

db = SessionLocal()

# Get segment.created and path.calculated events from same timestamp
segment_events = db.query(FrontendEvent).filter(
    FrontendEvent.EventType == 'smartborder.segment.created'
).order_by(FrontendEvent.CreatedDate.desc()).limit(50).all()

path_events = db.query(FrontendEvent).filter(
    FrontendEvent.EventType == 'smartborder.path.calculated'
).order_by(FrontendEvent.CreatedDate.desc()).limit(20).all()

print("=" * 100)
print("SEGMENT CREATION vs FINAL PATH - INPUT HEIGHT COMPARISON")
print("=" * 100)

# Find a timestamp where we have both events
for path_event in path_events[:5]:
    path_payload = json.loads(path_event.Payload) if path_event.Payload else {}
    
    # Find segment.created events from same timestamp (within 50ms)
    matching_segments = []
    for seg_event in segment_events:
        if abs(path_event.ClientTimestamp - seg_event.ClientTimestamp) < 50:
            seg_payload = json.loads(seg_event.Payload) if seg_event.Payload else {}
            if seg_payload.get('objectId') == 'input':
                matching_segments.append((seg_event, seg_payload))
    
    if matching_segments:
        print(f"\nTimestamp: {path_event.CreatedDate} (Client: {path_event.ClientTimestamp})")
        
        # Show segment creation
        for seg_event, seg_payload in matching_segments[:1]:
            segment_data = seg_payload.get('segment', {})
            print(f"\n1. SEGMENT CREATED (smartborder.segment.created):")
            print(f"   yStart: {segment_data.get('yStart')}")
            print(f"   yEnd: {segment_data.get('yEnd')}")
            print(f"   Height: {segment_data.get('segmentHeight')}px")
        
        # Show final path
        segments = path_payload.get('segments', [])
        for seg in segments:
            source = seg.get('source', {})
            if source.get('dataGridObject') == 'input':
                print(f"\n2. FINAL PATH SEGMENT (smartborder.path.calculated):")
                print(f"   yStart: {seg.get('yStart')}")
                print(f"   yEnd: {seg.get('yEnd')}")
                print(f"   Height: {seg.get('yEnd', 0) - seg.get('yStart', 0)}px")
        
        print(f"\n   MATCH: {segment_data.get('segmentHeight') == (seg.get('yEnd', 0) - seg.get('yStart', 0))}")
        break

db.close()

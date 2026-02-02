import sys
sys.path.insert(0, 'C:\\Users\\tonyk\\OneDrive\\Projects\\EventLeadPlatform\\backend')

from common.database import SessionLocal
from models.log import FrontendEvent
import json

db = SessionLocal()

# Get the most recent SE drag capture run
events = db.query(FrontendEvent).filter(
    FrontendEvent.EventType.like('smartborder%')
).order_by(FrontendEvent.CreatedDate.desc()).limit(300).all()

print("=" * 100)
print("SMARTBORDER ANALYSIS - Most Recent SE Drag")
print("=" * 100)

# Group events by type
grid_objects_events = []
segments_events = []

for e in reversed(events):
    if 'gridObjects' in e.EventType:
        grid_objects_events.append(e)
    elif 'segments.final' in e.EventType:
        segments_events.append(e)

print(f"\nFound {len(grid_objects_events)} gridObjects events")
print(f"Found {len(segments_events)} segments.final events\n")

# Analyze the most recent drag sequence
if grid_objects_events:
    print("\n" + "=" * 100)
    print("GRID OBJECTS DURING DRAG (Label Width Tracking)")
    print("=" * 100)
    
    for i, event in enumerate(grid_objects_events[-10:]):  # Last 10 events
        payload = json.loads(event.Payload) if event.Payload else {}
        metrics = payload.get('gridObjectMetrics', [])
        
        print(f"\n[{i+1}] Timestamp: {event.CreatedDate} (Client: {event.ClientTimestamp})")
        print(f"    Component: {payload.get('componentId', 'unknown')}")
        
        for metric in metrics:
            if metric.get('id') == 'label':
                print(f"    LABEL: width={metric.get('width')}, height={metric.get('height')}")
            elif metric.get('id') == 'input':
                print(f"    INPUT: width={metric.get('width')}, height={metric.get('height')}")
            elif metric.get('id') == 'validation':
                print(f"    VALIDATION: width={metric.get('width')}, height={metric.get('height')}")

if segments_events:
    print("\n" + "=" * 100)
    print("SEGMENTS DURING DRAG (Showing Label Segment)")
    print("=" * 100)
    
    for i, event in enumerate(segments_events[-10:]):  # Last 10 events
        payload = json.loads(event.Payload) if event.Payload else {}
        
        print(f"\n[{i+1}] Timestamp: {event.CreatedDate}")
        print(f"    Component: {payload.get('componentId', 'unknown')}")
        print(f"    Segment Count: {payload.get('segmentCount', 0)}")
        print(f"    Sources: {payload.get('segmentSources', [])}")
        
        bounds = payload.get('bounds', {})
        print(f"    Bounds: minX={bounds.get('minX')}, maxX={bounds.get('maxX')}")
        print(f"            minY={bounds.get('minY')}, maxY={bounds.get('maxY')}")

db.close()

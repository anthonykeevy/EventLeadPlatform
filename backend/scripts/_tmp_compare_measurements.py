import sys
sys.path.insert(0, 'C:\\Users\\tonyk\\OneDrive\\Projects\\EventLeadPlatform\\backend')

from common.database import SessionLocal
from models.log import FrontendEvent
import json

db = SessionLocal()

# Get gridObjects and segment.created events from the same time
grid_events = db.query(FrontendEvent).filter(
    FrontendEvent.EventType == 'smartborder.calculate.gridObjects'
).order_by(FrontendEvent.CreatedDate.desc()).limit(5).all()

segment_events = db.query(FrontendEvent).filter(
    FrontendEvent.EventType == 'smartborder.segment.created'
).order_by(FrontendEvent.CreatedDate.desc()).limit(30).all()

print("=" * 100)
print("DOM MEASUREMENT vs SEGMENT CREATION COMPARISON")
print("=" * 100)

# Get the first gridObjects event
if grid_events:
    grid_payload = json.loads(grid_events[0].Payload) if grid_events[0].Payload else {}
    metrics = grid_payload.get('gridObjectMetrics', [])
    
    print(f"\n1. GRID OBJECTS MEASUREMENT (from getBoundingClientRect on node):")
    print(f"   Timestamp: {grid_events[0].CreatedDate}")
    
    for metric in metrics:
        if metric.get('id') == 'input':
            print(f"\n   INPUT:")
            print(f"     Node rect width: {metric.get('width')}")
            print(f"     Node rect height: {metric.get('height')}")
            print(f"     Target (getMeasurementTarget) width: {metric.get('targetWidth')}")
            print(f"     Target (getMeasurementTarget) height: {metric.get('targetHeight')}")

# Find a segment.created event for input from around the same time
print(f"\n2. SEGMENT CREATION (from getBoundingClientRect on target):")
for event in segment_events:
    payload = json.loads(event.Payload) if event.Payload else {}
    if payload.get('objectId') == 'input':
        print(f"   Timestamp: {event.CreatedDate}")
        raw = payload.get('rawRect', {})
        unscaled = payload.get('unscaled', {})
        print(f"\n   INPUT:")
        print(f"     Raw rect width: {raw.get('width')}")
        print(f"     Raw rect height: {raw.get('height')}")
        print(f"     Unscaled height: {unscaled.get('height')}")
        break

print("\n" + "=" * 100)
print("ANALYSIS:")
print("=" * 100)
print("The 'Node rect' is from the original node with data-grid-object='input'")
print("The 'Target rect' is from getMeasurementTarget (handles display:contents)")
print("The 'Raw rect' in segment creation is from the target element")
print("\nIf these don't match, getMeasurementTarget might be selecting wrong element")

db.close()

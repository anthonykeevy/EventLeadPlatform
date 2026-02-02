import sys
sys.path.insert(0, 'C:\\Users\\tonyk\\OneDrive\\Projects\\EventLeadPlatform\\backend')

from common.database import SessionLocal
from models.log import FrontendEvent
import json

db = SessionLocal()

# Get smartborder.path.calculated events
events = db.query(FrontendEvent).filter(
    FrontendEvent.EventType == 'smartborder.path.calculated'
).order_by(FrontendEvent.CreatedDate.desc()).limit(20).all()

print("=" * 100)
print("COMPARING SEGMENTS: DURING DRAG vs AFTER DROP")
print("=" * 100)

# Find events during drag (with isResizing=true) and after drop (isResizing=false)
during_drag = None
after_drop = None

# Get calculate.start events to check isResizing flag
calc_events = db.query(FrontendEvent).filter(
    FrontendEvent.EventType == 'smartborder.calculate.start'
).order_by(FrontendEvent.CreatedDate.desc()).limit(20).all()

# Build a map of timestamps to isResizing status
resize_status = {}
for calc_event in calc_events:
    calc_payload = json.loads(calc_event.Payload) if calc_event.Payload else {}
    resize_status[calc_event.ClientTimestamp] = calc_payload.get('isResizing', False)

# Now find path.calculated events during and after drag
for event in reversed(events[:10]):
    payload = json.loads(event.Payload) if event.Payload else {}
    is_resizing = resize_status.get(event.ClientTimestamp, None)
    
    if is_resizing and during_drag is None:
        during_drag = (event, payload)
    elif is_resizing == False and after_drop is None:
        after_drop = (event, payload)
    
    if during_drag and after_drop:
        break

if during_drag:
    event, payload = during_drag
    print("\n1. DURING DRAG (isResizing=true)")
    print(f"   Timestamp: {event.CreatedDate}")
    print(f"   Component: {payload.get('componentId')}")
    
    segments = payload.get('segments', [])
    print(f"   Segment Count: {len(segments)}")
    
    for seg in segments:
        source = seg.get('source', {})
        obj_id = source.get('dataGridObject', 'unknown')
        yStart = seg.get('yStart', 0)
        yEnd = seg.get('yEnd', 0)
        print(f"   - {obj_id}: yStart={yStart:.2f}, yEnd={yEnd:.2f}, height={yEnd-yStart:.2f}px")
    
    bounds = payload.get('bounds', {})
    print(f"   Overall Height: {bounds.get('maxY', 0) - bounds.get('minY', 0):.2f}px")

if after_drop:
    event, payload = after_drop
    print("\n2. AFTER DROP (isResizing=false)")
    print(f"   Timestamp: {event.CreatedDate}")
    print(f"   Component: {payload.get('componentId')}")
    
    segments = payload.get('segments', [])
    print(f"   Segment Count: {len(segments)}")
    
    for seg in segments:
        source = seg.get('source', {})
        obj_id = source.get('dataGridObject', 'unknown')
        yStart = seg.get('yStart', 0)
        yEnd = seg.get('yEnd', 0)
        print(f"   - {obj_id}: yStart={yStart:.2f}, yEnd={yEnd:.2f}, height={yEnd-yStart:.2f}px")
    
    bounds = payload.get('bounds', {})
    print(f"   Overall Height: {bounds.get('maxY', 0) - bounds.get('minY', 0):.2f}px")

print("\n" + "=" * 100)
print("KEY DIFFERENCE:")
print("=" * 100)
if during_drag and after_drop:
    _, drag_payload = during_drag
    _, drop_payload = after_drop
    
    drag_sources = [s.get('source', {}).get('dataGridObject') for s in drag_payload.get('segments', [])]
    drop_sources = [s.get('source', {}).get('dataGridObject') for s in drop_payload.get('segments', [])]
    
    if 'synthetic-preview' in drag_sources and 'synthetic-preview' not in drop_sources:
        print("During drag: 'synthetic-preview' segment is added")
        print("After drop: 'synthetic-preview' segment is removed")
        print("\nThe synthetic-preview segment extends to full component height!")
        print("This is what creates the 'extra space' below validation during drag.")

db.close()

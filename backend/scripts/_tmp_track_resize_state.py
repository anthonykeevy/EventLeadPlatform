import sys
sys.path.insert(0, 'C:\\Users\\tonyk\\OneDrive\\Projects\\EventLeadPlatform\\backend')

from common.database import SessionLocal
from models.log import FrontendEvent
import json

db = SessionLocal()

# Get all calculate.start events to understand isResizing context
calc_events = db.query(FrontendEvent).filter(
    FrontendEvent.EventType == 'smartborder.calculate.start'
).order_by(FrontendEvent.CreatedDate.desc()).limit(30).all()

print("=" * 100)
print("TRACKING isResizing FLAG OVER TIME")
print("=" * 100)

for event in reversed(calc_events[:15]):
    payload = json.loads(event.Payload) if event.Payload else {}
    
    print(f"\nTimestamp: {event.CreatedDate} (Client: {event.ClientTimestamp})")
    print(f"  isResizing: {payload.get('isResizing')}")
    print(f"  parent height: {payload.get('parent', {}).get('height')}px")

# Now get gridObjects events to see actual DOM measurements
print("\n\n" + "=" * 100)
print("INPUT DOM HEIGHT DURING DIFFERENT STATES")
print("=" * 100)

grid_events = db.query(FrontendEvent).filter(
    FrontendEvent.EventType == 'smartborder.calculate.gridObjects'
).order_by(FrontendEvent.CreatedDate.desc()).limit(20).all()

# Cross-reference with calc events to get isResizing status
for grid_event in reversed(grid_events[:10]):
    grid_payload = json.loads(grid_event.Payload) if grid_event.Payload else {}
    
    # Find matching calc event by timestamp (within 100ms)
    matching_calc = None
    for calc_event in calc_events:
        if abs(grid_event.ClientTimestamp - calc_event.ClientTimestamp) < 100:
            matching_calc = calc_event
            break
    
    is_resizing = None
    if matching_calc:
        calc_payload = json.loads(matching_calc.Payload) if matching_calc.Payload else {}
        is_resizing = calc_payload.get('isResizing')
    
    metrics = grid_payload.get('gridObjectMetrics', [])
    for metric in metrics:
        if metric.get('id') == 'input':
            print(f"\nTimestamp: {grid_event.CreatedDate} (Client: {grid_event.ClientTimestamp})")
            print(f"  isResizing: {is_resizing}")
            print(f"  Input DOM height (scaled): {metric.get('height')}px")
            print(f"  Input DOM height (target): {metric.get('targetHeight')}px")

db.close()

import sys
sys.path.insert(0, 'C:\\Users\\tonyk\\OneDrive\\Projects\\EventLeadPlatform\\backend')

from common.database import SessionLocal
from models.log import FrontendEvent
import json

db = SessionLocal()

# Get gridObjects events with full metrics
events = db.query(FrontendEvent).filter(
    FrontendEvent.EventType == 'smartborder.calculate.gridObjects'
).order_by(FrontendEvent.CreatedDate.desc()).limit(10).all()

print("=" * 100)
print("INPUT OBJECT HEIGHT ANALYSIS")
print("=" * 100)

for idx, event in enumerate(reversed(events[:3])):  # Last 3 events
    payload = json.loads(event.Payload) if event.Payload else {}
    
    print(f"\nEvent #{idx+1} - Timestamp: {event.CreatedDate}")
    print(f"Component: {payload.get('componentId', 'unknown')}")
    
    metrics = payload.get('gridObjectMetrics', [])
    for metric in metrics:
        if metric.get('id') == 'input':
            print(f"\nINPUT OBJECT:")
            print(f"  display: {metric.get('display')}")
            print(f"  width: {metric.get('width')}")
            print(f"  height: {metric.get('height')}")
            print(f"  targetTag: {metric.get('targetTag')}")
            print(f"  targetWidth: {metric.get('targetWidth')}")
            print(f"  targetHeight: {metric.get('targetHeight')}")

# Now get the path.calculated events to see the segment created from input
events2 = db.query(FrontendEvent).filter(
    FrontendEvent.EventType == 'smartborder.path.calculated'
).order_by(FrontendEvent.CreatedDate.desc()).limit(5).all()

print("\n" + "=" * 100)
print("INPUT SEGMENT IN SMARTBORDER PATH")
print("=" * 100)

for idx, event in enumerate(reversed(events2[:2])):  # Last 2 events
    payload = json.loads(event.Payload) if event.Payload else {}
    
    print(f"\nEvent #{idx+1} - Timestamp: {event.CreatedDate}")
    segments = payload.get('segments', [])
    for seg in segments:
        source = seg.get('source', {})
        if source.get('dataGridObject') == 'input':
            print(f"\nINPUT SEGMENT:")
            print(f"  yStart: {seg.get('yStart')}")
            print(f"  yEnd: {seg.get('yEnd')}")
            print(f"  Segment Height: {seg.get('yEnd', 0) - seg.get('yStart', 0):.2f}px")
            print(f"  xLeft: {seg.get('xLeft')}")
            print(f"  xRight: {seg.get('xRight')}")
            print(f"  Segment Width: {seg.get('xRight', 0) - seg.get('xLeft', 0):.2f}px")

db.close()

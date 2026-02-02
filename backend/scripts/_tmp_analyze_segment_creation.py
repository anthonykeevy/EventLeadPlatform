import sys
sys.path.insert(0, 'C:\\Users\\tonyk\\OneDrive\\Projects\\EventLeadPlatform\\backend')

from common.database import SessionLocal
from models.log import FrontendEvent
import json

db = SessionLocal()

# Get the most recent smartborder.segment.created events
events = db.query(FrontendEvent).filter(
    FrontendEvent.EventType == 'smartborder.segment.created'
).order_by(FrontendEvent.CreatedDate.desc()).limit(20).all()

print("=" * 100)
print("SEGMENT CREATION ANALYSIS - INPUT OBJECT")
print("=" * 100)

# Find an input segment during drag
for event in reversed(events):
    payload = json.loads(event.Payload) if event.Payload else {}
    
    if payload.get('objectId') == 'input':
        print(f"\nTimestamp: {event.CreatedDate}")
        print(f"Component: {payload.get('componentId')}")
        print(f"\nRAW DOM Rect (getBoundingClientRect):")
        raw = payload.get('rawRect', {})
        print(f"  height: {raw.get('height')}px")
        
        print(f"\nScale:")
        scale = payload.get('scale', {})
        print(f"  scaleY: {scale.get('y')}")
        
        print(f"\nUnscaled Coordinates:")
        unscaled = payload.get('unscaled', {})
        print(f"  top: {unscaled.get('top')}")
        print(f"  height: {unscaled.get('height')}")
        print(f"  bottom: {unscaled.get('bottom')}")
        
        print(f"\nWrapper Offset:")
        offset = payload.get('wrapperOffset', {})
        print(f"  y: {offset.get('y')}")
        
        print(f"\nPadding:")
        print(f"  p: {payload.get('padding')}")
        
        print(f"\nFINAL SEGMENT:")
        segment = payload.get('segment', {})
        print(f"  yStart: {segment.get('yStart')}")
        print(f"  yEnd: {segment.get('yEnd')}")
        print(f"  segmentHeight: {segment.get('segmentHeight')}")
        
        print("\n" + "=" * 100)
        print("CALCULATION CHECK:")
        print("=" * 100)
        expected_height = unscaled.get('height', 0)
        actual_segment_height = segment.get('segmentHeight', 0)
        print(f"Expected unscaled height: {expected_height}px")
        print(f"Actual segment height (including padding): {actual_segment_height}px")
        print(f"Segment height without padding (2*5px): {actual_segment_height - 10}px")
        print(f"\nDISCREPANCY: {(actual_segment_height - 10) - expected_height:.2f}px")
        
        # Only show first input segment
        break

db.close()

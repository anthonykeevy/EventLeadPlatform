import sys
sys.path.insert(0, 'C:\\Users\\tonyk\\OneDrive\\Projects\\EventLeadPlatform\\backend')

from common.database import SessionLocal
from models.log import FrontendEvent
import json

db = SessionLocal()

# Get all corner commit logs (start + complete pairs)
events = db.query(FrontendEvent).filter(
    FrontendEvent.EventType.in_(['resize.corner.commit.start', 'resize.corner.commit.complete'])
).order_by(FrontendEvent.CreatedDate.desc()).limit(200).all()

print("=" * 120)
print("RESIZE DISCREPANCY ANALYSIS WITH CONSTRAINT DETECTION")
print("=" * 120)

# Group by handle and analyze constraints
handle_analysis = {}

# Pair start/complete events
events_by_time = sorted(events, key=lambda e: e.CreatedDate)
pairs = []
for i in range(0, len(events_by_time) - 1):
    if events_by_time[i].EventType == 'resize.corner.commit.start' and \
       events_by_time[i+1].EventType == 'resize.corner.commit.complete':
        pairs.append((events_by_time[i], events_by_time[i+1]))

print(f"\nFound {len(pairs)} complete resize operations\n")

for start_event, complete_event in pairs:
    start_payload = json.loads(start_event.Payload) if start_event.Payload else {}
    complete_payload = json.loads(complete_event.Payload) if complete_event.Payload else {}
    
    handle = start_payload.get('handle', 'unknown')
    
    if handle not in handle_analysis:
        handle_analysis[handle] = {
            'operations': [],
            'constraint_hit_count': 0,
            'clean_operations': 0,
        }
    
    # Extract data
    mouse = start_payload.get('mouse', {})
    deltaX = mouse.get('deltaX', 0)
    deltaY = mouse.get('deltaY', 0)
    
    current = start_payload.get('current', {})
    expected = start_payload.get('expected', {})
    final = complete_payload.get('final', {})
    discrepancy = complete_payload.get('discrepancy', {})
    match_flags = complete_payload.get('match', {})
    
    preview = start_payload.get('preview', {})
    equivalent = start_payload.get('equivalent', {})
    h_handle = equivalent.get('horizontalHandle', '')
    v_handle = equivalent.get('verticalHandle', '')
    
    # Analyze constraints
    constraints_hit = []
    
    # Check width constraints
    width_discrepancy = discrepancy.get('width', 0)
    if abs(width_discrepancy) > 1:
        # Check if it's due to min width constraint
        final_width = final.get('width', 0)
        expected_width = expected.get('width', 0)
        
        # If final width is consistently smaller, might be hitting min constraint
        if width_discrepancy < -5:
            constraints_hit.append(f'WIDTH: Final {final_width:.1f}px < Expected {expected_width:.1f}px (delta: {width_discrepancy:.1f}px)')
    
    # Check position constraints
    pos_disc = discrepancy.get('position', {})
    pos_x_disc = pos_disc.get('x', 0)
    pos_y_disc = pos_disc.get('y', 0)
    
    if abs(pos_x_disc) > 1:
        constraints_hit.append(f'POSITION X: {pos_x_disc:+.1f}px discrepancy')
    
    if abs(pos_y_disc) > 1:
        constraints_hit.append(f'POSITION Y: {pos_y_disc:+.1f}px discrepancy')
    
    # Determine if this is a "clean" operation (no constraints violated)
    is_clean = len(constraints_hit) == 0
    
    operation_data = {
        'handle': handle,
        'mouse_delta': {'x': deltaX, 'y': deltaY},
        'discrepancy': discrepancy,
        'constraints_hit': constraints_hit,
        'is_clean': is_clean,
        'match_flags': match_flags,
        'equivalent_handles': {'h': h_handle, 'v': v_handle},
    }
    
    handle_analysis[handle]['operations'].append(operation_data)
    if not is_clean:
        handle_analysis[handle]['constraint_hit_count'] += 1
    else:
        handle_analysis[handle]['clean_operations'] += 1

# Print analysis
print("\n" + "=" * 120)
print("SUMMARY BY HANDLE")
print("=" * 120)

for handle in sorted(handle_analysis.keys()):
    data = handle_analysis[handle]
    ops = data['operations']
    
    print(f"\n{'='*120}")
    print(f"HANDLE: {handle.upper()}")
    print(f"{'='*120}")
    print(f"Total operations: {len(ops)}")
    print(f"Operations with constraints hit: {data['constraint_hit_count']}")
    print(f"Clean operations (no constraints): {data['clean_operations']}")
    
    # Analyze clean operations separately
    clean_ops = [op for op in ops if op['is_clean']]
    constrained_ops = [op for op in ops if not op['is_clean']]
    
    if clean_ops:
        print(f"\n--- CLEAN OPERATIONS (no constraints) ---")
        clean_width_discs = [op['discrepancy'].get('width', 0) for op in clean_ops]
        clean_x_discs = [op['discrepancy'].get('position', {}).get('x', 0) for op in clean_ops]
        clean_y_discs = [op['discrepancy'].get('position', {}).get('y', 0) for op in clean_ops]
        
        print(f"  Width discrepancy: avg={sum(clean_width_discs)/len(clean_width_discs):.2f}px, "
              f"max={max(abs(d) for d in clean_width_discs):.2f}px, "
              f"range=[{min(clean_width_discs):.2f}, {max(clean_width_discs):.2f}]")
        print(f"  Position X discrepancy: avg={sum(clean_x_discs)/len(clean_x_discs):.2f}px, "
              f"max={max(abs(d) for d in clean_x_discs):.2f}px, "
              f"range=[{min(clean_x_discs):.2f}, {max(clean_x_discs):.2f}]")
        print(f"  Position Y discrepancy: avg={sum(clean_y_discs)/len(clean_y_discs):.2f}px, "
              f"max={max(abs(d) for d in clean_y_discs):.2f}px, "
              f"range=[{min(clean_y_discs):.2f}, {max(clean_y_discs):.2f}]")
    
    if constrained_ops:
        print(f"\n--- CONSTRAINED OPERATIONS ---")
        for i, op in enumerate(constrained_ops, 1):
            print(f"\n  Operation {i}:")
            print(f"    Mouse delta: x={op['mouse_delta']['x']:.1f}px, y={op['mouse_delta']['y']:.1f}px")
            print(f"    Constraints hit:")
            for constraint in op['constraints_hit']:
                print(f"      - {constraint}")

print("\n" + "=" * 120)
print("INTERPRETATION")
print("=" * 120)
print("""
This analysis separates resize operations into two categories:

1. CLEAN OPERATIONS: No apparent constraints hit (discrepancies < 1px in all dimensions)
   - These should theoretically have zero discrepancy
   - Any discrepancy here represents unexpected behavior

2. CONSTRAINED OPERATIONS: One or more discrepancies > 1px
   - Could be due to min/max width/height limits
   - Could be due to collision detection
   - Could be due to canvas boundary constraints
   - Could be due to gap constraints (labelGap, inputHelpGap)

Next step: Add detailed constraint tracking to the resize logic itself to log:
- Which specific constraint was applied (minInputWidth, maxInputHeight, etc.)
- The constraint value that was enforced
- The requested value that was clamped
""")

db.close()

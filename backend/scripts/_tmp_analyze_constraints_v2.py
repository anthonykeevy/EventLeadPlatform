import sys
sys.path.insert(0, 'C:\\Users\\tonyk\\OneDrive\\Projects\\EventLeadPlatform\\backend')

from common.database import SessionLocal
from models.log import FrontendEvent
import json

db = SessionLocal()

print("=" * 120)
print("CONSTRAINT-AWARE RESIZE ANALYSIS (Using Agent Logging System)")
print("=" * 120)

# Get corner commit logs (start + complete pairs)
corner_events = db.query(FrontendEvent).filter(
    FrontendEvent.EventType.in_(['resize.corner.commit.start', 'resize.corner.commit.complete'])
).order_by(FrontendEvent.CreatedDate.desc()).limit(200).all()

# Get constraint logs (width + vertical)
constraint_events = db.query(FrontendEvent).filter(
    FrontendEvent.EventType.in_(['resize.constraints.width', 'resize.constraints.vertical'])
).order_by(FrontendEvent.CreatedDate.desc()).limit(200).all()

# Pair start/complete events
corner_events_by_time = sorted(corner_events, key=lambda e: e.CreatedDate)
pairs = []
for i in range(0, len(corner_events_by_time) - 1):
    if corner_events_by_time[i].EventType == 'resize.corner.commit.start' and \
       corner_events_by_time[i+1].EventType == 'resize.corner.commit.complete':
        pairs.append((corner_events_by_time[i], corner_events_by_time[i+1]))

print(f"\nFound {len(pairs)} complete resize operations")
print(f"Found {len(constraint_events)} constraint violation events\n")

# Build map of constraints by component/timestamp
constraints_by_component = {}
for event in constraint_events:
    payload = json.loads(event.Payload) if event.Payload else {}
    comp_id = payload.get('componentId', 'unknown')
    timestamp = event.CreatedDate.timestamp()
    
    if comp_id not in constraints_by_component:
        constraints_by_component[comp_id] = []
    
    constraints_by_component[comp_id].append({
        'timestamp': timestamp,
        'event_type': event.EventType,
        'handle': payload.get('handle', '?'),
        'constraints': payload.get('constraintsApplied', []),
        'payload': payload,
    })

# Group by handle and analyze
handle_analysis = {}

for start_event, complete_event in pairs:
    start_payload = json.loads(start_event.Payload) if start_event.Payload else {}
    complete_payload = json.loads(complete_event.Payload) if complete_event.Payload else {}
    
    handle = start_payload.get('handle', 'unknown')
    comp_id = start_payload.get('componentId', 'unknown')
    
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
    
    discrepancy = complete_payload.get('discrepancy', {})
    match_flags = complete_payload.get('match', {})
    
    # Check if this operation hit constraints
    # Look for constraint events within 1 second of this operation
    op_timestamp = start_event.CreatedDate.timestamp()
    matching_constraints = []
    
    if comp_id in constraints_by_component:
        for constraint in constraints_by_component[comp_id]:
            time_diff = abs(constraint['timestamp'] - op_timestamp)
            if time_diff < 1.0:  # Within 1 second
                matching_constraints.extend(constraint['constraints'])
    
    # Analyze discrepancies
    width_disc = discrepancy.get('width', 0)
    pos_disc = discrepancy.get('position', {})
    pos_x_disc = pos_disc.get('x', 0)
    pos_y_disc = pos_disc.get('y', 0)
    
    # Determine if clean (no constraints AND no discrepancies)
    has_discrepancy = (abs(width_disc) > 1) or (abs(pos_x_disc) > 1) or (abs(pos_y_disc) > 1)
    is_clean = not has_discrepancy
    
    operation_data = {
        'handle': handle,
        'mouse_delta': {'x': deltaX, 'y': deltaY},
        'discrepancy': discrepancy,
        'constraints_applied': matching_constraints,
        'is_clean': is_clean,
        'match_flags': match_flags,
    }
    
    handle_analysis[handle]['operations'].append(operation_data)
    if not is_clean:
        handle_analysis[handle]['constraint_hit_count'] += 1
    else:
        handle_analysis[handle]['clean_operations'] += 1

# Print analysis
print("\n" + "=" * 120)
print("SUMMARY BY HANDLE (WITH CONSTRAINT TRACKING)")
print("=" * 120)

for handle in sorted(handle_analysis.keys()):
    data = handle_analysis[handle]
    ops = data['operations']
    
    print(f"\n{'='*120}")
    print(f"HANDLE: {handle.upper()}")
    print(f"{'='*120}")
    print(f"Total operations: {len(ops)}")
    print(f"Operations with discrepancies: {data['constraint_hit_count']}")
    print(f"Clean operations (no discrepancies): {data['clean_operations']}")
    
    # Analyze clean operations separately
    clean_ops = [op for op in ops if op['is_clean']]
    constrained_ops = [op for op in ops if not op['is_clean']]
    
    if clean_ops:
        print(f"\n--- CLEAN OPERATIONS (0px discrepancy) ---")
        clean_width_discs = [op['discrepancy'].get('width', 0) for op in clean_ops]
        clean_x_discs = [op['discrepancy'].get('position', {}).get('x', 0) for op in clean_ops]
        clean_y_discs = [op['discrepancy'].get('position', {}).get('y', 0) for op in clean_ops]
        
        print(f"  Count: {len(clean_ops)}")
        print(f"  Width discrepancy: avg={sum(clean_width_discs)/len(clean_width_discs):.2f}px, "
              f"max={max(abs(d) for d in clean_width_discs):.2f}px")
        print(f"  Position X discrepancy: avg={sum(clean_x_discs)/len(clean_x_discs):.2f}px, "
              f"max={max(abs(d) for d in clean_x_discs):.2f}px")
        print(f"  Position Y discrepancy: avg={sum(clean_y_discs)/len(clean_y_discs):.2f}px, "
              f"max={max(abs(d) for d in clean_y_discs):.2f}px")
        print(f"  --> All clean operations should have 0.00px discrepancy (indicates perfect implementation)")
    
    if constrained_ops:
        print(f"\n--- OPERATIONS WITH DISCREPANCIES ---")
        for i, op in enumerate(constrained_ops, 1):
            print(f"\n  Operation {i}:")
            print(f"    Mouse delta: x={op['mouse_delta']['x']:.1f}px, y={op['mouse_delta']['y']:.1f}px")
            
            disc = op['discrepancy']
            print(f"    Discrepancies:")
            if abs(disc.get('width', 0)) > 1:
                print(f"      - Width: {disc.get('width', 0):+.1f}px")
            if abs(disc.get('position', {}).get('x', 0)) > 1:
                print(f"      - Position X: {disc.get('position', {}).get('x', 0):+.1f}px")
            if abs(disc.get('position', {}).get('y', 0)) > 1:
                print(f"      - Position Y: {disc.get('position', {}).get('y', 0):+.1f}px")
            
            if op['constraints_applied']:
                print(f"    Constraints applied (explains discrepancy):")
                for constraint in op['constraints_applied']:
                    print(f"      - {constraint}")
            else:
                print(f"    [!] NO CONSTRAINTS LOGGED - This discrepancy needs investigation!")

print("\n" + "=" * 120)
print("CONSTRAINT EVENTS SUMMARY")
print("=" * 120)

if constraint_events:
    print(f"\nTotal constraint events logged: {len(constraint_events)}")
    
    # Group by type
    width_constraints = [e for e in constraint_events if e.EventType == 'resize.constraints.width']
    vertical_constraints = [e for e in constraint_events if e.EventType == 'resize.constraints.vertical']
    
    print(f"  Width constraints: {len(width_constraints)}")
    print(f"  Vertical constraints: {len(vertical_constraints)}")
    
    # Show recent examples
    print(f"\nRecent constraint violations:")
    for event in constraint_events[:5]:
        payload = json.loads(event.Payload) if event.Payload else {}
        print(f"\n  [{event.EventType}] - Component: {payload.get('componentId', '?')}")
        print(f"    Handle: {payload.get('handle', '?')}")
        for constraint in payload.get('constraintsApplied', []):
            print(f"    - {constraint}")
else:
    print("\n[!] No constraint events found in database!")
    print("This means either:")
    print("1. No resizes have hit constraints yet (all operations were clean)")
    print("2. Frontend logging is not sending events to backend")
    print("3. Need to perform test resizes with the updated logging code")

print("\n" + "=" * 120)
print("INTERPRETATION")
print("=" * 120)
print("""
This analysis uses the Agent Logging System to separate resize operations into:

1. CLEAN OPERATIONS: No discrepancies (< 1px in all dimensions)
   - These operations had no constraints applied
   - Should have 0.00px discrepancy in all dimensions
   - Any discrepancy here indicates a bug in the implementation

2. CONSTRAINED OPERATIONS: Has discrepancies (> 1px in any dimension)
   - Check if matching constraint events explain the discrepancy
   - If constraints are logged, discrepancy is EXPECTED (not a bug)
   - If NO constraints logged, discrepancy needs investigation

To extract constraint logs:
python backend/enhanced_diagnostic_logs.py --frontend-only --frontend-filter "resize.constraints" --limit 20

To extract corner commit logs:
python backend/enhanced_diagnostic_logs.py --frontend-only --frontend-filter "resize.corner.commit" --limit 20
""")

db.close()

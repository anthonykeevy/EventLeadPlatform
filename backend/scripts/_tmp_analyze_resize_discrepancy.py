import sys
sys.path.insert(0, 'C:\\Users\\tonyk\\OneDrive\\Projects\\EventLeadPlatform\\backend')

from common.database import SessionLocal
from models.log import FrontendEvent
import json

db = SessionLocal()

# Get all corner commit complete events
events = db.query(FrontendEvent).filter(
    FrontendEvent.EventType == 'resize.corner.commit.complete'
).order_by(FrontendEvent.CreatedDate.desc()).limit(100).all()

print("=" * 100)
print("CORNER & EDGE RESIZE DISCREPANCY ANALYSIS")
print("=" * 100)

# Group by handle
handle_stats = {}

for event in reversed(events):
    payload = json.loads(event.Payload) if event.Payload else {}
    
    handle = payload.get('handle', 'unknown')
    discrepancy = payload.get('discrepancy', {})
    match_flags = payload.get('match', {})
    
    if handle not in handle_stats:
        handle_stats[handle] = {
            'count': 0,
            'position_x_errors': [],
            'position_y_errors': [],
            'width_errors': [],
            'perfect_matches': 0,
        }
    
    stats = handle_stats[handle]
    stats['count'] += 1
    
    pos_disc = discrepancy.get('position', {})
    width_disc = discrepancy.get('width', 0)
    
    stats['position_x_errors'].append(pos_disc.get('x', 0))
    stats['position_y_errors'].append(pos_disc.get('y', 0))
    stats['width_errors'].append(width_disc)
    
    if match_flags.get('positionX') and match_flags.get('positionY') and match_flags.get('width'):
        stats['perfect_matches'] += 1

print(f"\nTotal resize operations captured: {len(events)}")
print(f"Handles tested: {', '.join(sorted(handle_stats.keys()))}\n")

# Print summary for each handle
for handle in sorted(handle_stats.keys()):
    stats = handle_stats[handle]
    
    print(f"\n{'='*100}")
    print(f"HANDLE: {handle.upper()}")
    print(f"{'='*100}")
    print(f"Total operations: {stats['count']}")
    print(f"Perfect matches (within 1px): {stats['perfect_matches']} ({stats['perfect_matches']/stats['count']*100:.1f}%)")
    
    # Calculate averages and ranges
    avg_x = sum(stats['position_x_errors']) / len(stats['position_x_errors']) if stats['position_x_errors'] else 0
    avg_y = sum(stats['position_y_errors']) / len(stats['position_y_errors']) if stats['position_y_errors'] else 0
    avg_width = sum(stats['width_errors']) / len(stats['width_errors']) if stats['width_errors'] else 0
    
    max_x = max(abs(e) for e in stats['position_x_errors']) if stats['position_x_errors'] else 0
    max_y = max(abs(e) for e in stats['position_y_errors']) if stats['position_y_errors'] else 0
    max_width = max(abs(e) for e in stats['width_errors']) if stats['width_errors'] else 0
    
    print(f"\nPosition X Discrepancy:")
    print(f"  Average: {avg_x:+.2f}px")
    print(f"  Max: {max_x:.2f}px")
    print(f"  Range: [{min(stats['position_x_errors']):.2f}, {max(stats['position_x_errors']):.2f}]")
    
    print(f"\nPosition Y Discrepancy:")
    print(f"  Average: {avg_y:+.2f}px")
    print(f"  Max: {max_y:.2f}px")
    print(f"  Range: [{min(stats['position_y_errors']):.2f}, {max(stats['position_y_errors']):.2f}]")
    
    print(f"\nWidth Discrepancy:")
    print(f"  Average: {avg_width:+.2f}px")
    print(f"  Max: {max_width:.2f}px")
    print(f"  Range: [{min(stats['width_errors']):.2f}, {max(stats['width_errors']):.2f}]")

print("\n" + "="*100)
print("INTERPRETATION:")
print("="*100)
print("- Position X: Affects horizontal placement (should be 0 for E handles, may vary for W)")
print("- Position Y: Affects vertical placement (should be 0 for S handles, may vary for N)")
print("- Width: Difference between expected and final width")
print("- Perfect match: All discrepancies < 1px")

db.close()

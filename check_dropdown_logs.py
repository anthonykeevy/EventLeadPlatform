import pyodbc
import json
from datetime import datetime, timedelta

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=EventLeadPlatform;Trusted_Connection=yes;')
cursor = conn.cursor()

print("=" * 80)
print("DROPDOWN COMPONENT VALIDATION LOGS")
print("=" * 80)

# 1. Check for dropdown width calculation events
print("\n" + "=" * 80)
print("1. DROPDOWN WIDTH CALCULATIONS")
print("=" * 80)
cursor.execute("""
SELECT TOP 30 EventType, Payload, CreatedDate 
FROM log.FrontendEvent 
WHERE EventType LIKE '%dropdown.width%'
ORDER BY CreatedDate DESC
""")

width_events = cursor.fetchall()
if width_events:
    print(f"\nFound {len(width_events)} dropdown width events:\n")
    for idx, row in enumerate(width_events, 1):
        print(f"\n--- Event #{idx}: {row[0]} at {row[2]} ---")
        try:
            data = json.loads(row[1])
            print(json.dumps(data, indent=2))
        except:
            print(row[1][:500] if row[1] else "No payload")
else:
    print("WARNING: No dropdown width calculation events found")
    print("   This means:")
    print("   - Dropdown component hasn't been rendered yet, OR")
    print("   - Logging isn't working (check frontend .env settings)")

# 2. Check for component creation/drop events (to find dropdown components)
print("\n" + "=" * 80)
print("2. DROPDOWN COMPONENT CREATION/DROP EVENTS")
print("=" * 80)
cursor.execute("""
SELECT TOP 20 EventType, Payload, CreatedDate 
FROM log.FrontendEvent 
WHERE (EventType LIKE '%component.dropped%' OR EventType LIKE '%toolbox.component.dropped%')
  AND (Payload LIKE '%dropdown%' OR Payload LIKE '%"type":"dropdown"%')
ORDER BY CreatedDate DESC
""")

drop_events = cursor.fetchall()
if drop_events:
    print(f"\nFound {len(drop_events)} dropdown drop events:\n")
    for idx, row in enumerate(drop_events, 1):
        print(f"\n--- Event #{idx}: {row[0]} at {row[2]} ---")
        try:
            data = json.loads(row[1])
            # Extract component info
            component_id = data.get('componentId', 'unknown')
            component_type = data.get('componentType', data.get('type', 'unknown'))
            print(f"Component ID: {component_id}")
            print(f"Component Type: {component_type}")
            if 'options' in data:
                options = data.get('options', [])
                print(f"Options Count: {len(options)}")
                if options:
                    print(f"First Option: {options[0]}")
        except:
            print(row[1][:500] if row[1] else "No payload")
else:
    print("WARNING: No dropdown component drop events found")

# 3. Check for component rendering events
print("\n" + "=" * 80)
print("3. DROPDOWN COMPONENT RENDERING")
print("=" * 80)
cursor.execute("""
SELECT TOP 20 EventType, Payload, CreatedDate 
FROM log.FrontendEvent 
WHERE EventType LIKE '%canvas.component.rendered%'
  AND (Payload LIKE '%dropdown%' OR Payload LIKE '%"type":"dropdown"%')
ORDER BY CreatedDate DESC
""")

render_events = cursor.fetchall()
if render_events:
    print(f"\nFound {len(render_events)} dropdown render events:\n")
    for idx, row in enumerate(render_events, 1):
        print(f"\n--- Event #{idx}: {row[0]} at {row[2]} ---")
        try:
            data = json.loads(row[1])
            print(json.dumps(data, indent=2))
        except:
            print(row[1][:500] if row[1] else "No payload")
else:
    print("WARNING: No dropdown render events found")

# 4. Check for options section changes (when user adds/modifies options)
print("\n" + "=" * 80)
print("4. OPTIONS SECTION CHANGES (Property Panel)")
print("=" * 80)
cursor.execute("""
SELECT TOP 20 EventType, Payload, CreatedDate 
FROM log.FrontendEvent 
WHERE EventType LIKE '%panel.property.changed%'
  AND (Payload LIKE '%options%' OR Payload LIKE '%dropdown%')
ORDER BY CreatedDate DESC
""")

options_events = cursor.fetchall()
if options_events:
    print(f"\nFound {len(options_events)} options change events:\n")
    for idx, row in enumerate(options_events, 1):
        print(f"\n--- Event #{idx}: {row[0]} at {row[2]} ---")
        try:
            data = json.loads(row[1])
            # Show relevant parts
            if 'options' in data:
                options = data.get('options', [])
                print(f"Options Count: {len(options)}")
                if options:
                    longest = max(options, key=lambda x: len(str(x.get('label', x.get('value', '')))))
                    print(f"Longest Option: {longest}")
            print(json.dumps(data, indent=2))
        except:
            print(row[1][:500] if row[1] else "No payload")
else:
    print("WARNING: No options change events found")

# 5. Check for appearance/style changes (font changes that affect width)
print("\n" + "=" * 80)
print("5. APPEARANCE CHANGES (Font/Size changes affecting dropdown width)")
print("=" * 80)
cursor.execute("""
SELECT TOP 20 EventType, Payload, CreatedDate 
FROM log.FrontendEvent 
WHERE (EventType LIKE '%panel.property.changed%' OR EventType LIKE '%panel.globalstyle.changed%')
  AND (Payload LIKE '%fontSize%' OR Payload LIKE '%fontFamily%' OR Payload LIKE '%fontWeight%')
ORDER BY CreatedDate DESC
""")

style_events = cursor.fetchall()
if style_events:
    print(f"\nFound {len(style_events)} style change events:\n")
    for idx, row in enumerate(style_events, 1):
        print(f"\n--- Event #{idx}: {row[0]} at {row[2]} ---")
        try:
            data = json.loads(row[1])
            # Show font-related changes
            font_keys = ['fontSize', 'fontFamily', 'fontWeight']
            relevant_data = {k: v for k, v in data.items() if any(fk in k.lower() for fk in font_keys)}
            if relevant_data:
                print(json.dumps(relevant_data, indent=2))
            else:
                print(json.dumps(data, indent=2))
        except:
            print(row[1][:500] if row[1] else "No payload")
else:
    print("WARNING: No style change events found")

# 6. Summary: Find all dropdown-related events
print("\n" + "=" * 80)
print("6. SUMMARY: ALL DROPDOWN-RELATED EVENTS (Last 30)")
print("=" * 80)
cursor.execute("""
SELECT TOP 30 EventType, Payload, CreatedDate 
FROM log.FrontendEvent 
WHERE EventType LIKE '%dropdown%'
   OR (Payload LIKE '%dropdown%' AND EventType LIKE '%component%')
ORDER BY CreatedDate DESC
""")

all_dropdown_events = cursor.fetchall()
if all_dropdown_events:
    print(f"\nFound {len(all_dropdown_events)} total dropdown-related events:\n")
    event_types = {}
    for row in all_dropdown_events:
        event_type = row[0]
        event_types[event_type] = event_types.get(event_type, 0) + 1
    
    print("Event Type Breakdown:")
    for event_type, count in sorted(event_types.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {event_type}: {count} events")
    
    print("\nMost Recent Events:")
    for idx, row in enumerate(all_dropdown_events[:5], 1):
        print(f"\n  {idx}. {row[0]} at {row[2]}")
else:
    print("WARNING: No dropdown-related events found at all")

# 7. Check for migration events (select -> dropdown)
print("\n" + "=" * 80)
print("7. MIGRATION EVENTS (select -> dropdown)")
print("=" * 80)
cursor.execute("""
SELECT TOP 10 EventType, Payload, CreatedDate 
FROM log.FrontendEvent 
WHERE Payload LIKE '%"type":"select"%'
   OR Payload LIKE '%select%'
ORDER BY CreatedDate DESC
""")

migration_events = cursor.fetchall()
if migration_events:
    print(f"\nFound {len(migration_events)} potential 'select' type events:\n")
    print("WARNING: If you see 'select' type here, migration may not be working")
    for idx, row in enumerate(migration_events, 1):
        print(f"\n--- Event #{idx}: {row[0]} at {row[2]} ---")
        try:
            data = json.loads(row[1])
            if 'type' in data and data['type'] == 'select':
                print("WARNING: Found 'select' type - should be 'dropdown'")
            print(json.dumps(data, indent=2))
        except:
            print(row[1][:200] if row[1] else "No payload")
else:
    print("SUCCESS: No 'select' type events found (migration working correctly)")

print("\n" + "=" * 80)
print("VALIDATION COMPLETE")
print("=" * 80)
print("\nNext Steps:")
print("1. Review the events above")
print("2. Check that dropdown.width.calculated shows correct calculations")
print("3. Verify width updates when options are added/modified")
print("4. Confirm visual guide appears in builder mode")
print("5. Check that Input category changes trigger width recalculation")

conn.close()






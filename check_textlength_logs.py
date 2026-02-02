import pyodbc
import json
from datetime import datetime, timedelta

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=EventLeadPlatform;Trusted_Connection=yes;')
cursor = conn.cursor()

# Check for textlength calculation events
print("=== TextLengthIndicator Events ===")
cursor.execute("""
SELECT TOP 20 EventType, Payload, CreatedDate 
FROM log.FrontendEvent 
WHERE EventType LIKE '%textlength%' 
   OR EventType LIKE '%text.length%'
ORDER BY CreatedDate DESC
""")

textlength_events = cursor.fetchall()
if textlength_events:
    for row in textlength_events:
        print(f'\n--- {row[0]} at {row[2]} ---')
        try:
            data = json.loads(row[1])
            print(json.dumps(data, indent=2))
        except:
            print(row[1][:500] if row[1] else "No payload")
else:
    print("No textlength events found")

# Check for component rendering events
print("\n\n=== Component Rendering Events ===")
cursor.execute("""
SELECT TOP 20 EventType, Payload, CreatedDate 
FROM log.FrontendEvent 
WHERE EventType LIKE '%fieldshell.structure.loaded%'
   OR EventType LIKE '%fieldshell.objects.filtered%'
   OR EventType LIKE '%canvas.component.rendered%'
ORDER BY CreatedDate DESC
""")

render_events = cursor.fetchall()
if render_events:
    for row in render_events:
        print(f'\n--- {row[0]} at {row[2]} ---')
        try:
            data = json.loads(row[1])
            print(json.dumps(data, indent=2))
        except:
            print(row[1][:500] if row[1] else "No payload")
else:
    print("No rendering events found")

# Check for input renderer events (if we log them)
print("\n\n=== Input Renderer Events ===")
cursor.execute("""
SELECT TOP 20 EventType, Payload, CreatedDate 
FROM log.FrontendEvent 
WHERE EventType LIKE '%input%'
   OR EventType LIKE '%renderer%'
ORDER BY CreatedDate DESC
""")

input_events = cursor.fetchall()
if input_events:
    for row in input_events:
        print(f'\n--- {row[0]} at {row[2]} ---')
        try:
            data = json.loads(row[1])
            # Only show relevant parts
            if 'maxLength' in str(data) or 'validation' in str(data):
                print(json.dumps(data, indent=2))
        except:
            pass

# Check recent component creation/drop events
print("\n\n=== Recent Component Drop/Creation ===")
cursor.execute("""
SELECT TOP 10 EventType, Payload, CreatedDate 
FROM log.FrontendEvent 
WHERE EventType LIKE '%component.dropped%'
   OR EventType LIKE '%toolbox.component.dropped%'
ORDER BY CreatedDate DESC
""")

drop_events = cursor.fetchall()
if drop_events:
    for row in drop_events:
        print(f'\n--- {row[0]} at {row[2]} ---')
        try:
            data = json.loads(row[1])
            print(json.dumps(data, indent=2))
        except:
            print(row[1][:500] if row[1] else "No payload")

conn.close()

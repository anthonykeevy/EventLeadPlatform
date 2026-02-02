# Universal FieldShell Logging Guide

**Purpose:** Quick reference for logging Universal FieldShell operations during implementation and testing.

> **Status (2026-01):** This guide predates the current Component Framework logging pass and contains **planned** event names and workflows that may not exist in the current codebase.
>
> Use `docs/AGENT-LOGGING-GUIDE.md` as the source of truth for:
> - how to enable/capture logs (Dev Logs download)
> - the current event prefixes to filter (`fieldshell.*`, `resize.*`, `smartborder.*`, `gridlayout.*`, etc.)

---

## 🚀 Quick Start

### Enable Logging

```bash
# In frontend/.env or frontend/.env.local
VITE_ENABLE_DEV_LOGS=true
# Optional: verbose resize + SmartBorder logs to console
VITE_LOG_VERBOSE_RESIZE=false
```

### View Logs

- **Preferred**: Use the Builder header **Dev Logs** button to download the JSON bundle.
- **Optional**: Set `VITE_LOG_VERBOSE_RESIZE=true` to mirror many events to the browser console.

---

## 📊 Event Categories

### 1. Structure Evaluation
- `fieldshell.structure.loaded` - Component structure loaded from registry/database/default
- `fieldshell.structure.validation.failed` - Structure validation errors
- `fieldshell.structure.default.generated` - Default structure generated for component

### 2. Object Filtering
- `fieldshell.objects.filtered` - Conditional objects filtered based on rules
- `fieldshell.conditional.evaluated` - Individual conditional rule evaluation

### 3. Layout Operations
- `fieldshell.layout.changed` - Layout type changed (vertical/horizontal/mixed)
- `fieldshell.layout.groups.changed` - Layout groups modified
- `fieldshell.layout.effective` - Effective layout calculated (default vs override)

### 4. SmartBorder Operations
- `fieldshell.smartborder.ref.attached` - SmartBorder container ref attached
- `fieldshell.collision.checked` - Collision detection using SmartBorder bounds
- `fieldshell.collision.detected` - **Collision detected with detailed component snapshots** (WARN level)
- `smartborder.path.calculated` - SmartBorder SVG path calculated with bounds info
- `smartborder.drag.state` - Component enters/exits drag state (isDragging change)
- `smartborder.selection.changed` - Component selection state changed (isSelected change)
- `smartborder.bounds.live` - **Real-time bounds during drag** (every 500ms for collision debugging)

### 5. Drag Operations
- `fieldshell.drag.start` - **Component snapshot BEFORE grab**
- `fieldshell.drag.grabbed` - Position after initial grab
- `fieldshell.drag.beforeDrop` - **Component snapshot BEFORE drop**
- `fieldshell.drag.drop` - **Component snapshots BEFORE and AFTER drop**

### 6. Resize Operations
- `fieldshell.resizehandles.attached` - ResizeHandles attached to SmartBorder container
- `fieldshell.resize.start` - **Component snapshot BEFORE grab**
- `fieldshell.resize.grabbed` - **Component snapshot AFTER grab**
- `fieldshell.resize.preview` - Resize preview updated (during drag)
- `fieldshell.resize.beforeDrop` - **Component snapshot BEFORE drop**
- `fieldshell.resize.commit` - **Component snapshots BEFORE and AFTER drop**

### 7. Properties Panel
- `fieldshell.properties.layout.changed` - Object layout changed in Properties Panel
- `fieldshell.properties.styling.changed` - Typography/spacing/colors changed

### 8. Migration Events
- `fieldshell.migration.component` - Component migrated to structure system
- `fieldshell.migration.form.completed` - Form migration script completed

---

## 🔍 Testing Workflow

### Step 1: Enable Logging
Set environment variables as shown above.

### Step 2: Perform User Actions
1. **Open Form Builder** → Logs structure loading
2. **Add Component** → Logs structure evaluation, SmartBorder attachment
3. **Change Layout** → Logs layout changes in Properties Panel
4. **Resize Component** → Logs resize operations
5. **Move Component** → Logs collision detection
6. **Change Properties** → Logs styling/spacing changes

### Step 3: Download Logs
Use browser console or UI button to download logs.

### Step 4: Agent Review
Agent reviews JSON log file to verify:
- Structure loading works correctly
- Object filtering applies conditional rules
- Layout changes persist
- ResizeHandles attach to SmartBorder container
- Collision detection uses SmartBorder bounds
- Properties panel changes are logged

---

## 📋 Logging Checklist

**During Implementation:**

- [x] UniversalFieldShell logs structure loading
- [x] UniversalFieldShell logs object filtering
- [x] UniversalFieldShell logs layout calculation
- [x] UniversalFieldShell logs SmartBorder ref attachment
- [x] SmartBorder logs path calculation with bounds
- [x] SmartBorder logs drag state changes (isDragging)
- [x] SmartBorder logs selection state changes
- [x] SmartBorder logs live bounds during drag (every 500ms)
- [x] SortableComponent logs ResizeHandles attachment
- [x] SortableComponent logs resize operations with snapshots (before grab, after grab, before drop, after drop)
- [x] Collision detection logs bounds checks
- [x] Collision detection logs detailed component snapshots when collisions occur
- [x] BuilderPage logs drag operations with snapshots (before grab, after grab, before drop, after drop)
- [ ] Properties Panel logs layout changes
- [ ] Properties Panel logs styling changes
- [ ] Migration script logs migration events

**After Testing:**

- [ ] Download logs after each test scenario
- [ ] Verify all expected events are present
- [ ] Check for errors/warnings in logs
- [ ] Verify event payloads contain expected data
- [ ] Confirm component IDs are consistent across events

---

## 🎯 Example Log Entries

### Structure Loaded
```json
{
  "ts": 1705123456789,
  "level": "info",
  "event": "fieldshell.structure.loaded",
  "payload": {
    "componentId": "first-name-123",
    "componentType": "first-name",
    "structure": {
      "objects": [
        { "id": "label", "type": "label", "required": true, "order": 1 },
        { "id": "input", "type": "input", "required": true, "order": 2 },
        { "id": "validation", "type": "validation", "required": false, "order": 3 }
      ],
      "defaultLayout": "mixed",
      "layoutGroups": { "row1": ["label", "input"], "row2": ["validation"] }
    },
    "source": "registry"
  }
}
```

### Objects Filtered
```json
{
  "ts": 1705123456790,
  "level": "debug",
  "event": "fieldshell.objects.filtered",
  "payload": {
    "componentId": "first-name-123",
    "totalObjects": 3,
    "visibleObjects": 3,
    "hiddenObjects": [],
    "conditionalContext": {
      "component": { "id": "first-name-123", "type": "first-name" },
      "componentProps": { "required": true },
      "validationErrors": null
    }
  }
}
```

### SmartBorder Ref Attached
```json
{
  "ts": 1705123456791,
  "level": "info",
  "event": "fieldshell.smartborder.ref.attached",
  "payload": {
    "componentId": "first-name-123",
    "hasRef": true,
    "containerElement": "div"
  }
}
```

### Resize Operation
```json
{
  "ts": 1705123456792,
  "level": "info",
  "event": "fieldshell.resize.commit",
  "payload": {
    "componentId": "first-name-123",
    "handle": "e",
    "finalProps": { "width": "400px" },
    "duration": 250
  }
}
```

### Collision Detection
```json
{
  "ts": 1705123456793,
  "level": "debug",
  "event": "fieldshell.collision.checked",
  "payload": {
    "componentId": "first-name-123",
    "otherComponentIds": ["email-456"],
    "hasCollision": true,
    "bounds": {
      "x": 200,
      "y": 100,
      "width": 400,
      "height": 80
    },
    "method": "smartborder-container"
  }
}
```

### SmartBorder Path Calculated
```json
{
  "ts": 1705123456794,
  "level": "debug",
  "event": "smartborder.path.calculated",
  "payload": {
    "componentId": "first-name-123",
    "bounds": {
      "width": 320,
      "height": 85,
      "padding": 5
    },
    "profileCount": 3,
    "pointCount": 8
  }
}
```

### SmartBorder Drag State Change
```json
{
  "ts": 1705123456795,
  "level": "debug",
  "event": "smartborder.drag.state",
  "payload": {
    "componentId": "first-name-123",
    "isDragging": true,
    "isSelected": true,
    "hasDragListeners": true
  }
}
```

### SmartBorder Live Bounds (During Drag)
```json
{
  "ts": 1705123456796,
  "level": "debug",
  "event": "smartborder.bounds.live",
  "payload": {
    "componentId": "first-name-123",
    "bounds": {
      "x": 245,
      "y": 180,
      "width": 320,
      "height": 85
    },
    "timestamp": 1705123456796
  }
}
```

---

## 🚨 Error Logging

Errors are logged with `level: "error"` and include:
- Error message
- Stack trace (if available)
- Component context
- Operation that failed

**Example:**
```json
{
  "ts": 1705123456794,
  "level": "error",
  "event": "fieldshell.smartborder.ref.failed",
  "payload": {
    "componentId": "first-name-123",
    "error": "Cannot attach ref to null element",
    "stackTrace": "UniversalFieldShell.tsx:45:12"
  }
}
```

---

## 📈 Performance Logging

Performance events use `level: "debug"` and include duration in milliseconds:

```json
{
  "ts": 1705123456795,
  "level": "debug",
  "event": "fieldshell.performance.objects.filtered",
  "payload": {
    "componentId": "first-name-123",
    "duration": 2.5,
    "objectCount": 3
  }
}
```

---

## 🔧 Integration Points

### Component Snapshot Utility

**New File:** `frontend/src/features/builder/utils/componentSnapshot.ts`

Utility to capture complete component state for logging:
- Component ID, type, position, dimensions
- Component props (objectLayout, layoutGroups, objectSpacing, styleOverrides)
- DOM bounds (SmartBorder container bounds)
- Timestamp for duration calculations

### Existing Infrastructure
- **devLogger**: `frontend/src/features/builder/utils/devLogger.ts`
- **Buffer**: 500 entries max (FIFO)
- **Download**: JSON format
- **Console**: Mirrors warn/error events

### Backend Logging
- Form saves → `log.ApiRequest` (automatic)
- Component updates → `log.ApiRequest` (automatic)
- Migration errors → `log.ApplicationError` (automatic)

---

## 📝 Implementation Notes

### When to Log

**Always Log:**
- Structure loading (info)
- Layout changes (info)
- Resize operations (info)
- Errors (error)

**Debug Log:**
- Object filtering (debug)
- Conditional evaluation (debug)
- Collision checks (debug)
- Performance metrics (debug)

### What to Include in Payloads

**Required:**
- `componentId` - Component identifier
- `componentType` - Component type string

**Optional but Recommended:**
- `oldValue` / `newValue` - For change events
- `duration` - For performance events
- `error` / `stackTrace` - For error events

---

## 🎓 Agent Review Process

1. **Download logs** after user completes test scenario
2. **Filter by component** to see all events for a specific component
3. **Check event flow** - Structure → Filter → Layout → Render → Resize
4. **Verify expected events** are present
5. **Check for errors** - Filter by `level: "error"` or `level: "warn"`
6. **Verify payloads** contain expected data
7. **Confirm behavior** matches expected outcomes

---

**Remember: Comprehensive logging makes troubleshooting and validation much easier!** 🚀




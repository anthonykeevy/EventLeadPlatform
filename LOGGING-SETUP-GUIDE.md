# Frontend Logging Setup Guide

## Issue: No Frontend Logs Appearing

If you're not seeing frontend logs after performing actions, follow these steps:

### Step 1: Enable Frontend Logging

Create or update `frontend/.env` file with:

```bash
VITE_ENABLE_DEV_LOGS=true
# Optional: set to true for detailed resize + SmartBorder logs in console
VITE_LOG_VERBOSE_RESIZE=false
# Optional: persist logs across reloads (localStorage). Off by default.
VITE_LOG_PERSIST_TO_STORAGE=false
```

### Step 2: Restart Frontend Dev Server

After updating `.env`, restart your frontend dev server:

```bash
cd frontend
npm run dev
```

### Step 3: Verify Logging is Active

In the Builder UI header, a **“Dev Logs”** download button appears only when logging is enabled. If you don’t see it, re-check `.env` and restart the dev server.

### Step 4: Perform Actions and Check Logs

1. Perform actions in the builder (resize, drag, etc.)
2. Click **Dev Logs** to download the JSON bundle
3. (Optional) If `VITE_LOG_VERBOSE_RESIZE=true`, you’ll also see mirrored console output for many events

### Step 5: Force Log Flush (If Needed)

Frontend logs are currently **local (in-browser) + downloadable**. Backend-synced frontend logs are planned, but not wired end-to-end yet.

---

## Expected Log Events for Resize Operations

When you resize a Text component, you should see:

### For E/W (Width) Resize:
- `fieldshell.resize.start` / `fieldshell.resize.grabbed`
- `fieldshell.resize.preview` (during drag)
- `resize.width.chain` / `resize.width.comparison` (math + verification)
- `fieldshell.resize.commit` (final commit with before/after snapshots)

### For N/S (Height) Resize:
- `resize.phase.transition` (height/gap phase transitions)
- `fieldshell.resize.commit` (final commit with before/after snapshots)

### For Corner (Scale) Resize:
- `resize.corner.commit.start` / `resize.corner.commit.complete`

---

## Troubleshooting

### No logs at all:
- ✅ Check `.env` file exists and has correct values
- ✅ Restart frontend dev server
- ✅ Check browser console for errors
- ✅ Confirm you can see the **Dev Logs** button in the Builder header

### Logs appear but missing specific events:
- ✅ Check the event is actually being logged in code (grep for devLogger.info)
- ✅ Check event name matches filter pattern
- ✅ Check component ID matches if filtering by component

---

## Quick Test

After setup, perform this test:

1. Add a Text Input component
2. Resize it using the E (East) handle
3. Click **Dev Logs** and open the JSON file

You should see events like `resize.pointer.down`, `fieldshell.resize.preview`, and `fieldshell.resize.commit`.

# UAT Checklist: T04

**Story:** 5.1 - Background Asset Management
**Task:** T04 - Frontend Builder Asset Upload + Library + Reference Wiring
**Generated:** 2026-02-09

---

## Pre-conditions

- [x] Backend server is running
- [x] Frontend dev server is running (`npm run dev` in frontend/)
- [x] User is logged in
- [x] User has access to Builder UI
- [x] Form is open in Builder (or create new form)

---

## Test Steps

### AC1: Builder stores only asset references in DefinitionJSON

- [x] Step 1: Open Builder UI → Open the **Canvas Background** / Background Style section → Click the **Image** tab (next to Color) → Verify the **"Select from Library"** button is visible below "Background Image"
- [x] Step 2: Upload an image via AssetLibrary → Verify asset is selected and preview shows
- [x] Step 3: Save form definition → Open browser DevTools → Inspect network request → Verify DefinitionJSON contains `background.asset` object with `assetId`, `assetKey`, etc.
- [x] Step 4: Verify DefinitionJSON does NOT contain Data URLs (no `value` starting with `data:`)

### AC2: Upload + picker flow works end-to-end with backend API

- [x] Step 1: Click "Select from Library" → Verify AssetLibrary modal opens
- [x] Step 2: Click "Upload New Image" → Select an image file → Verify upload progress indicator shows
- [x] Step 3: Verify upload completes → Asset appears in library grid → Asset is auto-selected
- [x] Step 4: Verify background preview updates with uploaded image
- [x] Step 5: Close modal → Verify selected asset persists in background properties
- [x] Step 6: Select different asset from library → Verify preview updates
- [x] Step 7: Check browser Network tab → Verify POST to `/api/assets/backgrounds/upload` succeeded (201 status)

### AC3: Limits are surfaced clearly to users

- [x] Step 1: Try uploading file > 10MB → Verify error message: "File size exceeds 10MB limit. Please choose a smaller image."
- [x] Step 2: Try uploading non-image file (e.g., .txt) → Verify error message: "Invalid file type. Please select an image file (PNG, JPG, GIF, etc.)"
- [x] Step 3: Verify error messages are displayed in red alert box with icon
- [x] Step 4: Verify error messages are clear and actionable

---

## Regression Check

- [x] Verify existing background color selection still works
- [x] Verify external URL input still works (legacy support)
- [x] Verify overlay settings (color, opacity) still work
- [x] Verify image size/position options still work
- [x] No console errors in browser DevTools
- [x] No new backend errors in logs

---

## Post-conditions

- [x] Form definition can be saved successfully
- [x] Background asset reference is persisted correctly
- [x] Asset library shows uploaded assets

---

## Edge Cases

- [x] Upload duplicate asset (same file) → Verify deduplication works (isDuplicate flag)
- [x] Upload asset, then switch to color background → Verify asset is cleared (image settings retained for switch back)
- [x] Upload asset, then enter external URL → Verify asset reference is cleared
- [x] Remove asset → Verify background clears correctly
- [x] Upload multiple assets → Verify all appear in library

---

**Instructions for Human Tester:**
1. Execute each step in order
2. Mark ✅ or ❌ for each item
3. Add notes for any failures
4. Capture screenshots of:
   - AssetLibrary modal with uploaded assets
   - Network request showing asset upload (201 response)
   - DefinitionJSON showing asset reference (not Data URL)
   - Error messages for limit violations
5. When complete, run `@ralf-uat *record-uat` with your results

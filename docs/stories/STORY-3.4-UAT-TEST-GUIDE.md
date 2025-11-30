# Story 3.4 UAT Test Guide - Component Library & Free-Form Canvas

**Status:** ✅ PASSED
**Story:** `docs/stories/story-3.4.md`
**Context:** `docs/spec/BUILDER-GLOSSARY.md`

---

## 🛠️ Pre-requisites

Before starting the tests, ensure the following:
1.  **Application is running:** The frontend development server is active (`npm run dev`).
2.  **Route:** Navigate to `/forms/:formId/builder`.
3.  **Environment:** Use a desktop browser (Chrome/Edge recommended).
4.  **State:** Start with a blank canvas (refresh if needed).

---

## 🧪 Test Scenarios

### Scenario 1: Scalable Viewport & Device Modes
**Goal:** Verify the "Fit-to-Screen" scaling logic and device dimensions.

*   **Step 1:** Observe the Canvas. It should be a white rectangle floating in the center.
*   **Step 2:** Resize your browser window (make it smaller).
    *   **Check:** The Canvas should shrink (scale down) to stay fully visible. No scrollbars should appear on the gray background.
    *   **Check:** The Scale Indicator (top bar) should show a percentage (e.g., "57%").
*   **Step 3:** Click the **Mobile Icon** (Smartphone).
    *   **Check:** The Canvas changes shape to a tall vertical rectangle (375x667).
    *   **Check:** The Scale Indicator updates to "Mobile (375x667)".
*   **Step 4:** Click the **Desktop Icon** (Monitor).
    *   **Check:** The Canvas returns to the wide aspect ratio (1920x980).

**Expected Result:**
*   [x] Canvas maintains aspect ratio regardless of window size.
*   [x] Scale percentage updates in real-time.
*   [x] Switching devices changes the logical dimensions instantly.

**Result:** ✅ PASSED

---

### Scenario 2: Toolbox "Gold Standard" Preview
**Goal:** Verify the "First Name" component looks identical in the Toolbox as it will on the Canvas.

*   **Step 1:** Look at the **"First Name"** component in the Toolbox.
*   **Step 2:** **Verify Visuals:**
    *   It has a label: "First Name *"
    *   It has an input box with placeholder text.
    *   It has a validation message: "Numbers and Special characters are not allowed" (greyed out).
    *   It has a custom non-rectangular border (Skyline shape) hugging the content.
*   **Step 3:** Hover over the component.
    *   **Check:** The cursor changes to a "Grab Hand" anywhere inside the shape.

**Expected Result:**
*   [x] Component is a "Rich Preview" (miniature actual component), not just an icon.
*   [x] "Skyline" border is visible and correct.
*   [x] Hitbox works on the entire shape.

**Result:** ✅ PASSED

---

### Scenario 3: Precision Drag & Drop (WYSIWYG)
**Goal:** Verify that dragging and dropping works precisely even when the canvas is scaled/zoomed out.

*   **Step 1:** Ensure you are in **Desktop Mode**.
*   **Step 2:** Drag the "First Name" component from the Toolbox.
    *   **Check:** The "Ghost Image" attached to your mouse is the **same size** as the scaled canvas components (not huge).
*   **Step 3:** Drop the component anywhere on the white canvas.
    *   **Check:** The component lands **exactly** where the Ghost Image was. It should not jump or shift.
*   **Step 4:** Drag the component again to move it to the bottom-right corner.
    *   **Check:** It moves smoothly and stays under the mouse.

**Expected Result:**
*   [x] Ghost Image scale matches Canvas scale.
*   [x] Drop coordinates are precise (no "jump" on release).
*   [x] Component can be placed freely (absolute positioning).

**Result:** ✅ PASSED

---

### Scenario 4: Grid Snapping & Toggling
**Goal:** Verify the 8px magnetic grid can be enabled and disabled.

*   **Step 1:** **Enable Grid:** Click the Grid Icon (top right) so grid lines are visible.
*   **Step 2:** Drag a component.
    *   **Check:** It "jumps" in 8px increments (snapping).
*   **Step 3:** **Disable Grid:** Click the Grid Icon again (lines disappear).
*   **Step 4:** Drag a component.
    *   **Check:** It moves smoothly (pixel-perfect) without snapping.

**Expected Result:**
*   [x] Snapping is active when Grid is visible.
*   [x] Snapping is disabled when Grid is hidden.
*   [x] Visual grid lines toggle correctly.

**Result:** ✅ PASSED

---

### Scenario 5: Background Mode (Layers)
**Goal:** Verify the separation between Content (Layer 1) and Background (Layer 0).

*   **Step 1:** Click the **"Background"** button in the top toolbar layer switcher.
    *   **Check:** The Canvas gets a blue/indigo border indicating "Background Mode".
    *   **Check:** The "First Name" component (if any) becomes semi-transparent/ghosted.
*   **Step 2:** Try to drag the "First Name" component.
    *   **Check:** You CANNOT drag it. It is locked (cursor shows "not-allowed" or default arrow).
*   **Step 3:** Click **"Elements"** button to return to normal mode.
    *   **Check:** The component is fully visible and draggable again.

**Expected Result:**
*   [x] Layer switching visually distinguishes the active layer.
*   [x] Components on inactive layers are locked from interaction.

**Result:** ✅ PASSED

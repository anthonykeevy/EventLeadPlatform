# Story 3.4: Component Library & Grid Layout

**Epic:** 3 - Form Builder & Logic Engine  
**Domain:** Visual Builder  
**Status:** ✅ Completed  
**Priority:** High  

---

## 📖 User Story

**As a** Form Designer,  
**I want to** drag new components from a "Toolbox" sidebar and place them precisely on the canvas using a grid system,  
**So that** I can construct professional, aligned forms without layout errors or overlaps.

**Context & Entry Point:**  
The user is already in the Builder (Route: `/forms/:formId/builder`).
- **Left Panel:** "Toolbox" containing available components.
- **Canvas Area:** The drop zone (implemented in 3.3, now enhanced with grid/snap).

---

## ✅ Acceptance Criteria

### 1. Component Registry (The Toolbox)
- [x] Create a central `ComponentRegistry` mapping component types to their React implementations and default schemas.
- [x] Implement the "Toolbox" sidebar panel listing available components.
    - **Refinement:** Implemented "Gold Standard" WYSIWYG previews in the toolbox.
- [x] **Interaction:** Users can drag items from the Toolbox onto the Canvas (copy operation).

### 2. Visual Structure (3-Part Component)
- [x] Implement a standardized wrapper for all Input components:
    - **Part 1: Label** (Top or Left aligned).
    - **Part 2: Input Control** (The actual form field).
    - **Part 3: Validation Message** (Error text area).
- [x] Ensure this structure is consistent for Text, Number, and Checkbox inputs.

### 3. Free-Form Canvas (Replaced Layout Containers)
- [x] **Refinement:** Replaced "Row/Column" concept with **Absolute Positioning** and a Layered Canvas.
- [x] **Background Layer (Layer 0):** For static assets/colors.
- [x] **Functional Layer (Layer 1):** For interactive components.

### 4. Grid Snapping & Precision
- [x] Implement a visual grid (background pattern or guides) on the canvas.
- [x] **Snapping:** When dragging, the item's position must snap to 8px increments.
- [x] **Toggle:** Grid snapping can be enabled/disabled.

### 5. Scalable Viewport (WYSIWYG)
- [x] **Fit-to-Screen:** The 1920x980 logical stage scales down to fit the available browser window using CSS Transforms.
- [x] **Inverse-Scale Drag:** Mouse movements map 1:1 to visual movements even when the canvas is zoomed out.
- [x] **Device Modes:** Desktop (1920x980), Tablet (768x1024), Mobile (375x667).

---

## 🛠️ Technical Notes

- **Library:** `dnd-kit` with `useDraggable`/`useDroppable`.
- **New Pattern:** "Skyline Border" - An SVG path that dynamically outlines non-rectangular component shapes using `getBoundingClientRect` and `ResizeObserver`.
- **Viewport Logic:** Used `flex-shrink-0` on the stage container to prevent aspect ratio distortion before scaling.
- **Coordinate System:** All coordinates stored as logical pixels (1920px space), translated from screen pixels via `(ScreenDelta / ScaleFactor)`.

---

## 🧪 UAT Test Guide

*(See full guide in `docs/stories/STORY-3.4-UAT-TEST-GUIDE.md`)*

---

## 📋 Completion Report

**Date:** 2025-11-30  
**Summary:**  
Story 3.4 successfully implemented the core "Visual Builder" experience. We pivoted from a standard list-based layout to a high-fidelity **Free-Form Canvas** inspired by design tools.

**Key Achievements:**
1.  **Gold Standard Component:** The "First Name" component established the architecture for all future inputs, featuring the 3-part structure and the unique "Skyline" bounding box.
2.  **Scalable Stage:** The viewport engine allows users to design for 4K/Full HD screens on smaller laptops without scrolling, providing a true "Presentation Slide" experience.
3.  **Layer Management:** Strict separation between Background (Layer 0) and Elements (Layer 1) prevents accidental edits.
4.  **Theme Support:** Full Light/Dark mode compatibility implemented using Tailwind's `dark:` modifiers.

**Next Steps (Story 3.5):**
- Implement the "Properties Panel" to allow editing the properties (Label, Placeholder, Validation) of the selected component.
- Hook up the `updateComponent` store action to form inputs in the right sidebar.

# EventLead Platform - Builder Glossary & Concepts

This document defines the standard terminology and conceptual model for the Visual Form Builder. It ensures alignment between the Product Owner and Development Team regarding the "Free-Form Canvas" approach.

## 1. The Screen Concept (The "Stage")

The core philosophy is that we are building a **"Fixed-Stage" Application**, similar to a presentation slide or a kiosk screen, rather than a scrolling web document.

### 1.1 The Stage (Logical Canvas)
*   **Definition:** The rectangular area that represents the *exact* logical dimensions of the end-user's screen.
*   **Behavior:** 
    *   It has fixed dimensions based on the target device type (see below).
    *   It is the coordinate system origin (0,0 is Top-Left).
    *   **Flexibility:** The stage container prevents aspect ratio distortion using `flex-shrink-0`.
*   **Standard Dimensions (Logical):**
    *   **Desktop:** 1920 x 980 (Full HD minus browser chrome).
    *   **Tablet:** 768 x 1024 (iPad Portrait).
    *   **Mobile:** 375 x 667 (Standard Smartphone).

### 1.2 The Viewport (Builder Window)
*   **Definition:** The visible area within the Builder UI where the Stage is rendered.
*   **Problem:** The Builder UI (sidebars, headers) consumes space, meaning a full 1920px Stage cannot fit 1:1 on most screens.
*   **Solution (Viewport Scaling):** 
    *   The Stage is "fit-to-screen" within the Viewport using a **CSS Transform Scale** (e.g., `transform: scale(0.57)`).
    *   This ensures the user sees the *entire* 1920x980 design without horizontal or vertical scrollbars on the builder itself.
    *   **Scale State:** The Scale Factor is calculated dynamically based on window size and stored in the global store (`useBuilderStore`) to coordinate other UI elements.

## 2. Layers & Hierarchy

The Stage is composed of distinct Z-Index planes (Layers).

### 2.1 Background Layer (Layer 0)
*   **Purpose:** Purely decorative elements that sit behind everything.
*   **Content:** Full-screen images, colors, or patterns.
*   **Interaction:** Controlled exclusively via the **Background Toolbar**.
*   **Z-Index:** Bottom-most.

### 2.2 Functional Layer (Layer 1)
*   **Purpose:** The interactive elements of the form.
*   **Content:** Input Fields, Text, Buttons ("Smart Objects").
*   **Interaction:** These float *above* the background.
*   **Z-Index:** Top-most.

## 3. Components ("Smart Objects")

Every item on the Functional Layer is a "Smart Object."

### 3.1 Definition
*   **Self-Contained:** A complete unit containing Label, Input, Validation Message, and Skyline Border.
*   **Intrinsic Sizing:** The object's size is determined by its content (e.g., length of text, number of checkboxes), not by the container. It "shrink-wraps" its content.
*   **Positioning:** 
    *   **Absolute:** Placed at specific X, Y coordinates.
    *   **Coordinate Logic:** Coordinates are stored relative to the Logical Stage (unscaled).
    *   **Grid-Snapped:** Aligning to the magnetic grid (8px) for precision.

### 3.2 Skyline Border
*   **Definition:** The custom, non-rectangular SVG border that outlines the Smart Object.
*   **Reactive:** It automatically redraws itself if the object's content changes.
*   **Hitbox:** The SVG path itself is the clickable/draggable area, ensuring precise interaction even with irregular shapes.

### 3.3 Ghost Image (Drag Preview)
*   **Definition:** The representation of a Smart Object that appears attached to the mouse cursor while dragging.
*   **Scaled Dragging:** 
    *   The Ghost Image must visually match the **Scaled Stage**.
    *   If the Stage is at 50% scale, the Ghost Image is rendered at `transform: scale(0.5)`.
    *   This ensures "What You See Is What You Get" (WYSIWYG) continuity from Toolbox -> Drag -> Drop.

## 4. Interaction Logic

### 4.1 Drop Coordinate Calculation
*   **Problem:** When dropping on a Scaled Stage, screen pixels do not match canvas pixels (100px mouse move = 200px canvas move at 50% scale).
*   **Solution:** 
    *   `Canvas Position = (Mouse Position - Canvas Offset) / Scale Factor`
    *   This calculation converts "Screen Coordinates" back into "Logical Stage Coordinates" (1920x980 space).

## 5. Interface Elements

### 5.1 Toolbox (Sidebar)
*   **Function:** Palette of Smart Object types.
*   **Preview:** Shows "Rich Previews" (actual rendered components) rather than just icons, so users see the "Skyline" shape before dragging.

### 5.2 Background Toolbar (Layer 0 Controller)
*   **Function:** The exclusive control center for Layer 0.
*   **Behavior:** 
    *   Activating this toolbar enters "Background Mode," locking Layer 1 interaction.
    *   Allows switching **Canvas Dimensions** (Desktop/Tablet/Mobile).

### 5.3 Global Properties Toolbar (The "Theme")
*   **Function:** Sets the defaults for all components (Font, Size, Spacing, Colors).
*   **Cascade/Reset:** Changing a value here immediately updates *all* components on the canvas to the new value, overriding customizations.

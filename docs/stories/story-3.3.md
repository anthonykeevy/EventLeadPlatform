# Story 3.3: Drag-and-Drop Canvas

**Epic:** 3 - Form Builder & Logic Engine
**Domain:** Visual Builder
**Status:** ✅ Complete
**Priority:** High

---

## 📖 User Story

**As a** Form Designer,
**I want to** have a drag-and-drop canvas area where I can visually arrange form components,
**So that** I can intuitively build the form structure without writing JSON manually.

**Context & Entry Point:**
The Form Builder is accessed via a **"Edit Design"** button on the Form Dashboard (or Form List).
- **Route:** `/forms/:formId/builder` (or similar)
- **Context:** The builder MUST initialize with the specific `formId` passed from the dashboard to load the correct schema.

---

## ✅ Acceptance Criteria

### 1. Library Setup
- [x] Install `@dnd-kit/core`, `@dnd-kit/sortable`, `@dnd-kit/utilities`.
- [x] Configure basic sensors (Mouse, Touch, Keyboard) for accessibility.

### 2. Canvas Component Structure
- [x] Create `FormBuilderCanvas` layout.
    - **Reference:** `docs/ux-specification.md` (Section 4.1.3 - "Maximized workspace (no side navigation)").
- [x] Implement a "Page" container (since we decided on a multi-page schema).
- [x] Within the page, implement a `SortableContext` vertical list.

### 3. Drag-and-Drop Logic
- [x] Implement `onDragEnd` handler to reorder components within the list.
- [x] Ensure the state update reflects the new order in the `FormDefinition` JSON structure.
- [x] Support moving items between pages (optional for V1, but good to keep in mind). *For this story: Focus on single page reordering first.*

### 4. Visual Feedback
- [x] Render "Draggable" component wrappers.
- [x] Show a "Drag Overlay" (ghost image) when dragging.
- [x] Show a placeholder indicator where the item will drop.
- **UX Guideline:** "Show, Don't Tell" - Ensure immediate visual feedback.

### 5. State Integration
- [x] Connect the Canvas to the Form Editor Store (Zustand/Redux).
- [x] Ensure that dropping an item updates the `FormDefinition` object correctly.
- [x] **Initialization:** The store must hydrate data based on the `formId` from the URL.

---

## 🛠️ Technical Notes

- **UX Reference:** See `docs/ux-specification.md` for detailed design principles and component specs.
- **Library:** `dnd-kit` (as per UX Spec Section 4.1).
- **State Management:** We need a store that holds the `FormDefinition`.
    - Actions: `moveComponent(pageId, fromIndex, toIndex)`, `addComponent`, `removeComponent`.
- **Component Rendering:**
    - Iterate through `formDefinition.pages[activePage].components`.
    - Map each component to a `SortableItem` wrapper.
- **Accessibility:** Ensure `dnd-kit` keyboard support is enabled.

### Proposed Component Hierarchy
```tsx
// Route: /forms/:formId/builder
<DndContext onDragEnd={handleDragEnd}>
  <div className="builder-layout h-screen flex">
    {/* Sidebar and Properties Panel placeholders for now */}
    <Sidebar /> 
    
    <main className="canvas-area flex-1 bg-gray-50 p-8 overflow-auto">
       {/* Visual representation of the form page */}
      <div className="form-page-container bg-white shadow-lg max-w-2xl mx-auto min-h-[800px] p-8">
        <SortableContext items={components.map(c => c.id)}>
          {components.map(component => (
            <SortableComponent key={component.id} id={component.id} data={component} />
          ))}
        </SortableContext>
      </div>
    </main>

    <PropertiesPanel />
  </div>
  <DragOverlay>...</DragOverlay>
</DndContext>
```

---

## 🧪 UAT Test Guide

*(See full guide in `docs/stories/STORY-3.3-UAT-TEST-GUIDE.md`)*

---

## 📋 Completion Report

### Implementation Summary
- **Dependencies:** Installed `@dnd-kit` libraries.
- **Architecture:**
    - Created `features/builder` module structure.
    - Implemented `useBuilderStore` using Zustand for efficient state management.
    - Created `BuilderLayout` providing a maximized workspace environment.
- **Core Components:**
    - `FormBuilderCanvas`: Central drop zone using `DndContext` and `SortableContext`.
    - `SortableComponent`: Draggable wrapper with accessibility supports (Keyboard sensors).
    - `ComponentSidebar`: Visual placeholder for the toolbox (ready for Story 3.4).
- **Integration:**
    - Added `/forms/:formId/builder` route.
    - Added "Design" button to Dashboard Form Cards for seamless navigation.

### Test Results
All UAT scenarios passed:
- [x] Entry Point Navigation (Dashboard -> Builder)
- [x] Basic Drag-and-Drop Reordering
- [x] Keyboard Accessibility (Space/Arrows reordering)
- [x] State Synchronization (UI matches Store)

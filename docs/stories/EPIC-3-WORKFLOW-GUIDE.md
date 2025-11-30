# Epic 3 Workflow Guide - Advanced Agentic Development

**Current Focus:** Story 3.4 - Component Library  
**Status:** 🟢 Ready for Execution  

---

## 🚨 **PM MAINTENANCE INSTRUCTIONS**
**FOR THE PM AGENT:**
At the end of every story, you **MUST** update this document.
1.  Identify the **Next Story** from `EPIC-3-STATUS.md`.
2.  **REWRITE** the prompts in Stages 1, 2, 3, and 4 below to be specific to that new story (replace "3.4" with "3.5", update goals, update context).
3.  Ensure the "Current Focus" header above reflects the new story.
4.  Only then is the story considered "Closed".

---

## 📋 **Stage 1: Create Story (Scrum Master)**

**Current Target:** Story 3.4  
**Goal:** Populate the builder with actual components and layout tools.

### **Copy/Paste this Prompt for the Scrum Master (@sm.mdc)**
```markdown
@sm.mdc Please create Epic 3 Story 3.4: Component Library.

Context:
- Previous Story: 3.3 (Canvas Foundation - Basic Drag/Sort implemented)
- Focus Domain: Visual Builder
- Goal: Implement the "Toolbox" sidebar and the Registry of components.
- **USER CONCERN TO ADDRESS:** The user wants to ensure "Placement", "Grid", and "Overlap" functionality is covered.
  - **Requirement:** Implement the "3-Part Component Structure" (Label/Input/Validation) for all input items.
  - **Requirement:** Implement Layout Containers (`Row`, `Column`) for structured placement.
  - **Requirement:** Implement "Preview Mode" (Device Toggles) for aspect ratio validation.
  - **Requirement:** Implement "Grid Snapping" (snap to 8px/16px grid).
  - **Requirement:** Implement "Collision Detection" (prevent dropping if overlapping).

Requirements:
1. Create story file: docs/stories/story-3.4.md
2. Create context file: docs/stories/story-context-3.4.xml
3. Update Epic 3 Status: docs/stories/EPIC-3-STATUS.md
4. **CRITICAL:** Include a placeholder section for "UAT Test Guide" in the story file.

Deliverables:
- Story File (Must include Grid/Snap, Collision, and Layout Components)
- Context File
- Status Update
- Creation Summary
```

---

## 🧪 **Stage 2: UAT Design (Developer)**

**When:** Immediately after Story 3.4 is created.  
**Goal:** Define the test cases before coding.

### **Copy/Paste this Prompt for the Developer (@dev.mdc)**
```markdown
@dev.mdc Please design the UAT Test Guide for Story 3.4.

Story Location: docs/stories/story-3.4.md
Context: docs/stories/story-context-3.4.xml

Goal:
Create a comprehensive `docs/stories/STORY-3.4-UAT-TEST-GUIDE.md` document.

Requirements:
- Define Pre-requisites.
- **Test Scenario 1: The Toolbox.** Verify dragging from sidebar with ghost offset (item follows mouse relative to click).
- **Test Scenario 2: Layout Containers.** Verify dropping items into Rows/Columns.
- **Test Scenario 3: Grid Snapping.** Verify items snap to grid increments when moved.
- **Test Scenario 4: Collision Prevention.** Verify items cannot be dropped on top of each other (red outline/rejection).
- **Test Scenario 5: Preview Mode.** Verify toggling Device View resizes the canvas area.
- For each scenario, list: Steps to Execute -> Expected Result.

Do NOT write any implementation code yet. Just the test guide.
```

---

## 🔧 **Stage 3: Implementation (Developer)**

**When:** After you (the User) have **Approved** the UAT Test Guide.  
**Goal:** Write the code to pass the UATs.

### **Copy/Paste this Prompt for the Developer (@dev.mdc)**
```markdown
@dev.mdc Please implement Story 3.4 based on the approved UAT Guide.

Story: docs/stories/story-3.4.md
UAT Guide: docs/stories/STORY-3.4-UAT-TEST-GUIDE.md
Architecture Ref: docs/stories/EPIC-3-ARCHITECTURE-REF.md

Requirements:
1. **Component Registry:** Update Registry to include `Row`, `Column` and core Inputs (Text, Number, Checkbox).
2. **Visual Structure:** Implement the standard "Label + Input + Validation" structure for inputs.
3. **Grid System:** Implement Snap-to-Grid logic in the `useBuilderStore` or `DndContext` modifiers.
4. **Collision Detection:** Implement logic to reject drops that overlap existing items (unless in a container).
5. **Drag Interaction:** Ensure drag preview follows mouse relative to pick-up point.

Focus Areas:
- UX Fidelity (Snapping, Overlap warnings).
- Layout Nesting (Columns inside Rows).
- Component Standard Structure.

Please confirm completion and provide a summary.
```

---

## 📊 **Stage 4: Completion & Handover (Developer)**

**When:** Implementation is done and you have verified the UATs pass.  
**Goal:** Finalize artifacts and update documentation and git.

### **Copy/Paste this Prompt for the Developer (@dev.mdc)**
```markdown
@dev.mdc Please finalize Story 3.4.

Requirements:
1. Update `docs/stories/story-3.4.md` with a "Completion Report".
2. Mark all tests in `docs/stories/STORY-3.4-UAT-TEST-GUIDE.md` as ✅ PASSED.
3. Update `docs/stories/EPIC-3-STATUS.md` (Mark 3.4 as Complete, 3.5 as Next).
4. Update `docs/stories/EPIC-3-ARCHITECTURE-REF.md` with any new component patterns discovered.
5. **GIT UPDATE:** Run the following commands to checkpoint progress:
   ```powershell
   git add .
   git commit -m "feat(epic3): Complete Story 3.4 - Component Library & Grid System"
   # git push
   ```

Deliverable:
- Finalized Story artifacts.
- Handover summary.
```

---

## 🔄 **Stage 5: Cycle Reset (PM Agent)**

**When:** Story 3.4 is finalized.  
**Goal:** Prepare this document for Story 3.5.

### **Copy/Paste this Prompt for the PM Agent (@pm.mdc)**
```markdown
@pm.mdc Please reset the cycle for the next story.

Requirements:
1. Read `docs/stories/EPIC-3-STATUS.md` to identify the next story (Story 3.5).
2. Update `docs/stories/EPIC-3-WORKFLOW-GUIDE.md`:
   - Update "Current Focus" to Story 3.5.
   - Rewrite Stages 1-4 prompts to be specific to Story 3.5 (Properties Panel).
   - **Key Requirement:** Story 3.5 must cover "Global vs Individual" property controls and "Layout Toggles" (Horizontal/Vertical).
   - Ensure goals and context match the new story.
3. Confirm ready for execution.
```

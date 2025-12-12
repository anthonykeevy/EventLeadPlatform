# Epic 3 Workflow Guide - Advanced Agentic Development

**Current Focus:** Story 3.5 - Properties Panel  
**Status:** 🟢 Ready for Execution  

---

## 🚨 **PM MAINTENANCE INSTRUCTIONS**
**FOR THE PM AGENT:**
At the end of every story, you **MUST** update this document.
1.  Identify the **Next Story** from `EPIC-3-STATUS.md`.
2.  **REWRITE** the prompts in Stages 1, 2, 3, and 4 below to be specific to that new story (replace "3.5" with "3.6", update goals, update context).
3.  Ensure the "Current Focus" header above reflects the new story.
4.  Only then is the story considered "Closed".

---

## 📋 **Stage 1: Create Story (Scrum Master)**

**Current Target:** Story 3.5  
**Goal:** Build the "Inspector" panel for configuring component properties.

### **Copy/Paste this Prompt for the Scrum Master (@sm.mdc)**
```markdown
@sm.mdc Please create Epic 3 Story 3.5: Properties Panel.

Context:
- Previous Story: 3.4 (Component Library & Grid - Toolbox and Canvas items implemented)
- Focus Domain: Visual Builder
- Goal: Implement the Right Sidebar (Properties Panel) to edit selected component settings.
- **USER CONCERN TO ADDRESS:** The user needs flexible control over layout and global vs. individual settings.
  - **Requirement:** Implement "Global vs Individual" controls (e.g., set font size for ALL inputs vs just this one).
  - **Requirement:** Implement "Layout Toggles" (switch individual component between Vertical/Horizontal layout).
  - **Requirement:** Implement standard property editors: Label, Required, Placeholder, Validation Rules.

Requirements:
1. Create story file: docs/stories/story-3.5.md
2. Create context file: docs/stories/story-context-3.5.xml
3. Update Epic 3 Status: docs/stories/EPIC-3-STATUS.md
4. **CRITICAL:** Include a placeholder section for "UAT Test Guide" in the story file.

Deliverables:
- Story File (Must include Global/Individual toggles and Layout Toggles)
- Context File
- Status Update
- Creation Summary
```

---

## 🧪 **Stage 2: UAT Design (Developer)**

**When:** Immediately after Story 3.5 is created.  
**Goal:** Define the test cases before coding.

### **Copy/Paste this Prompt for the Developer (@dev.mdc)**
```markdown
@dev.mdc Please design the UAT Test Guide for Story 3.5.

Story Location: docs/stories/story-3.5.md
Context: docs/stories/story-context-3.5.xml

Goal:
Create a comprehensive `docs/stories/STORY-3.5-UAT-TEST-GUIDE.md` document.

Requirements:
- Define Pre-requisites.
- **Test Scenario 1: Selection.** Verify clicking a component on canvas populates the Right Panel.
- **Test Scenario 2: Basic Edits.** Verify changing Label/Placeholder updates the Canvas in real-time.
- **Test Scenario 3: Layout Toggle.** Verify switching a component from "Vertical" to "Horizontal" changes its rendering on Canvas.
- **Test Scenario 4: Global Styles.** Verify changing a Global Setting (e.g., Theme Color) updates ALL components.
- **Test Scenario 5: Individual Override.** Verify changing a specific component's style overrides the Global setting.
- For each scenario, list: Steps to Execute -> Expected Result.

Do NOT write any implementation code yet. Just the test guide.
```

---

## 🔧 **Stage 3: Implementation (Developer)**

**When:** After you (the User) have **Approved** the UAT Test Guide.  
**Goal:** Write the code to pass the UATs.

### **Copy/Paste this Prompt for the Developer (@dev.mdc)**
```markdown
@dev.mdc Please implement Story 3.5 based on the approved UAT Guide.

Story: docs/stories/story-3.5.md
UAT Guide: docs/stories/STORY-3.5-UAT-TEST-GUIDE.md
Architecture Ref: docs/stories/EPIC-3-ARCHITECTURE-REF.md

Requirements:
1. **Properties Panel UI:** Create the sidebar container that listens to `selectedId` in the store.
2. **Property Inputs:** Create reusable inputs for the panel (TextEdit, Toggle, Select).
3. **Component Config:** Connect the panel inputs to update the `FormDefinition` in the store.
4. **Global Settings:** Implement the "Theme/Global" tab in the Properties Panel.
5. **Layout Toggles:** Add the logic to switch component `layout` prop (vertical/horizontal).

Focus Areas:
- Real-time updates (high performance).
- Selection state management.
- Global vs Local state hierarchy.

Please confirm completion and provide a summary.
```

---

## 📊 **Stage 4: Completion & Handover (Developer)**

**When:** Implementation is done and you have verified the UATs pass.  
**Goal:** Finalize artifacts and update documentation and git.

### **Copy/Paste this Prompt for the Developer (@dev.mdc)**
```markdown
@dev.mdc Please finalize Story 3.5.

Requirements:
1. Update `docs/stories/story-3.5.md` with a "Completion Report".
2. Mark all tests in `docs/stories/STORY-3.5-UAT-TEST-GUIDE.md` as ✅ PASSED.
3. Update `docs/stories/EPIC-3-STATUS.md` (Mark 3.5 as Complete, 3.6 as Next).
4. Update `docs/stories/EPIC-3-ARCHITECTURE-REF.md` with details on Property Handling.
5. **GIT UPDATE:** Run the following commands to checkpoint progress:
   ```powershell
   git add .
   git commit -m "feat(epic3): Complete Story 3.5 - Properties Panel"
   # git push
   ```

Deliverable:
- Finalized Story artifacts.
- Handover summary.
```

---

## 🔄 **Stage 5: Cycle Reset (PM Agent)**

**When:** Story 3.5 is finalized.  
**Goal:** Prepare this document for Story 3.6.

### **Copy/Paste this Prompt for the PM Agent (@pm.mdc)**
```markdown
@pm.mdc Please reset the cycle for the next story.

Requirements:
1. Read `docs/stories/EPIC-3-STATUS.md` to identify the next story (Story 3.6).
2. Update `docs/stories/EPIC-3-WORKFLOW-GUIDE.md`:
   - Update "Current Focus" to Story 3.6.
   - Rewrite Stages 1-4 prompts to be specific to Story 3.6 (Conditional Logic UI).
   - Ensure goals and context match the new story.
3. Confirm ready for execution.
```

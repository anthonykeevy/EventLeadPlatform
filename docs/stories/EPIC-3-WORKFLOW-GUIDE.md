# Epic 3 Workflow Guide - Advanced Agentic Development

**Current Focus:** Story 3.3 - Drag-and-Drop Canvas  
**Status:** 🟢 Ready for Execution  

---

## 🚨 **PM MAINTENANCE INSTRUCTIONS**
**FOR THE PM AGENT:**
At the end of every story, you **MUST** update this document.
1.  Identify the **Next Story** from `EPIC-3-STATUS.md`.
2.  **REWRITE** the prompts in Stages 1, 2, 3, and 4 below to be specific to that new story (replace "3.3" with "3.4", update goals, update context).
3.  Ensure the "Current Focus" header above reflects the new story.
4.  Only then is the story considered "Closed".

---

## 📋 **Stage 1: Create Story (Scrum Master)**

**Current Target:** Story 3.3  
**Goal:** Establish the frontend Drag-and-Drop interface foundation.

### **Copy/Paste this Prompt for the Scrum Master (@sm.mdc)**
```markdown
@sm.mdc Please create Epic 3 Story 3.3: Drag-and-Drop Canvas.

Context:
- Previous Story: 3.2 (JSON Schema & Validation Implemented)
- Focus Domain: Visual Builder
- Goal: Initialize the React Drag-and-Drop environment (dnd-kit) and basic canvas structure.

Requirements:
1. Create story file: docs/stories/story-3.3.md
2. Create context file: docs/stories/story-context-3.3.xml
3. Update Epic 3 Status: docs/stories/EPIC-3-STATUS.md
4. **CRITICAL:** Include a placeholder section for "UAT Test Guide" in the story file.

Deliverables:
- Story File
- Context File
- Status Update
- Creation Summary
```

---

## 🧪 **Stage 2: UAT Design (Developer)**

**When:** Immediately after Story 3.3 is created.  
**Goal:** Define the test cases before coding.

### **Copy/Paste this Prompt for the Developer (@dev.mdc)**
```markdown
@dev.mdc Please design the UAT Test Guide for Story 3.3.

Story Location: docs/stories/story-3.3.md
Context: docs/stories/story-context-3.3.xml

Goal:
Create a comprehensive `docs/stories/STORY-3.3-UAT-TEST-GUIDE.md` document. 
This document must define the EXACT scenarios we will test to prove the story is complete.

Requirements:
- Define Pre-requisites (e.g., "React app running").
- Define 3-5 core Test Scenarios (e.g., "Drag item from sidebar", "Drop item on canvas", "Reorder items").
- For each scenario, list: Steps to Execute -> Expected Result.
- Include edge cases (e.g., "Drop outside canvas").

Do NOT write any implementation code yet. Just the test guide.
```

---

## 🔧 **Stage 3: Implementation (Developer)**

**When:** After you (the User) have **Approved** the UAT Test Guide.  
**Goal:** Write the code to pass the UATs.

### **Copy/Paste this Prompt for the Developer (@dev.mdc)**
```markdown
@dev.mdc Please implement Story 3.3 based on the approved UAT Guide.

Story: docs/stories/story-3.3.md
UAT Guide: docs/stories/STORY-3.3-UAT-TEST-GUIDE.md
Architecture Ref: docs/stories/EPIC-3-ARCHITECTURE-REF.md

Requirements:
1. Install `dnd-kit` (core, sortable, utilities) in the frontend.
2. Create `BuilderCanvas` component (The drop zone).
3. Create `ComponentSidebar` component (The draggable source).
4. Implement basic state management for the form definition (using React State or Context).
5. Ensure strict adherence to the UAT scenarios defined in the guide.

Focus Areas:
- Drag-and-Drop mechanics
- Visual feedback (DragOverlay)
- State updates on Drop

Please confirm completion and provide a summary.
```

---

## 📊 **Stage 4: Completion & Handover (Developer)**

**When:** Implementation is done and you have verified the UATs pass.  
**Goal:** Finalize artifacts and update documentation and git.

### **Copy/Paste this Prompt for the Developer (@dev.mdc)**
```markdown
@dev.mdc Please finalize Story 3.3.

Requirements:
1. Update `docs/stories/story-3.3.md` with a "Completion Report".
2. Mark all tests in `docs/stories/STORY-3.3-UAT-TEST-GUIDE.md` as ✅ PASSED.
3. Update `docs/stories/EPIC-3-STATUS.md` (Mark 3.3 as Complete, 3.4 as Next).
4. Update `docs/stories/EPIC-3-ARCHITECTURE-REF.md` with Canvas/DND details.
5. **GIT UPDATE:** Run the following commands to checkpoint progress:
   ```powershell
   git add .
   git commit -m "feat(epic3): Complete Story 3.3 - Drag-and-Drop Canvas"
   # git push
   ```

Deliverable:
- Finalized Story artifacts.
- Handover summary.
```

---

## 🔄 **Stage 5: Cycle Reset (PM Agent)**

**When:** Story 3.3 is finalized.  
**Goal:** Prepare this document for Story 3.4.

### **Copy/Paste this Prompt for the PM Agent (@pm.mdc)**
```markdown
@pm.mdc Please reset the cycle for the next story.

Requirements:
1. Read `docs/stories/EPIC-3-STATUS.md` to identify the next story (Story 3.4).
2. Update `docs/stories/EPIC-3-WORKFLOW-GUIDE.md`:
   - Update "Current Focus" to Story 3.4.
   - Rewrite Stages 1-4 prompts to be specific to Story 3.4 (Component Library).
   - Ensure goals and context match the new story.
3. Confirm ready for execution.
```

# Epic 3 Workflow Guide - Advanced Agentic Development

**Current Focus:** Story 3.8 - Public Form Renderer  
**Status:** 🟢 Ready for Execution  

---

## 🚨 **PM MAINTENANCE INSTRUCTIONS**
**FOR THE PM AGENT:**
At the end of every story, you **MUST** update this document.
1.  Identify the **Next Story** from `EPIC-3-STATUS.md`.
2.  **REWRITE** the prompts in Stages 1, 2, 3, and 4 below to be specific to that new story (replace "3.8" with "3.9", update goals, update context).
3.  Ensure the "Current Focus" header above reflects the new story.
4.  Only then is the story considered "Closed".

---

## 📋 **Stage 1: Create Story (Scrum Master)**

**Current Target:** Story 3.8  
**Goal:** Build the **Slim Public Form Renderer** (“The Player”) that renders `DefinitionJSON` into a fast, tablet-friendly public experience.

### **Copy/Paste this Prompt for the Scrum Master (@sm.mdc)**
```markdown
@sm.mdc Please create Epic 3 Story 3.8: Public Form Renderer.

Context:
- Previous Story: 3.7 (Rule Evaluation Engine complete - runtime logic applied in preview/renderer)
- Focus Domain: Rendering & Submission
- Goal: Render the public form from `FormVersion.DefinitionJSON` using the Component Registry, optimized for tablets/mobile.
- **Scope Boundary:** This story is **rendering + client-side UX**. The async submission/outbox pipeline is Story 3.9.

Requirements:
1. Create story file: docs/stories/story-3.8.md
2. Create context file: docs/stories/story-context-3.8.xml
3. Update Epic 3 Status: docs/stories/EPIC-3-STATUS.md
4. **CRITICAL:** Include a placeholder section for \"UAT Test Guide\" in the story file.

Functional Requirements (High Level):
- Public route/view renders the form from `DefinitionJSON` (theme + pages + components).
- Uses the same Component Registry as the Builder (no duplication).
- Supports runtime effects from Story 3.7 (visibility/required/disabled).
- Safe behavior for unknown component types or malformed config (fallback UI; do not crash).
- Data entry UX exists (field state + validation message area), but **submission transport/outbox** is deferred to Story 3.9.

Requirements:
Deliverables:
- Story File
- Context File
- Status Update
- Creation Summary
```

---

## 🧪 **Stage 2: UAT Design (Developer)**

**When:** Immediately after Story 3.8 is created.  
**Goal:** Define the test cases before coding.

### **Copy/Paste this Prompt for the Developer (@dev.mdc)**
```markdown
@dev.mdc Please design the UAT Test Guide for Story 3.8.

Story Location: docs/stories/story-3.8.md
Context: docs/stories/story-context-3.8.xml

Goal:
Create a comprehensive `docs/stories/STORY-3.8-UAT-TEST-GUIDE.md` document.

Requirements:
- Define Pre-requisites.
- Include scenarios for rendering from stored `DefinitionJSON` (happy path + unknown component fallback).
- Include responsive/tablet scenarios (layout, scrolling, touch-friendly interactions).
- Include runtime logic scenarios (rules affect visibility/required/disabled during entry).
- Include broken/missing reference behavior (do not crash).
- For each scenario, list: Steps to Execute -> Expected Result.

Do NOT write any implementation code yet. Just the test guide.
```

---

## 🔧 **Stage 3: Implementation (Developer)**

**When:** After you (the User) have **Approved** the UAT Test Guide.  
**Goal:** Write the code to pass the UATs.

### **Copy/Paste this Prompt for the Developer (@dev.mdc)**
```markdown
@dev.mdc Please implement Story 3.8 based on the approved UAT Guide.

Story: docs/stories/story-3.8.md
UAT Guide: docs/stories/STORY-3.8-UAT-TEST-GUIDE.md
Architecture Ref: docs/stories/EPIC-3-ARCHITECTURE-REF.md

Requirements:
1. Implement the **Public Form Renderer** that renders `DefinitionJSON` into a public-facing view.
2. Use the Component Registry for rendering (shared types/components where appropriate).
3. Apply runtime logic outputs (visibility/required/disabled) from Story 3.7.
4. Surface unknown/broken components safely (fallback UI; do not crash).
5. Keep submission/outbox **out of scope** (Story 3.9).

Focus Areas:
- Fast, reliable renderer UX (tablet-friendly).
- Deterministic rendering from stored DefinitionJSON (no builder-only assumptions).
- Maintain JSON-only contract (no code in DefinitionJSON).

Please confirm completion and provide a summary.
```

---

## 📊 **Stage 4: Completion & Handover (Developer)**

**When:** Implementation is done and you have verified the UATs pass.  
**Goal:** Finalize artifacts and update documentation and git.

### **Copy/Paste this Prompt for the Developer (@dev.mdc)**
```markdown
@dev.mdc Please finalize Story 3.8.

Requirements:
1. Update `docs/stories/story-3.8.md` with a \"Completion Report\".
2. Mark all tests in `docs/stories/STORY-3.8-UAT-TEST-GUIDE.md` as ✅ PASSED.
3. Update `docs/stories/EPIC-3-STATUS.md` (Mark 3.8 as Complete, 3.9 as Next).
4. Update `docs/stories/EPIC-3-ARCHITECTURE-REF.md` with renderer details (routes, fallback behavior, performance notes).
5. **GIT UPDATE (general):** Stage and commit all files changed for the story (including documentation):
   ```powershell
   git add .
   git commit -m "<type>(epic3): complete Story 3.8 - Public Form Renderer"
   # git push
   ```

Deliverable:
- Finalized Story artifacts.
- Handover summary.
```

---

## 🔄 **Stage 5: Cycle Reset (PM Agent)**

**When:** Story 3.8 is finalized.  
**Goal:** Prepare this document for Story 3.9.

### **Copy/Paste this Prompt for the PM Agent (@pm.mdc)**
```markdown
@pm.mdc Please reset the cycle for the next story.

Requirements:
1. Read `docs/stories/EPIC-3-STATUS.md` to identify the next story (Story 3.9).
2. Update `docs/stories/EPIC-3-WORKFLOW-GUIDE.md`:
   - Update \"Current Focus\" to Story 3.9.
   - Rewrite Stages 1-4 prompts to be specific to Story 3.9 (Dynamic Submission / Outbox).
   - Ensure goals and context match the new story.
3. Confirm ready for execution.
```

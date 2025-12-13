# Epic 3 Workflow Guide - Advanced Agentic Development

**Current Focus:** Story 3.7 - Rule Evaluation Engine  
**Status:** 🟢 Ready for Execution  

---

## 🚨 **PM MAINTENANCE INSTRUCTIONS**
**FOR THE PM AGENT:**
At the end of every story, you **MUST** update this document.
1.  Identify the **Next Story** from `EPIC-3-STATUS.md`.
2.  **REWRITE** the prompts in Stages 1, 2, 3, and 4 below to be specific to that new story (replace "3.7" with "3.8", update goals, update context).
3.  Ensure the "Current Focus" header above reflects the new story.
4.  Only then is the story considered "Closed".

---

## 📋 **Stage 1: Create Story (Scrum Master)**

**Current Target:** Story 3.7  
**Goal:** Implement the **runtime evaluation engine** that interprets `DefinitionJSON.logic.rules` and applies actions during preview/runtime.

### **Copy/Paste this Prompt for the Scrum Master (@sm.mdc)**
```markdown
@sm.mdc Please create Epic 3 Story 3.7: Rule Evaluation Engine.

Context:
- Previous Story: 3.6 (Conditional Logic UI complete - rules are persisted into DefinitionJSON)
- Focus Domain: Logic Engine
- Goal: **Execute** conditional rules at runtime (builder preview + renderer) like: \"Show Field X if Field Y equals 'Yes'\".
- **Scope Boundary:** This story is the **evaluation engine + runtime application**. The rule authoring UI and data model were built in Story 3.6.

Requirements:
1. Create story file: docs/stories/story-3.7.md
2. Create context file: docs/stories/story-context-3.7.xml
3. Update Epic 3 Status: docs/stories/EPIC-3-STATUS.md
4. **CRITICAL:** Include a placeholder section for \"UAT Test Guide\" in the story file.

Functional Requirements (High Level):
- Evaluate rules stored in DefinitionJSON (`formDefinition.logic.rules`) on every relevant value change.
- Apply actions in the **builder preview** and in the **renderer**:
  - show/hide, enable/disable, require/unrequire
- Ensure deterministic and predictable rule application (ordering matters).
- Provide safe behavior for missing/broken references (rule is ignored and surfaced as a warning in UI).

Requirements:
Deliverables:
- Story File
- Context File
- Status Update
- Creation Summary
```

---

## 🧪 **Stage 2: UAT Design (Developer)**

**When:** Immediately after Story 3.7 is created.  
**Goal:** Define the test cases before coding.

### **Copy/Paste this Prompt for the Developer (@dev.mdc)**
```markdown
@dev.mdc Please design the UAT Test Guide for Story 3.7.

Story Location: docs/stories/story-3.7.md
Context: docs/stories/story-context-3.7.xml

Goal:
Create a comprehensive `docs/stories/STORY-3.7-UAT-TEST-GUIDE.md` document.

Requirements:
- Define Pre-requisites.
- Include runtime scenarios for all supported actions: show/hide, enable/disable, require/unrequire.
- Include ordering scenarios (multiple rules affecting same target).
- Include broken-reference scenarios (deleted source/target).
- For each scenario, list: Steps to Execute -> Expected Result.

Do NOT write any implementation code yet. Just the test guide.
```

---

## 🔧 **Stage 3: Implementation (Developer)**

**When:** After you (the User) have **Approved** the UAT Test Guide.  
**Goal:** Write the code to pass the UATs.

### **Copy/Paste this Prompt for the Developer (@dev.mdc)**
```markdown
@dev.mdc Please implement Story 3.7 based on the approved UAT Guide.

Story: docs/stories/story-3.7.md
UAT Guide: docs/stories/STORY-3.7-UAT-TEST-GUIDE.md
Architecture Ref: docs/stories/EPIC-3-ARCHITECTURE-REF.md

Requirements:
1. Implement the **Rule Evaluation Engine** (runtime) that reads `formDefinition.logic.rules`.
2. Apply rule actions in the builder preview and renderer (show/hide, enable/disable, require/unrequire).
3. Ensure deterministic ordering and avoid infinite loops (engine safety).
4. Surface broken-reference rules as warnings (do not crash).
5. Do NOT change the authoring UI beyond what’s required to display runtime effects.

Focus Areas:
- Deterministic evaluation and predictable outcomes.
- Clear separation between rule authoring (3.6) and rule execution (3.7).
- Maintain JSON-only contract (no code in DefinitionJSON).

Please confirm completion and provide a summary.
```

---

## 📊 **Stage 4: Completion & Handover (Developer)**

**When:** Implementation is done and you have verified the UATs pass.  
**Goal:** Finalize artifacts and update documentation and git.

### **Copy/Paste this Prompt for the Developer (@dev.mdc)**
```markdown
@dev.mdc Please finalize Story 3.7.

Requirements:
1. Update `docs/stories/story-3.7.md` with a \"Completion Report\".
2. Mark all tests in `docs/stories/STORY-3.7-UAT-TEST-GUIDE.md` as ✅ PASSED.
3. Update `docs/stories/EPIC-3-STATUS.md` (Mark 3.7 as Complete, 3.8 as Next).
4. Update `docs/stories/EPIC-3-ARCHITECTURE-REF.md` with engine/runtime evaluation details.
5. **GIT UPDATE (general):** Stage and commit all files changed for the story (including documentation):
   ```powershell
   git add .
   git commit -m "<type>(epic3): complete Story 3.7 - Rule Evaluation Engine"
   # git push
   ```

Deliverable:
- Finalized Story artifacts.
- Handover summary.
```

---

## 🔄 **Stage 5: Cycle Reset (PM Agent)**

**When:** Story 3.7 is finalized.  
**Goal:** Prepare this document for Story 3.8.

### **Copy/Paste this Prompt for the PM Agent (@pm.mdc)**
```markdown
@pm.mdc Please reset the cycle for the next story.

Requirements:
1. Read `docs/stories/EPIC-3-STATUS.md` to identify the next story (Story 3.8).
2. Update `docs/stories/EPIC-3-WORKFLOW-GUIDE.md`:
   - Update \"Current Focus\" to Story 3.8.
   - Rewrite Stages 1-4 prompts to be specific to Story 3.8 (Public Form Renderer).
   - Ensure goals and context match the new story.
3. Confirm ready for execution.
```

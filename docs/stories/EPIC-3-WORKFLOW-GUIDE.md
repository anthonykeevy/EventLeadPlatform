# Epic 3 Workflow Guide - Advanced Agentic Development

**Current Focus:** Story 3.1 - Form Versioning Architecture  
**Status:** 🟢 Ready for Execution  

---

## 🚨 **PM MAINTENANCE INSTRUCTIONS**
**FOR THE PM AGENT:**
At the end of every story, you **MUST** update this document.
1.  Identify the **Next Story** from `EPIC-3-STATUS.md`.
2.  **REWRITE** the prompts in Stages 1, 2, 3, and 4 below to be specific to that new story (replace "3.1" with "3.2", update goals, update context).
3.  Ensure the "Current Focus" header above reflects the new story.
4.  Only then is the story considered "Closed".

---

## 📋 **Stage 1: Create Story (Scrum Master)**

**Current Target:** Story 3.1  
**Goal:** Establish the database foundation for form versioning.

### **Copy/Paste this Prompt for the Scrum Master (@sm.mdc)**
```markdown
@sm.mdc Please create Epic 3 Story 3.1: Form Versioning Architecture.

Context:
- Previous Story: None (Epic Start)
- Focus Domain: Schema & Versioning
- Goal: Establish the database foundation (FormVersion table) and backend logic to store and retrieve JSON form definitions.

Requirements:
1. Create story file: docs/stories/story-3.1.md
2. Create context file: docs/stories/story-context-3.1.xml
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

**When:** Immediately after Story 3.1 is created.  
**Goal:** Define the test cases before coding.

### **Copy/Paste this Prompt for the Developer (@dev.mdc)**
```markdown
@dev.mdc Please design the UAT Test Guide for Story 3.1.

Story Location: docs/stories/story-3.1.md
Context: docs/stories/story-context-3.1.xml

Goal:
Create a comprehensive `docs/stories/STORY-3.1-UAT-TEST-GUIDE.md` document. 
This document must define the EXACT scenarios we will test to prove the story is complete.

Requirements:
- Define Pre-requisites (e.g., "Database is migrated").
- Define 3-5 core Test Scenarios (e.g., "Create new form version", "Retrieve specific version", "Publish version").
- For each scenario, list: Steps to Execute -> Expected Result.
- Include edge cases (e.g., "Retrieve non-existent version").

Do NOT write any implementation code yet. Just the test guide.
```

---

## 🔧 **Stage 3: Implementation (Developer)**

**When:** After you (the User) have **Approved** the UAT Test Guide.  
**Goal:** Write the code to pass the UATs.

### **Copy/Paste this Prompt for the Developer (@dev.mdc)**
```markdown
@dev.mdc Please implement Story 3.1 based on the approved UAT Guide.

Story: docs/stories/story-3.1.md
UAT Guide: docs/stories/STORY-3.1-UAT-TEST-GUIDE.md
Architecture Ref: docs/stories/EPIC-3-ARCHITECTURE-REF.md

Requirements:
1. Implement the `FormVersion` SQLAlchemy model and migration.
2. Implement the `FormService` logic for version control (Draft/Published).
3. Ensure strict adherence to the UAT scenarios defined in the guide.
4. Run linter checks on all edited files.

Focus Areas:
- Database Migration (Alembic)
- JSON Storage (SQL Server NVARCHAR(MAX))
- Service Logic (Versioning Strategy)

Please confirm completion and provide a summary.
```

---

## 📊 **Stage 4: Completion & Handover (Developer)**

**When:** Implementation is done and you have verified the UATs pass.  
**Goal:** Finalize artifacts and update documentation.

### **Copy/Paste this Prompt for the Developer (@dev.mdc)**
```markdown
@dev.mdc Please finalize Story 3.1.

Requirements:
1. Update `docs/stories/story-3.1.md` with a "Completion Report".
2. Mark all tests in `docs/stories/STORY-3.1-UAT-TEST-GUIDE.md` as ✅ PASSED.
3. Update `docs/stories/EPIC-3-STATUS.md` (Mark 3.1 as Complete, 3.2 as Next).
4. Update `docs/stories/EPIC-3-ARCHITECTURE-REF.md` with the final `FormVersion` table schema.

Deliverable:
- Finalized Story artifacts.
- Handover summary.
```

---

## 🔄 **Stage 5: Cycle Reset (PM Agent)**

**When:** Story 3.1 is finalized.  
**Goal:** Prepare this document for Story 3.2.

**PM Instructions:**
1.  Read `EPIC-3-STATUS.md` to confirm Story 3.2 is next.
2.  **Update this file (`EPIC-3-WORKFLOW-GUIDE.md`)**:
    *   Change "Current Target" to **Story 3.2**.
    *   Update Stage 1 Prompt with Story 3.2 Context/Goals.
    *   Update Stage 2, 3, 4 Prompts with "3.2" file paths.
3.  Notify the user that the guide is ready for the next cycle.

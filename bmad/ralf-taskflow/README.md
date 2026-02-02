# Ralf Taskflow Module

**BMAD v6 Module for Complete Task Lifecycle: Decompose → Execute → Validate → Learn**

## Overview

The Ralf Taskflow module provides four intelligent agents that work together in a complete task lifecycle:

| Agent | Role | Responsibility |
|-------|------|----------------|
| **Ralf (ralf-sm)** | Scrum Master | Decomposes stories into small, testable tasks |
| **Ralf-Dev (ralf-dev)** | Task Executor | Implements ONE task per session with strict verification |
| **Ralf-UAT (ralf-uat)** | UAT Gatekeeper | Validates with human testers, records evidence |
| **Ralf-Retro (ralf-retro)** | Memory Curator | Extracts lessons and test improvements |

Each task runs in its own isolated conversation session, with continuous learning to reduce future rework.

---

## Complete Workflow (Main Chat + Task Chats Architecture)

```
┌─────────────────────────────────────────────────────────────────┐
│                   MAIN CHAT (persistent)                        │
├─────────────────────────────────────────────────────────────────┤
│  1. STORY DECOMPOSITION (@ralf-sm)                              │
│     Story.md ──→ *decompose-story ──→ TASK-PLAN.md (skeleton)   │
│                                       T01.md (detailed)          │
│                                       T02.md (placeholder)       │
│                          │                                       │
│                          ▼                                       │
│     [Open NEW Task Chat for T01]                                │
│                          │                                       │
│                          ▼                                       │
│  2. NEXT TASK (@ralf-sm) - after Task Chat returns              │
│     *next-task ──→ Update TASK-PLAN.md                          │
│                ──→ Create T02.md (detailed)                     │
│                ──→ Check story completion                       │
│                          │                                       │
│                          ▼                                       │
│     [Open NEW Task Chat for T02]                                │
│                          │                                       │
│                     [repeat until done]                         │
│                          │                                       │
│  3. STORY COMPLETE (@dev.mdc) - finalize, git commit            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   TASK CHAT (one per task, isolated)            │
├─────────────────────────────────────────────────────────────────┤
│  A. EXECUTE (@ralf-dev)                                         │
│     T01.md ──→ *run-task ──→ T01.completion.md                  │
│                          ──→ T01.uat.md (AUTO-GENERATED)        │
│                          │                                       │
│  B. HUMAN TESTS - execute UAT checklist manually                │
│                          │                                       │
│  C. RECORD (@ralf-uat) ──→ *record-uat ──→ T01.uat-results.md   │
│                          │                                       │
│         ┌────────────────┴────────────────┐                     │
│         │ PASS                            │ FAIL                │
│         ▼                                 ▼                     │
│  D. RETRO (@ralf-retro)           [Fix + Re-test]               │
│     *run-retro ──→ T01.retro.md                                 │
│                ──→ LESSONS-LEARNED                              │
│                          │                                       │
│  [Close Task Chat, return to Main Chat]                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Module Structure

```
bmad/ralf-taskflow/
├── module.yaml
├── config.yaml
├── README.md
├── agents/
│   ├── ralf-sm/ralf-sm.agent.yaml
│   ├── ralf-dev/ralf-dev.agent.yaml
│   ├── ralf-uat/ralf-uat.agent.yaml
│   └── ralf-retro/ralf-retro.agent.yaml
├── workflows/
│   ├── decompose-story/          # ralf-sm
│   ├── refine-task/              # ralf-sm
│   ├── run-task/                 # ralf-dev
│   ├── scope-check/              # ralf-dev
│   ├── prepare-uat/              # ralf-dev
│   ├── handoff/                  # ralf-dev
│   ├── uat-generate/             # ralf-uat
│   ├── uat-record/               # ralf-uat
│   ├── uat-scope-check/          # ralf-uat
│   ├── uat-handoff/              # ralf-uat
│   ├── retro-run/                # ralf-retro
│   ├── retro-testing-playbook/   # ralf-retro
│   ├── retro-spec-improvement/   # ralf-retro
│   └── retro-route-item/         # ralf-retro
└── memory/
    ├── decomposition-patterns.yaml
    ├── failure-patterns.yaml
    ├── high-leverage-tests.yaml
    ├── dev-patterns.yaml
    ├── common-failures.yaml
    ├── test-shortcuts.yaml
    ├── uat-failure-patterns.yaml
    ├── uat-checklist-patterns.yaml
    ├── automation-opportunities.yaml
    ├── retro-patterns.yaml
    ├── test-gap-patterns.yaml
    └── process-improvements.yaml

.cursor/rules/bmad/ralf-taskflow/agents/
├── ralf-sm.mdc
├── ralf-dev.mdc
├── ralf-uat.mdc
└── ralf-retro.mdc
```

---

## Agent: Ralf-SM (Scrum Master)

**Purpose:** Decomposes stories into small, testable tasks and manages task progression.

### Commands

| Command | Description |
|---------|-------------|
| `*decompose-story` | Story → TASK-PLAN + Task Specs (skeleton upfront) |
| `*next-task` | Review completed task, prepare next task (Main Chat) |
| `*refine-task` | Update task spec based on feedback |
| `*scope-check` | Verify if request is in-scope |
| `*generate-uat` | Generate UAT checklist |
| `*record-lesson` | Record lesson to LESSONS-LEARNED.md |

### Activation

```
@ralf-sm
```

---

## Agent: Ralf-Dev (Task Executor)

**Purpose:** Executes exactly ONE task per session with strict verification and auto-generates UAT checklist.

### Commands

| Command | Description |
|---------|-------------|
| `*run-task` | Execute task (implement + verify + complete + **auto-generate UAT**) |
| `*scope-check` | Check if request is in-scope for task |
| `*prepare-uat` | Generate UAT checklist from changes (manual trigger) |
| `*handoff` | Complete task + prepare handoff |

**Note:** `*run-task` now automatically generates the UAT checklist after completion, reducing manual steps.

### Core Principles

1. Follow Task Spec exactly - do not expand scope
2. If not verifiable, it's not done
3. Smallest viable change - minimize file touch
4. One session = one task

### Activation

```
@ralf-dev
```

---

## Agent: Ralf-UAT (Human UAT Gatekeeper)

**Purpose:** Generates UAT checklists and records human test results.

### Commands

| Command | Description |
|---------|-------------|
| `*generate-uat` | Generate UAT checklist from Task Spec + Completion Note |
| `*record-uat` | Record human results and update status |
| `*scope-check` | Check if request is defect or out-of-scope |
| `*handoff` | Complete UAT and route to next agent |

### Core Principles

1. No code changes - only validate and record
2. Defects only if they violate Acceptance Criteria
3. Demand reproducible evidence
4. Every failure is an automation opportunity

### Activation

```
@ralf-uat
```

---

## Agent: Ralf-Retro (Retrospective + Memory Curator)

**Purpose:** Extracts lessons and test improvements from completed tasks.

### Commands

| Command | Description |
|---------|-------------|
| `*run-retro` | Run full retrospective on completed task |
| `*update-testing-playbook` | Update testing playbook with patterns |
| `*spec-improvement` | Improve Task Spec clarity (no scope expansion) |
| `*route-item` | Route scope creep / new work to backlog |

### Core Principles

1. Evidence over opinion - cite files/outputs
2. Prevent recurrence - every defect yields prevention action
3. Prefer automation - convert manual checks into tests
4. Append-only learning - never delete lessons

### Activation

```
@ralf-retro
```

---

## Output Artifacts

### Per Story (from ralf-sm)

```
docs/tasks/{story-id}/
├── TASK-PLAN.md
├── T01-{slug}.md
├── T02-{slug}.md
└── LESSONS-LEARNED.md
```

### Per Task (from ralf-dev)

```
docs/tasks/{story-id}/
├── T01-{slug}.completion.md
└── T01-{slug}.qa-notes.md
```

### Per UAT (from ralf-uat)

```
docs/tasks/{story-id}/
├── T01-{slug}.uat.md          # Checklist
├── T01-{slug}.uat-results.md  # Results + evidence
└── STATUS.md                  # Task statuses
```

### Per Retro (from ralf-retro)

```
docs/tasks/{story-id}/
├── T01-{slug}.retro.md        # Retro summary
├── LESSONS-LEARNED.md         # Appended lessons
└── BACKLOG-ITEMS.md           # Routed scope creep

docs/learning/
└── testing-playbook.md        # Reusable test patterns
```

---

## Retro Output Detail

### Task Retro Summary

```markdown
# Task Retrospective: T01-setup

## What Went Well
| Item | Evidence |
|------|----------|
| Tests caught edge case | completion.md line 45 |

## What Went Wrong
| Issue | Root Cause | Evidence |
|-------|------------|----------|
| UAT failed on empty input | Missing AC | uat-results.md |

## Prevention Actions
| Issue | Prevention | Owner |
|-------|------------|-------|
| Missing AC | Add edge case template | ralf-sm |

## Test Improvements
| Test Type | Description | Location |
|-----------|-------------|----------|
| unit | Validate empty input | form.test.ts |

## Process Improvements
- ralf-sm: Include edge case checklist
- ralf-dev: Run validation tests first
- ralf-uat: Add empty input to checklist
```

---

## Memory System

### Shared Memory

| File | Used By | Purpose |
|------|---------|---------|
| `high-leverage-tests.yaml` | All agents | Test patterns that catch bugs |
| `process-improvements.yaml` | All agents | Proven process improvements |

### ralf-sm Memory

| File | Purpose |
|------|---------|
| `decomposition-patterns.yaml` | Proven decomposition strategies |
| `failure-patterns.yaml` | Known failure modes to prevent |

### ralf-dev Memory

| File | Purpose |
|------|---------|
| `dev-patterns.yaml` | Implementation patterns |
| `common-failures.yaml` | Common breakages and prevention |
| `test-shortcuts.yaml` | Quick test commands |

### ralf-uat Memory

| File | Purpose |
|------|---------|
| `uat-failure-patterns.yaml` | Recurring UAT failure modes |
| `uat-checklist-patterns.yaml` | Best checklist structures |
| `automation-opportunities.yaml` | Tests to add earlier |

### ralf-retro Memory

| File | Purpose |
|------|---------|
| `retro-patterns.yaml` | Root causes and prevention |
| `test-gap-patterns.yaml` | Common test gaps |
| `process-improvements.yaml` | Process refinements |

---

## Continuous Learning Flow

```
ralf-retro
    │
    ├── Updates retro-patterns.yaml
    │       └── ralf-sm reads to improve decomposition
    │
    ├── Updates test-gap-patterns.yaml
    │       └── ralf-dev reads to add missing tests
    │
    ├── Updates process-improvements.yaml
    │       └── All agents read to improve process
    │
    └── Updates testing-playbook.md
            └── Humans reference for test patterns
```

---

## Installation

The agents are ready to use:

```
.cursor/rules/bmad/ralf-taskflow/agents/
├── ralf-sm.mdc     ✅
├── ralf-dev.mdc    ✅
├── ralf-uat.mdc    ✅
└── ralf-retro.mdc  ✅
```

Activate with:
- `@ralf-sm` - Decompose story into tasks
- `@ralf-dev` - Execute a single task
- `@ralf-uat` - Validate with human UAT
- `@ralf-retro` - Run retrospective

---

## Typical Session Flow (Main Chat + Task Chats)

### Main Chat: Decompose Story
```
@ralf-sm
*decompose-story
[Provide story file path]
→ Generates TASK-PLAN.md (skeleton), T01.md (detailed), T02.md (placeholder), etc.
```

### Task Chat: Execute Task 1 (NEW CHAT)
```
@ralf-dev
*run-task
[Provide T01.md path]
→ Implements task
→ Generates T01.completion.md
→ AUTO-GENERATES T01.uat.md (UAT checklist)

[Human tests using UAT checklist]

@ralf-uat
*record-uat
[Provide results]
→ Records results, sets status

@ralf-retro
*run-retro
[Provide task files]
→ Generates T01.retro.md, updates lessons

[Close Task Chat]
```

### Main Chat: Prepare Next Task
```
@ralf-sm
*next-task
[Provide story ID and completed task ID]
→ Updates TASK-PLAN.md
→ Verifies completion
→ Creates/refines T02.md (detailed)
→ Provides instructions for next Task Chat
```

### Repeat for T02, T03, etc. until all tasks complete

---

## Version History

- **1.6.0** (2026-01-14) - **DevTools MCP integration**: Added DevTools MCP usage for technical verification in ralf-uat. Added safe TypeScript checking methods to ralf-dev to avoid Cursor chat crashes.
- **1.5.0** (2026-01-14) - **ralf-uat auto-complete fix**: Agent now automatically creates uat-results.md and updates TASK-PLAN.md on pass without asking. Added mandatory handoff instructions to ralf-retro.
- **1.4.0** (2026-01-14) - Added `*next-task` workflow to ralf-sm, auto-UAT generation in ralf-dev, Main Chat + Task Chats architecture
- **1.3.0** (2026-01-11) - Added ralf-retro agent with retrospective workflows
- **1.2.0** (2026-01-11) - Added ralf-uat agent with UAT workflows
- **1.1.0** (2026-01-11) - Added ralf-dev agent with execution workflows
- **1.0.0** (2026-01-11) - Initial release with ralf-sm

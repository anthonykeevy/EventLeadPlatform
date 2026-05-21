# Epic 6 — SM Tools Registry

**Owner:** SM (Scrum Master agent)  
**Purpose:** Single index of scripts and automation the SM and Dev agents use during Epic 6 stories. When closeout audits surface repeated manual steps, add a tool here and wire it into `EPIC-6-WORKFLOW-GUIDE.md`.

**Rule:** Before inventing a one-off script in a story, check this registry. If a similar tool exists, extend it. If you add a new tool, register it in the same PR as the story implementation (or SM housekeeping PR).

---

## Workflow scripts (`scripts/workflow/`)

| Tool | When to use | Output artifact |
|------|-------------|-----------------|
| `preflight-story.ps1` | Start of every story; verifies worktree, branch, DB URL parity | `STORY-6.x-PREFLIGHT.md` |
| `run-green-gate.ps1` | Before UAT request; enforces full pytest/lint summary | `STORY-6.x-GATE-EVIDENCE.md` |
| `generate-story-evidence.ps1` | Sync gate evidence into UAT results | `STORY-6.x-UAT-RESULTS.md` |
| `collect-tool-feedback.ps1` | End of story; Dev rates workflow tools | SM process improvement |

---

## Git / story bootstrap

| Tool | When to use |
|------|-------------|
| `scripts/git/new-story.ps1` | SM opens new story branch + worktree + Draft PR |

---

## Story-specific / domain tools (`backend/scripts/`)

| Tool | Story | When to use |
|------|-------|-------------|
| `story_6_5b_prompt_equivalence_diff.py` | 6.5b | Backend-only prompt path changes; AC-19 gate |
| `check_uat_forms_504_813.py` | 6.5c | UAT form replay diagnostics |
| `verify_component_catalog_alignment.py` | **6.5d** | After any `FormBuilderComponent` change; proves init = resolver = prompt = validator |

---

## Planned / requested tools (backlog)

| Idea | Trigger | Owner |
|------|---------|-------|
| `alembic_head_report.ps1` | Tony asks "what migrations are pending?" | SM doc only — **never run Alembic in agent** |
| Local deploy smoke (uvicorn + health) | Pre-push gate optional | Consider extending `run-green-gate.ps1` |
| Friction log aggregator | Parse `STORY-*-IMPLEMENTATION-FRICTION-LOG.md` across stories | Post-Epic 6 retro |

---

## How SM uses this at closeout

1. Confirm story PR registered any **new** tools in this file.
2. If Dev's friction log names a repeated manual step → open a tool task for next story or workflow amendment.
3. Cross-link from `EPIC-6-WORKFLOW-GUIDE.md` § Workflow Automation Toolkit.

---

*Last updated: 2026-05-21 (Story 6.5d SM pack).*

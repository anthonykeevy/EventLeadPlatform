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

## Diagnostics & logging (platform-wide)

| Tool | When to use | Output / data source |
|------|-------------|----------------------|
| **`docs/AGENT-LOGGING-GUIDE.md`** | Builder UI bugs, Form AI failures, API/auth issues — **canonical** investigation path | `log.ApiRequest`, `log.FrontendEvent`, `log.ApplicationError`, `log.AuthEvent` via `python backend/enhanced_diagnostic_logs.py` |
| `backend/enhanced_diagnostic_logs.py` | Pull correlated DB logs by path, `RequestID`, or frontend filter | Console report (redact secrets) |
| Frontend Dev Logs | Builder resize/toolbox/canvas issues | JSON download from UI + optional `POST /api/v1/logs/frontend` |

**Quick commands (from AGENT-LOGGING-GUIDE):**

```bash
python backend/enhanced_diagnostic_logs.py --limit 50
python backend/enhanced_diagnostic_logs.py --path-filter form-ai --limit 20
python backend/enhanced_diagnostic_logs.py --request-id "<uuid>" --correlation-only
```

---

## Database schema & seed reference (`docs/database/` + generator)

| Tool | When to use | Output artifact |
|------|-------------|-----------------|
| **`docs/database/schema-reference/*.md`** | Human-readable table/column reference by schema (`dbo`, `ref`, `log`, `audit`, `config`, `cache`) | Static MD (may be stale — regenerate if migrations changed) |
| **`docs/database/SEED-DATA-REFERENCE.md`** | Seed SQL / reference data for ref tables (incl. AU `AddressValidationProvider`, `CompanyValidationProvider`) | Static MD |
| `scripts/get_database_schema.py` | Regenerate full schema export from live DB | Default: `docs/database-schema.md`; or `-o path` / `--file` |

**Regenerate schema (Tony or Dev — requires working `DATABASE_URL`):**

```powershell
python scripts/get_database_schema.py --file
# or explicit path:
python scripts/get_database_schema.py -o docs/database-schema.md
```

**Maintenance note (2026-05-21):** Per-schema files under `docs/database/schema-reference/` were produced during Epic 1 rebuild (`REBUILD-PLAN-SUMMARY.md`); they are **not** auto-updated by the script unless you split/regenerate manually. After large migration stories, run `get_database_schema.py` and diff against `schema-reference/` or replace.

---

## Story-specific / domain tools (`backend/scripts/`)

| Tool | Story | When to use |
|------|-------|-------------|
| `story_6_5b_prompt_equivalence_diff.py` | 6.5b | Backend-only prompt path changes; AC-19 gate |
| `check_uat_forms_504_813.py` | 6.5c | UAT form replay diagnostics |
| `verify_component_catalog_alignment.py` | **6.5d** | After any `FormBuilderComponent` change; proves init = resolver = prompt = validator |

---

## Integration handoff docs (external / cross-project)

| Doc | When to use |
|-----|-------------|
| `docs/architecture/au-address-lookup-geoscape-handoff.md` | 6.5d `address-lookup-au` — points to JobTrackerDB GeoScape implementation |
| `docs/architecture/abr-company-lookup-builder-handoff.md` | ABR builder component — reuse `abr_client` + onboarding UX |

---

## Planned / requested tools (backlog)

| Idea | Trigger | Owner |
|------|---------|-------|
| `alembic_head_report.ps1` | Tony asks "what migrations are pending?" | SM doc only — **never run Alembic in agent** |
| Local deploy smoke (uvicorn + health) | Pre-push gate optional | Consider extending `run-green-gate.ps1` |
| Friction log aggregator | Parse `STORY-*-IMPLEMENTATION-FRICTION-LOG.md` across stories | Post-Epic 6 retro |
| Schema-reference sync script | Split `database-schema.md` → `schema-reference/*.md` | After 6.5d if manual drift painful |

---

## How SM uses this at closeout

1. Confirm story PR registered any **new** tools in this file.
2. If Dev's friction log names a repeated manual step → open a tool task for next story or workflow amendment.
3. Cross-link from `EPIC-6-WORKFLOW-GUIDE.md` § Workflow Automation Toolkit.

---

*Last updated: 2026-05-21 (Tony: agent logging + database reference tools; GeoScape/ABR handoffs).*

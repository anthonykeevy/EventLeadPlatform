# KB + Kaizen Workflow (SQL-authoritative) — PM Agent Protocol

**Goal**: Capture ideas and evolving business/technical knowledge without turning everything into delivery work prematurely.

**Authoritative store**: SQL Server `EventLeadPlatform` database, schema `kb` (created by Alembic migration `backend/migrations/versions/036_kb_knowledge_base.py`).

**Important**: KB records live in SQL. **Do not scan the repo** to find “open ideas” — always query the `kb` schema via `kb_cli.py`.

**Key rule**: A GitHub Issue/Project item is created **only** when an idea is explicitly approved for delivery work (status `approved_to_build`).

---

## Quick start (recommended)

- Start (or checkpoint mid-chat): `@pm.mdc` → `*kb-intake`
- End of chat: `@pm.mdc` → `*kb-close`
- Any time you need to refresh the protocol: `@pm.mdc` → `*kb`

These two checkpoints are the safest way to prevent “context blowouts” in long ideation sessions.

## What to do in every ideation chat (agent-owned)

When a user shares an idea or changes direction mid-chat:

1. **Create/Update an `Aspect`** (durable dossier) and link it to related aspects via `kb.AspectRelation`.
2. **Create/Update an `Idea`** (incubation item) and link it to the aspect via `kb.IdeaAspect`.
3. **Record a `SessionNote`** summarizing:
   - what changed in direction
   - decisions made (accepted/rejected and why)
   - next questions / next step
4. **Generate a context pack** for the current aspect when needed (prevents context blowouts).
5. **If a decision impacts other aspects**, enqueue Kaizen impact reviews using `kb.EnqueueRelatedAspectReviews`.

This ensures the conversation is never “lost” and can be revisited later.

---

## Where Analyst + Architect fit (BMAD leverage)

You don’t need a special “agent-to-agent call” mechanism to benefit from Analyst/Architect thinking:

- **Option A (single PM chat, no persona switching)**: run the same BMAD workflows directly from PM:
  - `*brainstorm-project` (option space)
  - `*research` (market/competitive/technical)
  - `*product-brief` (turn findings into a structured brief)
- **Option B (persona switching)**: invoke the other agents explicitly when you want their voice:
  - `@analyst.mdc` → `*brainstorm-project`, `*research`, `*product-brief`
  - `@architect.mdc` → `*tech-spec` or `*solution-architecture` (when an idea is trending toward `approved_to_build`)

**KB rule remains unchanged**: record results as `SessionNote` (and later `DocRef`) and keep the idea in SQL until it is explicitly approved.

---

## Status model (practical)

### Ideas (`kb.IdeaStatus.StatusCode`)

- `captured`: recorded but not evaluated
- `exploring`: research/options/impact analysis in progress
- `parked`: intentionally paused; keep next trigger/review reason in notes
- `rejected`: rejected with rationale; can be revisited
- `approved_to_build`: approved for delivery work (may create GitHub work item)
- `implemented`: implementation completed and linked
- `validated`: value validated; keep maintenance cadence

### Aspects (`kb.AspectState.StateCode`)

- `active`: being explored/maintained
- `parked`: paused but intentionally preserved
- `deprecated`: kept only for history

---

## CLI commands (agent runs these)

All commands run from repo root.

### Create an aspect

```powershell
python backend/scripts/kb_cli.py create-aspect --key "process.knowledge-management" --title "Process: Knowledge management" --summary "..." --pretty
```

### Create an idea (incubation)

```powershell
python backend/scripts/kb_cli.py create-idea --title "<idea title>" --problem-statement "..." --status captured --pretty
```

### Link idea → aspect

```powershell
python backend/scripts/kb_cli.py link-idea-aspect --idea-id <IdeaID> --aspect "process.knowledge-management" --pretty
```

### Link aspects (typed)

```powershell
python backend/scripts/kb_cli.py link-aspects --from "process.knowledge-management" --to "process.git-workflow" --type impacts --pretty
```

### Record a session note (capture the chat)

```powershell
python backend/scripts/kb_cli.py add-session-note --title "<note title>" --summary "..." --decisions "..." --aspect "process.knowledge-management" --idea <IdeaID> --pretty
```

### Context pack (for reliable prompting)

```powershell
python backend/scripts/kb_cli.py context-pack --aspect "process.knowledge-management" --pretty
```

### Open ideas (with linked aspects)

Use this when you want “what ideas are still open?” without any extra reasoning or repo scanning.

```powershell
python backend/scripts/kb_cli.py open-ideas --pretty
```

### Idea pack (full recall by IdeaID)

Use this when you want “tell me everything about IdeaID X” without repo scanning.

```powershell
python backend/scripts/kb_cli.py idea-pack --idea-id <IdeaID> --pretty
```

### DocRefs (structured references to docs/sections)

Use these to attach durable document references to ideas/aspects (instead of burying paths in free-text notes).

Create (or reuse) a DocRef:

```powershell
python backend/scripts/kb_cli.py add-docref --path "docs/workflows/KB-KAIZEN-KNOWLEDGE-BASE-WORKFLOW.md" --context-note "KB protocol hub" --pretty
```

Link DocRef → Idea:

```powershell
python backend/scripts/kb_cli.py link-idea-docref --idea-id <IdeaID> --docref-id <DocRefID> --notes "Why this doc matters to the idea" --pretty
```

Link DocRef → Aspect:

```powershell
python backend/scripts/kb_cli.py link-aspect-docref --aspect "process.knowledge-management" --docref-id <DocRefID> --notes "Why this doc matters to the aspect" --pretty
```

### Enqueue Kaizen impact review tasks

```powershell
python backend/scripts/kb_cli.py enqueue-review --aspect "process.knowledge-management" --reason "<why this change impacts related aspects>" --pretty
```

---

## PM agent prompt snippet (copy/paste)

```markdown
@pm.mdc

I’m going to give you an idea. You must manage it in the SQL Knowledge Base (schema `kb`) using `python backend/scripts/kb_cli.py`.

Rules:
- Create/update an Aspect and link it to related aspects (typed relations).
- Create/update an Idea and link it to the Aspect.
- Always record a SessionNote summarizing the conversation and the decision (even if we reject/park).
- Do NOT create GitHub Issues/Project items unless I explicitly say: **ApproveToBuild**.
- If a decision impacts other aspects, enqueue Kaizen impact review tasks.

Idea:
<paste idea here>
```


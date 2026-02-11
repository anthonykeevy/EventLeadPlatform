# KB Intake (mid-chat checkpoint) — PM Agent

**When to run**: at the start of an ideation chat, or whenever the conversation pivots.

**Goal**: create/link the core KB records *now* (before context truncation) and capture a durable checkpoint as a `SessionNote`.

**Authoritative store**: SQL Server `EventLeadPlatform`, schema `kb`.

---

## Steps (agent-owned)

### 1) Pick the primary aspect

Decide a primary `AspectKey` for this conversation.

**Key format** (recommended):
- Lowercase + dot-separated category + hyphenated slug
- Examples:
  - `process.knowledge-management`
  - `product.enterprise-onboarding`
  - `tech.frontend-build-stability`

### 2) Check whether the aspect already exists

Run a context pack lookup. If it exists, keep going. If it does not exist, create it.

```powershell
python backend/scripts/kb_cli.py context-pack --aspect "<AspectKey>" --pretty
```

If it returns `Aspect not found`, create it:

```powershell
python backend/scripts/kb_cli.py create-aspect --key "<AspectKey>" --title "<Aspect title>" --summary "<1-2 sentence summary>" --maturity M0 --state active --pretty
```

### 3) Create the idea (captured)

```powershell
python backend/scripts/kb_cli.py create-idea --title "<Idea title>" --problem-statement "<What problem are we solving?>" --hypothesis "<Why might this help?>" --next-step "<What do we do next?>" --status captured --pretty
```

### 4) Link idea → aspect

```powershell
python backend/scripts/kb_cli.py link-idea-aspect --idea-id <IdeaID> --aspect "<AspectKey>" --notes "<Why this idea belongs to this aspect>" --pretty
```

### 5) Record the intake checkpoint as a SessionNote

Use this as a durable “checkpoint” so we can safely continue the chat.

```powershell
python backend/scripts/kb_cli.py add-session-note --title "<Short checkpoint title (YYYY-MM-DD)>" --summary "<What we’re exploring + current direction>" --decisions "<Any decisions so far>" --source-type cursor_chat --source-ref "<optional>" --idea <IdeaID> --aspect "<AspectKey>" --pretty
```

### 6) Optional: move to exploring + run structured ideation

If we’re going to research/compare options, set the idea to `exploring`:

```powershell
python backend/scripts/kb_cli.py set-idea-status --idea-id <IdeaID> --status exploring --pretty
```

Then optionally run (still in PM agent):
- `*brainstorm-project` (generate option space quickly)
- `*research` (market/competitive/technical research)
- `*product-brief` (turn outcomes into a structured brief)

---

## Output to keep visible in the chat thread

- **AspectKey**: `<AspectKey>`
- **IdeaID**: `<IdeaID>`


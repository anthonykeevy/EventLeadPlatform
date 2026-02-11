# KB Close (end-of-chat closeout) — PM Agent

**When to run**: at the end of an ideation chat (or before switching topics).

**Goal**: capture final decisions + next step as a `SessionNote`, then set the correct `IdeaStatus` so the KB queue stays trustworthy.

---

## Steps (agent-owned)

### 1) Identify the primary AspectKey and IdeaID

If you already have them in the chat thread, reuse them.

If you only have the aspect key, pull the context pack and pick the right `IdeaID` from the output:

```powershell
python backend/scripts/kb_cli.py context-pack --aspect "<AspectKey>" --pretty
```

If nothing exists yet, fall back to `*kb-intake` first.

### 2) Record the closeout SessionNote (final summary)

```powershell
python backend/scripts/kb_cli.py add-session-note --title "<Closeout title (YYYY-MM-DD)>" --summary "<What we concluded + why>" --decisions "<Decision + rationale + next step>" --source-type cursor_chat --source-ref "<optional>" --idea <IdeaID> --aspect "<AspectKey>" --pretty
```

### 3) Set the final idea status

Pick the status that matches the conversation outcome:

- **Still investigating**:

```powershell
python backend/scripts/kb_cli.py set-idea-status --idea-id <IdeaID> --status exploring --pretty
```

- **Parked intentionally** (paused with an explicit trigger to resume):

```powershell
python backend/scripts/kb_cli.py park-idea --idea-id <IdeaID> --decision-summary "<Why parked + what would trigger resuming>" --pretty
```

- **Rejected**:

```powershell
python backend/scripts/kb_cli.py set-idea-status --idea-id <IdeaID> --status rejected --decision-summary "<Why rejected>" --pretty
```

- **Approved for delivery** (create GitHub delivery work only after this):

```powershell
python backend/scripts/kb_cli.py approve-idea --idea-id <IdeaID> --decision-summary "<Why approved + expected value>" --pretty
```

### 4) If the decision impacts other aspects, enqueue Kaizen impact reviews

```powershell
python backend/scripts/kb_cli.py enqueue-review --aspect "<AspectKey>" --reason "<What changed and why related aspects should be reviewed>" --pretty
```

### 5) Final sanity check (optional)

```powershell
python backend/scripts/kb_cli.py context-pack --aspect "<AspectKey>" --pretty
```


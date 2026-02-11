# KB: Idea pack (full recall) — PM Agent

**Goal**: return “everything we know” about a specific idea in one command, without repo scanning.

Includes:
- Idea core fields (problem/hypothesis/impact/risks/next step/status)
- Linked aspects
- Linked session notes
- Linked DocRefs
- Linked work items (if any)

---

## Steps (agent-owned)

### 1) Run the one-command query

```powershell
python backend/scripts/kb_cli.py idea-pack --idea-id <IdeaID> --pretty
```

### 2) Present results as a compact summary

Show:
- **Idea**: title + status + next step
- **Aspects**: list `AspectKey`
- **DocRefs**: list `DocPath` (and `AnchorID` if present)
- **Latest session note**: title + 1–2 sentence summary


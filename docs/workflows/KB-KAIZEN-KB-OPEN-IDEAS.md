# KB: List open ideas (fast) — PM Agent

**Goal**: return a concise list of “open” ideas and the aspects they are linked to.

**Definition (default)**: “open” = IdeaStatus not in `rejected`, `validated`.

---

## Steps (agent-owned)

### 1) Run the one-command query

```powershell
python backend/scripts/kb_cli.py open-ideas --pretty
```

### 2) Present results as a compact list

For each idea, show:
- **IdeaID** + **Title** + **StatusCode**
- **Aspects**: list `AspectKey` values (and optionally titles)

If the list is empty, explicitly say: “No open ideas found (per current definition).”


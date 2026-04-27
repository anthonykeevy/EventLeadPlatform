# Story 6.4.4.1 — Preflight

**Story:** 6.4.4.1 — Locale Architecture: Wire the Registry
**Owner:** Dev (fills this template at Step 0 of the dev prompt)
**Date:** _(fill at preflight execution)_
**Worktree (expected):** `C:\wt\elp\story-epic6-6.4.4.1-locale-architecture-wire-registry`
**Branch (expected):** `story/epic6-6.4.4.1-locale-architecture-wire-registry`

---

## Tooling preflight

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.4.1-locale-architecture-wire-registry" `
  -ExpectedBranch "story/epic6-6.4.4.1-locale-architecture-wire-registry" `
  -ReportFile "docs/stories/STORY-6.4.4.1-PREFLIGHT.md"
```

**Output (paste verbatim):**

```text
<paste preflight script output here>
```

---

## Database connection consistency check (Workflow Guide §🗄️)

| Source | Value |
|---|---|
| `os.getenv("DATABASE_URL")` | _(fill)_ |
| Runtime-resolved (via `common.database`) | _(fill)_ |
| Match? | Yes / No (must be Yes — escalate if No) |

---

## Alembic state

| Item | Value |
|---|---|
| `alembic current` (before) | _(fill — should be the head from PR #72 + PR #74 merges)_ |
| Migration files present (063–071) | _(fill list)_ |
| `alembic heads` count | 1 (must be 1; >1 means a branch — fix before proceeding) |

---

## Dependency pre-conditions

| Pre-condition | Status |
|---|---|
| PR #74 (closeout amendment) merged to `master` | Pass / Fail |
| PR #72 (Story 6.4.4) merged to `master` | Pass / Fail |
| 12 live judge JSONs present under `_bmad-output/eval-runs/story-6.4.4-live-baseline-vs-{h1,h2,h4,combined}/` | Pass / Fail |
| `docs/stories/STORY-6.4.4-CLOSEOUT-AMENDMENT.md` exists on master | Pass / Fail |
| `docs/stories/STORY-6.4.3b-RUBRIC-ADR.md` has supersession footer | Pass / Fail |
| Worktree path matches expected | Pass / Fail |
| Branch name matches expected | Pass / Fail |

If any pre-condition fails: **STOP**, do not start implementation, notify Human.

---

## Capability snapshot policy check (Workflow Guide §🧬)

This story does **not** modify component renderer manifests. Therefore:

- **Capability snapshot bump required?** No.
- **`FORM_AI_CAPABILITY_POLICY` version reference in evidence?** Inherit from current; no change.

If the implementation uncovers a renderer-touching scope creep, **STOP** and escalate before proceeding.

---

## Green CI/CD baseline (pre-implementation)

```powershell
python -m pytest backend/tests --tb=short
```

**Pre-implementation summary:** _(paste `=== X passed, Y skipped ===` line here)_

```powershell
cd frontend; npm run lint
```

**Pre-implementation lint:** _(paste output summary)_

```powershell
cd frontend; npm run test:unit -- --watch=false
```

**Pre-implementation frontend tests:** _(paste output summary)_

If any of the three is red **before** implementation begins, **STOP** and notify Human — fix the regression first.

---

## Sign-off

- [ ] Preflight script run and output captured.
- [ ] DB connection consistency confirmed.
- [ ] Alembic head matches expectation.
- [ ] All dependency pre-conditions Pass.
- [ ] Capability snapshot policy reviewed.
- [ ] Green CI/CD baseline captured.

**Dev signature:** _(name + date)_
**Outcome:** Proceed / Hold (with reason)

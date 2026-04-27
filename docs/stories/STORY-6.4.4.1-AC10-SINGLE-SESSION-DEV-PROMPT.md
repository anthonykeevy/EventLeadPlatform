# Story 6.4.4.1-ac10 Single-Session Dev Prompt

You are implementing **Story 6.4.4.1-ac10 — AC-10 Baseline Re-Judge Execution**.

**Worktree:** `C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge`
**Branch:** `story/epic6-6.4.4.1-ac10-baseline-rejudge`
**PR:** TBD (Draft PR opened by SM via `new-story.ps1`)
**Base:** `master` (must include `6d6bf13` — PR #75 merge)

---

## Mission

Execute AC-10 from Story 6.4.4.1 (deferred to manual). Extend `run.py` with parallel-batch slicing so 6 background agents run one locale each (compresses wall-clock from ~30–45 min sequential to ~6–8 min parallel). Verify judge-package prompts include explicit output file paths so Cursor judges write outputs without ambiguity. Aggregate to a **single judge package** (3 judges × 1 session each, not 18 sessions). Run the gate. Record verdict. Recommend the next story.

This is execution + a small code extension — not architecture.

---

## Read First

1. `docs/stories/story-6.4.4.1-ac10.md` — story spec + AC-1..9.
2. `docs/stories/story-6.4.4.1.md` — parent story; AC-10 origin and ingest schema context.
3. `docs/stories/STORY-6.4.4.1-RUBRIC-V2-ADR.md` — rubric v2 governance + AC-10 escape clause (§7).
4. `docs/stories/STORY-6.4.4.1-PROMPTS-V1.1-SPEC.md` — benchmark layout (15 prompts × 6 locales × 3 reps).
5. `docs/stories/STORY-6.4.4.1-JUDGE-PROMPTS.md` — Claude 4.7 + Grok 4 + GPT-5 mini judge prompt templates.
6. `backend/tests/form_ai_eval/run.py` — current harness entry point.
7. `backend/tests/form_ai_eval/judge_pack.py` — current judge package generator.
8. `backend/tests/form_ai_eval/judge_ingest.py` — ingest with rubric_v2 path.
9. `backend/tests/form_ai_eval/prompts.yaml` — v1.1 benchmark.
10. `docs/FORM-AI-EVAL-HARNESS.md` + `docs/FORM-AI-EVAL-JUDGE-WORKFLOW.md` + `docs/FORM-AI-EVAL-DIFF-STATS.md` — harness public docs.

---

## Step 0 — Preflight

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.4.1-ac10-baseline-rejudge" `
  -ExpectedBranch "story/epic6-6.4.4.1-ac10-baseline-rejudge" `
  -ReportFile "docs/stories/STORY-6.4.4.1-AC10-PREFLIGHT.md"
```

Verify pre-conditions:

- `gh pr view 75 --json state,mergedAt` shows `MERGED` (story 6.4.4.1 merged).
- `git log --oneline master | head -3` includes `6d6bf13` (PR #75 merge).
- 9 migrations 063–071 already applied locally (alembic head includes them).
- `prompts-v1.1` (`backend/tests/form_ai_eval/prompts.yaml`) is the v1.1 spec (270 cells; rows have `audience_locale`).
- `rubric_v2.md` exists at `backend/tests/form_ai_eval/rubric_v2.md`.

If any pre-condition fails: STOP, notify Human.

---

## Step 1 — Add `--locale-filter` to `run.py`

Open `backend/tests/form_ai_eval/run.py`. Add a CLI flag:

```python
parser.add_argument(
    "--locale-filter",
    type=str,
    default=None,
    help="Run only rows whose audience_locale matches the given ISO/locale (e.g. AU). Defaults to all rows.",
)
```

Inside the run loop, filter the loaded prompts:

```python
if args.locale_filter:
    rows = [r for r in rows if (r.get("audience_locale") or "").upper() == args.locale_filter.upper()]
    if not rows:
        raise SystemExit(f"No prompts matched --locale-filter={args.locale_filter}")
```

Run-id should encode the locale slice when filter is active, e.g. default `--variant rubric-v2-baseline` becomes `--variant rubric-v2-baseline-AU` if `--locale-filter AU` (or pass-through whatever user supplies and let them name it).

**Add a unit test** in `backend/tests/test_form_ai_eval_harness.py` (or new file `backend/tests/test_form_ai_eval_locale_filter.py`):

- `--locale-filter AU` slices to exactly 45 rows (15 prompts × 3 reps).
- Each filtered row has `audience_locale == 'AU'`.
- Empty match raises `SystemExit`.

Run focused tests:

```powershell
python -m pytest backend/tests/test_form_ai_eval_harness.py backend/tests/test_form_ai_eval_locale_filter.py --tb=short
```

Must be green.

---

## Step 2 — Verify (and patch if needed) `judge_pack.py` path-clarity

Open `backend/tests/form_ai_eval/judge_pack.py`. Generate a sample package locally (using a small fixture or the existing baseline) and inspect the emitted prompts. Each of the 3 prompts (Claude / Grok / GPT-5 mini) **must include the exact output JSON path** the judge should write to.

Required text inside each emitted judge prompt (or equivalent — exact wording flexible, but the path must be unambiguous):

> "Save your output JSON to: `_bmad-output/eval-runs/<run-id>/judge-package/results/judge-output-<judge>.json`. Do not write anywhere else. Create the file if it does not exist."

If the current generator already does this: confirm via inspection, no change.

If not: patch `judge_pack.py` to include the path in the emitted prompt template. Add a unit test in `backend/tests/test_judge_pack.py` confirming the path appears in the generated prompt.

Run focused tests:

```powershell
python -m pytest backend/tests/test_judge_pack.py --tb=short
```

Must be green.

---

## Step 3 — Generate baseline (6 parallel locale runs via background agents)

Spawn **6 parallel background agents**, one per locale. Each invokes `run.py` with a different `--locale-filter` and a unique output run-id.

Recommended layout:

```
_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-AU/
_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-NZ/
_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-UK/
_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-US/
_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-INTL_ONLINE/
_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-EU/
```

Per-agent command (substitute `<LOC>` per locale):

```powershell
python -m backend.tests.form_ai_eval.run `
  --benchmark prompts-v1.1 `
  --locale-filter <LOC> `
  --variant rubric-v2-baseline-<LOC>
```

Use the Agent tool with `run_in_background: true` and `subagent_type: general-purpose` (or whichever Dev's tool model supports). Kick off all 6 in a single message with parallel tool calls.

While the runs execute (wall-clock ~6–8 min if 6 parallel; ~30–45 min if sequential — kick all 6 simultaneously):

- Monitor each agent for completion.
- On completion, verify each produced `metrics.jsonl`, `summary.csv`, `run-metadata.json`.

Total cells across 6 runs = 270 (15 × 6 × 3). Confirm aggregate.

---

## Step 4 — Aggregate into a single judge package

Choose minimal-change path:

**Option A (recommended):** small `judge_pack.py --inputs <run-id>[,<run-id>...]` flag that consumes multiple run dirs and merges their `metrics.jsonl` / `summary.csv` into a single package.

**Option B (no code change):** pre-merge step — concatenate the 6 sub-runs' artifacts into `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline/` (parent), then run standard `judge_pack.py`.

**Option C:** the 6 parallel runs already write to subdirectories under one parent run-id; `judge_pack.py` reads from sub-dirs natively (requires generator change).

Pick whichever is smallest. Document choice in commit message.

Generated package layout:

```
_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline/judge-package/
├── rubric_v2.md
├── judge-input-batch.md
├── judge-output-template.json
├── judge-package-metadata.json
└── results/             ← Cursor judges write here (paths embedded in prompts)
```

Verify the 3 emitted prompts each carry their explicit output path (Step 2 verification confirmed this is in place).

---

## Step 5 — Hand 3 judge prompts to Tonyk in chat

Post in chat (one message, three labeled blocks):

```
Tonyk — judge package ready. 3 prompts to paste into Cursor (one per chat window):

[CLAUDE 4.7 PROMPT]
<paste full prompt body here, including the explicit output path>

[GROK 4 PROMPT]
<paste full prompt body here>

[GPT-5 MINI PROMPT]
<paste full prompt body here>

Output paths the prompts specify:
- _bmad-output/eval-runs/story-6.4.4.1-ac10-baseline/judge-package/results/judge-output-claude.json
- _bmad-output/eval-runs/story-6.4.4.1-ac10-baseline/judge-package/results/judge-output-grok.json
- _bmad-output/eval-runs/story-6.4.4.1-ac10-baseline/judge-package/results/judge-output-gpt5mini.json

Run all three concurrently if you can — ~30 min per session.

Reply when all three JSONs are saved.
```

While Tonyk runs the Cursor sessions, you can:

- Verify the harness round-trips the v1 historical files (backwards-compat smoke).
- Pre-stage the ingest command.
- Pre-stage stale-field housekeeping fix branch (Step 7 below).
- Update the closeout report skeleton.

---

## Step 6 — Ingest + AC-10 gate verdict

Once Tonyk confirms all 3 JSONs are saved:

```powershell
python -m backend.tests.form_ai_eval.judge_ingest --run-id story-6.4.4.1-ac10-baseline
```

Inspect `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline/judge-package/judge-ingest-summary.json`:

- **Pass:** Grok 4 mean drops below 5.00 AND each judge scores ≥1 cell below 4 across the baseline.
  - Record outcome in `STORY-6.4.4.1-AC10-CLOSEOUT-REPORT.md`.
  - Recommend next story = **6.4.4.2** (re-evaluate H2/H4 under v2).
  - Continue to Step 7.

- **Ceiling-lock (round 1 — all three judges still 5/5 every cell):** invoke Multi-Round UAT Protocol:
  - Open `STORY-6.4.4.1-AC10-UAT-RESULTS.md` and add a round row.
  - Single variable change: sharpen one anchor on item 7 (tone register) or item 8 (mandatory strictness) to a tighter threshold.
  - Regenerate package; post 3 new prompts to Tonyk; re-judge.
  - Re-ingest. If pass → Step 7. If still locked → escape clause.

- **Ceiling-lock (round 2 — escape clause invoked):**
  - Add `JUDGE-ARCHITECTURE-RE-INVESTIGATION` (P0) to `EPIC-6-CARRY-FORWARD-BACKLOG.md`.
  - Record outcome in `STORY-6.4.4.1-AC10-CLOSEOUT-REPORT.md`.
  - Recommend next story = **6.4.5** (skip 6.4.4.2; architecture not blocked).
  - Continue to Step 7.

---

## Step 7 — Stale-field housekeeping commit

Apply 4 doc fixes from story §2.7 (these address the post-merge stale-field audit identified by SM):

| File | Line | Fix |
|---|---|---|
| `docs/stories/STORY-6.4.4.1-CLOSEOUT-REPORT.md` | 7 | "Closeout decision: ready to merge via PR #75." → "Closeout decision: merged via PR #75 on 2026-04-27." |
| `docs/stories/EPIC-6-STATUS.md` | row 81 | "✅ **Complete / ready to merge** (2026-04-27, PR #75)" → "✅ **Complete** (merged 2026-04-27, PR #75)" |
| `docs/stories/EPIC-6-WORKFLOW-GUIDE.md` | line 16 | Same fix; prepend "merged ". |
| `docs/stories/story-6.4.4.1.md` | 6 | "**Status:** Complete / ready to merge (2026-04-27)" → "**Status:** Complete (merged 2026-04-27, PR #75)" |

Verify rg-scan is clean post-fix:

```powershell
rg -n "ready to merge" docs/stories/STORY-6.4.4.1-CLOSEOUT-REPORT.md docs/stories/EPIC-6-STATUS.md docs/stories/EPIC-6-WORKFLOW-GUIDE.md docs/stories/story-6.4.4.1.md
```

Should return **no hits**.

---

## Step 8 — Closeout artefacts

- `docs/stories/STORY-6.4.4.1-AC10-CLOSEOUT-REPORT.md` — mandatory:
  - AC-10 outcome (pass / escape clause).
  - Recommended next story (6.4.4.2 / 6.4.5).
  - Round summary if any calibration round was needed.
  - Files added (judge JSONs, ingest summary, harness flag).
  - Carry-forward additions if escape clause invoked.

- `docs/stories/STORY-6.4.4.1-AC10-GATE-EVIDENCE.md`:
  - Focused-test summary line (Steps 1, 2 unit tests).
  - Backend regression: `python -m pytest backend/tests --tb=short` final summary.
  - Ingest summary excerpt (mean per judge; AC-10 verdict).

- `docs/stories/STORY-6.4.4.1-AC10-UAT-RESULTS.md`:
  - Round table: round 1 outcome; round 2 if needed.
  - Tonyk-confirmed Cursor session completion timestamps.
  - RequestID lineage if calibration round invoked.

Update `EPIC-6-STATUS.md` (add 6.4.4.1-ac10 row, status = Complete with PR# + merge date placeholder).
Update `EPIC-6-WORKFLOW-GUIDE.md` Current Focus = 6.4.4.2 or 6.4.5 per AC-10 outcome.

---

## Step 9 — Green CI/CD gate

```powershell
.\scripts\workflow\run-green-gate.ps1 `
  -StoryId "6.4.4.1-ac10" `
  -FocusedTestCommand "python -m pytest backend/tests/test_form_ai_eval_locale_filter.py backend/tests/test_judge_pack.py --tb=short" `
  -BackendGateCommand "python -m pytest backend/tests --tb=short" `
  -EvidenceFile "docs/stories/STORY-6.4.4.1-AC10-GATE-EVIDENCE.md"
```

Anti-Hallucination Protocol: read full `=== X passed, Y failed ===` summary line. Don't end the turn until you can read it in full.

Frontend: not touched in this story; `npm run lint` not required unless any frontend file changed (it shouldn't).

---

## Step 10 — Stale-field audit + push + un-Draft

```powershell
gh pr view <PR#> --json state,isDraft,mergedAt,headRefName,baseRefName,url
rg -n "Draft|Ready for UAT|Keep PR .* open|Current Focus" `
  docs/stories/story-6.4.4.1-ac10.md `
  docs/stories/STORY-6.4.4.1-AC10-CLOSEOUT-REPORT.md `
  docs/stories/EPIC-6-STATUS.md `
  docs/stories/EPIC-6-WORKFLOW-GUIDE.md
```

Fix any drift in a final SM housekeeping commit. Push. Mark PR Ready for review (un-Draft).

---

## Constraints (do NOT break)

- **No new Gemini judge.** Panel is Claude 4.7 + Grok 4 + GPT-5 mini, unchanged.
- **No rubric_v3.** Anchor sharpening on items 7/8 is allowed in a calibration round; structural rubric changes are not.
- **No cross-comparison of v1 and v2 results.** Inviolable per the v1 ADR baseline-re-snapshot policy.
- **No mocking the LLM in tests.** Harness uses live calls in Step 3; tests in Steps 1, 2 use fixtures and never call live.
- **No skipping the ingest backwards-compat smoke.** Re-ingest one v1 historical file (Story 6.4.4) post-Step 1 to confirm the v1 path still works.
- **No indefinite block on AC-10.** Escape clause is a real path; document carry-forward and close.
- **No stale "ready to merge" text** anywhere in the 4 housekeeping docs after Step 7.

---

## Done when

- All 9 ACs from `story-6.4.4.1-ac10.md` green.
- AC-10 outcome (pass / escape clause) documented in closeout report with recommended next story.
- 3 judge JSONs + ingest summary + judge-package committed under `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline/`.
- Harness extension (`--locale-filter`) tested and committed.
- Judge prompt path-clarity verified or patched.
- Stale-field housekeeping clean.
- Backend regression green.
- SM stale-field audit clean.
- PR un-Drafted.

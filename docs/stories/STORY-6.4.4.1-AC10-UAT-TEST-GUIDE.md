# Story 6.4.4.1-ac10 — UAT Test Guide

**Story:** 6.4.4.1-ac10 — AC-10 Baseline Re-Judge Execution.
**UAT owner:** Human (Tonyk) + SM.
**Mode:** Multi-Round UAT Protocol — single variable per round; full RequestID lineage in `STORY-6.4.4.1-AC10-UAT-RESULTS.md`.

This guide is short and execution-focused. The architecture work was UAT'd in Story 6.4.4.1; this story tests the **execution mechanics** + **AC-10 gate outcome**.

---

## §1 Code change verification — `--locale-filter` works (AC-1)

```powershell
python -m backend.tests.form_ai_eval.run --benchmark prompts-v1.1 --locale-filter AU --variant smoke-au-only
```

**Pass criteria:**

- Run completes (or fails on first generation if API quota exhausted — that's fine, we're not testing generation here).
- Console output indicates 45 rows queued (15 prompts × 3 reps).
- If you Ctrl-C immediately after the first row queues, that's enough for this UAT step.

Also verify:

```powershell
python -m pytest backend/tests/test_form_ai_eval_locale_filter.py --tb=short
```

**Pass criteria:** unit test for `--locale-filter` is green.

**Section §1 Final:** Pass / Fail

---

## §2 Judge prompt path-clarity (AC-2) [Tonyk-eyeball]

Once Dev has generated the judge package (Step 4 of dev prompt), Dev posts the 3 prompts in chat. Open each judge prompt and confirm:

- The exact output JSON file path is stated explicitly in the prompt body.
- The path is one of:
  - `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline/judge-package/results/judge-output-claude.json`
  - `…/judge-output-grok.json`
  - `…/judge-output-gpt5mini.json`
- Each prompt names the correct rubric (`rubric_v2.md`) and includes the "name at least one weakness per row before scoring" calibration nudge.
- Each prompt includes the required JSON shape (rubric_version, judge_model, judge_model_version, scores per cell, rationale).

**Pass criteria:** all 3 prompts pass these checks. If any path is missing or wrong, send back to Dev to patch `judge_pack.py`.

**Section §2 Final:** Pass / Fail

---

## §3 6 parallel locale runs aggregated to single judge package (AC-3)

After Dev orchestrates Step 3 of the dev prompt (6 parallel background agents):

```powershell
ls _bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-*
```

**Pass criteria:**

- 6 sub-run directories exist (AU / NZ / UK / US / INTL_ONLINE / EU).
- Each contains `metrics.jsonl` (45 rows), `summary.csv`, `run-metadata.json`.

After Dev's aggregation step:

```powershell
ls _bmad-output/eval-runs/story-6.4.4.1-ac10-baseline/judge-package/
```

**Pass criteria:** judge-package contains `rubric_v2.md`, `judge-input-batch.md`, `judge-output-template.json`, `judge-package-metadata.json`, plus an empty `results/` for judge outputs. The aggregated batch covers all 270 cells (verify count in `judge-input-batch.md` or metadata).

**Section §3 Final:** Pass / Fail

---

## §4 Cursor judge sessions completed (AC-4) [Tonyk-time]

Per Dev's chat post (Step 5 of dev prompt):

1. Open three Cursor chat windows (one per judge: Claude 4.7, Grok 4, GPT-5 mini).
2. Paste the corresponding prompt into each.
3. Each judge runs through the rubric_v2 scoring on all 270 cells and writes its output JSON to the path embedded in the prompt.
4. When all three are complete, run:

```powershell
ls _bmad-output/eval-runs/story-6.4.4.1-ac10-baseline/judge-package/results/
```

**Pass criteria:** 3 JSON files present:

- `judge-output-claude.json`
- `judge-output-grok.json`
- `judge-output-gpt5mini.json`

Each is well-formed JSON with `rubric_version: "rubric_v2"`, `judge_model_version` populated, all 9 metric keys present per row, scores in `0..2`.

**Section §4 Final:** Pass / Fail

---

## §5 Ingest summary + AC-10 gate verdict (AC-5, AC-6) [GATE]

Dev runs:

```powershell
python -m backend.tests.form_ai_eval.judge_ingest --run-id story-6.4.4.1-ac10-baseline
```

Inspect `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline/judge-package/judge-ingest-summary.json`.

**AC-10 Pass criteria** (record in `STORY-6.4.4.1-AC10-CLOSEOUT-REPORT.md`):

- **Pass:** Grok 4 mean drops below 5.00 AND each judge scores ≥1 cell below 4 across the baseline.
- **Escape clause invoked:** ceiling-lock confirmed in round 1; one calibration tweak (anchor sharpening on item 7 or 8); re-judge in round 2; if still ceiling-locked, escape clause closes AC-10 with `JUDGE-ARCHITECTURE-RE-INVESTIGATION` registered as P0 carry-forward.

Decision routing (per Rubric v2 ADR §7):

| Outcome | Recommended next story |
|---|---|
| Pass with real variance (Grok+Claude differ ≥1 across cells) | Story 6.4.4.2 (re-evaluate H2/H4 under v2) |
| Pass but H2/H4 evidence still inconclusive | Skip 6.4.4.2 → Story 6.4.5 directly |
| Escape clause invoked | Skip 6.4.4.2 → Story 6.4.5 directly; carry-forward registered |

**Section §5 Final:** Pass / Pass-with-escape / Fail

---

## §6 Stale-field housekeeping (AC-7)

```powershell
rg -n "ready to merge" docs/stories/STORY-6.4.4.1-CLOSEOUT-REPORT.md docs/stories/EPIC-6-STATUS.md docs/stories/EPIC-6-WORKFLOW-GUIDE.md docs/stories/story-6.4.4.1.md
```

**Pass criteria:** no hits.

```powershell
rg -n "Complete \(merged 2026-04-27, PR #75\)" docs/stories/EPIC-6-STATUS.md docs/stories/EPIC-6-WORKFLOW-GUIDE.md
```

**Pass criteria:** at least 2 hits (status doc + workflow guide).

**Section §6 Final:** Pass / Fail

---

## §7 Backend regression (AC-8)

```powershell
python -m pytest backend/tests --tb=short
```

**Pass criteria:**

- `=== <N> passed, <M> skipped ===` line read in full (Anti-Hallucination Protocol).
- No new failures vs the post-PR-#75 baseline (`793 passed, 26 skipped`).
- Numbers may differ slightly if the new `--locale-filter` test added rows; expect approximately `795+ passed`.

**Section §7 Final:** Pass / Fail

---

## §8 Status doc + decision artifact (AC-9)

Open `docs/stories/EPIC-6-STATUS.md` and `docs/stories/EPIC-6-WORKFLOW-GUIDE.md`. Verify:

- `EPIC-6-STATUS.md` has a row for Story 6.4.4.1-ac10 with status `✅ Complete (merged <date>, PR #<N>)` once the PR merges (or "Ready for review" pre-merge).
- `EPIC-6-WORKFLOW-GUIDE.md` Current Focus advances to whichever story §5's verdict recommends (6.4.4.2 or 6.4.5).
- `STORY-6.4.4.1-AC10-CLOSEOUT-REPORT.md` clearly states the recommended next story and the reasoning.

**Section §8 Final:** Pass / Fail

---

## Round-by-Round Summary (chronological — populate during UAT)

| Round | Date | Focus | Single variable changed | RequestID(s) | Outcome | Follow-up |
|---|---|---|---|---|---|---|
| 1 | TBD | AC-10 first re-judge | n/a (initial run) | TBD | TBD | TBD |
| 2 | TBD (conditional) | AC-10 calibration tweak | rubric anchor `item-7-tone` or `item-8-mandatory` | TBD | TBD | TBD |

---

## §9 Final result (overall — populate during UAT)

| Section | Outcome |
|---|---|
| §1 `--locale-filter` works | TBD |
| §2 Judge prompt path-clarity | TBD |
| §3 Parallel batches aggregated | TBD |
| §4 Cursor judge sessions completed | TBD |
| §5 Ingest summary + AC-10 verdict | TBD |
| §6 Stale-field housekeeping | TBD |
| §7 Backend regression | TBD |
| §8 Status doc + decision artifact | TBD |

**Overall outcome:** TBD (Pass / Pass-with-escape / Fail / Partial).
**Recommended next story:** TBD (6.4.4.2 / 6.4.5).

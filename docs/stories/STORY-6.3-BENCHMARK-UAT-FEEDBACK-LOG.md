# Story 6.3 — Benchmark UAT feedback & change log

**Purpose:** Single ledger for **human review → code/context changes → re-test**. Use it to decide **lock**, **iterate**, or **rollback**.

**How to use**

1. Add a row under **Feedback received** when you review a form (BM01–BM10).
2. For each issue, add or update a row under **Changes applied** with status: `proposed` → `in_branch` → `locked` or `rolled_back`.
3. Re-run the benchmark in Builder (or pytest for harness); note **Form IDs** and **before/after** screenshots if useful.
4. Suggested evaluation rubric per change: **Intent** (does it match feedback?), **Regression** (other benchmarks still pass?), **Rollback** (revert commit / restore doc snippet — cite file paths).

---

## Feedback received

| ID | Date | Benchmark | Form ID | Source | Finding |
|----|------|-----------|---------|--------|---------|
| F-001 | 2026-03-31 | BM01 Party RSVP | 402 | Anthony / UAT screenshot | Inter-field vertical spacing is even and good; **top margin** before first field vs **bottom margin** after last control is **asymmetric** (narrow top, large bottom). |
| F-002 | 2026-03-31 | BM01 Party RSVP | 402 | Anthony | Prefer **~half canvas** for fields and **~half** for **event information** (RSVP context: date, venue, copy) instead of full-bleed single column. |
| F-003 | 2026-03-31 | BM01 Party RSVP | 402 | Anthony | Number field label **ambiguous** (“How many people are you bringing?”); prefer explicit **excluding yourself** / additional guests wording. |
| — | — | BM02–BM10 | — | — | *Pending your per-form feedback* |

---

## Changes applied

| Change ID | Tied to | Status | Summary | Files / notes |
|-----------|---------|--------|---------|----------------|
| C-001 | F-001 | `in_branch` | Single-column vertical rebalance now uses a **floating** gap `available_space / (n+1)` so **top and bottom margins match** (integer `//` previously left spare pixels at the bottom only). Backend post-process + Builder **measured relayout** aligned. | `backend/modules/form_ai/service.py` (`_rebalance_single_column_vertical_spacing`); `frontend/.../AIAgentPanel.tsx` (`relayoutFromRenderedHeights`); `backend/tests/test_story_6_2_ai_generation_loop.py` expected `y` values updated. |
| C-002 | F-003 | `in_branch` (revised) | **Context pack only** for clearer labels when user/benchmark wording is vague (e.g. guest counts). **Reverted** edits to `STORY-6.2-BENCHMARK-FORMS.md` BM01 prompt/table and harness `_bm01` label so the **benchmark baseline stays stable**. | `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md` (§ Copy and question clarity). |
| C-003 | F-002 | `in_branch` (revised) | **Context pack**: canvas-aware **width/margins** (variable `canvasSettings`), discourage default ~90% stretch; optional **event-context split** using **relative** bands of **actual** canvas width; **F-001 note:** vertical rebalance only affects **y**, not required full width — compatible with narrower columns. | `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md` (§ Canvas width…, § Compatibility with vertical spacing, § Event-context split). |

**Lock criteria (suggestion):** Re-run BM01 with the **original** benchmark prompt from `STORY-6.2-BENCHMARK-FORMS.md` (unchanged text); confirm margins (C-001), width/margins (C-003), and label clarity (C-002 via context). Then set C-001–C-003 to `locked` and note the commit SHA if required.

**Rollback:** Revert the listed files from the last good commit; restore prior `expected_y` in `test_story_6_2_ai_generation_loop.py` if rolling back C-001 only.

---

## Process suggestions

- **One benchmark per pass:** Finish BM01 (prompt → generate → screenshot → log → we patch → you re-run) before BM02, so each diff is attributable.
- **Stable prompts:** Treat `STORY-6.2-BENCHMARK-FORMS.md` as the **canonical prompt**; copy from there for each re-test.
- **Harness vs live:** `test_story_63_benchmark_harness.py` stays **mocked**; live quality is proven only in Builder (AC-9).
- **Optional column in this table:** “Passes pytest” / “Passes eyeball” checkboxes per change.

---

## References

- `STORY-6.3-BENCHMARK-PROMPTS-AND-OUTCOMES.md` — prompt + outcome cheat sheet  
- `STORY-6.3-UAT-TEST-GUIDE.md` — §5 Builder canvas  
- `STORY-6.3-CLOSEOUT-REPORT.md` — final disposition and redesign direction
- `docs/FORM-AI-POST-PROCESSING-GUIDE.md` — post-processing enable/disable guidance

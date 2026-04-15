---
experiment_id: REG-CONF-BASELINE-2026-04
status: active
last_completed_iteration: 5
current_block: 3
block_1_completed_at_note: "Checkpoint 2026-04-02 — see §3 Block summary"
block_2_completed_at_note: "Checkpoint 2026-04-02 — see §3 Block summary"
user_prompt_unchanged: true
eventlead_backend_root: "../EventLeadPlatform/backend"
baseline_run_at_utc: "2026-04-02 (CLI)"
---

# Form AI first-shot experiment — REG-CONF-BASELINE-2026-04

**Fixed user prompt** (verbatim; do not edit between iterations):

```
Build a registration form for a tech conference. Include first name, last name, email address, phone number, company name, job title, and a country dropdown with these options: Australia, United States, United Kingdom, Canada, New Zealand, Other. Add a submit button labeled 'Register'.
```

**Tools**

- CLI: `python scripts/form_ai_first_shot_tune.py` (from EventLead `backend/`; requires `OPENAI_API_KEY` in `backend/.env`)
- This run: **no** `--addendum-file`; first-shot only (`max_system_correction_attempts=0`)
- Changelog: `docs/experiments/form-ai-first-shot/changelog.jsonl`

---

## 1. Indicator registry (evolving)

| Id | Description | Source / formula | Target direction | Notes |
|----|-------------|------------------|------------------|-------|
| L | Layout score (0–100) | `score_layout(collisions, boundaries, schema)` | Higher | |
| G | Goal score (0–100) | `score_goal_coverage(definition, user_prompt)` | Higher | |
| C | Combined | `combined_score(L, G, 0.5)` | Higher | |
| V | Validator valid (first shot) | `attempts[0].validation.valid` | true | |
| coll | Collisions | `collisionCount` | Lower | |
| bnd | Boundaries | `boundaryViolationCount` | Lower | |
| sch | Schema errors | `schemaErrorCount` | Lower | |

| Id | Parent | Description | How measured |
|----|--------|-------------|--------------|
| G_shell | G | (optional split) Field *types* and labels vs prompt vs *rendered* overspill | Manual / future DOM metric; not in CLI today |
| coll_s | coll | (Block 2+) Enumerate **which** component pairs overlap via `debug_form_ai_collisions.py` on saved DefinitionJSON | Script output; explains why `coll` stays flat |

---

## 2. Per-iteration log

| Iter | Block | Addendum fingerprint / path | Planned change (ONE) | Hypothesis | Expected (indicators) | Actual L/G/C coll/bnd sch valid | Δ vs prev | Outcome vs expected | Reviewer notes |
|------|-------|-----------------------------|----------------------|------------|----------------------|----------------------------------|-----------|---------------------|----------------|
| 0 | 1 | baseline / none | — | Baseline | — | L=41.0 G=100 C=70.5 coll=7 bnd=3 sch=0 V=F first-shot-invalid ~46s CLI | — | — | G maxed; layout failed — see interpretation below |
| 1 | 1 | `docs/experiments/form-ai-first-shot/REG-CONF-BASELINE-2026-04-addendum-iter1.md` | Add explicit no-overlap layout contract with minimum spacing between vertically stacked fields. | The model will stop placing fields into intersecting y-bands when spacing is made explicit as a hard rule. | `coll ↓`, `bnd ↓`, `L ↑`; `G` unchanged. | L=26.0 G=100 C=63.0 coll=7 bnd=3 sch=1 V=F | vs Iter 0: L -15.0, G +0, C -7.5, coll +0, bnd +0, sch +1, V no-change | Surprise | Schema error introduced; layout did not improve. |
| 2 | 1 | `docs/experiments/form-ai-first-shot/REG-CONF-BASELINE-2026-04-addendum-iter2.md` | Add strict schema-validity instruction (valid JSON shape first, then layout constraints). | Making response-shape correctness explicit should remove schema errors that are depressing layout score. | `sch ↓ to 0`, `L ↑`, `C ↑`; `G` unchanged. | L=41.0 G=100 C=70.5 coll=7 bnd=3 sch=0 V=F | vs Iter 0: L +0.0, G +0, C +0.0, coll +0, bnd +0, sch +0, V no-change | Partial | Schema recovered, but no layout gain yet. |
| 3 | 1 | `docs/experiments/form-ai-first-shot/REG-CONF-BASELINE-2026-04-addendum-iter3.md` | Add explicit two-column row template to prevent horizontal overlap and drifting outside canvas. | Hard row/column guidance should reduce both collisions and boundary violations versus free-form placement. | `coll ↓`, `bnd ↓`, `L ↑`, `C ↑`; `G` unchanged. | L=41.0 G=100 C=70.5 coll=7 bnd=3 sch=0 V=F | vs Iter 0: L +0.0, G +0, C +0.0, coll +0, bnd +0, sch +0, V no-change | Surprise | Two-column template had no measurable effect. |
| 4 | 1 | `docs/experiments/form-ai-first-shot/REG-CONF-BASELINE-2026-04-addendum-iter4.md` | Switch to strict single-column stacked layout to remove any cross-column interference. | A single-column layout should reduce overlap complexity and improve first-shot layout validity. | `coll ↓`, `bnd ↓`, `L ↑`, `C ↑`; `G` unchanged. | L=65.0 G=100 C=82.5 coll=7 bnd=0 sch=0 V=F | vs Iter 0: L +24.0, G +0, C +12.0, coll +0, bnd -3, sch +0, V no-change | Partial | Boundary violations cleared and score improved; collisions still unchanged. |
| 5 | 1 | `docs/experiments/form-ai-first-shot/REG-CONF-BASELINE-2026-04-addendum-iter5.md` | Increase mandatory vertical spacing buffer to aggressively separate stacked controls. | Larger fixed spacing should reduce remaining collisions while preserving boundary compliance. | `coll ↓`, `L ↑`, `C ↑`; `bnd` stays low; `G` unchanged. | L=65.0 G=100 C=82.5 coll=7 bnd=0 sch=0 V=F | vs Iter 0: L +24.0, G +0, C +12.0, coll +0, bnd -3, sch +0, V no-change | Partial | Spacing increase held gains from Iter 4 but did not cut collisions further. |
| 1 | 2 | `docs/experiments/form-ai-first-shot/REG-CONF-BASELINE-2026-04-addendum-b2-i1.md` | Add per-field minimum height contract (text/email/tel/select/button) to avoid underestimated bounding boxes causing overlap. | If height assumptions match backend footprint expectations better, pairwise collisions should drop without reintroducing boundary violations. | `coll ↓`, `L ↑`, `C ↑`; keep `bnd=0`, `G=100`, `sch=0`. | L=50.0 G=100 C=75.0 coll=7 bnd=0 sch=1 V=F | vs prev (B1I5): L -15.0, G +0, C -7.5, coll +0, bnd +0, sch +1, V no-change | Surprise | Schema regressed and collisions unchanged; artifact pushed to Form 403 draft version 1. |
| 2 | 2 | `docs/experiments/form-ai-first-shot/REG-CONF-BASELINE-2026-04-addendum-b2-i2.md` | Replace basic component parameter assumptions with company-default theme/globalStyles parameters for render clarity. | Aligning generated definition with company defaults should improve visible component separation and reduce overlap perception while preserving geometry constraints. | `coll ↓`, `L ↑`, `C ↑`; keep `bnd=0`, `G=100`, `sch=0`. | L=49.0 G=100 C=74.5 coll=7 bnd=2 sch=0 V=F | vs prev (B2I1): L -1.0, G +0, C -0.5, coll +0, bnd +2, sch -1, V no-change | Surprise | Visual/theme defaults applied but geometry regressed on boundaries; collisions still invariant. |
| 3 | 2 | `docs/experiments/form-ai-first-shot/REG-CONF-BASELINE-2026-04-addendum-b2-i3.md` | Enforce footprint-locked dimensions and deterministic vertical stepping (`next.y = prev.y + prev.height + gap`). | Hard-coding footprint math per component should remove ambiguous geometry decisions and reduce overlap pairs. | `coll ↓`, `L ↑`, `C ↑`; keep `bnd low`, `G=100`, `sch=0`. | L=0.0 G=100 C=50.0 coll=7 bnd=3 sch=9 V=F | vs prev (B2I2): L -49.0, G +0, C -24.5, coll +0, bnd +1, sch +9, V no-change | Surprise | Over-constrained wording triggered severe schema/geometry regression; artifact saved for inspection. |
| 4 | 2 | `docs/experiments/form-ai-first-shot/REG-CONF-BASELINE-2026-04-addendum-b2-i4.md` | Use measured toolbox runtime footprint sizes as authoritative (including submit-button=72) via `--runtime-json`, with no size inflation. | Removing inflated footprint guesses should align geometry assumptions and reduce avoidable overlap/boundary misses. | `L ↑`, `C ↑`, `sch ↓`; target `coll ↓` while holding `G=100`. | L=85.0 G=100 C=92.5 coll=0 bnd=0 sch=1 V=F | vs prev (B2I3): L +85.0, G +0, C +42.5, coll -7, bnd -3, sch -8, V no-change | Partial | Major geometry win (zero coll/bnd); one remaining schema error keeps run invalid. |
| 5 | 2 | `docs/experiments/form-ai-first-shot/REG-CONF-BASELINE-2026-04-addendum-b2-i5.md` | Increase inter-component clearance using rendered-block spacing safety margins (vertical + horizontal + extra after submit). | Reserving explicit shell-aware spacing should reduce slight visual overlap while preserving zero collisions/boundaries. | Keep `coll=0`, `bnd=0`; `L/C` hold or improve; `sch ↓`; `G=100`. | L=95.0 G=100 C=97.5 coll=1 bnd=0 sch=0 V=F | vs prev (B2I4): L +10.0, G +0, C +5.0, coll +1, bnd +0, sch -1, V no-change | Partial | Best combined/layout score so far; tiny collision reintroduced while schema cleared. |
| 1 | 3 | `docs/experiments/form-ai-first-shot/REG-CONF-BASELINE-2026-04-addendum-b3-i1.md` | Add explicit dropdown auto-width rule so dropdown component width tracks widest option text, not full-row span. | Preventing oversized dropdown container width should remove dropdown-related visual/validator collision risk while preserving spacing gains. | `coll ↓`, keep `bnd=0`, keep `sch=0`, `L/C` hold high, `G=100`. | L=95.0 G=100 C=97.5 coll=1 bnd=0 sch=0 V=F | vs prev (B2I5): L +0.0, G +0, C +0.0, coll +0, bnd +0, sch +0, V no-change | Partial | Stable high-quality output; residual single visual collision persists. |

---

## 3. Block summaries

### Block 1 — after iteration 5

**Aggregate (vs Iter 0 baseline)**

| Metric | Baseline (0) | Best in block | Δ (best vs 0) |
|--------|----------------|---------------|----------------|
| C | 70.5 | **82.5** (iter 4, 5) | **+12.0** |
| L | 41.0 | **65.0** (iter 4, 5) | **+24.0** |
| coll | 7 | 7 | 0 |
| bnd | 3 | **0** (iter 4, 5) | **−3** |
| sch | 0 | 0 (except iter 1 = 1) | 0 |
| G | 100 | 100 | 0 |

- **Mean C** (iters 1–5): 73.8 · **Median C**: 70.5  
- **Worst:** Iter 1 (C=63, L=26, sch=1) — layout+schema regression  
- **Best:** Iter 4 = Iter 5 (plateau)

**Interpretation**

1. **Boundaries were the lever that moved.** Clearing **bnd** (iter 4 single-column addendum) delivered all measurable **L/C** improvement. That matches server-side checks: staying inside `canvasSettings` with footprint-aware widths.
2. **Collisions are stuck at 7 across all six runs** (0–5). Instructions on spacing, two-column, and “larger vertical buffer” did not change **pairwise collision count**. Outcome vs expectation: **Surprise** for iters 1, 3, 5 on `coll`; **Partial** on iters 4–5 (bnd only).
3. **Iter 1** shows **adding only** overlap prose can **worsen** output (sch=1, L down) without helping coll — order of constraints and JSON-shape discipline matters.
4. **Framework lens (`COMPONENT-FRAMEWORK-REFERENCE.md`):** Validator uses DefinitionJSON boxes, not UniversalFieldShell chrome. **G=100** with **coll=7** means field shopping list is satisfied while **geometry** still has seven overlapping pairs — likely **underestimated `style.height` vs effective stacking** and/or **rows** that remain overlapping under `_flatten_collision_visual_components` math.
5. **Iter 5 = Iter 4** on all scored fields — marginal spacing text hit a **plateau**; next block needs a **different collision strategy**, not “more of the same spacing words.”

**Decisions before Block 2**

- [x] Keep indicator set + **add** `coll_s` (enumerate collision pairs from saved JSON)
- [ ] Split indicator: **bnd** already validated as responsive; focus splits on **coll** drivers
- [ ] Add indicator: optional **pair_list_hash** once JSON captured
- [x] Deprioritize: repeating-only “vertical spacing buffer” without pair-level diagnosis

**Next block hypotheses (for Chat A/B)**

1. Export **first-shot `definitionJSON`** for iter 4/5 best runs → run `backend/scripts/debug_form_ai_collisions.py` → addendum names **exact ids** and “move `y` ≥ …” using same math as collision hints in service.
2. Addendum: require **minimum `style.height`** per component type aligned with backend `_minimum_render_height` / footprint intent so stacked **y** cannot lie inside inflated boxes.
3. Optional: **`--include-definition`** on one CLI run + store under `docs/experiments/form-ai-first-shot/artifacts/` for diffing across iterations.

---

## 4. Checkpoint log

| Date | Participants | Themes | Commitments for next block |
|------|--------------|--------|----------------------------|
| 2026-04-02 | Tonyk + Chat A (Form Builder Master) | Block 1 review; **coll** invariant; **bnd** fixed by single-column | Snapshot JSON for best run; enumerate collision pairs; collision-targeted addendum v1 |
| 2026-04-02 | Tonyk + Chat B (execution) | Block 2 run complete; runtime measured footprints + spacing margins gave near-zero collisions | Start Block 3 with dropdown auto-width semantics in addendum |

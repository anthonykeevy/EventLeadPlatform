---
experiment_id: "{{experiment_id}}"
status: active
current_block: 1
last_completed_iteration: 0
user_prompt_unchanged: true
eventlead_backend_root: "{{eventlead_backend_root}}"
---

# Form AI first-shot experiment — {{experiment_id}}

**Fixed user prompt** (verbatim; do not edit between iterations):

> (paste full prompt below)

```

```

**Tools**

- CLI: `python scripts/form_ai_first_shot_tune.py` (run from `eventlead_backend_root`; requires `backend/.env` with `OPENAI_API_KEY`)
- Server path: `max_system_correction_attempts=0`, optional `systemPromptAddendum` = addendum file content
- Code references: `modules/form_ai/first_shot_scoring.py` (layout vs goal), `modules/form_ai/service.py` (system addendum append target)

---

## 1. Indicator registry (evolving)

_Agents may **add** rows or **split** an indicator into finer metrics when interpretation becomes noisy. Each row must stay **measurable** (CLI number, validator count, or pass/fail check)._

| Id | Description | Source / formula | Target direction | Notes |
|----|-------------|------------------|------------------|-------|
| L | Layout score (0–100) | `first_shot_scoring.score_layout(collisions, boundaries, schema)` | Higher | Penalizes collisions most per unit in default formula |
| G | Goal score (0–100) | `score_goal_coverage(definition, user_prompt)` keyword-gated checks | Higher | Extend in code when you add stable checks; document here |
| C | Combined | `combined_score(L, G, layout_weight)` | Higher | Default weight 0.5/0.5 unless experiment says otherwise |
| V | Validator valid (first shot) | `trace.attempts[0].validation.valid` | true | Binary |
| coll | Collisions | first-attempt `collisionCount` | Lower | |
| bnd | Boundaries | first-attempt `boundaryViolationCount` | Lower | |

_Add splits or derived indicators below as needed (example):_

| Id | Parent | Description | How measured |
|----|--------|-------------|--------------|
| | | | |

---

## 2. Per-iteration log (one row per run)

_Fill **before** each CLI run: Planned change (single), Hypothesis, Expected shift (which indicators, direction). Fill **after**: Actual metrics, Delta vs previous baseline, Outcome vs expectation._

| Iter | Block | Addendum fingerprint / path | Planned change (ONE) | Hypothesis | Expected (indicators) | Actual L/G/C coll/bnd valid | Δ vs prev | Outcome vs expected | Reviewer notes |
|------|-------|-----------------------------|----------------------|------------|----------------------|-----------------------------|-----------|---------------------|----------------|
| 0 | 1 | baseline / none | — | Baseline | — | | | | |
| 1 | 1 | | | | | | | | |

---

## 3. Block summaries (every {{runs_per_block}} iterations)

### Block 1 — after iteration {{runs_per_block}}

**Aggregate**

- Mean/median combined (this block):
- Best / worst iteration:
- Indicators that moved vs stalled:

**Interpretation**

- Did small tweaks behave as predicted? If not, variance vs wrong model?

**Decisions before next block**

- [ ] Keep indicator set
- [ ] Split indicator: ___ → ___
- [ ] Add indicator: ___
- [ ] Deprioritize: ___

**Next block hypotheses** (bullet list; still one change per iteration in the block)

---

## 4. Checkpoint log (human–agent ideation)

_Record dated notes when pausing between blocks._

| Date | Participants | Themes | Commitments for next block |
|------|--------------|--------|----------------------------|
| | | | |

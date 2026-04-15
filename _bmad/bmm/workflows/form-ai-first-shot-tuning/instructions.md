# Form AI first-shot tuning workflow

**Workflow:** `form-ai-first-shot-tuning`  
**Purpose:** Improve **first model reply** quality with a **fixed user prompt**, **system addendum only**, **measurable scores**, and **blocks of five** runs with a **mandatory review/ideation checkpoint** between blocks.

---

## Why BMAD workflow + master persona

- **Workflow**: Repeating steps (hypothesis → one change → measure → record) stay consistent across agent sessions.
- **Form Builder Master persona**: Concentrates canvas rules, component set, and validator behavior so reviewers do not re-derive domain facts each time.
- Together they support **comparing actual deltas to expected deltas** and **evolving indicators** without losing history.

---

## Architecture

- **Step-file lite**: Follow sections 1–5 in order. Stop at **checkpoints** where marked.
- **Project root**: Story worktree containing `_bmad` (e.g. `story-epic6-6.3-ai-context-benchmark-baseline`).
- **Backend**: Resolve `eventlead_backend_root` (workflow variable or env `EVENTLEAD_BACKEND`). Scripts live under that path.

### Frontend execution mode (sectioned prompt architecture)

When the experiment is running from the Builder AI Agent panel (instead of direct CLI injection):

1. Build the system addendum from ordered prompt sections (layout, data collection, validation, appearance, logic, delivery summary).
2. Concatenate sections into one `systemPromptAddendum` and submit one generate request.
3. Set panel **System correction attempts** to the experiment value (default **1** for control evaluation).
4. Log section metadata per run with frontend events:
   - `ai.sections.run.start`
   - `ai.sections.run.result`
   - `ai.sections.run.error`
5. Ensure frontend-to-backend logging is enabled (`VITE_LOG_SEND_TO_BACKEND=true`) so rows land in `log.FrontendEvent`.

Reference implementation:

- `scripts/form_ai_first_shot_tune.py` — first shot only (`max_system_correction_attempts=0`), scoring, `--repeat`, `--changelog-jsonl`
- `modules/form_ai/first_shot_scoring.py` — layout / goal / combined
- Context pack (system baseline): `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md` in EventLead repo

---

## INITIALIZATION (Step 1)

1. Read `workflow.yaml` and resolve `config_source`, `output_folder`, `default_output_file`, `variables`.
2. Set `experiment_id` (unique string, e.g. `REG-CONF-2026-04`).
3. Ensure directory exists: `{project-root}/docs/experiments/form-ai-first-shot/`
4. If review file does not exist, copy `experiment-review-template.md` → `default_output_file` (resolve `{{experiment_id}}`, `{{runs_per_block}}`, `{{eventlead_backend_root}}`).
5. Paste the **full fixed user prompt** into the review doc (verbatim).

---

## INDICATOR REGISTRY (Step 2)

1. Confirm default rows (L, G, C, V, coll, bnd) match `first_shot_scoring.py`.
2. **Agents may add or split indicators** when:
   - A single score hides tradeoffs (e.g. split **G** into `G_fields` vs `G_options` after extending checks in code), or
   - A new measurable signal is needed (e.g. “submit label exact match”).
3. Any **code change** to scoring must be **one commit / one experiment row** and reflected in the registry table.

---

## BLOCK EXECUTION (Step 3) — repeat for each block

**Constants**

- `runs_per_block` = **5** (unless user explicitly changes workflow variable and documents why).

For **each iteration** `i` in `1..runs_per_block`:

### 3a — Plan (before any API call)

1. In the review doc **Per-iteration log**, add row for iteration `i`.
2. Record **Planned change (ONE)** — e.g. “Addendum §2: require vertical spacing ≥ N between stacked fields.”
3. Record **Hypothesis** — causal link to model behavior.
4. Record **Expected** — which indicators move (e.g. “coll ↓, L ↑; G unchanged”).
5. Save addendum file; note path and fingerprint (CLI logs `addendumFingerprint` in jsonl).

### 3b — Execute

From resolved `eventlead_backend_root`:

1. Choose a **stable artifact path** for this iteration’s definition (so the next step can push the same bytes the server scored), e.g.  
   `{project-root}/docs/experiments/form-ai-first-shot/artifacts/<experiment_id>-b<current_block>-i<iteration>.json`
2. Run the CLI with **`--save-definition`** pointing at that path:

```text
python scripts/form_ai_first_shot_tune.py --user-prompt "<verbatim>" ^
  --addendum-file <path> ^
  --repeat 1 ^
  --experiment-id <experiment_id> ^
  --changelog-jsonl <path-to-changelog.jsonl> ^
  --layout-weight 0.5 ^
  --save-definition <artifact-path.json>
```

(Use shell-appropriate continuation; WSL/bash uses `\`.)

Optional: `--repeat 3` **only** for variance probes — document that the row aggregates min/mean/max. For variance rows, still **save one** representative definition for push (e.g. run `--repeat 1` after choosing the sample to anchor, or save the JSON you want to inspect).

### 3c — Record (after run)

1. Fill **Actual**: L, G, C, collisions, boundaries, valid.
2. **Δ vs prev**: compared to previous iteration (or block baseline if first in block).
3. **Outcome vs expected**: *Match* | *Partial* | *Surprise* — if Surprise, note whether to **rerun once** before changing strategy.
4. Short **Reviewer notes** (agent + human): tweak same lever, new lever, or split indicator?

### 3d — Push draft to database + human gate (after record)

**Goal:** Match the product behaviour where **Generate from Draft** replaces the whole builder canvas with the model output — but do it **on the server** so opening `/forms/403/builder` loads the same DefinitionJSON without manual paste.

From `eventlead_backend_root` (same venv / `DATABASE_URL` as the API):

```text
python scripts/push_form_draft_definition.py ^
  --form-id 403 ^
  --definition <same artifact-path.json as --save-definition> ^
  --user-id <UserID with EDIT on form 403> ^
  --comment "<experiment_id> block <N> iter <i>"
```

- The script updates the **latest DRAFT** `FormVersion` for FormID **403** (highest `VersionNumber` with `Status = DRAFT`), unless `--version-number` is set.
- On success, note **`FormID` + `VersionNumber`** in the review row (e.g. “pushed → DB draft v7”).

**Agent stop:** Report scores, artifact path, and DB push result. Tell the human to **hard-refresh** or re-open Form **403** in the builder and confirm layout vs intent. **Do not start the next iteration** until the user explicitly says they are satisfied (or documents a defect to fix in the next loop).

---


## BLOCK CHECKPOINT (Step 4) — MANDATORY STOP

**Do not start the next block until the user explicitly approves.**

1. Complete **Block summary** in the review doc (aggregate stats, stalled vs moving indicators).
2. **Visual / DB anchor:** Each iteration should already have been **pushed** to Form **403**’s latest DRAFT in Step **3d**. At block end, optionally keep a **named best** JSON on disk: from the winning first-shot run, `form_ai_first_shot_tune.py --save-definition ...` with the winning addendum (`--repeat 1`) →  
   `docs/experiments/form-ai-first-shot/artifacts/<experiment_id>-block<N>-best.json`, and link it in the review doc. **Do not** replace the narrative content of `FORM-403`; that file is the methodology. **Do** use saved JSON when you want canvas/SmartBorder visuals for the same draft the server scored (see `FORM-403` §9 re server vs canvas).
3. Update **Indicator registry** if splits/additions were decided.
4. Append **Checkpoint log** row: date, topics, commitments for next block.
5. **Ideation** with user: next hypotheses, risks, whether to adjust `layout_weight` or extend `score_goal_coverage` in code.

---

## NEXT BLOCK OR CLOSE (Step 5)

1. Increment `current_block` in review frontmatter.
2. If user requests another block, return to **Step 3**.
3. If closing experiment, run **checklist.md** archival items.

---

## Agent behaviour

- Prefer **one additive change** per iteration; if multiple ideas emerge, queue them for future iterations.
- When scores **contradict** expectation, default to **one rerun** before concluding the lever is wrong.
- Cite **validator truth** (collisions/boundaries) separately from **goal coverage** so boundary-vs-collision confusion is visible in the log.

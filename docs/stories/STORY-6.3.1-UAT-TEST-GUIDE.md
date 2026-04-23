# Story 6.3.1 — UAT Test Guide

**Story:** 6.3.1 — Simplified AI Output + Deterministic Layout Foundation  
**Owner:** Anthony (Human UAT)  
**Prep:** Dev provides `STORY-6.3.1-GATE-EVIDENCE.md` + merged PR link

---

## Environment

- Branch: story branch containing 6.3.1 (or `master` post-merge confirmation pass).
- Backend: usual local API + DB.
- LLM: optional for manual smoke; core gates should be deterministic/mocked where possible.

---

## §1 — Automated gates (witness)

| Step | Command | Expected |
|------|---------|----------|
| 1.1 | From `backend/`: `python -m pytest --tb=short` | Pass |
| 1.2 | From `frontend/`: `npm run lint` | Pass |
| 1.3 | From `frontend/`: `npm run test:unit -- --watch=false` | Pass |
| 1.4 | From repo root: `python -m pytest "backend/tests/test_story_631_deterministic_compiler.py" "backend/tests/test_story_631_governance_persistence.py" "backend/tests/test_story_631_form_ai_governance_api.py" -q` | `21 passed` and no failures (3 new measured-heights compiler tests + 2 new remeasure-service tests added in UAT round 5) |

Record summary lines in UAT notes / gate evidence.

Governance-specific assertion checklist for Step 1.4:
- Runtime resolver returns active governance IDs when baselines are present (`db-active`).
- Persistence writes `GenerationRun` + `GenerationArtifact` rows for each generation attempt.
- API response trace remains stable for `db-empty` and `db-resolution-error` (nullable governance IDs, no schema break).
- Compiler path is explicitly reported as `compilerMode = deterministic-grid`.
- Semantic-only step accepts coordinate-free intent and compiler deterministically resolves final positions/sizes.

---

## §2 — Framework-driven capability ingestion

| Step | Action | Expected |
|------|--------|----------|
| 2.1 | Review capability snapshot artifact referenced by gate evidence | Snapshot version exists and is tied to this build |
| 2.2 | Compare sampled components against `docs/COMPONENT-FRAMEWORK-REFERENCE.md` | Capabilities/validation support align; no obvious manual drift |
| 2.3 | Validate new/rare component coverage sample | Components present in framework metadata appear in capability snapshot without hand-added exceptions |

---

## §3 — Validation contract checks (per component)

| Step | Action | Expected |
|------|--------|----------|
| 3.1 | Inspect one text-like component contract | Allowed rules + parameter schema + compatibility constraints present |
| 3.2 | Inspect one selection component contract | Option-related and selection-specific rules represented correctly |
| 3.3 | Run one negative case (unsupported rule for component type) | Deterministic rejection with clear trace/user-facing reason |

---

## §4 — Canvas-responsive width class behavior

| Step | Action | Expected |
|------|--------|----------|
| 4.1 | Generate a form with mixed width intents (`compact`, `half`, `full`) on default canvas | Deterministic width outcomes with no overlaps |
| 4.2 | Change canvas width and regenerate same semantic intent | Width classes re-resolve according to policy (span/px) |
| 4.3 | Trigger constrained scenario | Fallback/downgrade rules apply deterministically and are traceable |

---

## §5 — Builder canvas visibility (mandatory)

Goal: Confirm Generate still applies compiled output directly to Builder canvas.

| Step | Action | Expected |
|------|--------|----------|
| 5.1 | Open draft in Form Builder and run Generate | Success path applies definition to canvas |
| 5.2 | Verify components are visible/selectable/editable | Canvas is not empty; properties panel binds correctly |
| 5.3 | Repeat with a second benchmark-style prompt | Same expected result |

If this cannot be verified, do not mark story complete.

---

## §6 — Logging and one-change tuning discipline (mandatory)

Follow `docs/AGENT-LOGGING-GUIDE.md`.

| Step | Action | Expected |
|------|--------|----------|
| 6.1 | Capture inbound `RequestID` for at least one key run | RequestID is recorded in evidence |
| 6.2 | Capture correlated outbound chain (`:outbound:` rows) | Chain evidence included |
| 6.3 | Show one-variable-at-a-time sequence (>= 2 runs) | Each run changes one variable only; outcome deltas are attributable |
| 6.4 | Record terminal reason + validation counts per run | Causal tuning ledger is complete |

---

## §7 — Render-then-measure (two-phase compile, mandatory)

Goal: Confirm the new "render-then-measure" second pass eliminates
estimate-vs-rendered height collisions (introduced UAT round 5 to fix
Prompt 6 / Prompt 7 layout failures).

The flow:
1. `POST /api/form-ai/generate` returns a first-pass `DefinitionJSON`
   compiled from per-type **estimated** heights, plus a new
   `generationRunId`.
2. The frontend renders the definition on the live canvas.
3. The frontend measures each component's actual rendered height from
   the DOM and `POST`s them to `POST /api/form-ai/remeasure` with the
   same `generationRunId`.
4. `/remeasure` re-runs the deterministic compiler with the
   ground-truth heights and returns a refined `DefinitionJSON`. The
   frontend swaps to it on success; on failure it keeps the first pass.

| Step | Action | Expected |
|------|--------|----------|
| 7.1 | Generate **Prompt 6** (option-heavy form) on Desktop and Mobile | First-pass + second-pass both render with no overlapping components; no off-canvas items. (Pre-round-5: Prompt 6 collided.) |
| 7.2 | Generate **Prompt 7** (paragraph + form fields) on Desktop and Mobile | Same as 7.1. (Pre-round-5: Prompt 7 collided despite being a simple form.) |
| 7.3 | In the trace JSON for one of the runs, confirm `compileSummary.heightsSource` exists and equals `"estimated"` for the first pass | Field present and equal to `"estimated"` |
| 7.4 | In the same run, locate the persisted `remeasure-output` artifact (or inspect the live `/remeasure` response in DevTools Network) and confirm `compileSummary.heightsSource` equals `"measured"` (or `"mixed"`) | Field present and equal to `"measured"`/`"mixed"` with `measuredComponentCount > 0` |
| 7.5 | Generate any prompt with the network panel open and watch for the `/remeasure` call to fire after `/generate` returns | Exactly one `/remeasure` call per `/generate` (no duplicates, no infinite loop); call carries `generationRunId` and a `measurements` array |
| 7.6 | Force a remeasure failure (e.g. throttle the `/remeasure` call so it errors) | Frontend gracefully keeps the first-pass definition; canvas is not blanked; no uncaught error in console |

If §7.1 or §7.2 still collide, do not mark story complete — the
render-then-measure path is the contracted fix for those failure cases.

---

## §8 — Consent / legal-acknowledgement nudge (LLM)

Goal: Confirm the system prompt nudges the LLM to use the `terms`
component (with linkable document) instead of a plain `checkbox` for
legal/consent intent.

| Step | Action | Expected |
|------|--------|----------|
| 8.1 | Generate a form whose prompt mentions "marketing consent" or "I agree to receive emails" | Output contains a `terms` component (not a `checkbox`) for the consent line |
| 8.2 | Generate a form whose prompt mentions "I have read the privacy policy" or "GDPR opt-in" | Output contains a `terms` component |
| 8.3 | Generate a form whose prompt mentions "interests: sport, music, food" (non-legal multi-select) | Output uses a `checkbox` (consent nudge does **not** over-fire on preference checkboxes) |
| 8.4 | If company-managed terms are uploaded, confirm the `terms` component links to the company doc (existing `termsDefaults` runtime block) | Link text matches company config; `props.termsContent` not duplicated |

---

## §10 — Country / locale awareness (LLM prompt addendum)

Goal: Confirm the LLM prompt addendum instructs the model to honour the
caller's country/locale (Australia/New Zealand by default) for spelling,
field naming and validation. Added in UAT round 7 after the Australian
"Post Code" vs American "Zip Code" feedback.

| Step | Action | Expected |
|------|--------|----------|
| 10.1 | Generate a form with an address component on a default (AU) account | Component label uses `Post Code` / `State`, not `Zip` / `State (US)` |
| 10.2 | Generate a form with a phone component on a default (AU) account | Phone validation pattern accepts AU format (e.g. `04xx xxx xxx`) |
| 10.3 | Generate a contact form with prompt mentioning "favourite color" | Output uses `colour` (UK/AU spelling) in labels/help text where possible |
| 10.4 | Confirm the runtime context passed to `/generate` includes the locale code (`AU` / `NZ`) | Locale present in trace `governanceVersions` or runtime block; addendum text mentions the locale |

---

## §11 — Layout-mode selection (horizontal-stacked vs vertical-packed)

Goal: Confirm the compiler picks the right layout mode per canvas width
(threshold = 600 px) and that the LLM prompt nudge for horizontal-stacked
fires only when the canvas allows it. Added in UAT round 6.

| Step | Action | Expected |
|------|--------|----------|
| 11.1 | Generate any benchmark prompt with the canvas set to **Mobile** (≤ 600 px wide) | Components render in vertical-packed mode: label above input, full-width inputs, no horizontal collisions |
| 11.2 | Generate the same prompt with the canvas set to **Desktop** (≥ 1200 px wide) | Components render in horizontal-stacked mode: label / input / validation in a single row, label band aligned across components |
| 11.3 | Generate the same prompt with the canvas set to **Tablet** (768 × 1024) | Layout mode = horizontal-stacked (tablet portrait still ≥ 600 px); no overlapping components |
| 11.4 | In the trace JSON, confirm `compileSummary.layoutMode` reports `"horizontal-stacked"` for desktop/tablet and `"vertical-packed"` for mobile | Matches the visual layout |
| 11.5 | Inspect the LLM system prompt (one trace from each canvas) and confirm the horizontal-stacked nudge block is present for desktop/tablet only | Block present on desktop/tablet, absent on mobile |

---

## §12 — Horizontal-stacked validator parity (collision / boundary checks)

Goal: Confirm the validator does **not** raise phantom collision or
boundary warnings on horizontal-stacked rows. Added in UAT round 11
after desktop/tablet generations were consistently failing the
collision check despite visually clean layouts.

| Step | Action | Expected |
|------|--------|----------|
| 12.1 | Generate Prompt 5 (sales lead form) on Desktop several times | Result status is `completed` every time; no phantom collision warnings in the trace; canvas is visually clean |
| 12.2 | Repeat 12.1 on Tablet | Same as 12.1 |
| 12.3 | Repeat 12.1 on Mobile | Result is `completed`; layout switches to vertical-packed and the validator continues to flag genuine overlaps if any (regression check that the trust-the-compiler rule did not silence real problems on the inflated-height path) |
| 12.4 | Open the persisted trace for one Desktop run and confirm `validationSummary.collisionCount == 0` and `boundaryViolationCount == 0` | Both counts are 0 |

Backed by `test_horizontal_stacked_rows_do_not_trigger_phantom_collisions`
and `test_collision_check_still_inflates_when_height_missing` in
`backend/tests/test_story_63_context_pack_path.py`.

---

## §13 — Framework parity per component (Submit / Rating / Terms / Dropdown)

Goal: Spot-check that AI-generated components stay editable through the
*standard* form-builder controls — the central guarantee from UAT round
10 ("framework_first" decision). All overrides the compiler stamps must
be re-adjustable through the existing Appearance / Dimensions / Grid
Layout panels.

| Step | Component | Expected |
|------|-----------|----------|
| 13.1 | Submit button | Width / alignment editable from the standard properties panel; `props.width` matches `style.width`; preview shows the configured button text |
| 13.2 | Rating | Number of stars + style editable from properties panel; star row does not wrap; E/W resize handles work; preview shows configured ratings without overlap |
| 13.3 | Terms | Checkbox + label + link on a single row; properties panel can change link text and target URL; validation message appears next to the link, not below |
| 13.4 | Dropdown | Options editable; selecting an option does not hide the validation message; dropdown widens to fit the longest option; preview shows the placeholder text in the closed control |
| 13.5 | Generic text / email / phone | Width and label editable; validation placeholder visible in design mode and resolves to a real message in preview when the user submits an empty form |

Note: §13.1 ("submit-button design vs preview validation parity") is
still open in this story (see §15). Mark §13 as **Pass with caveat**
until that gap closes.

---

## §14 — Canvas height growth (mandatory)

Goal: Confirm the compiler grows the canvas vertically when the form
has more components than fit in the initial canvas height, *both* in
the form builder canvas (edit mode) and the preview. Added in UAT
round 9 after the user observed mobile canvases not resizing in edit
mode while preview showed the full layout.

| Step | Action | Expected |
|------|--------|----------|
| 14.1 | Generate a tall form (e.g. Prompt 4 — job application) on **Mobile** with the default 980 px canvas | Builder canvas grows vertically to fit the submit button; no scrollbar over a clipped layout |
| 14.2 | Switch the same generated form to **Preview** mode | Preview height matches builder canvas; submit button is fully visible |
| 14.3 | Switch back to a wide canvas (Desktop) without re-generating | Canvas height shrinks back to fit the now-shorter horizontal-stacked layout (no leftover empty rows) |
| 14.4 | In the trace, confirm `compileSummary.canvasHeightAdjustment` (or equivalent) is non-zero for the Mobile run and zero/negative for the Desktop run | Adjustment value is present and matches direction |

---

## §15 — Builder edit-after-AI parity (regression guard)

Goal: Verify that all AI-generated components remain fully editable
using the standard form-builder controls — width, height, label,
help text, validation rules, grid placement. The story's success
criterion is **AI builds the form, the user takes over with the
existing tools**.

| Step | Action | Expected |
|------|--------|----------|
| 15.1 | Generate any benchmark prompt | Each component selects normally; properties panel populates with the correct values |
| 15.2 | Edit the width of two components via the Dimensions panel | New widths persist; canvas redraws without collision warnings |
| 15.3 | Edit the label of a `terms` component to a longer text | Label re-flows; validation message stays inline; canvas does not exceed its bounds |
| 15.4 | Add a new component from the toolbox to the AI-generated form | New component appears in tab order at the click position; saves without losing the AI-generated components |
| 15.5 | Save the form and reopen it | Reloaded form is identical to the saved state (no compiler re-run on load) |

Open item still in flight: `g-frontend-submit-parity` — submit-button
shows a per-field validation pill in design mode but a form-level
summary message in preview. Both reveal the validation; the user is
asking for design / preview parity. Tracked outside this UAT pass; do
not block sign-off on this point but record any new repro under §15.5.

---

## §9 — UAT Result

| Section | Pass / Fail / Skipped | Notes |
|---------|----------------------|-------|
| §1 Automated gates | | |
| §2 Capability ingestion | | |
| §3 Validation contracts | | |
| §4 Width class responsiveness | | |
| §5 Builder visibility | | |
| §6 Logging + one-change discipline | | |
| §7 Render-then-measure | | |
| §8 Consent / legal nudge | | |
| §10 Country / locale awareness | | |
| §11 Layout-mode selection | | |
| §12 Horizontal-stacked validator parity | | |
| §13 Framework parity per component | | |
| §14 Canvas height growth | | |
| §15 Builder edit-after-AI parity | | |

**Sign-off:** _Name / date_

# Story 6.4.5 — Component Property Cheat Sheet H3

**Epic:** 6 — AI Generation & Monetization Engine  
**Story ID:** 6.4.5  
**Title:** Component Property Cheat Sheet H3  
**Status:** Measured/no-change — H3 no-go as-is  
**Branch:** `story/epic6-6.4.5-component-property-cheat-sheet`  
**PR:** [#81](https://github.com/anthonykeevy/EventLeadPlatform/pull/81) — merged 2026-04-29
**Created:** 2026-04-28  
**Completed:** 2026-04-29  
**Depends On:** Story 6.4.4.2 ([PR #79](https://github.com/anthonykeevy/EventLeadPlatform/pull/79)) and post-merge stamp ([PR #80](https://github.com/anthonykeevy/EventLeadPlatform/pull/80)) merged.  
**Unblocks:** Story 6.5a clarification questions and later additive AI capability stories.

---

## 1) Goal

Measure H3: add a concise **Component Property Cheat Sheet** to the Form AI prompt path so the model knows which semantic properties matter for each registered component type without inventing unsupported props.

H2 and H4 both failed under `rubric_v2`, so this story is the next prompt candidate. It must stay evidence-first: ship H3 only if the eval harness and judge evidence show no material regression and a useful improvement signal. A measured/no-change closeout is acceptable.

Success means:

- H3 is implemented as a bounded additive prompt block.
- The block is generated only from/for capability-snapshot component types available to the compiler.
- `prompts-v1.1` / `rubric_v2` evaluation is run against the AC10 baseline.
- H3 ships only if evidence supports it.

---

## 2) In Scope

### 2.1 Component property cheat sheet prompt block

Add a compact prompt block near the existing allowed-component block in `backend/modules/form_ai/service.py`.

Expected shape:

```text
COMPONENT PROPERTY CHEAT SHEET (use only these semantic properties):
  - text/email/phone/url: label, placeholder, helpText, validationIntent.required/pattern/minLength/maxLength, widthIntent
  - textarea: label, placeholder, helpText, validationIntent, widthIntent=full for long responses
  - dropdown/radio/checkbox: label, options[{label,value}], validationIntent.required, widthIntent
  - terms: label, validationIntent.required, leave legal URLs/content empty unless user provided them
  - header/paragraph/divider: display copy only; no validationIntent
  - submit-button: label/action copy, widthIntent compact/half, no validationIntent
```

Implementation may use a small static map filtered to the active capability snapshot. Do not expose components that are not in the snapshot.

### 2.2 Tests

Add focused tests proving:

- The H3 block is omitted when no capability snapshot exists.
- The H3 block includes only component types present in the snapshot.
- The H3 block does not mention unsupported/future components.
- The initial system prompt includes the H3 block in the right area when enabled.

### 2.3 Eval harness run

Run H3 against the same control family:

- Control: `_bmad-output/eval-runs/story-6.4.4.1-ac10-baseline-v2/`
- Benchmark: `prompts-v1.1`
- Rubric: `rubric_v2`
- Variant label: `story-6.4.5-h3-component-property-cheat-sheet`

Generate judge packages with Claude 4.7, Grok 4, and GPT-5 mini. Ingest outputs and run diff/statistics against the AC10 baseline.

### 2.4 Decision artifact

Record the verdict in:

- `STORY-6.4.5-HYPOTHESIS-EVIDENCE.md`
- `STORY-6.4.5-CLOSEOUT-REPORT.md`

Ship H3 only if it clears the bar.

---

## 3) Out of Scope

| Item | Reason / future home |
|---|---|
| H1/H2/H4 prompt changes | H1 rejected/suspect; H2/H4 failed Story 6.4.4.2. |
| New component types or renderer changes | This story only describes existing component properties. |
| Capability snapshot migration/version bump | Not needed unless renderer manifest data changes; avoid unless Dev proves it is required. |
| Frontend UI changes | No UI surface expected. |
| Rubric v3 or judge-panel redesign | `rubric_v2` remains authoritative. |
| Image-to-Form / style intent / PII detection | Later 6.5 stories. |

---

## 4) Acceptance Criteria

1. **AC-1 H3 block implemented:** Form AI system prompt can include a concise component-property cheat sheet.
2. **AC-2 Snapshot filtering:** H3 only lists component types present in the active capability snapshot.
3. **AC-3 No unsupported props:** H3 does not instruct the model to emit unsupported/future properties or component types.
4. **AC-4 Prompt contract tests:** Focused backend tests cover H3 rendering and prompt inclusion.
5. **AC-5 H3 eval run complete:** H3 variant runs over `prompts-v1.1` with 270 generated definitions or a documented retry/failure outcome.
6. **AC-6 Judge packages generated:** H3 has a rubric_v2 judge package with explicit output paths for Claude, Grok, and GPT-5 mini.
7. **AC-7 Judge outputs ingested:** H3 judge JSONs are valid and ingested into summary JSON/CSV.
8. **AC-8 Diff/statistics recorded:** H3 is compared against AC10 baseline with diff/stat outputs recorded.
9. **AC-9 Ship/no-change verdict recorded:** Evidence clearly states whether H3 ships or is reverted/no-change.
10. **AC-10 No unrelated AI capability work:** No H1/H2/H4, H5/H6, image-to-form, or frontend feature work leaks into this story.
11. **AC-11 Green gate evidence recorded:** Focused tests and backend regression evidence are recorded; frontend checks are only required if frontend files are touched.
12. **AC-12 Closeout complete:** Story/status/workflow docs are updated and stale-field audit passes before merge.

---

## 5) Definition of Done

- All ACs are mapped to evidence.
- Story branch is pushed to PR #81.
- H3 final state is either shipped with evidence or reverted/no-change.
- No untracked scratch artifacts are committed.
- Closeout report recommends the next story.

---

## 6) Closeout

**Verdict:** no-go as-is / measured no-change.

H3 was implemented and measured under `prompts-v1.1` / `rubric_v2`, but it is not shipped from PR #81. The diff/stat output showed useful positive signal, but also a material `field_label_f1` regression and additional `validation_intent_accuracy` / `row_group_agreement` regressions. The current evaluation framework also mixes prompt-candidate effects with locale/context-conflict noise.

Final code state: H3 prompt changes were removed; runtime prompt behavior remains unchanged.

Evidence:

- `STORY-6.4.5-HYPOTHESIS-EVIDENCE.md`
- `STORY-6.4.5-GATE-EVIDENCE.md`
- `STORY-6.4.5-UAT-RESULTS.md`
- `STORY-6.4.5-CLOSEOUT-REPORT.md`

Recommendation: do not continue prompt candidate sweeps until an AU-only diagnostic evaluation framework is implemented.


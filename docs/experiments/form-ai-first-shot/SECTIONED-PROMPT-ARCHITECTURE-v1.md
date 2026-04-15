# Sectioned Prompt Architecture v1 (Control Chat Baseline)

## Objective

Move Form AI evaluation from script-only addendum loops to a **frontend-driven, sectioned prompt pipeline** that is still delivered as one concatenated prompt to the LLM, while preserving measurable outcomes and DB-level observability.

## Source of truth used

- `docs/COMPONENT-FRAMEWORK-REFERENCE.md`
- `docs/AGENT-LOGGING-GUIDE.md`

## Section scope analysis

The component framework is broad; the section split below follows how the Builder already groups concerns (Layout, Data Collection, Validation Rules, Appearance, Logic) plus a delivery constraint section.

| Section | Framework coverage | Expected prompt size | Primary risks | Eval signals |
|---|---|---:|---|---|
| `layout` | canvas geometry, SmartBorder, collision/boundary rules, runtime footprints, grid/object precedence | 25-35% | false collisions, overflow, row drift | `coll`, `bnd`, Layout score (`L`) |
| `data_collection` | Identity + Data Collection properties (`label`, `placeholder`, `required`, `exportName`, `tabOrder`, options) | 15-20% | missing fields, wrong component type | Goal subscore: fields/options completeness |
| `validation_rules` | validation contract + per-type constraints/messages | 10-15% | schema-valid but behavior-invalid rules | valid flag (`V`), validation issue counts |
| `appearance` | global styles inheritance, styleOverrides, typography/colors/spacing widths | 15-20% | global override drift, toolbox/runtime mismatch | visual parity checks + `L` regressions |
| `logic` | initial visibility/enabled, logic source/target integrity, operator/action validity | 10-15% | broken refs, contradictory rules | logic-rule lint + runtime sanity |
| `delivery_summary` | output contract guardrails (JSON only, deterministic structure) | 5-10% | prose leakage, non-schema keys | schema validity + parser success |

## Why this split works

- It mirrors existing Builder panel taxonomy and property coverage matrix.
- Each section maps to testable validators without coupling all failures into one score.
- It keeps first-shot tuning compatible with current system addendum mechanism.

## Evaluation method (per run)

1. Build section objects (`id`, objective, instructions).
2. Concatenate into one system addendum (ordered sections).
3. Submit one request from AI Agent panel with explicit retry count.
4. Log section metadata at start and result at completion.
5. Score run with existing truth metrics (`L`, `G`, `C`, `coll`, `bnd`, `V`) and attach section metadata for correlation.

## Section-level logging contract

Use frontend dev logger events (persisted to `log.FrontendEvent` when `VITE_LOG_SEND_TO_BACKEND=true`):

- `ai.sections.run.start`
  - `sectionCount`
  - `sections[]`: `id`, `title`, `chars`, `hash`
  - `openaiTransport`
  - `maxSystemCorrectionAttempts`
  - `promptChars`
- `ai.sections.run.result`
  - `status`, `terminalReason`, `attemptCount`
  - `resolvedOpenaiTransport`
  - `validationSummary`
  - same section metadata
- `ai.sections.run.error`
  - transport/retry configuration and error message

This enables SQL/diagnostic filtering by event name and section id/hash across runs.

## Control-chat operating mode

- Run from Builder AI Agent panel (not script injection/paste workflow).
- Set **System correction attempts = 1** for evaluation baseline.
- Keep user prompt fixed per block.
- Change one section lever at a time between iterations.

## Next extension candidates

1. Split `layout` into `layout_geometry` and `layout_spacing` if collision improvements stall.
2. Split `appearance` into `appearance_dimensions` and `appearance_typography_colors` when style regressions dominate.
3. Add backend-side section result ingestion if per-section numeric scores are computed server-side.


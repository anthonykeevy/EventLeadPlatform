# Story 6.4.4.1 Closeout Report

## Summary

Story 6.4.4.1 wires Form AI locale architecture to a registry-backed prompt block system, adds `audienceLocale` and `brandPosture` API handling, and bumps the eval/judge harness to `prompts-v1.1` / `rubric_v2`.

Closeout decision: merged via PR #75 on 2026-04-27. Remaining non-blocking work is documented as carry-forward/manual follow-up.

## Implemented

- Added migrations `063`-`071` for:
  - `config.PromptTemplateLocaleBlock`
  - `ref.CountryCulturalDimensions`
  - MVP locale prompt block seeds
  - country cultural dimensions seeds
  - `dbo.GenerationRun` brand posture audit columns
  - `dbo.Company` brand posture defaults
  - `config.AppSetting` defaults for Form AI locale behavior
- Replaced the hard-coded locale prompt block with registry assembly, process-local cache, neutral fallback, and `log.ApplicationError` fallback logging.
- Added audience locale resolution chain: request, form event, company, user, AppSetting, fallback.
- Added brand posture resolution chain: request, company, AppSetting, fallback.
- Added response `meta.locale` / `meta.brand` resolution detail.
- Added frontend pass-through fields on `/api/form-ai/generate`; no Company Settings UI was added in this story.
- Updated eval harness to `prompts-v1.1` with 270 locale-conditioned cells.
- Updated judge packaging and ingest to `rubric_v2`, Claude + Grok primary mean, GPT-5 mini control deltas, and required `judge_model_version`.

## Verification

See `STORY-6.4.4.1-GATE-EVIDENCE.md`.

Targeted backend checks pass: `44 passed`.

Full backend suite passes after migrations were applied: `793 passed, 26 skipped`.

Frontend lint passes after worktree dependencies were installed.

## Known Gaps

- Company Settings UI for `Company.BrandPosture` and `Company.BrandHeritageOrigin` is not implemented in this story. The DB columns, backend resolution, and generation-run persistence are complete, but self-service editing belongs in follow-up `g-6441-company-brand-settings-ui` under Company Settings / Form Branding.
- AC-10 live judge rerun remains pending human/Cursor judge execution; judge prompts/package/ingest are implemented and ready.

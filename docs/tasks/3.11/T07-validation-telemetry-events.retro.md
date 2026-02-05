# Retro: T07 Validation Telemetry

**Story:** 3.11  
**Task:** Validation Telemetry - Events + Storage + Resolved vs Abandoned  
**Date:** 2026-02-05  
**Outcome:** ✅ Passed UAT

---

## What went well

- Telemetry payloads were emitted on blocked submits and stored reliably in `log.FrontendEvent`.
- Value diagnostics captured useful shape details without leaking raw input values.
- `clientSessionId` correlation enabled resolved vs abandoned analysis.

## Issues / Friction

- No explicit `submission_captured` event; correlation relies on `FormSubmission` records.

## Improvements / Action Items

- Add an automated check to assert a `validation_failed_submit` event precedes a successful submission in the same session (resolved flow).
- Consider a dedicated `submission_captured` event if analytics needs clearer event-based pipelines.

## Evidence

- Completion note: `docs/tasks/3.11/T07-validation-telemetry-events.completion.md`
- UAT results: `docs/tasks/3.11/T07-validation-telemetry-events.uat-results.md`

# Story 6.4.3b ADR — Rubric v1 Governance

**Status:** Template ready; Dev finalises with `rubric_v1.md`  
**Story:** 6.4.3b — Eval Judge Package + Rubric ADR  
**Decision Owner:** SM + Dev; Architect review required for rubric version changes  
**Date:** 2026-04-25

---

## Context

Epic 6 prompt changes need measured evidence. Category A structural metrics are deterministic and already covered by the 6.4.3a harness. Category B semantic quality requires judge scoring.

The approved brief locks the judge architecture:

- three judges via Cursor chats,
- GPT-5 mini as control,
- Claude and Gemini as cross-model primary judges,
- no API integration,
- rubric file versioning,
- future rubric changes require ADR and baseline re-snapshotting.

---

## Decision

Use `backend/tests/form_ai_eval/rubric_v1.md` as the locked rubric for the first generation of semantic judge scoring.

Primary score aggregation:

- Claude + Gemini mean is the primary metric value.
- GPT-5 mini is retained as a self-judging control and excluded from the primary mean.
- Bias delta is `gpt5mini_score - cross_model_mean`.

Rubric changes:

- Any scoring definition, anchor, metric key, or required JSON shape change creates `rubric_v2.md`.
- Bumping the rubric requires updating this ADR or adding a new ADR.
- Baseline judge packages must be regenerated and re-scored when the rubric version changes.

---

## Rationale

- Manual Cursor chats avoid new secrets and model API clients.
- A file-versioned rubric makes experiments reproducible.
- Claude + Gemini primary mean reduces GPT-5 mini self-preference risk.
- Keeping GPT-5 mini as control still surfaces self-bias deltas for the closeout retro.

---

## Consequences

Positive:

- Prompt experiments can cite stable semantic scoring evidence.
- Judge workflow remains low-cost and no-secret.
- Future rubric changes are visible and auditable.

Negative:

- Anthony has manual copy/paste work per sweep.
- Judging remains asynchronous and human-orchestrated.
- Rubric errors require re-scoring affected baselines.

---

## Required Implementation Evidence

Dev must complete this ADR with:

- final metric list from `rubric_v1.md`,
- final JSON schema summary,
- judge package folder shape,
- ingest behavior,
- rubric v2 trigger examples,
- baseline re-snapshot policy.

---

## Review Questions

1. Are all Category B metrics scoreable from the generated package without hidden context?
2. Are score anchors specific enough for three different models to follow consistently?
3. Does the JSON schema make invalid/missing rows obvious before ingest?
4. Does the workflow clearly tell Anthony which Cursor model to use for each file?
5. Is the rubric narrow enough to avoid judging style before H5/H6 stories?

# Story 6.4.2 ADR — FormSemanticPlan Backward Compatibility

**Status:** Template ready; Dev finalises during implementation  
**Story:** 6.4.2 — Capability Snapshot Prompt Cleanup  
**Decision Owner:** SM + Dev, with Architect review if compatibility changes  
**Date:** 2026-04-25

---

## Context

`FormSemanticPlan` is the internal LLM output contract introduced during Story 6.3.1. The model sometimes drifts into legacy or near-miss shapes, especially during correction loops and replay of older generations.

The current schema includes compatibility behavior:

- normalize missing or non-`"1.0"` `semanticPlanVersion` to `"1.0"`,
- accept `fields`, `items`, or `elements` as aliases for `components`,
- ignore extra root keys.

Story 6.4.2 records whether these choices are intentional and where the compatibility boundary ends before later stories add clarification, vision, and style-intent schema changes.

---

## Decision

`FormSemanticPlan` keeps a narrow internal backward-compatibility layer for LLM drift and replayability.

Accepted compatibility:

1. `semanticPlanVersion` missing or not equal to `"1.0"` is normalized to `"1.0"`.
2. If `components` is absent, the first list-valued alias among `fields`, `items`, and `elements` is treated as `components`.
3. Extra root keys are ignored.

Not promised:

1. This is not a public API compatibility guarantee.
2. Unknown component types are not accepted when a capability snapshot is active.
3. Future schema versions do not automatically inherit these aliases.
4. Style/theme fields remain out of scope until the style-intent story explicitly changes the contract.

---

## Rationale

- LLM correction loops should recover from harmless naming/version drift without spending an attempt on shape-only mistakes.
- Historic `GenerationRun` replay needs to remain useful while the system prompt evolves.
- The deterministic compiler and semantic validator still own strict safety checks after parsing.
- Keeping compatibility narrow prevents the schema from becoming an unbounded legacy sink.

---

## Consequences

Positive:

- Fewer avoidable correction attempts.
- More robust replay of historical generations.
- Clear separation between parse tolerance and semantic validation.

Negative:

- Root-level mistakes can be silently normalized, so tests must document the behavior.
- Future schema versions need explicit migration/retirement decisions.

---

## Tests Required

Dev must add or confirm tests for:

- version normalization to `"1.0"`,
- `fields` alias,
- `items` alias,
- `elements` alias,
- extra root key ignored,
- non-dict input still fails normally,
- active capability snapshot still rejects unknown component types after parse.

---

## Retirement Trigger

Revisit this ADR when:

- `semanticPlanVersion` gains a real v2 contract,
- Style Intent adds new root-level semantic fields,
- Image-to-Form introduces vision-specific plan metadata,
- historical replay no longer needs the alias behavior.

At that point, either:

- keep v1 compatibility behind an explicit parser version branch, or
- remove aliases after a replay-data migration/expiry decision.

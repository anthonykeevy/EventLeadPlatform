# Story 6.4.2 — Capability Parity Audit

**Story:** 6.4.2 — Capability Snapshot Prompt Cleanup  
**Status:** Complete — safe for active capability prompt use  
**Purpose:** Prove the active backend capability snapshot matches the frontend builder/runtime surfaces before the snapshot is made a hard prompt constraint.

---

## 1) Audit Inputs

| Source | Path / Query | Result |
|--------|--------------|--------|
| Active backend snapshot | `config.ComponentCapabilitySnapshot` latest active row | `ComponentCapabilitySnapshotID=4`, `SnapshotVersion=cf-6.3.1-v4`, `GeneratedDate=2026-04-21 11:19:39.740000`; 19 active types |
| Backend compiler/semantic validator | `backend/modules/form_ai/compiler.py`, `semantic_validator.py` | Validator rejects unknown types only when a snapshot exists; compiler has width tiers for all 19 active snapshot types |
| Frontend registry/toolbox | `frontend/src/features/builder/registry/ComponentRegistry.tsx` | All 19 active snapshot types have registry entries, toolbox previews, and runtime components |
| Runtime footprints | `frontend/src/features/builder/components/ai/buildAiRuntimeFootprints.ts` | All registry `input`/`display` types are included in AI footprints; type-specific height defaults cover all 19 active snapshot types |
| Frontend component capabilities | `frontend/src/features/builder/utils/componentCapabilities.ts` | Explicit capability handling covers most active types; `rating` and `file-upload` use the default input-capability fallback |

Do not run Alembic as part of this audit. Anthony runs any migration if a repair is needed.

---

## 2) Component Type Matrix

| Component Type | Backend Snapshot | Compiler / Validator | Frontend Registry / Renderer | Runtime Footprint | Classification | Decision |
|----------------|------------------|----------------------|------------------------------|-------------------|----------------|----------|
| `text` | yes | yes | yes | yes | `match` | Safe active type |
| `textarea` | yes | yes | yes | yes | `match` | Safe active type |
| `email` | yes | yes | yes | yes | `match` | Safe active type |
| `phone` | yes | yes | yes | yes | `match` | Safe active type |
| `number` | yes | yes | yes | yes | `match` | Safe active type |
| `date` | yes | yes | yes | yes | `match` | Safe active type |
| `address` | yes | yes | yes | yes | `match` | Safe active type |
| `dropdown` | yes | yes | yes | yes | `match` | Safe active type |
| `radio` | yes | yes | yes | yes | `match` | Safe active type |
| `checkbox` | yes | yes | yes | yes | `match` | Safe active type |
| `terms` | yes | yes | yes | yes | `match` | Safe active type |
| `header` | yes | yes | yes | yes | `match` | Safe active type |
| `paragraph` | yes | yes | yes | yes | `match` | Safe active type |
| `divider` | yes | yes | yes | yes | `match` | Safe active type |
| `submit-button` | yes | yes | yes | yes | `match` | Safe active type |
| `url` | yes | yes | yes | yes | `match` | Safe active type |
| `rating` | yes | yes | yes | yes | `match` | Safe active type |
| `file-upload` | yes | yes | yes | yes | `match` | Safe active type |
| `first-name` | yes | yes | yes | yes | `match` | Safe active type |

Allowed classifications:

- `match`
- `intentional-substitution`
- `frontend-only`
- `backend-only`
- `missing-renderer`
- `requires-follow-up`

---

## 3) Width Class Parity

| Component Type | Backend Width Classes | Compiler Tier Support | Frontend Footprint / Layout Notes | Decision |
|----------------|-----------------------|-----------------------|-----------------------------------|----------|
| `text` | `compact`, `half`, `full` | `COMPONENT_WIDTH_TIERS` supports `text` | Runtime footprint height default 110; width cap generic | Match |
| `textarea` | `half`, `full` | `COMPONENT_WIDTH_TIERS` supports `textarea` | Runtime footprint height default 200; wider cap for textarea/address | Match |
| `email` | `compact`, `half`, `full` | `COMPONENT_WIDTH_TIERS` supports `email` | Runtime footprint height default 110 | Match |
| `phone` | `compact`, `half`, `full` | `COMPONENT_WIDTH_TIERS` supports `phone` | Runtime footprint height default 110 | Match |
| `number` | `compact`, `half`, `full` | `COMPONENT_WIDTH_TIERS` supports `number` | Runtime footprint height default 110 | Match |
| `date` | `compact`, `half`, `full` | `COMPONENT_WIDTH_TIERS` supports `date` | Runtime footprint height default 110 | Match |
| `address` | `full` | `COMPONENT_WIDTH_TIERS` supports `address` | Runtime footprint height default 120; wider cap for textarea/address | Match |
| `dropdown` | `compact`, `half`, `full` | `COMPONENT_WIDTH_TIERS` supports `dropdown` | Runtime footprint height default 120 plus option growth | Match |
| `radio` | `half`, `full` | `COMPONENT_WIDTH_TIERS` supports `radio` | Runtime footprint height default 120 plus option growth | Match |
| `checkbox` | `half`, `full` | `COMPONENT_WIDTH_TIERS` supports `checkbox` | Runtime footprint height default 120 plus option growth | Match |
| `terms` | `full` | `COMPONENT_WIDTH_TIERS` supports `terms` | Runtime footprint height default 120 | Match |
| `header` | `full` | `COMPONENT_WIDTH_TIERS` supports `header` | Runtime footprint height default 52 | Match |
| `paragraph` | `full` | `COMPONENT_WIDTH_TIERS` supports `paragraph` | Runtime footprint height default 88 | Match |
| `divider` | `full` | `COMPONENT_WIDTH_TIERS` supports `divider` | Runtime footprint height default 20; narrower cap | Match |
| `submit-button` | `compact`, `half` | `COMPONENT_WIDTH_TIERS` supports `submit-button` | Runtime footprint height default 64, clamped to 72 | Match |
| `url` | `half`, `full` | `COMPONENT_WIDTH_TIERS` supports `url` | Runtime footprint height default 110; Story 6.2.1 force-include | Match |
| `rating` | `half`, `full` | `COMPONENT_WIDTH_TIERS` supports `rating` | Runtime footprint height default 96; Story 6.2.1 force-include | Match |
| `file-upload` | `full` | `COMPONENT_WIDTH_TIERS` supports `file-upload` | Runtime footprint height default 132; Story 6.2.1 force-include | Match |
| `first-name` | `half`, `full` | `COMPONENT_WIDTH_TIERS` supports `first-name` | Runtime footprint height default 110 | Match |

---

## 4) Findings

| ID | Finding | Severity | Decision / Follow-Up |
|----|---------|----------|----------------------|
| F-01 | Active snapshot has no component type without a frontend renderer/toolbox/runtime footprint. | P0 | Closed; no missing-renderer active capability. |
| F-02 | Compiler contains width tiers for extra non-active types (`last-name`, `time`, `select`). `select` is also a frontend type alias, but no active snapshot row or registry entry allows the LLM to emit it as a snapshot-approved type. | P3 | No blocker; snapshot prompt and validator remain authoritative. |
| F-03 | `componentCapabilities.ts` does not explicitly switch on `rating` or `file-upload`; both fall through to input defaults. | P3 | Accept; renderer/runtime paths exist and defaults are appropriate. |

P0/P1 parity findings block story closeout unless fixed in this PR or explicitly accepted by SM as a blocking carry-forward.

---

## 5) Audit Decision

Capability snapshot is safe to pass into the prompt by default when:

- no active snapshot component type is classified `missing-renderer`,
- no `backend-only` type can be emitted by the LLM without a matching frontend surface,
- runtime footprints either cover the type or the type is intentionally excluded with rationale,
- all P0/P1 findings are closed.

Decision: `safe`

The active `cf-6.3.1-v4` snapshot is safe to pass into the prompt as the authoritative component palette. No active snapshot component is classified `missing-renderer`, `backend-only`, or `requires-follow-up`.

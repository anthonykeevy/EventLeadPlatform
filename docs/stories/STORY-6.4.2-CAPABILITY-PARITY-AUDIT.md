# Story 6.4.2 — Capability Parity Audit

**Story:** 6.4.2 — Capability Snapshot Prompt Cleanup  
**Status:** Template ready; Dev completes before capability prompt behavior is changed  
**Purpose:** Prove the active backend capability snapshot matches the frontend builder/runtime surfaces before the snapshot is made a hard prompt constraint.

---

## 1) Audit Inputs

| Source | Path / Query | Result |
|--------|--------------|--------|
| Active backend snapshot | `config.ComponentCapabilitySnapshot` latest active row | `<snapshot id/version/date>` |
| Backend compiler/semantic validator | `backend/modules/form_ai/compiler.py`, `semantic_validator.py` | `<summary>` |
| Frontend registry/toolbox | `frontend/src/features/builder/registry/ComponentRegistry.tsx` | `<summary>` |
| Runtime footprints | `frontend/src/features/builder/components/ai/buildAiRuntimeFootprints.ts` | `<summary>` |
| Frontend component capabilities | `frontend/src/features/builder/utils/componentCapabilities.ts` | `<summary>` |

Do not run Alembic as part of this audit. Anthony runs any migration if a repair is needed.

---

## 2) Component Type Matrix

| Component Type | Backend Snapshot | Compiler / Validator | Frontend Registry / Renderer | Runtime Footprint | Classification | Decision |
|----------------|------------------|----------------------|------------------------------|-------------------|----------------|----------|
| `text` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<match/...>` | `<decision>` |
| `textarea` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<match/...>` | `<decision>` |
| `email` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<match/...>` | `<decision>` |
| `phone` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<match/...>` | `<decision>` |
| `number` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<match/...>` | `<decision>` |
| `date` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<match/...>` | `<decision>` |
| `address` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<match/...>` | `<decision>` |
| `dropdown` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<match/...>` | `<decision>` |
| `radio` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<match/...>` | `<decision>` |
| `checkbox` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<match/...>` | `<decision>` |
| `terms` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<match/...>` | `<decision>` |
| `header` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<match/...>` | `<decision>` |
| `paragraph` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<match/...>` | `<decision>` |
| `divider` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<match/...>` | `<decision>` |
| `submit-button` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<match/...>` | `<decision>` |
| `url` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<match/...>` | `<decision>` |
| `rating` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<match/...>` | `<decision>` |
| `file-upload` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<match/...>` | `<decision>` |
| `first-name` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<yes/no>` | `<match/...>` | `<decision>` |

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
| `<type>` | `<compact/half/full/...>` | `<summary>` | `<summary>` | `<decision>` |

---

## 4) Findings

| ID | Finding | Severity | Decision / Follow-Up |
|----|---------|----------|----------------------|
| `<id>` | `<finding>` | `<P0/P1/P2/P3>` | `<decision>` |

P0/P1 parity findings block story closeout unless fixed in this PR or explicitly accepted by SM as a blocking carry-forward.

---

## 5) Audit Decision

Capability snapshot is safe to pass into the prompt by default when:

- no active snapshot component type is classified `missing-renderer`,
- no `backend-only` type can be emitted by the LLM without a matching frontend surface,
- runtime footprints either cover the type or the type is intentionally excluded with rationale,
- all P0/P1 findings are closed.

Decision: `<safe / not safe / safe with listed carry-forward>`

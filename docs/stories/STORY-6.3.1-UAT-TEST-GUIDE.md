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

Record summary lines in UAT notes / gate evidence.

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

## §7 — UAT Result

| Section | Pass / Fail / Skipped | Notes |
|---------|----------------------|-------|
| §1 Automated gates | | |
| §2 Capability ingestion | | |
| §3 Validation contracts | | |
| §4 Width class responsiveness | | |
| §5 Builder visibility | | |
| §6 Logging + one-change discipline | | |

**Sign-off:** _Name / date_

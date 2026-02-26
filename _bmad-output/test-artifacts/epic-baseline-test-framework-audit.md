# Epic Baseline Test-Framework Audit (Pre-Epic 6)

Date: 2026-02-26  
Reviewer: TEA (Test Architect)  
Purpose: Consolidated readiness audit across completed epics before starting Epic 6 implementation

---

## Scope and evidence used

### In-scope epics
- Epic 2 (complete)
- Epic 3 (complete)
- Epic 5 completed stories (`5.1` to `5.9`; explicitly excluding open `5.11`)
- Epic 1 auth-token stabilization outputs as baseline reference

### Evidence artifacts reviewed
- `docs/stories/EPIC-2-STATUS.md`
- `docs/stories/EPIC-3-STATUS.md`
- `docs/stories/EPIC-5-STATUS.md`
- `docs/stories/story-5.9.md`
- `docs/stories/STORY-5.9-UAT-TEST-GUIDE.md`
- `_bmad-output/test-artifacts/phase-1-ds-implementation-summary.md`
- `_bmad-output/test-artifacts/phase-1-cr-review-summary.md`
- `_bmad-output/test-artifacts/phase-1-tea-rv-summary.md`
- `_bmad-output/test-artifacts/framework-setup-progress.md`
- `_bmad-output/test-artifacts/traceability-report.md`
- `backend/pytest-summary.txt`
- `backend/pytest-results.txt`
- `tests/README.md`
- `playwright.config.ts`
- `backend/pytest.ini`

---

## 1) Epic-by-epic coverage snapshot (unit / integration / e2e)

## Epic 2 (Complete)
- **Unit:** Present but uneven (selected backend/frontend units; marker hygiene inconsistent).
- **Integration/API:** Strong historical emphasis; Epic 2 status records 13/13 stories complete with UAT pass.
- **E2E:** Primarily human UAT evidence; no robust automated browser suite tied to Epic 2 critical flows.
- **Confidence:** Medium (completion/UAT docs strong; automated level split less explicit in artifacts).

## Epic 3 (Complete)
- **Unit:** Some frontend utility/component tests exist; backend unit specificity for Epic 3 logic is limited in current artifact set.
- **Integration/API:** Story-level completion and UAT evidence show major capability coverage (builder, renderer, logic, outbox).
- **E2E:** Epic 3 status reports substantial UAT scenarios, but automated E2E framework was still in scaffold phase during baseline artifacts.
- **Confidence:** Medium (UAT evidence strong, automation maturity mixed).

## Epic 5 (Completed stories 5.1-5.9 only)
- **Unit:** Frontend and utility tests exist (for example builder/utils and config/UI tests), but not clearly mapped per story done criteria.
- **Integration/API:** Concrete backend tests exist for key readiness foundations (`assets`, defaults, schema parity, resolver parity) and additional publish/lead API tests are present in test tree.
- **E2E:** Story 5.9 UAT guide demonstrates full user/admin lifecycle test execution with defect closure; automated E2E remains minimal (single scaffold example test in `tests/e2e`).
- **Confidence:** Medium-high on manual/UAT lifecycle; low-medium on automated E2E depth.

## Epic 1 stabilization baseline (reference only)
- Focused auth-token critical suites pass (`jwt_service`, `auth_middleware`, `team_invitations`) per Phase 1 DS/RV evidence.
- Residual concerns already documented: seed parity risk, async loop-scope config gap, datetime warning debt.

---

## 2) Traceability status per epic (P0/P1 gaps)

## Epic 2
- **P0:** Core auth/multi-tenant/admin governance paths have evidence, but explicit REQ->test ID traceability matrix is not maintained consistently.
- **P1 gaps:** Event and workflow variants rely heavily on story/UAT evidence versus stable automated trace mappings.

## Epic 3
- **P0:** Builder-renderer-logic critical paths documented as complete with UAT records.
- **P1 gaps:** Incomplete automated trace links from story acceptance criteria to persistent regression suites.

## Epic 5 (5.1-5.9 only)
- **P0:** Publish/review/preview lifecycle validated in Story 5.9 UAT.
- **P1 gaps:** Prior traceability audit flagged missing/partial automated coverage for publishing and lead collection; improvements are present in test tree but not yet represented in an updated consolidated trace gate.

## Cross-epic traceability maturity
- Current state is **artifact-rich but matrix-light**: many tests/docs exist, but durable P0/P1 trace anchors are fragmented across stories and ad-hoc summaries.

---

## 3) Flakiness and stability risks

### High-impact findings
- Full backend suite evidence in `backend/pytest-summary.txt` / `backend/pytest-results.txt` shows major instability in at least one baseline run:
  - `173 failed`, `89 errors`, very high warning volume.
- Marker hygiene issue exists (`PytestUnknownMarkWarning`) despite `--strict-markers` intent in config practices.
- Async warning and coroutine-handling warnings indicate environment/config drift risk.

### Interpretation for readiness
- Focused suites can be green while full-suite signal remains noisy/fragile.
- Without stabilizing full-suite execution posture, Epic 6 regression confidence is insufficient.

---

## 4) Fixture/data environment risks

### Carry-forward concerns (explicit)
1. **Seed parity risk**
   - Confirmed from Phase 1 CR/RV: invitation and related flows depend on seeded reference rows.
   - Risk: environment-to-environment nondeterminism if parity preflight is absent.

2. **Async loop-scope configuration gap**
   - `asyncio_default_fixture_loop_scope` deprecation warning appears in baseline outputs.
   - Risk: future pytest-asyncio defaults can silently alter behavior.

3. **Datetime warning debt**
   - Widespread `datetime.utcnow()` deprecation warnings persist across modules/tests.
   - Risk: warning noise masks regressions now and becomes break risk later.

### Additional fixture/process risks
- Mixed local DB assumptions and test data coupling still surface in broad-suite instability.
- E2E data fixture discipline is not yet represented by a broad automated browser suite.

---

## 5) CI gate recommendations (PR vs nightly)

## PR gate (required)
- Focused critical-path gates:
  - Auth-token stabilization suites (`test_jwt_service.py`, `test_auth_middleware.py`, `test_team_invitations.py`)
  - Epic 5 core foundation API tests (`assets/defaults/schema parity/resolver parity`)
  - Publish/lead P0 API checks (where present in test tree)
- Seed parity preflight check (hard gate)
- Async loop-scope explicit config check (hard gate)
- No-new-`datetime.utcnow()` policy check in touched scope
- Basic Playwright smoke (`tests/e2e`) retained as minimum browser gate

## Nightly gate (required)
- Broader backend regression suite (full run)
- Extended publishing/lead collection integration matrix
- Determinism burn-in for known brittle suites
- Warning trend report and debt budget tracking

## Weekly gate (recommended)
- Full cross-epic traceability report regeneration (P0/P1 mapping)
- Flake trend and quarantined test review
- E2E expansion progress audit against epic critical journeys

---

## 6) Prioritized remediation backlog (P0 / P1 / P2)

## P0 (must complete before Epic 6 execution)
1. Implement and enforce DB/config **seed parity preflight** in CI and local test bootstrap.
2. Set and enforce explicit `asyncio_default_fixture_loop_scope` in pytest configuration.
3. Introduce CI guard to block newly introduced `datetime.utcnow()` usage in touched scope.
4. Re-establish a **stable full-suite baseline** (reduce fail/error rate to acceptable gate thresholds).
5. Produce updated consolidated P0/P1 traceability matrix for Epics 2/3/5 completed scope.

## P1 (complete early in Epic 6 cycle, or pre-6 if capacity allows)
1. Expand automated E2E from scaffold to real critical lifecycle paths (publish + lead collection + admin review).
2. Register and normalize pytest markers to eliminate marker-noise warnings.
3. Convert high-value story/UAT paths into persistent automated regression suites.

## P2 (quality hardening)
1. Systematic timezone-aware datetime migration in test-adjacent and core modules.
2. Rationalize legacy brittle tests and quarantine policy for unstable long-tail suites.
3. Standardize evidence reporting format across DS/CR/RV/Trace artifacts.

---

## 7) Gate recommendation: Ready to start Epic 6?

### Decision: **CONCERNS** (Not ready to start implementation immediately)

### Rationale
- Completed epic artifacts demonstrate strong delivery and UAT discipline.
- However, baseline framework evidence still shows unresolved systemic risks:
  - seed parity dependency
  - async loop-scope config gap
  - datetime warning debt
  - broad-suite stability/traceability inconsistency
- Epic 5 status itself flags `5.11` tech debt remediation as next/required before Epic 6.

### Operational interpretation
- **Planning/design for Epic 6:** acceptable to continue.
- **Implementation start for Epic 6:** hold until P0 remediation backlog above is closed or explicitly waived with ownership and expiry.

---

## Final readiness statement

Epic delivery maturity is high, but framework baseline maturity is not yet at a "safe start" threshold for new major implementation. Close the P0 remediation items first to avoid compounding debt in Epic 6.

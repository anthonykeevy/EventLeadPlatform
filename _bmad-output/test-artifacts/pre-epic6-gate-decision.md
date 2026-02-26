# Pre-Epic-6 Gate Decision

Date: 2026-02-26  
Decision authority: BMAD TEA TR/RV sign-off

---

## Final recommendation

**Recommendation: Start Epic 6 with `GO_WITH_CONCERNS`.**

This is a formal pre-Epic-6 baseline sign-off. Baseline tests and guardrails are currently stable enough for branch start, with explicit risk controls required in Sprint 1.

---

## Prerequisites before Epic 6 branch work

Mandatory prerequisites satisfied at sign-off:
1. `test_preflight_seed_config_parity.py` passing.
2. `check_no_new_datetime_utcnow.py --base-ref origin/master` passing.
3. Full gate command passing: `pytest backend/tests -q --maxfail=12` with zero failures.

Required operating conditions to keep during Epic 6:
1. Keep seed/config parity preflight as a hard CI check.
2. Keep async loop-scope configuration explicit and unchanged unless deliberately reviewed.
3. Keep datetime guard active for touched Python scope.
4. Track warning volume and skip inventory each PR (or nightly at minimum).

---

## Monitoring plan for first Epic 6 sprint

1. **Per-PR checks**
   - Run seed/config preflight.
   - Run datetime guard against base ref.
   - Run targeted Epic 6 tests plus impacted baseline suites.

2. **Nightly checks**
   - Run full `pytest backend/tests -q --maxfail=12`.
   - Publish warning count trend and skipped-test count trend.

3. **Sprint checkpoints**
   - Day 3: Confirm warning count has not regressed above sign-off baseline.
   - Mid-sprint: Review skipped tests (owner + ETA or explicit waiver rationale).
   - Sprint close: Re-run TR-lite checkpoint before enabling wider Epic 6 rollout.

---

## Escalation triggers (auto-review)

Trigger a TEA re-review immediately if any of the following occurs:
- Any failure in guardrail checks (seed/config parity, async loop-scope posture, datetime guard).
- Full suite drops below all-pass state.
- Warning count increases materially without approved rationale.
- New critical-path tests become skipped or quarantined.

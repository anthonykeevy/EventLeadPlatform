# Remediation Wave 2 - Orchestrator Update

WAVE_2_STATUS: partial

## Broad-suite stability delta (before vs after)
- **Before (strict markers, no Wave 2 fixes):**
  - `pytest backend/tests -q --maxfail=12`
  - Stopped at collection: `1 error` (`story_1_4` marker not registered)

- **After Wave 2 stabilization (sampled broad run, excluding two known hanging suites):**
  - `pytest backend/tests -q --maxfail=12 --ignore=backend/tests/test_api_form_publishing.py --ignore=backend/tests/test_api_lead_collection.py`
  - `12 failed, 181 passed, 1 skipped, 0 errors`

- **Intermediate pre-fix sampled run (same command):**
  - `9 failed, 130 passed, 1 skipped, 3 errors`

Net effect:
- Hard-stop collection error resolved.
- Sampled runtime/setup errors reduced (`3 -> 0`).
- Pass signal before cutoff materially improved (`130 -> 181`).
- Remaining failures are mostly assertion/contract drift and a surfaced backend defect path.

## Wave 2 scope checkpoints
- Broad suite stabilization: **partial**
  - Marker gate fixed, key failing clusters reduced, but broad suite still not fully gate-clean.
- Public auth-route resilience regression: **pass**
  - Public login route ignores stale/invalid bearer header.
  - Protected route invalid bearer remains strict (`401`).
- Warning-budget reduction (targeted): **pass/partial**
  - Marker hygiene improved in touched scope.
  - Warning volume still high in broader runs.
- CI/local gate integration: **pass**
  - Practical flow includes preflight + no-new-utcnow checks and critical auth suites.

## Recommendation
- Proceed to **Wave 3 corrective DS** before TEA TR/RV sign-off, focused on:
  1. fixing residual `test_invitation_acceptance.py` API-contract drift and invitation router token path (`create_access_token` db argument),
  2. aligning `test_logging_integration.py` and `test_log_filters.py` with current logging/response contracts,
  3. resolving hang/determinism in `test_api_form_publishing.py` and `test_api_lead_collection.py`,
  4. targeted warning-budget reduction in the touched failing scope.

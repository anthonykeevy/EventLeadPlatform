# Remediation Wave 3 - Orchestrator Update

WAVE_3_STATUS: partial

## Cluster matrix
- `backend/tests/test_invitation_acceptance.py` -> **pass**  
  Note: API-contract drift corrected; invitation token minting `db` argument defect fixed in invitations router.

- `backend/tests/test_log_filters.py` -> **pass**  
  Note: nested sanitize expectation aligned to current redaction contract.

- `backend/tests/test_logging_integration.py` -> **pass**  
  Note: stale response-shape assertions and FK assumptions aligned to current middleware/exception behavior.

- `backend/tests/test_api_form_publishing.py` -> **pass**  
  Note: deterministic setup block removed (fixture cleanup lock + invalid hash path corrected in shared fixtures).

- `backend/tests/test_api_lead_collection.py` -> **pass**  
  Note: same fixture stabilization removed prior setup/runtime breakage for authenticated preview flow.

## Broad-run stability delta
- Baseline (Wave 2 sampled command):  
  `pytest backend/tests -q --maxfail=12 --ignore=backend/tests/test_api_form_publishing.py --ignore=backend/tests/test_api_lead_collection.py`  
  **12 failed, 181 passed, 1 skipped, 0 errors**

- Wave 3 same sampled command:  
  `pytest backend/tests -q --maxfail=12 --ignore=backend/tests/test_api_form_publishing.py --ignore=backend/tests/test_api_lead_collection.py`  
  **2 failed, 228 passed, 1 skipped, 10 errors**

- Wave 3 sampled command including previously hanging suites:  
  `pytest backend/tests -q --maxfail=12`  
  **2 failed, 234 passed, 1 skipped, 10 errors**

Delta interpretation:
- Target Wave 3 instability clusters are closed and no longer hanging/failing.
- Broad gate still blocked by remaining non-target residual errors, primarily in `test_multi_tenancy.py`.

## Recommendation
Require a **Wave 3 corrective micro-pass** before TEA TR/RV sign-off, focused on:
1. multi-tenancy fixture uniqueness/collision stabilization (`admin_a@company-a.com` duplicate inserts),
2. mailhog config expectation alignment (`test_mailhog_integration.py`),
3. stale model-count assertion alignment (`test_models_import.py`).

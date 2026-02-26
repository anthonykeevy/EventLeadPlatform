# Dev Handover: Critical Test Data Factory Fixes (Pre-Epic 6)

## Context

The TEA agent has completed an `*automate` and `*nfr-assess` workflow on the EventLeadPlatform backend API (specifically addressing gaps in Form Publishing and Lead Collection). 

The NFR Assessment resulted in a **FAIL** gate, primarily blocking Epic 6. The most urgent blocker is that the newly generated backend API Integration tests are failing with `422 Unprocessable Entity` and `404 Not Found` because the database fixtures are using raw `uuid.uuid4()` strings instead of actually seeding the test database with real mock data.

## Target Files

- `backend/tests/conftest.py`
- `backend/tests/test_api_form_publishing.py`
- `backend/tests/test_api_lead_collection.py`

## Mission

1. Open `backend/tests/conftest.py` and locate the `mock_draft_form` and `mock_published_form` fixtures.
2. Update these fixtures so that they:
   - Create a mock `Company` (if one doesn't exist).
   - Create a mock `User` linked to the company (or use existing).
   - Create a mock `Event` linked to the company.
   - Insert an actual `Form` record into the test database (using SQLAlchemy `test_db` session).
   - The `mock_draft_form` needs `StatusID` corresponding to 'draft' or equivalent.
   - The `mock_published_form` needs `StatusID` corresponding to 'published' or equivalent, and a valid `DefinitionJSON`.
   - Ensure the fixtures return the actual `FormID` of the inserted records.
3. Validate your implementation by running the two new test files:
   `pytest backend/tests/test_api_form_publishing.py backend/tests/test_api_lead_collection.py`
4. The goal is 100% green tests for these two files.

## Reference

- NFR Assessment Report: `_bmad-output/test-artifacts/nfr-assessment.md`
- Automation Summary: `_bmad-output/test-artifacts/automation-summary.md`

## Why is this important?

Before we introduce complex external integrations like Stripe Billing (Epic 6), the core workflows of publishing a form and collecting a lead *must* be demonstrably protected by robust integration tests. The test shells are built; we just need the data factories wired up correctly to satisfy the FastAPI endpoints' foreign key and business logic checks.

---

## ✅ Completion Report
*Status: COMPLETED (100% Green Tests)*

**Implemented Fixes:**
1. **Robust Data Factories**: Created interconnected `test_company`, `test_event`, `mock_draft_form`, and `mock_published_form` fixtures in `conftest.py`. They successfully create dependencies (`Country`, `EventType`, `FormVersion`, `FormPublicLink`) required by the endpoints.
2. **Role-based Auth Fixtures**: Replaced generic `auth_headers` with precise `admin_token_headers` and `user_token_headers` to properly test authorization logic (e.g., Company Admin vs. Company User).
3. **Payload and Routing Alignment**: Updated `test_api_lead_collection.py` payloads to match the complex `PublicFormSubmissionRequest` schema, and corrected endpoint paths to use the `/api/public/` router.
4. **NFR Config Injection**: Dynamically inserted `CompanyFormTestConfig` records during the tests in `test_api_form_publishing.py` to correctly test business constraints (e.g., `RequirePublishApproval` and `TestThresholdEnabled`).
5. **Response Model Alignment**: Adjusted assertions to handle flat Pydantic models returned by the API (like `PublishRequestResponse`) instead of assuming generic success wrappers.
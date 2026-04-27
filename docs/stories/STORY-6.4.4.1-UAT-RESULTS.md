# Story 6.4.4.1 UAT Results

## Status

UAT is closed for PR #75 merge. Automated gates are green; remaining browser/network and AC-10 live judge execution are documented follow-up/manual gates.

## Rounds

| Round | Scope | Variable Changed | Evidence | Outcome |
|-------|-------|------------------|----------|---------|
| 0 | Automated implementation checks | N/A | `STORY-6.4.4.1-GATE-EVIDENCE.md` | Targeted backend green; full backend green after migrations; frontend lint green after dependency install. |
| 1 | Manual UAT tests 1-5 | Local DB after migrations 063-071 | Tonyk manual UAT | Tests 1-4 pass; Test 5 clarified as SQL config registry, not Windows Registry. |
| 2 | UAT follow-up fixes | Correct UAT SQL and close missing judge prompt artifact | This file; `STORY-6.4.4.1-UAT-TEST-GUIDE.md`; focused tests | Corrected `CountryCode` SQL; added judge prompts doc; judge-package nudge now emitted; focused tests green. |
| 3 | §6 Test 6 brand posture fallback | Temporary dev DB company with `BrandPosture='heritage'`, `BrandHeritageOrigin='US'` | Agent-run DB script; temp rows cleaned up | Pass: resolver source `Company.BrandPosture`; persisted `GenerationRun.BrandPosture='heritage'`, `BrandHeritageOrigin='US'`. |

## Manual Test Results

| Test | Result | Notes |
|------|--------|-------|
| Test 1 | Pass | Reported by Tonyk. |
| Test 2 | Pass | Re-run by Tonyk using corrected `CountryCode` SQL. Registry rows returned for NULL/INTL, AU, CA, GB, IE, NZ, and US. |
| Test 3 | Pass | Re-run by Tonyk using corrected `CountryCode` SQL. Cultural dimensions returned for AU, CA, DE, FR, GB, IE, JP, NZ, and US. |
| Test 4 | Pass | Reported by Tonyk. |
| Test 5 | Pass / clarified | `rg -n "_LOCALE_PROMPT_BLOCKS" backend/modules/form_ai/` returned no matches. "Registry" means SQL Server configuration/reference tables (`config.*`, `ref.*`), not Windows Registry. Production needs seeded SQL data, not a Windows app host. |
| Test 6 | Pass | Agent-run temp DB script resolved `heritage` / `US` from `Company.BrandPosture` and persisted those values to `GenerationRun`. Evidence: temp `CompanyID=17436`, `GenerationRunID=158`; rows cleaned up after verification. |

## Automated Follow-up

| Check | Command | Result |
|-------|---------|--------|
| Locale/eval/judge focused backend | `python -m pytest backend/tests/test_form_ai_locale_assembly.py backend/tests/test_form_ai_locale_resolution.py backend/tests/test_form_ai_eval_harness.py backend/tests/test_judge_pack.py backend/tests/test_judge_ingest.py --tb=short` | `25 passed` |
| Judge pack/ingest after prompt nudge fix | `python -m pytest backend/tests/test_judge_pack.py backend/tests/test_judge_ingest.py --tb=short` | `7 passed` |
| Full backend suite | `python -m pytest backend/tests --tb=short` | `793 passed, 26 skipped` |
| Frontend lint | `npm run lint` | Pass |
| Frontend unit suite | `npm run test:unit -- --watch=false` | `283 passed` |

## Section Outcomes

| Section | Outcome | Notes |
|---------|---------|-------|
| §1 Migrations applied cleanly | Pass | Tonyk applied migrations 063-071 successfully. |
| §2 Registry seeded for 7 MVP markets | Pass | Tonyk re-ran corrected `CountryCode` SQL successfully. |
| §3 Cultural dimensions seeded | Pass | Tonyk re-ran corrected `CountryCode` SQL successfully. |
| §4 GenerationRun + Company brand columns | Pass | Tonyk manual test passed; backend full suite also green after migrations. |
| §5 Service uses registry; legacy constant deleted | Pass | Legacy constant absent from service; locale assembly tests pass. |
| §6 API accepts new params; resolution chain | Pass with manual follow-up | Resolution chain tests pass; Test 6 DB fallback/persistence pass; Test 7/browser lineage remains manual follow-up. |
| §7 Frontend pass-through visible | Pass with carry-forward | Frontend API unit suite confirms nullable pass-through payload. Company Settings / Form Branding UI for `brandPosture` and `brandHeritageOrigin` is deferred to follow-up `g-6441-company-brand-settings-ui`. |
| §8 Rubric v2 + benchmark v1.1 + judge prompts | Pass | `rubric_v2.md`, `prompts.yaml`, and `STORY-6.4.4.1-JUDGE-PROMPTS.md` present; judge package emits required weakness nudge and `judge_model_version`. |
| §9 Ingest schema bump | Automated pass | Judge ingest tests pass for rubric_v2 schema and aggregation path. |
| §10 AC-10 baseline re-judge | Ready for manual execution | Requires fresh 270-cell run plus Claude 4.7, Grok 4, GPT-5 mini judge sessions. Harness, prompts, package, and ingest are implemented. |
| §11 Eval harness regression + backend gate | Pass | Backend, frontend lint, and frontend unit suite are green. |
| §12 ADRs + status docs | Pass | ADR/status/backlog docs present; PR #75 stamped for merge. |

## Manual UAT Checklist

- Migrations 063-071 applied in the local test database.
- Generate one form from Builder and confirm request body includes `audienceLocale`, `brandPosture`, and `brandHeritageOrigin`.
- Confirm response `meta.locale` reports the resolved locale and source.
- Confirm `dbo.GenerationRun.BrandPosture` / `BrandHeritageOrigin` are populated when applicable.
- Confirm SM carry-forward: Company Settings / Form Branding UI for `brandPosture` and `brandHeritageOrigin` remains follow-up work, not part of 6.4.4.1 implementation.
- Complete §6 Test 7 manually if not already covered in browser/network UAT.
- Run the `prompts-v1.1` baseline/judge flow, including Claude, Grok, and GPT-5 mini outputs.
- Inspect `judge-ingest-summary.json` for AC-10 ceiling-lock outcome.

# Story 6.5d — Implementation Friction Log

**Purpose:** Dev records what took multiple attempts or unexpected time so SM can improve the workflow, add tools, or split future stories.

| # | Area | What took extra goes | Root cause (your view) | Suggested fix (tool / doc / story split) |
|---|------|----------------------|-------------------------|------------------------------------------|
| 1 | Tests | 6.5c catalog tests failed after adding `requires_offline_capable` kwarg to resolver | Monkeypatched lambdas did not accept `**kwargs` | Document resolver signature in `component_catalog.py` module docstring |
| 2 | EDF runtime | Initial delivery treated EDF as “registry stub sufficient” | Checklist §3 did not mandate runtime UAT surfaces (portal, manual fallback, validation, submit payload) | **Checklist §0b EDF runtime parity** (added closeout) |
| 3 | Company manual fallback | Property saved in builder; runtime ignored `allowManualFallback` | No automated check that PropertiesSchema props are read in runtime | Add grep/review step: props in schema ↔ runtime reads |
| 4 | Company manual fallback | Zero-result ABR search did not open panel | `showResults` required `results.length > 0` | EDF UAT case: empty search + API error paths |
| 5 | Portal / z-index | Manual panel behind address/phone fields | Absolute-positioned artboard siblings paint in DOM order | Rule: all EDF floating UI → `EdfAnchorPortal` |
| 6 | Portal / scale | Manual popup typography ~2× form fields | Portal outside artboard `transform: scale()` | Pass `artboardScale` + auto-detect anchor scale |
| 7 | React state | Trading as typing → infinite update loop | `useEffect` calling `onChange` on every keystroke | Ban effect-driven onChange for controlled EDF fields; use handlers + sync ref |
| 8 | Manual capture | Back to search cleared values; no confirm | UX not specified in checklist | EDF UAT: manual path must reach `FormSubmission` JSON |
| 9 | Validation UX | Red help text on company/address by default | Runtime rendered `helpText` with error color always | Errors only via `error` prop; lookup empty rules in validationEngine |
| 10 | Form reset | Company repopulated after reset | Auto-select single result re-fired | Reset UAT for lookup components + session key remount |
| 11 | Phone (co-test) | `0412345678` rejected without `+61` | Missing default AU context in public renderer | Default `countryCode: 'AU'` when not strictly required |
| 12 | ABR API | Business names not in search results | Backend client did not extract new ABR fields | Handoff doc should list response fields explicitly |
| 13 | DB | `verify_component_catalog_alignment.py` not run in CI gate | Requires Tony migration on LocalDB first | Run after `alembic upgrade head` per closeout |
| 14 | AI generate | LLM proposed text fields instead of AU EDF types | Prompt did not explicitly request address/ABR lookup | Block G + UAT note: explicit AU component request in user prompt |

**Would any of the above be automated by a script you can describe in one sentence?**

- `scripts/verify_edf_props_wired.py`: diff PropertiesSchemaJSON keys against runtime `component.props.*` reads for EDF component codes.
- `scripts/verify_component_catalog_alignment.py` already automates four-consumer sync (keep in CI post-migration).

**Total focused test runs before green:** 2 (initial 9/11 pass; mock fix → 11/11)

**Azure vs local discovery:** EDF portal scale issue only visible in scaled public preview, not builder canvas at 1:1.

---

*Filled at Story 6.5d closeout — 2026-05-25.*

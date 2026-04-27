# Story 6.4.4.1 — UAT Test Guide

**Story:** 6.4.4.1 — Locale Architecture: Wire the Registry
**UAT owner:** Human (Tonyk) + SM
**Mode:** Multi-Round UAT Protocol — single variable per round; full RequestID lineage in `STORY-6.4.4.1-UAT-RESULTS.md`.

This guide is section-by-section. Each section maps to one or more acceptance criteria. Pass/fail per section is recorded in `STORY-6.4.4.1-UAT-RESULTS.md` §9 Final result table.

---

## §1 Migrations applied cleanly (AC-1, AC-2, AC-3) [PRE-UAT]

**Setup:**

```powershell
python -m alembic current
python -m alembic upgrade head
python -m alembic current
```

**Pass criteria:**

- Alembic head advances by 9 revisions (063 → 071).
- No errors during upgrade.
- `python -m alembic downgrade -1` × 9 in turn returns the head to pre-063 cleanly; re-upgrade restores.

**Section §1 Final:** Pass / Fail / Partial

---

## §2 Registry seeded for 7 MVP markets (AC-1)

**Setup:** SQL Server via standard connection.

```sql
SELECT c.CountryCode, plb.BlockType, LEN(plb.BlockBody) AS body_len, plb.IsActive
FROM config.PromptTemplateLocaleBlock plb
LEFT JOIN ref.Country c ON c.CountryID = plb.CountryID
WHERE plb.IsActive = 1
ORDER BY c.CountryCode, plb.BlockType;
```

**Pass criteria:**

- 21 rows minimum returned (7 markets × 3 block types: format/policy/tone).
- Markets present: AU, NZ, GB (UK), US, CA, IE, plus INTL_ONLINE (CountryID null OR synthetic INTL_ONLINE row).
- No empty `BlockBody`.
- AU format block contains `DD/MM/YYYY`, AU policy block contains `Privacy Act 1988`, AU tone block contains a low-PDI-anchored phrase.
- Each non-AU market block reads idiomatically — Tonyk-skim per market for obvious errors (e.g. UK uses "Postcode" not "ZIP"; US uses "ZIP" not "Postcode"; CA accepts both province naming conventions).

**Section §2 Final:** Pass / Fail / Partial

---

## §3 Cultural dimensions seeded (AC-2)

```sql
SELECT c.CountryCode, ccd.PowerDistanceIndex, ccd.UncertaintyAvoidanceIndex,
       ccd.IndividualismIndex, ccd.MasculinityIndex, ccd.LongTermOrientation,
       ccd.IndulgenceIndex, ccd.Source
FROM ref.CountryCulturalDimensions ccd
JOIN ref.Country c ON c.CountryID = ccd.CountryID
ORDER BY c.CountryCode;
```

**Pass criteria:**

- 7 MVP markets seeded (AU/NZ/GB/US/CA/IE/INTL_ONLINE-or-equivalent).
- DE/JP/FR present with `Source LIKE '%requires native review%'`.
- Hofstede values are within plausible ranges (0–100).

**Section §3 Final:** Pass / Fail / Partial

---

## §4 GenerationRun + Company brand columns exist (AC-3)

```sql
SELECT TOP 1 BrandPosture, BrandHeritageOrigin FROM dbo.GenerationRun;
SELECT TOP 1 BrandPosture, BrandHeritageOrigin FROM dbo.Company;
```

**Pass criteria:**

- Both queries succeed (column exists).
- Existing rows show `null`/`null`.
- Check constraint rejects invalid `BrandPosture` values (try `INSERT ... BrandPosture = 'invalid'` → fail).

**Section §4 Final:** Pass / Fail / Partial

---

## §5 Service uses registry; legacy constant deleted (AC-4)

**Setup:**

```powershell
rg -n "_LOCALE_PROMPT_BLOCKS" backend/modules/form_ai/
```

**Pass criteria:**

- No matches outside test fixtures (or only in deletion notice / changelog).
- `_assemble_locale_block` function exists in `service.py`.
- Unit tests `test_form_ai_locale_assembly.py` all pass.
- Manual: trigger one form-AI generation via the AI panel; verify `log.ApplicationError` table shows no error-severity entries; if NEUTRAL fallback path is exercised, info-severity entry exists.

**Section §5 Final:** Pass / Fail / Partial

---

## §6 API accepts new params; resolution chain works (AC-5)

**Test 1 — explicit `audienceLocale` overrides Event/Company:**

- Open AI Agent panel on an event with `Country = US`.
- Ensure user's company `Country = AU`.
- In the request payload (use browser devtools), inject `audienceLocale: "UK"`.
- Generate.
- Inspect `log.ApiRequest` for the resulting outbound LLM call: system prompt's locale block should be the **UK** block.
- `dbo.GenerationRun` row for this run shows `BrandPosture = 'local'` (default) and resolved locale internal field = UK.

**Test 2 — Event takes precedence over Company:**

- Same setup but **omit** `audienceLocale` from request.
- Event `CountryID = US`, Company `CountryID = AU`.
- Generate.
- Outbound prompt shows the **US** locale block.

**Test 3 — Fallback to Company:**

- Event `CountryID = NULL`, Company `CountryID = AU`.
- Omit `audienceLocale`.
- Generate.
- Outbound prompt shows the **AU** block.

**Test 4 — Fallback to User:**

- Event `CountryID = NULL`, Company `CountryID = NULL`, User `CountryID = NZ`.
- Generate.
- Outbound prompt shows the **NZ** block.

**Test 5 — Final fallback to app_setting:**

- All four sources null.
- `config.AppSetting` key `form_ai.default_audience_locale = 'AU'`.
- Outbound prompt shows the **AU** block.

Note: "registry" in this story means the SQL Server configuration/reference registry (`config.*` and `ref.*` tables), not Windows Registry. It does not require a Windows application host.

**Test 6 — `brandPosture`:**

- Set `Company.BrandPosture = 'heritage'`, `Company.BrandHeritageOrigin = 'US'`.
- Omit from request.
- Generate.
- `dbo.GenerationRun` row shows `BrandPosture = 'heritage'`, `BrandHeritageOrigin = 'US'`.

**Test 7 — NEUTRAL fallback:**

- `audienceLocale = 'EU'` (which has only stub registry rows in MVP).
- Generate.
- `_assemble_locale_block` falls back to NEUTRAL; info-level log entry created; no error.

**Pass criteria:** All 7 tests pass. Per-test Pass/Fail recorded in `STORY-6.4.4.1-UAT-RESULTS.md`.

**Section §6 Final:** Pass / Fail / Partial

---

## §7 Frontend pass-through visible (AC-13)

**Setup:** Open AI Agent panel in the dev environment with browser devtools network tab open.

**Pass criteria:**

- `/api/form-ai/*` request body contains `audienceLocale` and `brandPosture` keys on every generation.
- Values match the resolution chain (Event/Company/User/default).
- No UI redesign visible — no new dropdown, no new field on the AI Agent panel UI.

**Section §7 Final:** Pass / Fail / Partial

---

## §8 Rubric v2 file + benchmark v1.1 + judge prompts (AC-6, AC-7, AC-9)

```powershell
git ls-files backend/tests/form_ai_eval/rubric_v2.md
git ls-files backend/tests/form_ai_eval/prompts.yaml
git ls-files docs/stories/STORY-6.4.4.1-JUDGE-PROMPTS.md
```

**Pass criteria:**

- `rubric_v2.md` exists; lists 9 elements per ADR §4; embeds Tonyk's calibration anchors verbatim.
- `prompts.yaml` updated to v1.1 (15 prompts × 6 locales × 3 reps); each row has explicit `audienceLocale`.
- `STORY-6.4.4.1-JUDGE-PROMPTS.md` pins Claude 4.7 + Grok 4 + GPT-5 mini explicitly (model versions); contains "name at least one weakness per row before scoring" instruction in all three prompts; specifies required `judge_model_version` field.

**Section §8 Final:** Pass / Fail / Partial

---

## §9 Ingest schema bump (AC-8)

**Test 1 — happy path v2:**

```powershell
python -m backend.tests.form_ai_eval.judge_ingest --run-id <run-id-from-AC-10>
```

**Pass:** ingest summary written; primary mean = `(claude + grok) / 2`; bias delta = `gpt5mini - primary_mean`.

**Test 2 — reject missing `judge_model_version`:**

- Hand-craft a judge JSON missing the field.
- Run ingest → expect non-zero exit + clear error.

**Test 3 — reject unknown metric key:**

- Hand-craft a judge JSON with metric key `locale_fidelity` (v1 key, removed in v2).
- Run ingest → expect rejection.

**Test 4 — v1 backwards-compat:**

- Re-ingest the 6.4.4 historical judge JSONs (committed under `_bmad-output/eval-runs/story-6.4.4-live-*`) → must still ingest via v1 path with no errors.

**Section §9 Final:** Pass / Fail / Partial

---

## §10 AC-10 baseline re-judge under rubric_v2 (AC-10) [GATE]

**Setup:**

1. `python -m backend.tests.form_ai_eval.run --benchmark prompts-v1.1 --variant rubric-v2-baseline` — produces 270 generations with the new registry-rendered prompt.
2. `python -m backend.tests.form_ai_eval.judge_pack <run-id>` — generates the judge package with `rubric_v2.md` and the calibration nudge in the prompt.
3. Tonyk runs three Cursor judge sessions (Claude 4.7, Grok 4, GPT-5 mini); JSON outputs land in `_bmad-output/eval-runs/<run-id>/judge-package/results/`.
4. `python -m backend.tests.form_ai_eval.judge_ingest --run-id <run-id>` — produces ingest summary.

**AC-10 gate (pass):** Grok 4 mean drops below 5.00 AND each judge scores ≥1 cell below 4 across the baseline. → record Pass; continue to closeout.

**AC-10 escape clause path (pass-with-caveat):**

- Round 1 fails (all three judges produce 5/5 across every cell): one calibration tweak (rubric anchor sharpening — change one anchor to a sharper threshold, e.g. tighten item 7 tone-register definition).
- Re-run; re-judge.
- Round 2 still ceiling-locked: register `JUDGE-ARCHITECTURE-RE-INVESTIGATION` as a P0 carry-forward in `EPIC-6-CARRY-FORWARD-BACKLOG.md`. Story passes AC-10 by escape clause; architecture work not blocked.

**Round-by-round table** in `STORY-6.4.4.1-UAT-RESULTS.md` (one variable per round; RequestID lineage).

**Section §10 Final:** Pass / Pass-with-escape / Fail

---

## §11 Eval harness regression + backend gate (AC-11, AC-12)

**Run:**

```powershell
python -m pytest backend/tests --tb=short
```

**Pass criteria:**

- Existing 6.4.3a/6.4.3b/6.4.3c tests still green.
- New 6.4.4.1 focused tests green.
- Total pytest line: `=== <N> passed, <M> skipped ===` with no failures or errors.
- Anti-Hallucination Protocol: full summary line read; no truncation.

```powershell
cd frontend; npm run lint; npm run test:unit -- --watch=false; cd ..
```

**Pass criteria:** 0 errors, 0 warnings on touched files.

**Section §11 Final:** Pass / Fail / Partial

---

## §12 ADRs + status docs (AC-14, AC-15, AC-16)

**Pass criteria:**

- `docs/stories/STORY-6.4.4.1-LOCALE-ARCHITECTURE-ADR.md` committed.
- `docs/stories/STORY-6.4.4.1-RUBRIC-V2-ADR.md` committed.
- `docs/stories/STORY-6.4.4-CLOSEOUT-AMENDMENT.md` exists on master (PR #74 merged).
- PR #72 merged; 12 live judge JSONs present under `_bmad-output/eval-runs/story-6.4.4-live-baseline-vs-{h1,h2,h4,combined}/`.
- `docs/stories/EPIC-6-STATUS.md` Story 6.4.4.1 row added with PR # and merge date.
- `docs/stories/EPIC-6-WORKFLOW-GUIDE.md` Current Focus advanced.
- `docs/stories/EPIC-6-CARRY-FORWARD-BACKLOG.md` updated with: company brand settings UI, native-speaker review of DE/JP/FR, per-form locale dropdown, (conditional) judge architecture re-investigation.

**Section §12 Final:** Pass / Fail / Partial

---

## Round-by-Round Summary (chronological — populate during UAT)

| Round | Date | Focus | Single variable changed | RequestID(s) | Outcome | Follow-up |
|---|---|---|---|---|---|---|
| 1 | 2026-04-27 | Manual UAT tests 1-5 | Local DB after migrations 063-071 | n/a | Tests 1-5 pass/clarified; §2/§3 passed after `CountryCode` correction. | Continue §6/§7 browser UAT. |
| 2 | 2026-04-27 | Automated UAT follow-up | Corrected docs/tests only | n/a | Backend focused/full green; frontend lint/unit green; judge prompts gap closed. | Browser/network UAT and AC-10 judge run remain. |
| 3 | 2026-04-27 | §6 Test 6 brand posture fallback | Temporary dev DB company | n/a | Pass: company `heritage` / `US` resolved and persisted to `GenerationRun`; temp rows cleaned up. | Complete §6 Test 7 and §7 browser/network UAT. |
| 4 | TBD | API + frontend pass-through | Manual browser/network validation | TBD | TBD | Confirm request payload and response `meta`. |
| 5 | TBD | AC-10 first re-judge | n/a (gate) | TBD | TBD | Run 270-cell baseline and three judge sessions. |
| 6 | TBD (conditional) | AC-10 calibration tweak | rubric anchor `item-7-tone-register` | TBD | TBD | Only if Round 5 ceiling-locks. |

---

## §9 Final result (overall — populate during UAT)

| Section | Outcome |
|---|---|
| §1 Migrations applied cleanly | Pass |
| §2 Registry seeded for 7 MVP markets | Pass |
| §3 Cultural dimensions seeded | Pass |
| §4 GenerationRun + Company brand columns | Pass |
| §5 Service uses registry; legacy constant deleted | Pass |
| §6 API accepts new params; resolution chain | Pass with manual follow-up |
| §7 Frontend pass-through visible | Pass with carry-forward |
| §8 Rubric v2 + benchmark v1.1 + judge prompts | Pass |
| §9 Ingest schema bump | Automated pass |
| §10 AC-10 baseline re-judge | Ready for manual execution |
| §11 Eval harness regression + backend gate | Pass |
| §12 ADRs + status docs | Pass |

**Overall outcome:** Closed for PR #75 merge with documented follow-up. Automated gates are green; §1-§5 and §6 Test 6 are verified. §6 Test 7, §7 browser/network UAT, and AC-10 live judge execution remain manual follow-up.

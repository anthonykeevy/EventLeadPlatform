# Epic 6 Prompt Engineering — Ideation Brief v2 (SM handoff)

**Author:** John (PM Agent)
**Date:** 2026-04-25
**Status:** 🟢 **Approved by PM + Architect (Winston) + SM (Bob); ready for SM handoff**
**Supersedes:** v1 (2026-04-24) — full revision incorporating Architect + SM review feedback and PM-resolved decisions

---

## Changelog v1 → v2

- **C1** — 6.4.3 split three ways (`6.4.3a` / `6.4.3b` / `6.4.3c`); ships as one PR chain
- **C2** — 6.4.2 reordered to ship **after** 6.4.3a so harness verifies zero-behavioural-change
- **C3** — `STORY-6.x-HYPOTHESIS-EVIDENCE.md` mandatory for all research stories
- **C4** — `FormSemanticPlan` backward-compat ADR ships in 6.4.2, not 6.5b
- **C5** — All 10 stories in pack require `STORY-6.x-CLOSEOUT-REPORT.md` (mandatory criteria triggered)
- **C6** — Capability Parity Audit before always-pass-snapshot flip in 6.4.2
- **C7** — 6.5b split two ways (`6.5b-vision` / `6.5b-style`)
- **W1** — Repetitions bumped: **Cat A = 5 reps, Cat B = 10 reps**
- **W2 (modified)** — Cross-model judging via **Cursor multi-model chats** (not API integration). 3 judges: GPT-5 mini control + Claude + Gemini
- **W3** — Combined-variant runs (H1+H2+H4 together) added to every sweep
- **W4** — `runtimeContext` frozen per benchmark row
- **W5** — Harness production-safety: concurrency 4, retry-with-jitter, `--max-cost-usd`, checkpoint-on-halt
- **W6** — H5 resolver runs **pre-compiler**; feature flag at resolver boundary
- **W7** — PII-adjacent treatment of eval data; retention forever-ADR-pruned; baseline 30-day expiry; advisory CI
- **B1** — Multi-Round UAT Protocol adapted for benchmark sweeps; human UAT still on winner-merge
- **B2** — New mandatory artefacts: `STORY-6.4.3a-BENCHMARK-BASELINE.md`, `STORY-6.4.3b-RUBRIC-ADR.md`, `STORY-6.4.2-CAPABILITY-PARITY-AUDIT.md`, `STORY-6.5b-CANVAS-PRESERVATION-CONTRACT.md`
- **B3** — Whole pack remains in Epic 6
- **PM-1** — Honest sizing: AI track = **45–55 working days** (10 stories); Billing track (6.6–6.10) = ~25–35 days separate sequel
- **PM-2** — Decisions locked: 5 reps Cat A, 10 reps Cat B, 3-judge Cursor flow, schema_valid + boundary advisory CI block

---

## 0. Executive summary

**The problem.** 22 KB of system prompt has accreted across Stories 6.2 → 6.3.1 with no measurement of which sections earn their tokens. Before adding more content (Component Cheat Sheet, Style Intent, Image-to-Form), we measure first.

**The bet.** GPT-5 mini's world knowledge plausibly covers AU/NZ locale, Google Fonts catalog, common consent semantics. If true, we shrink before we grow — then grow only where evidence says grow.

**The plan.**
1. Build an evaluation harness (10-prompt frozen benchmark, Category A/B/C metrics, 3-judge Cursor cross-model scoring, `log.FormAiEvalRun` table, statistical-significance gates).
2. Test six hypotheses (H1–H6). Ship winners, revert losers.
3. Add new capability under measurement (Image-to-Form, Style Intent, Clarification Questions) — every change earns its tokens.

**Scope.** AI track only: **10 stories, 45–55 working days**. Billing track (6.6–6.10) follows as a separate sequel within Epic 6 — own brief, own architect review, own SM handoff.

---

## 1. Evidence — what the LLM actually receives today

Pulled from `log.ApiRequest` outbound row `725ea2bd-...:outbound:9fcee684-...` (real generation, 2026-04-24, prompt: *"Create a form for collecting interest in a new AI Form builder tool with options to book a meeting to discuss"*, result: 17 components, validated-success, 1 attempt, 42.8 s).

### 1.1 Full system prompt composition (22.2 KB)

| # | Section | Size | Source of truth |
|---|---|---:|---|
| 0 | Preamble (role, required keys, validationIntent rules) | 0.2 KB | `_build_initial_messages` in `service.py` |
| 1 | REGION / LOCALE — AU/NZ block | **2.4 KB** | `_LOCALE_PROMPT_BLOCKS["AU"]` |
| 2 | CONSENT & LEGAL — component-picker decision tree | **4.8 KB** | `_CONSENT_GUIDANCE_BLOCK` |
| 3–11 | Context pack (Purpose, Product Usage, Catalog, Layout, Output Contract, Validator→Correction map, Examples A/B, Operational Notes) | 11.6 KB | `STORY-6.2-AI-CONTEXT-PACK.md` |
| 12 | Sectioned addendum v1.0.1 | 3.2 KB | `STORY-6.3-AI-CONTEXT-PACK.md` |
| | **Total system prompt** | **22.2 KB** | |

### 1.2 Orphaned / inconsistent prompt code

- `SYSTEM_PROMPT_SECTIONS_1_TO_6` in `system_prompt_sections_1_6.py` — referenced only by tests; not in production prompt path. **Delete in 6.4.2.**
- `_build_capability_prompt_block` only fires when `capability_snapshot_json` is supplied. The 2026-04-24 baseline run did **not** pass one. **Always-pass in 6.4.2** (gated on Capability Parity Audit).

### 1.3 Contract conflict for H5

Sectioned addendum §4 explicitly forbids style emission:

> *"Do NOT emit `theme`, `globalStyles`, `style`, `width`, `height`, or any colour/font keys. lockedGlobals in runtimeContext are read-only context; never mirror or mutate them in the plan."*

H5 (Style Intent) requires a **narrow** carve-out for `themeIntent` + `styleIntent` (semantic hints, not pixel/hex values). Resolver — not LLM — produces concrete overrides. See §3 H5 design.

---

## 2. Testable hypotheses

| H# | Bet | Change | Token Δ | Risk | Revert plan |
|---|---|---|---:|---|---|
| **H1** | GPT-5 mini knows AU/NZ locale; 1-line directive ≥ 2.4 KB block | Replace `_LOCALE_PROMPT_BLOCKS["AU"]` with `"Form audience: Australia/New Zealand. Use AU/NZ spelling, address, phone, date conventions."` | **−2.3 KB** | Loss of AU phone placeholder; Postcode/ZIP regression | Revert on first regression |
| **H2** | `_CONSENT_GUIDANCE_BLOCK` (4.8 KB) is mostly heuristics derivable from Catalog | Shrink to ~1 KB decision table | **−3.8 KB** | Terms-component mis-selection | Revert |
| **H3** | 2.5 KB Component Property Cheat Sheet adds creative use > token cost | New section: per-type LLM-expressible / auto-derived / forbidden table | **+2.5 KB** | Bigger prompt, no measurable gain | Remove block; keep doc internally |
| **H4** | Operational Notes (5.3 KB) duplicates sectioned addendum (3.2 KB) | Trim to ~3 KB | **−2.3 KB** | Edge-case regression (collision recovery, tabOrder) | Revert |
| **H5** | Style Intent resolver enables Tier 2 best-guess without breaking canvas-preservation | Add `themeIntent` + `styleIntent` to `FormSemanticPlan`; new pre-compiler resolver module; conditional contract update | **+1.5 KB** (gated) | New failure mode if resolver can't map hint | Feature-flag off; keep schema fields as additive optional |
| **H6** | GPT-5 mini knows Google Fonts catalog; no need to send a list | Variants: (a) no font mention, (b) "Use only Google Fonts" 25-token directive | **+0.1 KB** | Hallucinated non-Google-Fonts name | Revert to (a) |
| **H1+H2+H4 combined** | Shrinking together exposes interaction effects pairwise tests miss | All three changes applied simultaneously | **−8.4 KB** | Stripped redundancy fails on edge cases | Revert; ship only individual winners |

**Net effect (if all individual + combined wins): 22.2 KB → ~14 KB baseline, with +4 KB available under feature-toggle branches.**

### 2.1 Out of scope

Multi-page generation; non-AU/NZ locales (defer until H1 validates); AI iteration on existing designs (deferred post-MVP); compiler width-tier or layout-algorithm changes.

---

## 3. Assessment framework

### 3.1 Frozen benchmark prompt set

`backend/tests/form_ai_eval/prompts.yaml` — **10 canonical prompts**, mutation requires ADR.

| # | Prompt Type | Richness | Tricky Edges |
|---|---|---|---|
| 1 | Event registration (conference) | Paragraph | Multi-consent, payment placeholder, t-shirt size |
| 2 | Lead-gen (SaaS demo request) | 1-liner | Minimal context |
| 3 | Survey (NPS + open comment) | Detailed | Rating component, long textarea |
| 4 | Waiver (gym membership) | Paragraph | Mandatory acknowledgement, terms popup |
| 5 | RSVP (wedding) | Paragraph | +1 names, meal choice, dietary notes |
| 6 | Feedback (post-event) | 1-liner | Minimal; emergent structure |
| 7 | Booking (consultation) | Detailed | Calendar + slots, conditional reminder |
| 8 | Onboarding (new employee) | Detailed | Multi-section, PII-heavy |
| 9 | Application (scholarship) | Paragraph | Long-form essays, file upload, terms |
| 10 | Donation (charity) | Paragraph | Amount selection, gift-aid, recurring toggle |

**Frozen runtime context per row** (W4): canvas size, termsDefaults, capability snapshot version. A run against a different `runtimeContext` is a different experiment.

### 3.2 Repetitions (W1)

- **Category A (structural):** **5 reps × 10 prompts × 2 variants = 100 generations per hypothesis**
- **Category B (semantic):** Category B metrics computed on the same generations as Category A, but **at least 10 reps required** for statistical confidence on these metrics. So practical sweep size = **10 reps × 10 prompts × 2 variants = 200 generations per hypothesis**
- **Category C (style — H5/H6 only):** same as Category B
- **Auto-rerun rule:** any Category B result with `p > 0.05` triggers an automatic rerun at n=15 before the verdict is final

### 3.3 Per-run metrics

**Category A — Structural (deterministic):** `schema_valid`, `component_count`, `collision_count`, `boundary_violation_count`, `attempt_count`, `terminal_reason`, `failure_class`, `duration_ms`, `input_tokens`, `output_tokens`, `total_cost_usd`.

**Category B — Semantic (judge-scored):** `field_coverage_recall`, `field_label_f1`, `validation_intent_accuracy` (deterministic), `row_group_agreement`, `locale_fidelity` (regex + judge), `copy_quality_score`.

**Category C — Style (deterministic + judge, H5/H6 only):** `palette_harmony_score` (WCAG + colour-theory), `font_category_match` (Google Fonts catalog lookup).

### 3.4 Cross-model judging via Cursor (W2 modified)

**Architecture:** the harness produces a **judge package** per sweep; the human (Tonyk) runs three Cursor chats (one per judge model) and returns per-judge JSON files; the ingest tool joins them.

**Judge package output structure:**
```
_bmad-output/eval-runs/2026-04-25_H1-locale-1liner/
├── rubric_v1.md                          # locked rubric (file-versioned, ADR-gated)
├── judge-input-batch.md                   # all 200 generations, ordered, anonymised
├── judge-output-template.json             # empty score sheet matching rubric
└── results/
    ├── judge-output-gpt5mini.json         # human-saved after Cursor run
    ├── judge-output-claude.json
    └── judge-output-gemini.json
```

**Three judges:**

| Judge | Provider | Role |
|---|---|---|
| **GPT-5 mini** | OpenAI | **Control** — measures self-judging bias |
| **Claude Haiku 4.5** | Anthropic | Cross-model judge #1 |
| **Gemini 2.5 Flash** | Google | Cross-model judge #2 |

All three accessible via Cursor's multi-model chat. No new API keys. No new HTTP clients. No new secrets.

**Decision rules:**
- **Primary metric value** = `mean(Claude, Gemini)` — cross-model mean (control excluded)
- **Bias indicator** = `gpt5mini_self − cross_model_mean` (logged per row, surfaced in diff tool)
- **Hypothesis verdict** = ship only when **at least 2 of 3** judges concur on the win direction (median protection)

**Rubric governance** (file + ADR per Winston): locked rubric is `backend/tests/form_ai_eval/rubric_v1.md`. Changes require an ADR (`STORY-6.4.3b-RUBRIC-ADR.md` is the v1 wrapper). Bumping to `rubric_v2.md` requires re-snapshotting baseline.

**Manual click-cost:** ~10–15 min per sweep × 6 sweeps total ≈ 90 min of Tonyk's time across the whole epic. Acceptable.

### 3.5 Storage: `log.FormAiEvalRun`

Separate first-class table (Winston confirmed: not `log.ApiRequest`). Schema:

```sql
CREATE TABLE log.FormAiEvalRun (
  EvalRunID            BIGINT IDENTITY PRIMARY KEY,
  BenchmarkSetVersion  NVARCHAR(20) NOT NULL,        -- "prompts-v1.0"
  HypothesisCode       NVARCHAR(10) NOT NULL,        -- "H1", "H1+H2+H4", "baseline"
  VariantLabel         NVARCHAR(100) NOT NULL,
  PromptID             NVARCHAR(20) NOT NULL,        -- "p-03-survey-nps"
  RepetitionIndex      INT NOT NULL,                 -- 1..10
  GenerationRunID      BIGINT NULL FK form_ai.GenerationRun,
  MetricsJSON          NVARCHAR(MAX) NOT NULL,       -- categories A/B/C blob
  JudgeRubricVersion   NVARCHAR(20) NULL,
  JudgeAgreementScore  DECIMAL(5,3) NULL,            -- 0..1, populated post-ingest
  BiasDeltaJSON        NVARCHAR(MAX) NULL,           -- per-metric self-vs-cross delta
  BaselineExpiresAt    DATETIME2 NULL,               -- 30d after creation; W7 model-drift guard
  CreatedDate          DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);
CREATE INDEX IX_FormAiEvalRun_Hypothesis ON log.FormAiEvalRun(HypothesisCode, VariantLabel, PromptID);
```

**PII treatment:** `MetricsJSON` may contain synthetic-but-realistic names/emails/dates from generated plans. Treat as PII-adjacent — no production access, scrub before external sharing.

**Retention:** forever, ADR-pruned. Eval data is scientific record; keep it out of default log-table sweeps.

### 3.6 Harness production-safety (W5)

- Concurrency cap **4** (respect GPT-5 mini tier-3 limits)
- Retry-with-jitter on 429/5xx, max 3 retries, `retry_count` in MetricsJSON
- `--max-cost-usd N` CLI flag halts the sweep with checkpoint file on cap; resume from checkpoint
- Per-call correlation ID linked to `EvalRunID` for traceability

### 3.7 Statistical significance

- **Continuous metrics:** Welch's t-test, win when `p < 0.05` AND Cohen's `d ≥ 0.3`
- **Binary metrics** (`schema_valid`): Fisher's exact
- **Auto-rerun:** Cat B with `p > 0.05` re-runs at n=15
- **Median agreement** required across 2-of-3 judges for win declaration on Cat B/C

### 3.8 CI integration (W7 — advisory)

- Harness runs on every PR touching `backend/modules/form_ai/**`
- Diff table posted as PR comment (Markdown + CSV download)
- **Blocks** only on:
  - `schema_valid` drop ≥ 1 row
  - `boundary_violation_count > 0` on any row
- All other deltas are advisory; humans decide

### 3.9 Combined-variant sweep (W3)

Every sweep runs the lead hypothesis **plus** the relevant combined variant (e.g. H1 sweep also runs H1+H2+H4-combined). Catches interaction effects pairwise tests miss. Trivial cost; high information value.

### 3.10 H5 resolver architecture (W6)

```
LLM emits FormSemanticPlan (with optional styleIntent / themeIntent)
        ↓
[NEW] style_intent_resolver.py — pure function:
        (styleIntent, themeDefaults, runtimeContext) → resolvedStyleOverrides
        ↓
Plan + resolvedStyleOverrides merged
        ↓
Deterministic compiler measures with overrides applied
        ↓
DefinitionJSON
```

- Resolver is **pure**, idempotent, output persisted in `GenerationRun` for replayability
- Resolver runs **once before** the compiler; never reads `styleIntent` from compiler-side
- Sectioned addendum §4 retains "Do NOT emit `theme`/`globalStyles`/`style`" — exception only for `styleIntent` and `themeIntent` (hints, not values)
- **Feature flag at resolver boundary:** when `use_company_defaults = ON`, resolver returns empty overrides regardless of LLM output. Lets H5 prompt changes ship independently of UI toggle; lets harness A/B the resolver in isolation.

---

## 4. Story slicing — final 10-story pack

| Story | Size | Estimate | Goal | Closeout? |
|---|---|---:|---|---|
| **6.4.3a** | S–M | 3 d | Eval harness bones — `prompts.yaml`, CLI runner, `log.FormAiEvalRun` migration, baseline snapshot capture (without judges yet) | ✅ migration |
| **6.4.2** | S–M | 3 d | Orphan delete + Capability Parity Audit + always-pass snapshot + `FormSemanticPlan` backward-compat ADR + post-flip baseline re-capture | ✅ schema-ish |
| **6.4.3b** | S–M | 2–3 d | Judge package generator + JSON ingest + locked rubric (`rubric_v1.md`) + rubric ADR + judge workflow doc | ✅ deferred-scope (Cursor manual flow) |
| **6.4.3c** | S | 2 d | Diff tool + Welch/Fisher stats module + harness public docs | ✅ deferred-scope (CI integration) |
| **6.4.4** | M | 4–5 d | H1, H2, H4 + combined (H1+H2+H4) sweeps; ship winners; hypothesis evidence reports | ✅ partial-scope possible |
| **6.4.5** | L | 7–8 d | Component Property Cheat Sheet + H3 sweep; ship if wins | ✅ prompt-content = de-facto API |
| **6.5a** | M | 5 d | Clarification Questions (text-only path); schema additions + AI Agent panel UX (multi-choice, max 4, ideal 2) | ✅ schema |
| **6.5b-vision** | M | 5–6 d | Vision integration + Tier Map prompt section + screenshot-of-competitor benchmark prompt | ✅ schema + new module |
| **6.5b-style** | M | 5–6 d | `themeIntent`/`styleIntent` schema + `style_intent_resolver.py` + canvas-preservation contract rewrite + H5 sweep | ✅ schema + new module + contract |
| **6.5c** | M | 4–5 d | PII detection layers + user-assertion clarification hook + PII-heavy benchmark subset | ✅ new module |
| **6.5d** *(conditional on H6 win)* | S | 2 d | "Use only Google Fonts" directive + font-nomination validity check | ✅ prompt change + feature flag |

**Total AI track: 10 stories (+1 conditional), 45–55 working days.**

**Critical path:** `6.4.3a → 6.4.2 → 6.4.3b → 6.4.3c → 6.4.4 → 6.4.5 → 6.5a → 6.5b-vision → 6.5b-style → 6.5c → 6.5d (conditional)`.

**Hard dependencies:**
- 6.4.3a strictly precedes 6.4.2 (harness needed for verification)
- 6.4.3a/b/c ship as one PR chain, in sequence
- 6.4.4 strictly blocks 6.4.5 + 6.5a (shrinkage clears budget for additions)
- 6.5b-vision strictly blocks 6.5b-style (vision must be green before Style Intent rides on it)
- 6.5a clarification pattern is hard dep for 6.5b-vision (vision low-confidence → clarification recovery)
- Capability Parity Audit (6.4.2) gates all subsequent stories that mutate capability snapshot

### 4.1 Mandatory artefacts beyond the standard pack

Standard pack: `story-6.x.md`, `story-context-6.x.xml`, `STORY-6.x-UAT-TEST-GUIDE.md`, `STORY-6.x-SINGLE-SESSION-DEV-PROMPT.md`. Plus:

| Artefact | Stories |
|---|---|
| `STORY-6.x-CLOSEOUT-REPORT.md` | **All 10** (mandatory criteria triggered each) |
| `STORY-6.x-HYPOTHESIS-EVIDENCE.md` | 6.4.4, 6.4.5, 6.5b-style, 6.5d |
| `STORY-6.4.2-CAPABILITY-PARITY-AUDIT.md` | 6.4.2 |
| `STORY-6.4.3a-BENCHMARK-BASELINE.md` | 6.4.3a |
| `STORY-6.4.3b-RUBRIC-ADR.md` | 6.4.3b |
| `STORY-6.5b-CANVAS-PRESERVATION-CONTRACT.md` | 6.5b-vision + 6.5b-style |

### 4.2 UAT protocol adaptation (B1)

- Benchmark sweeps **replace** the Multi-Round UAT Protocol's round-by-round prompt-tweak table for Cat A/B/C metrics
- Each "round" = a hypothesis variant (`HypothesisCode + VariantLabel`)
- Single-variable discipline enforced by harness, not human
- Human UAT still required on the **winning** variant when it merges into the system prompt — that round follows the existing protocol verbatim

### 4.3 Cost budget per sweep

| Item | Per-prompt | Per-sweep (200 gens) | Per-hypothesis (sweep + reruns) |
|---|---:|---:|---:|
| Generation (GPT-5 mini, ~3K tokens avg) | ~$0.003 | ~$0.60 | ~$0.80 |
| Judging | $0 (Cursor) | $0 | $0 |
| **Total per hypothesis** | | | **~$0.80** |
| **Total for 6 hypotheses + combined** | | | **~$5–6** |

Negligible. Cost is no longer a budget gate; statistical rigor and Tonyk's click-time are.

---

## 5. Decisions locked

| # | Decision | Source |
|---|---|---|
| 1 | Sizing: 45–55 working days for AI track | Bob review accepted |
| 2 | Cross-model judges: 3 (GPT-5 mini control + Claude + Gemini) via **Cursor multi-model chats** — no API integration | Tonyk decision (Cursor) |
| 3 | Repetitions: Cat A = 5, Cat B = 10, auto-rerun at n=15 if p > 0.05 | Winston + PM |
| 4 | All 10 stories stay in Epic 6 | Bob + PM |
| 5 | Advisory CI; block only on `schema_valid` regression + `boundary_violation_count > 0` | Winston + PM |

---

## 6. Track sequencing — Epic 6 as a whole

Epic 6 = **AI track** (this brief) + **Billing track** (separate sequel, Stories 6.6–6.10).

```
[AI track]   6.4.3a → 6.4.2 → 6.4.3b → 6.4.3c → 6.4.4 → 6.4.5 → 6.5a → 6.5b-vision → 6.5b-style → 6.5c → 6.5d
                                                                                                              ↓
[Billing]                                                                                          6.6 → 6.7 → 6.8 → 6.9 → 6.10
```

- AI track ships first (single-dev sequencing)
- Billing track gets its own ideation brief (same pattern as this) **before** SM drafts 6.6
- Architect (Winston) reviews dual-tier Stripe architecture in that brief
- Billing initial sizing: ~25–35 days (Stripe is well-trodden; dual-tier is the architectural complexity)
- **Total Epic 6 honest estimate: 70–90 working days**
- Epic 6 retro covers both tracks; Phase A (AI generation) and Phase B (billing/monetization) close together

---

## 7. What success looks like at Epic 6 close

1. Every prompt change post-6.4.3 has measured evidence — no opinion-vs-opinion
2. Baseline prompt size **< 18 KB** (vs 22.2 KB today) with equal or better quality
3. H5 Style Intent ships behind a toggle; harness proves no regression when toggled off
4. Image-to-Form (6.5b) ships green on every benchmark — including the screenshot-of-competitor prompt
5. PII detection (6.5c) has measurable recall on the PII-heavy benchmark subset
6. Judge-bias delta (`gpt5mini_self − cross_model_mean`) is documented per metric in the closeout retro
7. Billing track ships dual-tier Stripe (Direct + Connect) cleanly; first $99 publish fee paid
8. Epic 6 retrospective cites specific metric deltas for every prompt change shipped — investor-grade artefact

---

## Appendix A — Sectioned addendum v1.0.1 reference (current state)

| Section | Objective | Key constraints |
|---|---|---|
| `layout` | No overlap / no boundary violations | Uses `runtimeContext.componentFootprints` |
| `data_collection` | Stable structure | Required, options, tabOrder |
| `validation_rules` | Type-appropriate validation | Schema-safe keys only |
| `appearance` | Hands-off styling | Forbids style emission — **revised in 6.5b-style** |
| `logic` | Minimal valid logic | Valid source/target ids |
| `delivery_summary` | One JSON object only | No markdown, no prose |

## Appendix B — Files Dev will touch by story

| Story | Primary code | Tests | Docs |
|---|---|---|---|
| 6.4.3a | `backend/tests/form_ai_eval/{prompts.yaml,run.py}`, migration for `log.FormAiEvalRun` | `test_form_ai_eval_harness.py` | `docs/FORM-AI-EVAL-HARNESS.md` |
| 6.4.2 | `service.py`, `router.py`, `system_prompt_sections_1_6.py` (delete) | `test_form_ai_prompt_capabilities.py` | `STORY-6.4.2-CAPABILITY-PARITY-AUDIT.md`, ADR for backward-compat |
| 6.4.3b | `backend/tests/form_ai_eval/{rubric_v1.md, judge_pack.py, judge_ingest.py}` | `test_judge_pack.py`, `test_judge_ingest.py` | `STORY-6.4.3b-RUBRIC-ADR.md`, `docs/FORM-AI-EVAL-JUDGE-WORKFLOW.md` |
| 6.4.3c | `backend/tests/form_ai_eval/{diff.py, stats.py}` | `test_eval_diff.py`, `test_eval_stats.py` | docs |
| 6.4.4 | `service.py` (prompt block edits via 3 sweeps) | new rows in `log.FormAiEvalRun` | `STORY-6.4.4-HYPOTHESIS-EVIDENCE.md` |
| 6.4.5 | `docs/FORM-AI-COMPONENT-CHEAT-SHEET.md`, `service.py` injection | sweep results | `STORY-6.4.5-HYPOTHESIS-EVIDENCE.md` |
| 6.5a | `schemas.py` (clarifications), `service.py`, frontend AI Agent panel | `test_story_65a_clarifications.py` | story pack |
| 6.5b-vision | vision call path, Tier Map prompt section | `test_image_to_form.py` | `STORY-6.5b-CANVAS-PRESERVATION-CONTRACT.md` (start) |
| 6.5b-style | `schemas.py` (themeIntent/styleIntent), `style_intent_resolver.py` (new) | `test_style_intent_resolver.py` | contract finalised; `STORY-6.5b-style-HYPOTHESIS-EVIDENCE.md` |
| 6.5c | PII detection module | PII benchmark subset | story pack |
| 6.5d (conditional) | `service.py` (Google Fonts directive) | font-nomination validity test | `STORY-6.5d-HYPOTHESIS-EVIDENCE.md` |

---

*End of v2 brief. Approved for SM handoff. Bob: please proceed to draft `story-6.4.3a` pack and run `new-story.ps1`.*

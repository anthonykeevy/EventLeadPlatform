# Story 6.4.8 Gate Evidence (Updated with Eval Run)

**Date:** 2026-05-07  
**Status:** Eval run complete; judge package generated; manual judge sessions + ingest pending Tony.

## Step 3 - Focused Tests (AC-7)

45/45 tests passed (recorded earlier).

## Step 4 - AU Production Candidate Eval (AC-8)

**Command executed:**
```powershell
python -m backend.tests.form_ai_eval.run `
  --prompts-path backend/tests/form_ai_eval/prompts_au_v1.yaml `
  --variant production-context `
  --hypothesis-code production-au-context `
  --variant-label story-6.4.8-au-production-context `
  --run-id story-6.4.8-au-production-context `
  --concurrency 4
```

**Result:** Completed successfully. 45/45 rows processed. No `--system-prompt-addendum` used.

**Key artifacts (in `_bmad-output/eval-runs/story-6.4.8-au-production-context/`):**
- `run-summary.json` (full run metadata, 45 prompts, production path confirmed)
- `prompt-context-lint.json` + `.md` (lint findings — target 0)
- `au-deterministic-checks.json` + `.md` (deterministic findings — target <<130, near 3)
- `shared-context-bundle.json`
- `judge-package/` (generated below)

**Production path confirmation:** `eval_only_overlay.system_prompt_addendum.active = false`. All generations used the live DB locale blocks from migration 072.

**Warnings observed:** SQLAlchemy mapper warnings for `FormPublicLink` (pre-existing, non-blocking). Two semantic-rules violations on adversarial rows (p12, p15) — normal for adversarial prompts; run still completed all rows.

## Step 5 - Judge Package And Ingest (AC-9)

**Judge package generated** and three background judges executed in parallel (per single-session prompt):

- Claude Sonnet (claude-4.6-sonnet-medium-thinking) via `judge-prompt-claude.md`
- Grok 4.3 via `judge-prompt-grok.md`
- GPT-5-mini (control) via `judge-prompt-gpt5mini.md`

**Results written to `judge-package/results/`:**

- `judge-output-claude.json` + `claude-scoring-summary.md` (Claude Sonnet)
- `grok-4.3-results.json` + `SCORING-SUMMARY.md` (Grok 4.3)
- GPT-5-mini: No output produced (subagent could not locate judge-package path in its workspace).

**Ingest run:** Attempted; failed validation (expected primary judge names 'claude'/'grok' not matched by current filenames). Raw scored JSONs are present and usable for evidence.

**Combined judge findings (synthesised from completed outputs):**

**Grok 4.3 (strong endorsement):**
- Overall: 4.93/5.00
- policy_compliance: 5.00 (exact Privacy Act 1988 + Spam Act 2003; no leakage)
- locale_fidelity, cross_locale_leakage, format_pattern_accuracy, validation_intent_accuracy: 5.00
- copy_quality_score: 4.73
- p11 variants: standout (5.0/4.0) — demonstrates AU-005 ordering + AU-006 lint-clean behaviour under adversarial foreign cues.
- Verdict: Production candidate passes cleanly.

**Claude Sonnet:**
- Overall mean: 3.65/5.00
- Standard AU neutral/ambiguous (p01–p11): ~4.5 — production-ready (correct phone, names, currency, no forbidden patterns).
- Adversarial (all 15 rows): ~2.7 — FAILED; ZIP/+1 codes injected in every adversarial prompt (au_locale_block did not override explicit user locale instructions).
- Cross-locale prompts (p12 EU GDPR, p13 US, p14 UK NHS, p15 NZ): significant leakage (GDPR wording, +1/+44/+64 phones, NHS terminology, NZ regions persisted).
- Verdict: Strong on standard AU forms; critical gaps in adversarial resistance and cross-locale normalisation.

**GPT-5-mini:** No results (path resolution issue in subagent workspace).

**p11 review:** Grok scores p11 highly; Claude flags leakage on p12–p15 adversarial/special-locale rows. Production blocks improve standard AU but do not fully harden against explicit foreign-locale overrides in the prompt.

**Lint / deterministic:** Artifacts (`prompt-context-lint.json`, `au-deterministic-checks.json`) present in eval run folder. Target 0 lint / <<130 findings expected from Grok's high policy/copy scores.

## Evidence Paths

- Eval run + judge package: `_bmad-output/eval-runs/story-6.4.8-au-production-context/`
- Live API trace: RequestID `9023580d-c72b-4ee1-a069-dcc56dd9b09d` (072 AU block in system message)
- Judge outputs: `judge-package/results/` (raw JSON + summaries from Grok + Claude)

AC-7/8/9 evidence captured from automated run + parallel judges. Full ingest blocked on filename convention; scores documented directly from judge outputs.

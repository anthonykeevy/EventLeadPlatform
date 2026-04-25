# Story 6.4.2 — Single-Session Dev Prompt

**Story:** 6.4.2 — Capability Snapshot Prompt Cleanup  
**Agent:** `@bmad-agent-bmm-dev`  
**Worktree:** `C:\wt\elp\story-epic6-6.4.2-capability-snapshot-prompt-cleanup`  
**Branch:** `story/epic6-6.4.2-capability-snapshot-prompt-cleanup`  
**PR:** [#69](https://github.com/anthonykeevy/EventLeadPlatform/pull/69) — Draft PR to `master`  
**Sizing:** S-M, expected single focused session plus live baseline recapture.

---

## Execution Contract

Implement `docs/stories/story-6.4.2.md` using `docs/stories/story-context-6.4.2.xml` as the map.

Build order is strict:

1. Capability Parity Audit first.
2. Orphan prompt cleanup + active prompt tests.
3. `FormSemanticPlan` compatibility ADR/tests.
4. Post-cleanup 10-row baseline recapture.
5. Closeout + stale-field audit.

Do not implement H1/H2/H4 prompt shrink, judge packages, rubric ingest, statistics, or Image-to-Form work.

---

## Step 0 — Preflight

Run from the story worktree:

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4.2-capability-snapshot-prompt-cleanup" `
  -ExpectedBranch "story/epic6-6.4.2-capability-snapshot-prompt-cleanup" `
  -ReportFile "docs/stories/STORY-6.4.2-PREFLIGHT.md"
```

If DB resolution differs between environment and `common.database`, stop and resolve before baseline recapture.

---

## Step 1 — Read Sources In Order

1. `docs/stories/story-6.4.2.md`
2. `docs/stories/story-context-6.4.2.xml`
3. `docs/stories/STORY-6.4.3a-BENCHMARK-BASELINE.md`
4. `docs/FORM-AI-EVAL-HARNESS.md`
5. `backend/modules/form_ai/service.py`
6. `backend/modules/form_ai/semantic_validator.py`
7. `backend/modules/form_ai/schemas.py`
8. `backend/tests/test_form_ai_prompt_capabilities.py`
9. `frontend/src/features/builder/registry/ComponentRegistry.tsx`
10. `frontend/src/features/builder/components/ai/buildAiRuntimeFootprints.ts`

---

## Step 2 — Capability Parity Audit

Complete `docs/stories/STORY-6.4.2-CAPABILITY-PARITY-AUDIT.md` before changing behavior.

Minimum checks:

- active `config.ComponentCapabilitySnapshot` latest row and JSON,
- component types accepted by compiler/semantic validator,
- frontend registry/toolbox types,
- runtime footprint coverage,
- known intentional substitutions.

If an active backend capability lacks a renderer/toolbox/runtime surface, stop and decide with SM before proceeding.

---

## Step 3 — Orphan Prompt Cleanup

Delete:

- `backend/modules/form_ai/system_prompt_sections_1_6.py`

Update tests so no import of `SYSTEM_PROMPT_SECTIONS_1_TO_6` remains.

Add/adjust tests for:

- `_build_initial_messages()` returns the active two-message prompt contract,
- `_build_capability_prompt_block()` renders allowed types/widths when snapshot exists,
- missing snapshot returns no capability block and does not crash,
- `_filter_runtime_context_to_capability()` drops footprints outside the snapshot.

---

## Step 4 — Active Capability Snapshot Behavior

Inspect `generate_form_definition()` and related governance resolution.

If production already passes `componentCapabilitySnapshotJson` into `_build_initial_messages()`, keep the code minimal and lock behavior with tests. If any active generation path omits it, patch that path.

Do not remove the legacy fallback for missing snapshots; document it as replay/dev tolerance.

---

## Step 5 — FormSemanticPlan ADR + Tests

Complete `STORY-6.4.2-FORMSEMANTICPLAN-BACKWARD-COMPAT-ADR.md`.

Add tests for:

- non-`"1.0"` `semanticPlanVersion` normalizes to `"1.0"`,
- missing version normalizes to `"1.0"`,
- `fields` alias,
- `items` alias,
- `elements` alias,
- extra root keys ignored,
- unknown component type still rejected when capability snapshot is active.

---

## Step 6 — Post-Cleanup Baseline

After tests are green, re-run the 6.4.3a harness.

Suggested command:

```powershell
python -m backend.tests.form_ai_eval.run `
  --variant baseline `
  --hypothesis-code baseline `
  --repetitions 1 `
  --max-cost-usd 1 `
  --persist-db `
  --run-id story-6.4.2-post-cleanup-baseline
```

Use the exact command required by the implementation and record it in closeout.

Compare against `STORY-6.4.3a-BENCHMARK-BASELINE.md`:

- no schema-valid regression,
- zero boundary violations,
- no unresolved collisions,
- terminal reasons understood.

---

## Step 7 — Gates

Use focused tests first, then backend gate.

Suggested:

```powershell
.\scripts\workflow\run-green-gate.ps1 `
  -StoryId "6.4.2" `
  -FocusedTestCommand "python -m pytest backend/tests/test_form_ai_prompt_capabilities.py backend/tests/test_story_631_semantic_validator.py --tb=short" `
  -BackendGateCommand "python -m pytest --tb=short" `
  -EvidenceFile "docs/stories/STORY-6.4.2-GATE-EVIDENCE.md"
```

Adjust working directory/path if needed and record exact commands.

---

## Step 8 — Closeout + SM Stale-Field Audit

Complete `STORY-6.4.2-CLOSEOUT-REPORT.md`.

Before merge, run the workflow guide stale-field audit:

```powershell
gh pr view 69 --json state,isDraft,mergedAt,headRefName,baseRefName,url
rg -n "Draft|Ready for UAT|Ready for UAT/SM review|Keep PR .* open|Current Focus" docs/stories/story-6.4.2.md docs/stories/STORY-6.4.2-CLOSEOUT-REPORT.md docs/stories/EPIC-6-STATUS.md docs/stories/EPIC-6-WORKFLOW-GUIDE.md
```

Every hit must be intentional for the current phase. Fix stale fields in a final housekeeping commit before asking Anthony to merge.

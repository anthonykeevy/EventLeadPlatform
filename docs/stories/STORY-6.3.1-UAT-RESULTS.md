# Story 6.3.1 — UAT Results

**Story:** 6.3.1 — Simplified AI Output + Deterministic Layout Foundation
**Owner:** Anthony (Human UAT)
**UAT rounds covered:** 1 → 11 (2026-04-15 closeout)
**Companion docs:** `STORY-6.3.1-UAT-TEST-GUIDE.md`, `STORY-6.3.1-GATE-EVIDENCE.md`

---

## §9 — UAT Result (final, post Round 11)

| Section | Pass / Fail / Skipped | Notes |
|---------|------------------------|-------|
| §1 Automated gates | **Pass** | `pytest`: 705 pass / 26 skip; `eslint`: 0 / 0; `vitest`: 272 pass. See `STORY-6.3.1-GATE-EVIDENCE.md`. |
| §2 Capability ingestion | **Pass** | `ComponentCapabilitySnapshot` resolved from DB; `FORM_AI_CAPABILITY_POLICY:v1` active. Migrations 053–057 cover ingestion / extension. |
| §3 Validation contracts | **Pass** | `component_validation_contract` table seeded; deterministic rejection verified by `test_story_631_semantic_validator.py`. |
| §4 Width class responsiveness | **Pass** | `compact` / `half` / `full` resolved against canvas in `compiler.py` and `frontend/.../utils/layoutMode.ts`; covered by `test_story_631_content_widths.py` + `layoutMode.test.ts`. |
| §5 Builder visibility | **Pass** | `BuilderPage.tsx` + `AIAgentPanel.tsx` flow applies the compiled definition directly to canvas; selection / properties verified manually each UAT round. |
| §6 Logging + one-change discipline | **Pass** | UAT rounds 4–11 each document a single-variable change in the GenerationRun trace; replay tooling (`scripts/story_631_replay.py`) reproduces by `RequestID` + `generationRunId`. |
| §7 Render-then-measure | **Pass** | `/api/form-ai/remeasure` round-trip implemented; `compileSummary.heightsSource` reports `estimated` → `measured`/`mixed`; Prompts 6 & 7 layouts now collision-free across desktop / tablet / mobile. |
| §8 Consent / legal nudge | **Pass** | "Terms defaults rule" injected into system prompt when company-managed terms exist; consent intent maps to `terms` component, generic multi-select preserved as `checkbox`. |
| §10 Country / locale awareness | **Pass** | AU/NZ locale addendum in system prompt; `Post Code` / AU phone pattern verified; locale recorded in `governanceVersions`. |
| §11 Layout-mode selection | **Pass** | 600 px threshold honoured; `compileSummary.layoutMode` reports `horizontal-stacked` / `vertical-packed` correctly; horizontal-stacked nudge gated by canvas width. |
| §12 Horizontal-stacked validator parity | **Pass** | UAT Round 11 fix: `MIN_PLAUSIBLE_RENDER_HEIGHT_PX = 32.0` lets the validator trust compiler-stamped heights. Regression covered by `test_horizontal_stacked_rows_do_not_trigger_phantom_collisions` and `test_collision_check_still_inflates_when_height_missing`. |
| §13 Framework parity per component | **Pass with caveat** | Submit / Rating / Terms / Dropdown / generic inputs all editable through standard properties panels. Caveat: submit-button validation parity (design pill vs preview summary) carried forward as `g-frontend-submit-parity` (see §15 follow-up). |
| §14 Canvas height growth | **Pass** | Compiler grows `canvas.height` for tall mobile layouts and shrinks for desktop; behaviour mirrors in builder + preview. |
| §15 Builder edit-after-AI parity | **Pass with caveat** | All AI-generated components remain selectable / editable; save/reload preserves state with no compiler re-run. Caveat: open follow-up `g-frontend-submit-parity`. |

**Final disposition:** **PASS** — story is release-eligible. Two caveats are tracked as follow-ups, neither blocking merge.

---

## Round-by-round summary (chronological)

| Round | Focus | Outcome | Notes |
|-------|-------|---------|-------|
| 1 | Initial semantic plan + first compiler | Partial | Compiler shipped; spacing/width drift noted. |
| 2 | Width class policy + canvas profiles | Partial | `compact/half/full` policy seeded; some collisions on Prompt 5 / 7. |
| 3 | Governance trace + replay tooling | Pass | `GenerationRun` / `GenerationArtifact` persistence verified; replay script confirmed reproducibility. |
| 4 | Capability snapshot extension | Pass | Migration 055 added `rating`, `file-upload`, `address`, `url`. |
| 5 | First-name / last-name + render-then-measure | Pass | Migrations 056/057 (`first-name` in, `last-name` deferred). New `/remeasure` endpoint introduced; Prompt 6 / 7 collisions cleared. |
| 6 | Layout-mode auto-selection (600 px) | Pass | `resolveLayoutModeForRequest.ts` added; horizontal-stacked nudge fires only ≥ 600 px canvases. |
| 7 | Country/locale awareness | Pass | AU/NZ addendum baked into system prompt. |
| 8 | Consent / terms nudge | Pass | "Terms defaults rule" appended when company terms present. |
| 9 | Canvas height growth (builder + preview) | Pass | Builder canvas resizes vertically to match preview. |
| 10 | Framework-first edit-after-AI | Pass with caveat | All standard property panels work on AI output; submit parity caveat noted. |
| 11 | Horizontal-stacked validator phantom collisions | Pass | `MIN_PLAUSIBLE_RENDER_HEIGHT_PX` trust-the-compiler rule resolved desktop/tablet false positives without regressing mobile. |

---

## Open follow-ups (do not block merge)

| ID | Description | Owner / next story |
|----|-------------|---------------------|
| `g-frontend-submit-parity` | Submit-button shows per-field pill in design mode but form-level summary in preview; user wants visual parity. | Story 6.4 backlog. |
| `g4b-second-pass-rows` | Wire second-pass measured heights into row reservation (currently used for vertical packing only). | Story 6.4 backlog. |
| `g-doc` | Document the framework-first architectural pattern (AI builds, user edits with existing tools). | Documentation pass after 6.4. |
| `g-backlog-dropdown-font` | Native `<select>` font size larger than scaled control on some devices. | Backlog. |

---

## Sign-off

**Anthony Keevy** — 2026-04-15 — **PASS** (release-eligible; carry the two caveats above into Story 6.4 planning).

# Story 6.5a — Architecture Phase: Clarification Data Plane + Prompt Assembly Registry Design

**Epic:** 6 — AI Generation & Monetization Engine
**Story ID:** 6.5a
**Title:** Architecture Phase — Clarification Data Plane + Prompt Assembly Registry Design (Dimitri-led)
**Status:** ✅ **Complete (Architecture Phase)** — Rev 9 approved 2026-05-09; companion registry doc landed; implementation decomposed into 6.5b / 6.5c / 6.5d
**Branch:** `story/epic6-6.5a-clarification-questions`
**PR:** [#87](https://github.com/anthonykeevy/EventLeadPlatform/pull/87) — Draft, currently to `develop` (will be **closed and superseded** when the architecture-closeout + 6.5b draft PR opens — see §6 below)
**Worktree:** `C:\wt\elp\story-epic6-6.5a-clarification-questions`
**Created:** 2026-05-07
**Closed:** 2026-05-20 (architecture phase only; implementation continues under 6.5b / 6.5c / 6.5d)

---

## 1) What Story 6.5a Set Out to Do

The original 6.5a brief was *"add clarification-question dropdowns to the AI Agent panel."* When Dimitri (Data Domain Architect) reviewed the brief against the existing locale architecture, the work expanded into a full data-plane redesign covering:

- A `ref.AudienceLocale` registry to eliminate the `AudienceLocale` enum.
- Two new `ref.*` tables for Form Purpose and Respondent Type.
- A new prompt block ("Block E") for clarification context.
- A platform-wide rule that every prompt block (A–I) must be database-driven.
- A companion **Prompt Assembly Registry** schema so all the other blocks (A, B, C, F, G, I) eventually move from Python string literals into versioned DB rows.

That work landed as two architecture documents — see §2. They are the actual deliverable of Story 6.5a.

---

## 2) Deliverable (Architecture Documents)

| Doc | Owner | Status | Purpose |
|-----|-------|--------|---------|
| [`decision-6.5a-clarification-options-data-model.md`](../architecture/decision-6.5a-clarification-options-data-model.md) | Dimitri | **Rev 9 — Approved (2026-05-09)** | Authoritative decision doc for the clarification data plane: `ref.AudienceLocale` (incl. `ClarificationSummary`), `ref.FormPurpose`, `ref.RespondentType`, three reference APIs, Company/Form/GenerationRun schema additions, Block E injection mechanics, locked product decisions (§16) |
| [`prompt-assembly-registry-architecture.md`](../architecture/prompt-assembly-registry-architecture.md) | Dimitri | Companion — landed | Full prompt tree (blocks A–I), `PromptAssemblyProfile*` / `PromptSection*` schema, catalog resolver, toolbox alignment, variant-level versioning. §2.7 is the authoritative post-implementation per-block source map; §10 is the sequencing/handoff |

Both documents live in `docs/architecture/` on this branch and will merge to `develop` as part of the architecture-closeout PR (see §6).

---

## 3) Key Decisions Locked in This Phase

All decisions are reproduced from `decision-6.5a-clarification-options-data-model.md` §16; this section is a quick index so the implementation stories don't have to re-litigate them.

| # | Topic | Decision |
|---|-------|----------|
| 1 | 4th clarification dropdown (Industry) | **Parked until after MVP** — three dropdowns only |
| 2 | Localised `PromptHint` sidecars (`*Locale` tables) | **Post-MVP** — English-only `PromptHint` on base tables for MVP |
| 3 | `DisplayName` column length | Keep `nvarchar(28)`; review in UI before adding any long-label column |
| 4 | E1 audience summary line | **Option B** — `ClarificationSummary` stored per locale on `ref.AudienceLocale`, injected verbatim |
| 5 | Panel labels vs persistence | UI shows `DisplayName`; DB / API persistence uses stable `Code` |
| 6 | All prompt blocks DB-driven | **Yes (platform rule)** — clarification (E) closes in 6.5d; remaining blocks (A/B/C/F/G/I) close via 6.5b + 6.5c |

---

## 4) Implementation Decomposition (Sets the Roadmap)

The original 6.5a brief — "add dropdowns" — has been re-decomposed into **three implementation stories**, sequenced so the R6 blocker (`context-pack-load-failed` in Test, carried forward from PR #101) is cleared first:

| Order | Story | Title | Why this order |
|-------|-------|-------|----------------|
| 1 | **6.5b** | **Prompt Assembly Registry Foundation** | Delivers the registry schema + renderer and migrates the "stored prose" blocks (A, B, C, G, I) from code into DB. **Block G migration closes R6** (the file-based context-pack load that fails on Azure). Without this, 6.5d UAT cannot run in Test. |
| 2 | **6.5c** | **Capability Catalog Cutover** | Makes `resolve_allowed_components` authoritative for Blocks A/F/I AND the frontend toolbox; replaces `brandPosture` enum with `ref.BrandPosture`. Isolates the highest-risk single cutover into its own story so it can be validated in Test on its own. |
| 3 | **6.5d** | **Clarification Data Plane** | The original "add dropdowns" work — three `ref.*` tables + APIs + Block E (now plugging into the registry from 6.5b) + frontend dropdowns + `AudienceLocale` enum elimination. |

**Why three packages instead of two:** isolating the toolbox/capability cutover (6.5c) into its own story keeps each PR mid-sized, makes the Test-environment UAT focused, and gives us a clean rollback boundary if the toolbox cutover misbehaves. R6 closes after 6.5b regardless of the decomposition.

Stories 6.5b/c/d will be drafted in `docs/stories/story-6.5b.md`, `story-6.5c.md`, `story-6.5d.md` as each one becomes the imminent next story (avoids rewriting them as requirements evolve). Forward-planning rows in `EPIC-6-STATUS.md` describe each one in one line.

---

## 5) Speculative Story Renumbering (Triggered by This Decomposition)

The new 6.5b / 6.5c / 6.5d slots collide with previously-pending speculative stories that hadn't started. To preserve their descriptive suffixes, they shift down one letter:

| Old ID | New ID | Description (unchanged) |
|--------|--------|--------------------------|
| 6.5b-vision | **6.5e-vision** | Image-to-Form Vision Path |
| 6.5b-style | **6.5f-style** | Style Intent Resolver |
| 6.5c | **6.5g-PII** | PII Detection Layers |
| 6.5d | **6.5h-fonts** | Google Fonts Directive (conditional) |

The renumbering is reflected in `EPIC-6-STATUS.md`. No work was in flight on any of these.

---

## 6) PR #87 Disposition

Per the re-decomposition decision (Tony, 2026-05-20):

- **PR #87** (current title: "Story 6.5a — Clarification Questions"; current target: `develop`) is being **closed as superseded**.
- A new PR opens from the same branch (`story/epic6-6.5a-clarification-questions`) to `develop` with title and body reflecting the architecture-closeout + 6.5b-draft scope — see §7.
- Rationale: cleaner audit trail. PR #87's body describes the original "add dropdowns" scope; that no longer matches what's being merged.

---

## 7) Architecture-Closeout PR Contents

When the new architecture-closeout PR opens, it carries:

| File | Change |
|------|--------|
| `docs/architecture/decision-6.5a-clarification-options-data-model.md` | Add (Dimitri Rev 9) |
| `docs/architecture/prompt-assembly-registry-architecture.md` | Add (companion) |
| `docs/stories/story-6.5a.md` | This file — repurposed as closed Architecture Phase story |
| `docs/stories/story-6.5b.md` | New — Registry Foundation, Ready for Dev |
| `docs/stories/EPIC-6-STATUS.md` | Update: 6.5a → ✅ Architecture Complete; add 6.5b/c/d rows; rename speculative 6.5b/c/d → 6.5e/f/g/h; add R6-resolved-by-6.5b note |

No production code changes in this PR — pure architecture + planning deliverable. Implementation begins in 6.5b on a new branch.

---

## 8) Closeout Notes

- The original 6.5a story body has been preserved in git history (the long-form ACs / scope tables from the draft are recoverable via `git log` on this file).
- The architecture work fully supersedes the original draft; nothing in the Rev 1 draft is being lost — content has either moved to 6.5d (clarification data plane), 6.5b (registry foundation), or post-MVP backlog.
- **R6 carry-forward** from PR #101 (`context-pack-load-failed`) is now formally owned by 6.5b (closes when Block G migrates to DB).
- No EPIC-6-WORKFLOW-GUIDE.md change required — the new stories ship under the already-documented Environment Promotion Workflow.

---

**Next:** Story 6.5b — Prompt Assembly Registry Foundation. See `story-6.5b.md`.

# Story 5.4 Single-Session Dev Prompt

**Purpose:** Copy this entire prompt into a **new chat** to implement Story 5.4 in one session (skip Ralf-SM decomposition and task cycle).  
**Agent:** @dev (BMAD Developer Agent)  
**Workspace:** Open the Story worktree in Cursor: `C:\wt\elp\story-epic5-5.4-shared-resolver-parity`

---

## Copy everything below this line into a new chat

```markdown
@dev Implement Story 5.4: Shared Resolver Parity in a single session. Skip Ralf; no task decomposition. Treat story-5.4.md and story-context-5.4.xml as the sole source of truth.

---

## Git discipline (MANDATORY)

- **Work only in the Story worktree:** `C:\wt\elp\story-epic5-5.4-shared-resolver-parity`
- **Branch:** `story/epic5-5.4-shared-resolver-parity` (confirm you are on this branch; do NOT work on master)
- **No task branches:** All implementation goes directly on the story branch
- **Commit discipline (from Epic 5 lessons):**
  1. **Implementation commits FIRST** — before any closeout. Run `git status`; if backend/ or frontend/ code is modified, commit it with `feat(5.4): <description>`. Do NOT leave implementation uncommitted.
  2. **Closeout commit = docs only** — UAT results, status updates, completion notes go in a separate commit after implementation is committed.
  3. **Verify clean tree before push** — run `git status`; working tree must be clean (or only intentionally untracked)
- **PowerShell:** Do NOT use `&&`; use `;` for command chaining

---

## Story inputs (READ THESE)

- **Story:** `docs/stories/story-5.4.md`
- **Context:** `docs/stories/story-context-5.4.xml`
- **UAT guide:** `docs/stories/STORY-5.4-UAT-TEST-GUIDE.md`
- **Backend merge:** `backend/modules/form_defaults/service.py` (resolve_definition_for_render, deep_merge)
- **Frontend merge:** `frontend/src/features/builder/utils/definitionResolver.ts` (resolveDefinitionForRender, deepMerge)
- **Asset resolution:** `backgroundAssetResolver.ts`, `useBackgroundImageUrl.ts`

---

## Implementation order

1. **Parity fixtures** — Create shared test fixtures: merged defaults (Global+Company) and form overrides. Use JSON files or Python dicts that can be passed to both backend and frontend logic.
2. **Parity tests** — Add tests in `backend/tests/` that compare backend `resolve_definition_for_render` output with frontend `resolveDefinitionForRender` output for theme, globalStyles, canvasSettings. Options: (a) call frontend via subprocess/Node, or (b) port the frontend merge logic to a small Python helper for test comparison, or (c) use pytest with a JS runner to execute definitionResolver. Simplest: (b) implement a minimal Python equivalent of the TypeScript deepMerge for test purposes and assert outputs match.
3. **Fix drift** — If parity tests fail, align backend and frontend merge logic until tests pass. Document edge cases.
4. **Documentation** — Create `docs/stories/STORY-5.4-RESOLUTION-RULES.md`: merge order (Global → Company → Form), merge algorithm, asset resolution (useBackgroundImageUrl, getBackgroundImageSource), future Review and Publish contract.
5. **Asset audit** — Confirm FormBuilderCanvas and PublicFormArtboard use `useBackgroundImageUrl` for backgrounds; document in STORY-5.4-RESOLUTION-RULES.md. Fix any divergent paths.
6. **UAT** — Run parity tests; run lint/build; record evidence in STORY-5.4-UAT-RESULTS.md.

---

## UAT (maximize automation — show evidence for EACH test)

Create `docs/stories/STORY-5.4-UAT-RESULTS.md` with a table:

| Test ID | Description | Command/Action | Result | Evidence |
|---------|-------------|----------------|--------|----------|
| DC1 | Defaults parity test | `pytest backend/tests/ -k parity` | PASS/FAIL | (snippet) |
| DC2 | Parity tests exist | — | — | — |
| DC3 | STORY-5.4-RESOLUTION-RULES.md exists | — | PASS | — |
| DC4 | Asset audit | grep useBackgroundImageUrl | PASS | FormBuilderCanvas, PublicFormArtboard use it |
| Build/lint | Backend + frontend | pytest; npm run lint | PASS/FAIL | (snippet) |

**Cap long output** — use `Select-Object -First 50` or redirect to file; report pass/fail + first/last lines.

---

## Workflow lessons (from Epic 5)

- **Cap long output** — pytest, npm run build can crash sessions. Limit output.
- **Implementation commits first** — never leave code uncommitted before closeout.
- **Single session** — Proceed: implement → verify → UAT → record → commit (impl first, then docs) → push.

---

## Deliverables

1. Parity tests in `backend/tests/` (shared fixtures + comparison)
2. `docs/stories/STORY-5.4-RESOLUTION-RULES.md`
3. `docs/stories/STORY-5.4-UAT-RESULTS.md` with evidence table
4. All implementation committed and pushed; working tree clean

---

## Human handoff

After you complete: I will run manual UAT (builder preview vs public form with same form), then merge the Story PR to master.
```

---

*Prompt created for Story 5.4 single-session implementation*  
*Last Updated: 2026-02-16*

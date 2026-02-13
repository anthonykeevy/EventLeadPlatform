# Task Retrospective: T08 Integration + UAT Polish

**Story:** 5.1 - Background Asset Management  
**Task:** T08 - Integration + UAT Polish  
**Final Status:** HumanDone  
**Date:** 2026-02-13  

---

## What Went Well

| What Went Well | Evidence |
|----------------|----------|
| Single build fix unblocked integration validation | useBuilderStore.ts: removed unused `BackgroundDefinition`; build passed |
| Browser automation enabled core UAT scenarios | Chrome DevTools MCP: login, builder, asset select, save, network inspection |
| DefinitionJSON verification via network capture | PUT /api/forms/50/versions/1 response: asset reference, no data:image |
| Full cycle executed end-to-end | Implement → Verify → UAT → Retro → Commit (per EPIC-5-WORKFLOW-GUIDE single-prompt cycle) |

---

## What Went Wrong

| Issue | Root Cause | Evidence |
|-------|------------|----------|
| Build failed initially | Unused import (`BackgroundDefinition`) in useBuilderStore | tsc error TS6133 |
| Scenarios 4–6 not automated | Require file upload + test assets | UAT guide steps involve oversized/invalid files |
| Orphan asset 404s in preview | Data hygiene: metadata exists, files missing | Network: /api/assets/11/content 404 (T05 known) |

---

## Prevention Actions

| Issue | Prevention Action | Owner |
|-------|-------------------|-------|
| Unused imports | Run `npm run build` before UAT in integration tasks | ralf-dev |
| Upload limit UAT | Add "prepare test assets" step to UAT guide; consider E2E with fixtures | ralf-uat |
| Orphan 404s | Document as known; seed script or migration to fix orphan metadata | PM/ralf-sm |

---

## Test Improvements

### Automated Tests to Add

| Test Type | Description | Location | Command |
|-----------|-------------|----------|---------|
| unit | dataUrlGuard: isDataUrl, stripDataUrlFromBackground | dataUrlGuard.test.ts | `npm test` |
| integration | Save form with asset background → assert definition has no data: | form version API test | `pytest` |

### UAT Automation Candidates

- Scenario 3: Parse PUT/POST response for form save; assert no `data:image/` (automated via browser MCP or API test)
- Scenario 8: API test sending definition with data:; assert 400 or strip

---

## Process Improvements

### For ralf-dev (Execution)

- Integration tasks: run build early; one-line fixes (unused imports) are in-scope for unblocking verification
- Use network capture to verify DefinitionJSON structure when persistence format is AC

### For ralf-uat (Validation)

- Mark scenarios as "Automated" vs "Human" in UAT checklists
- Add "Test asset preparation" subsection for upload-limit scenarios

---

## Scope Creep Discovered

None. T08 scope was validation only; build fix was minimal unblocker.

---

## If We Ran This Again

1. Run `npm run build` immediately at task start; fix blocking errors before UAT
2. Use network request inspection for DefinitionJSON verification (faster than DB query)
3. Create small test PNGs for upload-limit automation in a future task

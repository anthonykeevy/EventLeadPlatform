# UAT Checklist: T08 Integration + UAT Polish

**Story:** 5.1 - Background Asset Management  
**Task:** T08 - Integration + UAT Polish  
**Generated:** 2026-02-13

---

## Pre-conditions

- [ ] Backend server is running (http://127.0.0.1:8000)
- [ ] Frontend is running (http://localhost:3000)
- [ ] Test credentials available (see `docs/AGENT-LOGGING-GUIDE.md` for test accounts; logging setup for debug)
- [ ] User is logged in with access to Builder and forms

---

## T08-Specific Verification

### AC1: Automated checks captured with pass/fail evidence

- [ ] Step 1: Verify completion note records `npm run lint` result (pass/fail)
- [ ] Step 2: Verify completion note records `npm run build` result (pass/fail)
- [ ] Step 3: Verify backend checks if touched (e.g. `python -m compileall backend` or pytest)

### AC2: UAT guide ready for human execution

- [ ] Step 1: Confirm `docs/stories/STORY-5.1-UAT-TEST-GUIDE.md` is up to date
- [ ] Step 2: Confirm any T01–T07 evidence notes or caveats are reflected if needed
- [ ] Step 3: Confirm test credential / environment setup is documented or linked

### AC3: No open blockers on integration path

- [ ] Step 1: Run full Story 5.1 UAT guide (`docs/stories/STORY-5.1-UAT-TEST-GUIDE.md`) Scenarios 1–9
- [ ] Step 2: Record pass/fail per scenario in `T08-integration-and-uat-polish.uat-results.md`

---

## Story 5.1 UAT Guide (Execute)

Execute `docs/stories/STORY-5.1-UAT-TEST-GUIDE.md` in full. Summary:

| Scenario | Description | Pass/Fail |
|----------|-------------|-----------|
| 1 | Upload background image and apply to the form | ⬜ |
| 2 | Reload the form; background persists and renders | ⬜ |
| 3 | DefinitionJSON does not contain embedded base64 | ⬜ |
| 4 | Upload limit: max bytes enforced | ⬜ |
| 5 | Upload limit: allowed mime types enforced | ⬜ |
| 6 | Upload limit: max dimensions enforced | ⬜ |
| 7 | Renderer parity: public runtime resolves background asset | ⬜ |
| 8 | Data URL payload blocked or stripped | ⬜ |
| 9 | Provider swap smoke test (optional) | ⬜ / SKIP |

---

## Post-conditions

- [ ] All automated checks passed or documented
- [ ] Story 5.1 UAT guide executed; results recorded
- [ ] Story 5.1 ready for final merge to master (after T08 PR merge)

---

**Test credentials:** See `docs/AGENT-LOGGING-GUIDE.md` § UAT test credentials (user1@test.com, user2@test.com; check seed data for password).

**Instructions for Human Tester:**
1. Execute each step in order
2. Mark ✅ or ❌ for each item
3. Run the full STORY-5.1-UAT-TEST-GUIDE
4. Record results in `T08-integration-and-uat-polish.uat-results.md`

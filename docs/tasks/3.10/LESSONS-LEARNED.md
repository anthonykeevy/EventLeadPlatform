# Lessons Learned: Story 3.10 - Grid Layout System

**Story:** 3.10  
**Epic:** Epic 3 - Form Builder & Logic Engine  
**Created:** 2026-01-14  

---

## 📝 Lessons Log

_Append lessons as tasks are completed. Format:_

```markdown
### {date} - {lesson_type} Lesson

**Task:** {task_id}
**Context:** {brief context}
**Issue:** {what went wrong or could be improved}
**Lesson:** {actionable insight}
**Prevention:** {how to avoid in future}
```

---

## Lessons

### 2026-01-15 - Process Lesson

**Task:** T07  
**Context:** UAT for Global Defaults & Overrides  
**Issue:** Testing required multiple rounds and took longer than expected to reach PASS.  
**Lesson:** Add earlier state verification (badge state + layout mode toggle) during dev testing to avoid extended UAT cycles.  
**Prevention:**
1. Add a pre-UAT checklist for layout mode toggles and badge state
2. Use DevTools state checks before UAT to confirm gridLayout transitions
3. Add an E2E test for switching between Object Layout and Grid Layout

### 2026-01-14 - Process Lesson

**Task:** T01  
**Context:** First task in new Ralf workflow  
**Issue:** UAT agent asked "Would you like me to..." instead of completing documentation automatically. Missing files: uat-results.md, retro.md, TASK-PLAN update.  
**Lesson:** Agents should complete their outputs without asking permission. UAT pass should trigger automatic documentation completion.  
**Prevention:** 
1. Update ralf-uat agent to auto-create uat-results.md on pass
2. Update ralf-uat agent to auto-update TASK-PLAN.md status
3. Consider auto-invoking ralf-retro after UAT pass

### 2026-01-14 - Technical Lesson

**Task:** T02  
**Context:** Grid CSS rendering engine integration  
**Issue:** T03 code (GridLayoutSection.tsx) used non-existent lucide-react icons (`Columns3`, `Rows3`), blocking app loading during T02 testing.  
**Lesson:** Always verify icon/import existence before committing code. Use existing icon variants rather than assuming new ones exist.  
**Prevention:**
1. Audit lucide-react exports before using new icons
2. Add import validation to pre-commit hooks
3. Test that app loads after each file creation

### 2026-01-14 - Technical Lesson

**Task:** T02/T03  
**Context:** TypeScript compilation check in terminal  
**Issue:** Running `npx tsc --noEmit --skipLibCheck 2>&1 | Select-Object -First 30` caused Cursor to drop the chat session.  
**Lesson:** Avoid piping TypeScript output through PowerShell cmdlets. Use safer alternatives.  
**Prevention:**
1. Use `npx tsc --noEmit 2>&1 | head -30` (if using Git Bash)
2. Or redirect to file: `npx tsc --noEmit > tsc-output.txt 2>&1` then read file
3. Or use DevTools MCP `evaluate_script` to check for TypeScript errors in running app
4. Or use VSCode Problems panel (ReadLints tool) instead of terminal compilation

---

### 2026-01-14 - Process Lesson

**Task:** T02  
**Context:** UAT for rendering engine task  
**Issue:** Standard UAT checklist was too technical for visual verification since Grid Layout rendering requires T03 UI to configure.  
**Lesson:** "Engine" or "foundation" tasks need simplified UAT focused on code presence + no regression, not visual verification.  
**Prevention:**
1. Create "Simplified UAT" template for engine tasks
2. Include "full testing deferred to [dependent task]" note
3. Focus on: code exists, no TypeScript errors, no regression

---

### 2026-01-14 - Success Pattern

**Task:** T04  
**Context:** Implementing DnD for Grid Layout object assignment  
**What Worked:** Task spec referenced existing `ObjectLayoutSection.tsx` DnD patterns + included code examples  
**Lesson:** Pattern references in task specs significantly accelerate development and reduce errors.  
**Action:** Add "Pattern Reference" section to all UI task specs, especially for DnD, forms, and complex interactions.

---

### 2026-01-14 - Design Pattern

**Task:** T04  
**Context:** Edge case testing with Divider component (no objects)  
**What Worked:** Divider component with no objects was handled correctly without explicit edge case code  
**Lesson:** Well-designed frameworks with proper filtering logic (e.g., `visibleObjects` computation) handle edge cases emergently.  
**Action:** Trust framework design patterns; only specify edge cases that require explicit handling beyond the pattern.

---

## 📊 Pattern Observations

_Track recurring patterns that may inform future decompositions:_

| Pattern | Occurrences | Notes |
|---------|-------------|-------|
| Icon import validation needed | 1 (T03) | `Columns3`, `Rows3` don't exist in lucide-react |
| Engine tasks need simplified UAT | 1 (T02) | Visual testing deferred to dependent tasks |
| Parallel tasks can create blockers | 1 (T02/T03) | T03's broken code blocked T02 testing |
| Avoid piping tsc output in PowerShell | 1 (T02/T03) | `Select-Object` causes Cursor crash - use ReadLints or redirect to file |
| Pattern reference accelerates dev | 1 (T04) | Referencing existing code reduces errors and speeds implementation |
| Emergent edge case handling | 1 (T04) | Framework design handles edge cases without explicit code |
| Utility function templates in specs | 1 (T05) | Complete code examples in task specs accelerate implementation and reduce errors |
| Unit tests needed even for working code | 1 (T05) | Tests prevent regressions and provide faster feedback during development |

---

### 2026-01-14 - Success Pattern

**Task:** T05  
**Context:** Cell merging implementation with utility functions  
**What Worked:** Task Spec included complete utility function templates (`isValidMergeSelection()`, `mergeCells()`, `unmergeCells()`, etc.) with full code examples.  
**Lesson:** Providing utility function templates in task specs significantly accelerates development and reduces implementation errors.  
**Action:** Continue pattern of including complete utility function code examples in task specs for similar tasks.

---

### 2026-01-14 - Testing Lesson

**Task:** T05  
**Context:** All ACs passed on first UAT attempt, but no unit tests exist for merge utilities  
**Issue:** While implementation worked correctly, lack of unit tests means edge cases are only verified manually during UAT.  
**Lesson:** Utility functions should have unit tests even if they work correctly, to catch regressions and provide faster feedback.  
**Prevention:**
1. Add unit tests for all utility functions in task specs
2. Include test requirements in "Required Tests" section
3. Run tests before UAT to catch issues earlier

---

### 2026-01-14 - Success Pattern

**Task:** T06  
**Context:** Individual spacing controls implementation  
**What Worked:** All ACs passed on first UAT attempt, clean single-file implementation, proactive edge case handling  
**Lesson:** Well-scoped tasks with clear component templates and explicit edge case requirements result in zero-defect implementations.  
**Action:** Continue pattern of including complete component templates in task specs and explicit edge case cleanup requirements.

---

### 2026-01-14 - Testing Lesson

**Task:** T06  
**Context:** All ACs passed but no unit tests for gap change handlers  
**Issue:** While implementation worked correctly, gap change handlers (`handleIndividualColumnGapChange`, `handleResetColumnGap`, etc.) lack unit tests.  
**Lesson:** Handler functions should have unit tests even if they work correctly, to catch regressions and provide faster feedback during development.  
**Prevention:**
1. Add unit test requirements for handler functions in task specs
2. Include test examples in "Required Tests" section
3. Run tests before UAT to catch issues earlier

---

### 2026-01-14 - UX Observation Pattern

**Task:** T06  
**Context:** UAT identified UX enhancements (flicker, scroll jump) but correctly classified as enhancements not defects  
**What Worked:** UAT correctly distinguished between defects (AC violations) and enhancements (UX polish)  
**Lesson:** UX observations during UAT should be documented separately from defects. Not all UX issues are defects - some are polish improvements.  
**Action:** Continue pattern of documenting UX enhancements separately in UAT results, routing to backlog rather than blocking task completion.

---

## 📊 Pattern Observations

_Track recurring patterns that may inform future decompositions:_

| Pattern | Occurrences | Notes |
|---------|-------------|-------|
| Icon import validation needed | 1 (T03) | `Columns3`, `Rows3` don't exist in lucide-react |
| Engine tasks need simplified UAT | 1 (T02) | Visual testing deferred to dependent tasks |
| Parallel tasks can create blockers | 1 (T02/T03) | T03's broken code blocked T02 testing |
| Avoid piping tsc output in PowerShell | 1 (T02/T03) | `Select-Object` causes Cursor crash - use ReadLints or redirect to file |
| Pattern reference accelerates dev | 1 (T04) | Referencing existing code reduces errors and speeds implementation |
| Emergent edge case handling | 1 (T04) | Framework design handles edge cases without explicit code |
| Utility function templates in specs | 1 (T05) | Complete code examples in task specs accelerate implementation and reduce errors |
| Unit tests needed even for working code | 2 (T05, T06) | Tests prevent regressions and provide faster feedback during development |
| Component templates in specs accelerate dev | 2 (T05, T06) | Complete component code examples reduce implementation time and errors |
| Proactive edge case cleanup prevents bugs | 1 (T06) | Cleanup logic in resize handlers prevents invalid config state |
| ReadLints tool preferred over terminal tsc | 2 (T05, T06) | Avoids PowerShell piping issues, faster feedback |

---

*Lessons file maintained by Ralf agents throughout Story 3.10 execution*

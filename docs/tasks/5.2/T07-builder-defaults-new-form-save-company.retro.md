# Task T07 Retrospective

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task:** T07 - Builder Defaults on New Form + Save to Company Defaults  
**Date:** 2026-02-16  

---

## What went well

- **Minimal change:** T05 had already wired Save to Company Defaults and Init API; T07 only needed formContext availability fix
- **Clear ACs:** Task spec clearly defined the gap (formContext when eventId null)
- **Single-file change:** useBuilderStore.ts fix was contained and low-risk

## What could improve

- **Worktree build:** Task worktree had pre-existing build failures (apiBaseUrl, FormBrandingDefaultsPage). Consider ensuring worktree has clean build before task start.
- **Backend eventId:** Init API requires eventId; forms can have eventId null. Future: consider backend support for company-only Init (optional eventId).

## Lessons for memory

- formContext should be set whenever companyId exists, not only when both companyId and eventId present — enables Save to Company Defaults for edge cases
- Init API call remains conditional on eventId (backend contract)

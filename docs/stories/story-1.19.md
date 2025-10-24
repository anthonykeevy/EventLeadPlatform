# Story 1.19: Implement Frontend ABR Search UI

**Status:** Ready
**Priority:** High
**Estimate:** 3 Story Points
**Dependencies:** Story 1.10 (Backend ABR Search)

---

## Story

As a **Frontend Developer**,
I want to **implement the `SmartCompanySearch` React component**,
so that **the user can search for their company during the onboarding flow as specified in Story 1.10**.

---

## Context

This story covers the deferred frontend tasks from Story 1.10. The backend API (`/api/companies/smart-search`) is complete and ready for integration. This story involves creating the user-facing UI to consume that API.

---

## Acceptance Criteria

-   **AC-1.19.1:** Create `SmartCompanySearch.tsx` component.
-   **AC-1.19.2:** Implement search input with debouncing (300ms).
-   **AC-1.19.3:** Display loading states and handle API errors gracefully.
-   **AC-1.19.4:** Create `CompanySearchResults.tsx` to display results in a card format.
-   **AC-1.19.5:** Implement auto-selection for single results, pre-filling the onboarding form.
-   **AC-1.19.6:** Ensure the component is responsive and mobile-optimized.
-   **AC-1.19.7:** Create a "Manual Entry" fallback link.

---

## Dev Notes

-   Reference the frontend architecture and component specifications in `docs/stories/story-1.10.md`.
-   The component will be integrated into the main onboarding flow in Story 1.14.

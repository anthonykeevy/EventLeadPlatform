# Story 2.7 Implementation Prompt for Developer Agent

**Purpose:** Prompt for Developer Agent to implement Story 2.7  
**Date:** January 31, 2025  
**Status:** Ready for Implementation  
**Format:** Following EPIC-2-WORKFLOW-GUIDE.md Stage 2 template

---

## **Prompt to Use (Workflow Guide Format)**

Use this prompt following the **Stage 2: Story Implementation** format from `docs/stories/EPIC-2-WORKFLOW-GUIDE.md`:

```
@dev.mdc Please implement Epic 2 Story 2.7: Event Public Review Workflow Implementation

Story Location: docs/stories/story-2.7.md
UX Review: docs/stories/STORY-2.7-UX-REVIEW.md
Workflow Document: docs/event-public-review-workflow.md
Schema Analysis: docs/data-domains/event-review-workflow-schema-analysis.md
Epic 2 Status: docs/stories/EPIC-2-STATUS.md
Foundation Story: docs/stories/story-2.4.md (Event Management CRUD - already implemented)

Database Status:
- Epic 1 migrations: Complete (002_epic1_complete_schema.py)
- Epic 2 migrations: Complete up to 023_drop_old_public_review_status_column.py
- Database is ready - verify and skip any database setup tasks
- Focus on testing existing database functionality

Requirements:
- Implement all story requirements
- Verify database functionality (skip setup tasks)
- Implement all workflow guards (Guard 1-5)
- Implement all query guards (Platform-wide, Company Network, Admin Queue)
- Implement multi-step progressive disclosure flow (UX enhancements)
- Perform QA testing (backend/frontend as applicable)
- Conduct UAT testing (if frontend story)
- Update story file with implementation details
- Mark UAT tests as completed/passed
- Add reflection and lessons learned
- Update Epic 2 Status document

Focus Areas:
- Backend workflow guards implementation (Guard 1-5) - **Build on existing Story 2.4 service methods**
- Query guards implementation (Platform-wide, Company Network, Admin Queue)
- Frontend multi-step progressive disclosure flow (Step 1-4) - **Enhance existing Story 2.4 event form**
- UX components (EventTypeSelector, PlatformSearchabilityQuestion, etc.)
- Data integrity fixes for existing records
- All workflow scenarios from event-public-review-workflow.md

**Integration with Story 2.4:**
- Extend existing `create_event()` method in `backend/modules/events/service.py` with workflow guards
- Extend existing `update_event()` method with state transition guards
- Enhance existing event creation form with multi-step progressive disclosure
- Update existing event API integration to use PublicReviewStatusID FK
- Follow existing patterns from Story 2.4 (smart field inference, progressive disclosure, etc.)

Key Workflow Principles:
1. EventStatus is USER-CONTROLLED - Users control event lifecycle
2. IsSharedWithPlatform is USER-CONTROLLED - Users choose platform sharing
3. PublicReviewStatus is ADMIN-CONTROLLED - Admins control review decisions
4. Platform-wide visibility requires ALL conditions (IsPublic=True AND IsSharedWithPlatform=True AND PublicReviewStatus=APPROVED AND EventStatus=PUBLISHED)

UX Enhancements (Task 15):
- Step 1: Neutral wording "Is this event open to the public?" (no visibility statements)
- Step 2B: Search/Skip options for public events
- Step 3A: Search interface (skip platform question if event selected)
- Step 3B: Platform searchability question (only if skipped search)
- Step 4: Full form with compact "Search Event" button

Please confirm completion and provide implementation summary.
```

---

## **Additional Context for Developer**

**Story 2.7 Overview:**
- **Purpose:** Implement complete event public review workflow with guards, validation rules, and data integrity checks
- **Scope:** Backend workflow implementation, frontend API integration updates, UX components
- **Users:** Event creators (users) and System administrators
- **Status:** ✅ Approved - Ready for Implementation
- **Foundation:** Builds on Story 2.4 (Event Management CRUD) - reference existing patterns and code

**Story 2.4 Foundation (Already Implemented):**
- Event CRUD operations fully implemented
- Event model with basic fields (Name, Description, StartDateTime, EventTypeID, etc.)
- Event service layer (`backend/modules/events/service.py`) with `create_event()` and `update_event()` methods
- Event API endpoints (`backend/modules/events/router.py`)
- Event creation/update forms in frontend
- Dashboard integration with event list
- Multi-tenant filtering (company-scoped access)
- Smart field inference patterns
- Progressive disclosure patterns (tab-based form)
- **Reference:** `docs/stories/story-2.4.md` for implementation details and patterns

**What Story 2.7 Adds:**
- Workflow guards on top of existing CRUD operations
- Review status management (PublicReviewStatusID FK)
- Platform sharing control (IsSharedWithPlatform field)
- Multi-step progressive disclosure flow (UX enhancements)
- Query guards for visibility filtering
- Data integrity fixes

**Key Features:**
- Event creation workflow with visibility options
- Event update workflow with state transitions
- Review status management (Pending, Approved, Rejected)
- Platform-wide visibility rules
- Company network visibility
- Multi-step progressive disclosure flow (UX)

**Database Schema (Already Migrated):**
- ✅ `ref.PublicReviewStatus` table exists (migration 020)
- ✅ `IsSharedWithPlatform` field exists in `dbo.Event` (migration 021)
- ✅ `PublicReviewStatusID` FK exists in `dbo.Event` (migration 022)
- ✅ Old `PublicReviewStatus` VARCHAR column dropped (migration 023)

**Workflow Guards to Implement:**
1. **Guard 1:** Event Creation Guard - Sets review status based on IsPublic and IsSharedWithPlatform
2. **Guard 2:** IsPublic Update Guard - Handles IsPublic changes (True → False, False → True)
3. **Guard 3:** PublicReviewStatus Update Guard - Admin-only review operations with validation
4. **Guard 4A:** IsSharedWithPlatform Update Guard - Handles platform sharing changes
5. **Guard 4B:** EventStatus Update Guard - Handles event lifecycle changes (ARCHIVED, CANCELLED)

**Query Guards to Implement:**
1. **Platform-Wide Visibility Query** - Filters by all required conditions
2. **Company Network Visibility Query** - Filters public events
3. **Admin Review Queue Query** - Filters pending review events (excludes archived)

**UX Components to Implement (Task 15):**
1. **EventTypeSelector** (Step 1) - Neutral wording, no visibility statements
2. **EventSearchStep** (Step 2B) - Search/Skip options
3. **PlatformSearchabilityQuestion** (Step 3B) - Only if skipped search
4. **CompactEventSearchButton** - Compact button in full form
5. **ReviewStatusBadge** - Color-coded status display
6. **ReviewFeedbackPanel** - Review feedback for rejected events
7. **ReviewProcessInfoBanner** - Review process explanation

**Key Documents to Reference:**
- `docs/stories/story-2.7.md` - Full story with tasks and acceptance criteria
- `docs/stories/story-2.4.md` - **Foundation story** - Event Management CRUD (already implemented, reference for patterns)
- `docs/stories/STORY-2.7-UX-REVIEW.md` - UX Expert review with recommendations
- `docs/event-public-review-workflow.md` - Complete workflow mapping with all guards and scenarios
- `docs/data-domains/event-review-workflow-schema-analysis.md` - Schema analysis
- `docs/policies/public-event-guidelines.md` - Public Event Guidelines Policy (for user guidance)
- `backend/migrations/versions/020_create_public_review_status_ref_table.py` - PublicReviewStatus reference table
- `backend/migrations/versions/021_add_is_shared_with_platform_to_event.py` - IsSharedWithPlatform field
- `backend/migrations/versions/022_migrate_public_review_status_to_fk.py` - PublicReviewStatus VARCHAR → FK
- `backend/migrations/versions/023_drop_old_public_review_status_column.py` - Drop old VARCHAR column

**Existing Code to Reference (Story 2.4):**
- `backend/modules/events/service.py` - Existing `create_event()` and `update_event()` methods (add guards here)
- `backend/modules/events/router.py` - Existing event API endpoints (extend with review endpoints)
- `backend/modules/events/schemas.py` - Existing Pydantic schemas (update to use PublicReviewStatusID FK)
- `frontend/src/features/events/components/EventForm.tsx` - Existing event creation/update form (enhance with multi-step flow)
- `frontend/src/features/events/api/eventApi.ts` - Existing event API integration (update to use PublicReviewStatusID FK)

**Important Notes:**
- Database migrations are complete - verify functionality, don't create new migrations
- Follow all workflow guards from `event-public-review-workflow.md`
- Implement UX enhancements from `STORY-2.7-UX-REVIEW.md`
- Use neutral wording in Step 1: "Is this event open to the public?" (no visibility statements)
- Platform searchability question only shown if user skipped search
- If user selects existing event from search, skip platform searchability question

**Testing Requirements:**
- Backend API testing with Postman/curl
- End-to-end workflow testing
- UAT testing with comprehensive test suite
- Data integrity validation
- Accessibility testing (keyboard navigation, screen readers)

**Expected Deliverables:**
1. All backend workflow guards implemented
2. All query guards implemented
3. All UX components implemented
4. Frontend multi-step progressive disclosure flow
5. Data integrity fixes applied
6. Story file updated with completion report
7. All UAT tests marked as completed/passed
8. Epic 2 Status document updated

---

**Ready for Developer Agent** ✅  
**Follow workflow guide format** 📋


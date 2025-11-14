# Story 2.6 Creation Prompt for Scrum Master

**Purpose:** Create Story 2.6 - Admin Public Event Review Workflow  
**Date:** January 31, 2025  
**Status:** Ready for Story Creation  
**Format:** Following EPIC-2-WORKFLOW-GUIDE.md Stage 1 template

---

## **Prompt to Use (Workflow Guide Format)**

Use this prompt following the **Stage 1: Starting a New Story** format from `docs/stories/EPIC-2-WORKFLOW-GUIDE.md`:

```
@sm.mdc Please create the next Epic 2 story. 

Current Status:
- Epic 2 Status: docs/stories/EPIC-2-STATUS.md
- Last Completed Story: 2.4 - Event Management CRUD (✅ Complete - 12/12 UAT Passed)
- Current Domain: Event Management (Domain 2)
- Next Story Needed: Story 2.6 - Admin Public Event Review Workflow

Requirements:
- Create story file in docs/stories/ folder
- Create context file in docs/stories/ folder  
- Update Epic 2 Status document
- Ensure story includes comprehensive UAT tests
- Focus on Event Management domain (Domain 2)
- Follow BMAD v6 story creation standards
- Include creation summary for quality assurance

Expected Deliverables:
1. Story file: docs/stories/story-2.6.md
2. Context file: docs/stories/story-context-2.6.xml
3. Epic 2 Status update
4. Creation summary (BMAD standard)

Please confirm story creation and provide story ID.
```

---

## **Additional Context for SM (Reference When Creating Story)**

The Scrum Master should reference these documents for detailed context:

**Epic Goal Context:**
- **Epic 2 AC5 Requirement:** "Users can create, update, and manage events with multi-tenant filtering and public review process"
- **Current Status:** Story 2.4 delivered ~85% of AC5
  - ✅ Event Creation & Management: COMPLETE
  - ✅ Multi-Tenant Filtering: COMPLETE
  - 🔄 Public Review Process: PARTIAL (foundation ready, admin workflow needed)

**Story 2.4 Foundation (Already Implemented):**
- PENDING_REVIEW status implemented for public events
- Event model includes fields: PublicReviewStatus, PublicReviewDate, PublicReviewBy, PublicReviewComments
- Public events automatically set to PENDING_REVIEW status on creation
- EventCompany relationship management (participant vs organizer)
- Company-scoped event access filtering

**Story Scope (for story creation):**
- Admin dashboard showing events with PublicReviewStatus = 'PENDING'
- Admin review interface (approve/reject with comments)
- Event creator notifications (email when reviewed)
- Public visibility activation after approval
- Rejection workflow with feedback to creators
- Integration with existing Event model fields from Story 2.4
- Admin role verification and access control

**Technical Context:**
- Admin users exist from Epic 1 (RBAC middleware supports admin checks)
- Email service ready from Epic 1 for review notifications
- Event model already has all required fields for review workflow
- Multi-tenant consideration: Admins need access to all companies' pending events

**Key Documents to Reference:**
- `docs/stories/EPIC-2-STATUS.md` - See "Story Creation Instructions for Scrum Master" section
- `docs/tech-spec-epic-2.md` - AC5 requirements
- `docs/data-domains/events-domain-epic2-analysis.md` - Events domain analysis
- `docs/stories/story-2.4.md` - Story 2.4 completion report (foundation details)

**Important Notes:**
- Story 2.5 (Multi-Tenant Event Filtering) was cancelled - multi-tenant filtering already implemented in Story 2.4
- This story completes AC5 Epic goal (Event Management)
- Follow BMAD v6 non-interactive story creation workflow

---

**Ready for Scrum Master** ✅  
**Follow workflow guide format** 📋

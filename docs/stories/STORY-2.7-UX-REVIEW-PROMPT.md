# Story 2.7 UX Review Prompt for Sally 🎨

**Purpose:** Request UX Expert review of Story 2.7 for UX improvements  
**Date:** January 31, 2025  
**Status:** Ready for UX Review  
**For:** Sally (UX Expert Agent)

---

## **Prompt to Use**

```
@ux-expert.mdc Please review Epic 2 Story 2.7 for UX improvements.

Story Location: docs/stories/story-2.7.md
Workflow Document: docs/event-public-review-workflow.md
Schema Analysis: docs/data-domains/event-review-workflow-schema-analysis.md

Current Status:
- Story 2.7: Event Public Review Workflow Implementation
- Status: DRAFT - Ready for UX Review
- Focus: Backend workflow implementation with guards and validation rules
- Frontend Integration: Task 13 includes frontend API integration updates

Requirements:
- Review Story 2.7 for UX improvements
- Identify user-facing elements that need UX attention
- Suggest UX enhancements for:
  - Event creation workflow (IsPublic, IsSharedWithPlatform selection)
  - Event update workflow (visibility changes, platform sharing options)
  - Review status display (Pending, Approved, Rejected)
  - Error messages and validation feedback
  - User guidance and help text
  - Progressive disclosure patterns
  - Accessibility considerations
- Consider both event creator and admin user perspectives
- Focus on clarity, usability, and user guidance

Key Workflow Principles to Consider:
1. EventStatus is USER-CONTROLLED - Users control event lifecycle
2. IsSharedWithPlatform is USER-CONTROLLED - Users choose platform sharing
3. PublicReviewStatus is ADMIN-CONTROLLED - Admins control review decisions
4. Platform-wide visibility requires ALL conditions (IsPublic=True AND IsSharedWithPlatform=True AND PublicReviewStatus=APPROVED AND EventStatus=PUBLISHED)

Areas Requiring UX Attention:
- Event creation form: How to present "Company Network Only" vs "Share with Platform" options
- Event update form: How to handle visibility changes and their implications
- Review status display: How to show Pending/Approved/Rejected status to event creators
- Validation feedback: How to communicate required fields for platform-sharing events
- User guidance: How to explain review process and expectations
- Error handling: How to communicate validation errors and state transitions
- Progressive disclosure: When to show/hide review-related fields

Please provide:
1. UX improvement recommendations
2. User interface suggestions
3. User guidance and help text recommendations
4. Accessibility considerations
5. Error message improvements
6. Progressive disclosure patterns
7. Any additional UX enhancements

Expected Deliverables:
1. UX review document with recommendations
2. Updated story tasks (if needed) to include UX improvements
3. User interface mockups or descriptions (if applicable)
4. User guidance text suggestions

Please confirm UX review and provide recommendations.
```

---

## **Additional Context for Sally**

**Story 2.7 Overview:**
- **Purpose:** Implement complete event public review workflow with guards and validation rules
- **Scope:** Backend workflow implementation, frontend API integration updates
- **Users:** Event creators (users) and System administrators
- **Key Features:**
  - Event creation workflow with visibility options
  - Event update workflow with state transitions
  - Review status management (Pending, Approved, Rejected)
  - Platform-wide visibility rules
  - Company network visibility

**Workflow Scenarios to Consider:**
1. **Create Private Event** - User creates private event (no review needed)
2. **Create Public Event** - User creates public event with visibility options:
   - "Company Network Only" (no review needed)
   - "Share with Platform" (requires admin review)
3. **Change Private to Public** - User updates private event to public
4. **Change Public to Private** - User updates public event to private
5. **Enable Platform Sharing** - User enables platform sharing (requires review)
6. **Disable Platform Sharing** - User disables platform sharing (no review needed)
7. **Admin Approves Event** - Admin approves event (becomes visible when user publishes)
8. **Admin Rejects Event** - Admin rejects event (remains company network only)
9. **Resubmit Rejected Event** - User edits and resubmits rejected event

**Key Documents to Reference:**
- `docs/stories/story-2.7.md` - Full story with tasks and acceptance criteria
- `docs/event-public-review-workflow.md` - Complete workflow mapping with all scenarios
- `docs/data-domains/event-review-workflow-schema-analysis.md` - Schema analysis
- `docs/policies/public-event-guidelines.md` - Public event guidelines (for user guidance)

**Related Stories:**
- Story 2.4: Event Management CRUD (foundation)
- Story 2.6: Admin Public Event Review Workflow (depends on Story 2.7)

**Frontend Integration Points (Task 13):**
- Event creation/update forms need `IsSharedWithPlatform` field
- Event display components need review status from `PublicReviewStatusID` relationship
- Review status badges and indicators
- Validation feedback for required fields
- User guidance for review process

**UX Considerations:**
- **Clarity:** Users need to understand the difference between "Company Network Only" and "Share with Platform"
- **Guidance:** Users need to understand review process and expectations
- **Feedback:** Users need clear feedback on review status and next steps
- **Progressive Disclosure:** Show/hide review-related fields based on user selections
- **Accessibility:** Ensure all interactions are accessible (keyboard navigation, screen readers, etc.)
- **Error Handling:** Clear validation messages and state transition errors
- **Help Text:** Contextual help for review process and visibility options

---

**Ready for UX Expert Review** ✅  
**Focus on user-facing elements and guidance** 🎨


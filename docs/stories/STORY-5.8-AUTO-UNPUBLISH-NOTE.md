# Story 5.8 — Auto-Unpublish (Deferred)

**Status:** Deferred for MVP  
**Created:** 2026-02-20  

## Scope

When `Form.UnpublishMode` is `SCHEDULED` or `EVENT_END`, forms should auto-unpublish when the date passes.

## MVP Approach

- **Manual reminder:** Dashboard shows "Will unpublish on [date]" badge for forms with SCHEDULED or EVENT_END.
- **Manual unpublish:** Admin can unpublish at any time via FormReviewPage or Dashboard.
- **Auto-unpublish:** Not implemented in MVP. A background job or cron would be required.

## Future Implementation

1. Add a scheduled job (e.g. Azure Functions, cron, or Celery) that runs periodically.
2. Query forms where:
   - `UnpublishMode = 'SCHEDULED'` and `ScheduledUnpublishDate <= now`, or
   - `UnpublishMode = 'EVENT_END'` and linked Event's `EndDateTime <= now`
3. For each: set Form to UNPUBLISHED, deactivate FormPublicLink.
4. Optionally trigger in-app notification to Company Admins when auto-unpublish occurs.

## References

- Story 5.8: `docs/stories/story-5.8.md`
- Form model: `UnpublishMode`, `ScheduledUnpublishDate`
- Event model: `EndDateTime`

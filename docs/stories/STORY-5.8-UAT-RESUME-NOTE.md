# Story 5.8 UAT: Resume Note

**After implementing Form Approval Status alignment (2026-02-20)**

## Can I Continue UAT or Start Again?

**You can continue from Phase 1.2**, but with these caveats:

### Migration Required First

1. **Run the new migration** (050) before testing:
   ```
   alembic upgrade head
   ```
   This adds `APPROVED_FOR_PUBLISH` and deactivates unused statuses.

### Existing Test Data

- **Forms created before migration:** Forms in PENDING_REVIEW with an approved request will not automatically have the new APPROVED_FOR_PUBLISH status. The Form Status will stay PENDING_REVIEW until you re-approve or the backend is updated to migrate them.
- **Forms in "Pending Admin Review"** from a previous run: Use a **fresh form** for Phase 1.2e/1.2f to verify Approve only → "Ready to Publish" correctly.

### Recommended Approach

| Scenario | Recommendation |
|----------|----------------|
| Fresh UAT | Start from Phase 0 (setup), then Phase 1 with a new Form 1 |
| Resuming mid-UAT | Run migration, then re-run **Phase 1.2** (1.2a–1.2f) with a new form to verify Approve only behaviour |
| Phase 2+ (Approve & Publish, Unpublish, etc.) | Should work as before; no status changes for those flows |

### What Changed (Phase 1.2f Fix)

- After **Approve only**, form now shows **"Approved for Publish"** / **"Ready to Publish"** instead of "Pending Admin Review"
- Form Approval Status is set to APPROVED
- Admin can publish via Review page or direct publish
- Audit trail now logs publish requested, approved, published, rejected, unpublished

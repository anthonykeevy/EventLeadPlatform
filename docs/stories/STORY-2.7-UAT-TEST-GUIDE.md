# Story 2.7 UAT Test Guide - Event Public Review Workflow Implementation

**Status:** 📋 Ready for UAT Testing  
**Story:** `docs/stories/story-2.7.md`  
**Workflow Spec:** `docs/event-public-review-workflow.md`  
**Schema Analysis:** `docs/data-domains/event-review-workflow-schema-analysis.md`  

> Note: `story-2.7.md` references `docs/stories/story-context-2.7.xml`, but it is not present in the repository. This UAT guide uses the Story 2.7 acceptance criteria plus the workflow spec and schema analysis as the source of truth.

---

## 🛠️ Pre-requisites

### Accounts / Roles
1. **Event Creator account** (standard user / company user) with permission to create and edit events.
2. **System Admin account** (`system_admin`) to approve/reject public review submissions.
3. **Second company account** (optional but recommended) to validate “company network” visibility behaviors.

### Environment
1. **Backend services running** and reachable.
2. **Frontend running** (desktop browser + ability to use DevTools).
3. **Database reachable** for verification of FK fields and for optional setup.
4. **Email capture available** (MailHog or logs) if email notifications are part of your environment.

### Reference Data / Schema
1. `ref.PublicReviewStatus` exists with (at minimum) **PENDING**, **APPROVED**, **REJECTED**.
2. `dbo.Event` includes:
   - `IsPublic` (boolean)
   - `IsSharedWithPlatform` (boolean)
   - `PublicReviewStatusID` (FK to `ref.PublicReviewStatus`, nullable)
   - `EventStatusID` (FK to `ref.EventStatus`)
3. `ref.EventStatus` includes at minimum **DRAFT**, **PUBLISHED**, **CANCELLED**, **ARCHIVED**.

### How to verify “stored state” during testing (choose at least one)
- **Method A (Preferred): API response**
  - Use DevTools Network to inspect responses from event create/update endpoints.
  - Confirm `PublicReviewStatusID`, `IsSharedWithPlatform`, `IsPublic`, and `EventStatusID` values.

- **Method B: Database verification**
  - Query the Event row after each scenario and verify fields match expected workflow state.

---

## 🧪 Test Scenarios

### Category 1: Event Creation Workflow (Guard 1)

#### Test 1.1: Create Private Event (IsPublic = false)
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Log in as Event Creator. | User is authenticated. | |
| 2 | Create a new event with **Private** intent. | Event is created successfully. | |
| 3 | Verify persisted values for the event. | `IsPublic = False`; `IsSharedWithPlatform = False`; `PublicReviewStatusID = NULL`; review-required flag (if present) is False; `EventStatusID` remains user-controlled (typically DRAFT). | |

#### Test 1.2: Create Public Event – Company Network Only
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Create a new event and select **Public**. | Event creation UI proceeds. | |
| 2 | Choose **Company Network Only** (not platform searchable). | Event saves successfully. | |
| 3 | Verify persisted values. | `IsPublic = True`; `IsSharedWithPlatform = False`; `PublicReviewStatusID = NULL`; event is not placed into admin review queue. | |

#### Test 1.3: Create Public Event – Share with Platform (Requires Review)
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Create a new event and select **Public**. | Event creation UI proceeds. | |
| 2 | Choose **Share with Platform**. | Event saves successfully. | |
| 3 | Verify persisted values. | `IsPublic = True`; `IsSharedWithPlatform = True`; `PublicReviewStatusID = PENDING`; event appears in admin review queue. | |

#### Test 1.4: Creation validation – missing required fields for platform-sharing
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Attempt to create a **Share with Platform** event missing required fields (e.g., Description / StartDateTime / EventType). | Save is blocked OR the API returns a validation error. | |
| 2 | Observe the user-facing feedback. | Clear, actionable message listing missing required fields for platform sharing. | |
| 3 | Fix the fields and retry. | Event creates successfully and sets `PublicReviewStatusID = PENDING`. | |

#### Test 1.5: Creation guard – cannot be private + platform shared
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Attempt to create an event with `IsPublic = False` while enabling platform sharing (if UI allows). | UI prevents the combination OR backend forces `IsSharedWithPlatform = False` and clears review status. | |
| 2 | Verify final persisted state. | No state exists where `IsPublic = False` and `IsSharedWithPlatform = True`. | |

---

### Category 2: Event Update – IsPublic changes (Guard 2)

#### Test 2.1: Update Private → Public with platform sharing
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Start with an existing private event. | Event exists with `IsPublic = False`. | |
| 2 | Update event: set **IsPublic = True** and enable **Share with Platform**. | Update succeeds if required fields are complete. | |
| 3 | Verify persisted values. | `IsPublic = True`; `IsSharedWithPlatform = True`; `PublicReviewStatusID = PENDING`. | |

#### Test 2.2: Update Private → Public with company network only
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Start with an existing private event. | Event exists. | |
| 2 | Update event: set **IsPublic = True** but keep **IsSharedWithPlatform = False**. | Update succeeds. | |
| 3 | Verify persisted values. | `IsPublic = True`; `IsSharedWithPlatform = False`; `PublicReviewStatusID = NULL`. | |

#### Test 2.3: Update Public → Private
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Start with a public event (any sharing mode). | Event exists with `IsPublic = True`. | |
| 2 | Update event: set **IsPublic = False**. | Update succeeds. | |
| 3 | Verify persisted values. | `IsPublic = False`; `IsSharedWithPlatform = False`; `PublicReviewStatusID = NULL` (cleared). | |

---

### Category 3: Event Update – IsSharedWithPlatform changes (Guard 4A)

#### Test 3.1: Enable platform sharing on an existing public event
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Start with `IsPublic = True` and `IsSharedWithPlatform = False`. | Event exists. | |
| 2 | Enable **Share with Platform**. | Update succeeds if required fields are present. | |
| 3 | Verify persisted values. | `IsSharedWithPlatform = True`; `PublicReviewStatusID = PENDING`. | |

#### Test 3.2: Enable platform sharing validation (missing required fields)
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Start with a public event missing required platform-sharing fields. | Event exists. | |
| 2 | Enable **Share with Platform**. | Update is blocked; user sees clear field-level validation messages. | |
| 3 | Complete required fields and retry. | Update succeeds and sets `PublicReviewStatusID = PENDING`. | |

#### Test 3.3: Disable platform sharing while review is PENDING
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Start with `IsSharedWithPlatform = True` and `PublicReviewStatusID = PENDING`. | Event exists. | |
| 2 | Disable **Share with Platform**. | Update succeeds. | |
| 3 | Verify persisted values. | `IsSharedWithPlatform = False`; `PublicReviewStatusID` is cleared to NULL (pending review cancelled). | |

#### Test 3.4: Disable platform sharing after APPROVED/REJECTED
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Start with an event already **APPROVED** (or **REJECTED**). | Event exists. | |
| 2 | Disable **Share with Platform**. | Update succeeds. | |
| 3 | Verify behavior. | Platform sharing turns off; review history remains available for audit (status may remain APPROVED/REJECTED or be represented via review history fields). | |

---

### Category 4: Event Update – EventStatus changes (Guard 4B)

#### Test 4.1: Archive event with PENDING review
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Start with a platform-sharing event in PENDING review. | Event exists. | |
| 2 | Set `EventStatus` to **ARCHIVED**. | Update succeeds. | |
| 3 | Verify persisted values. | Pending review is cleared; platform sharing is disabled; event is removed from admin review queue. | |

#### Test 4.2: Archive event with APPROVED review
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Start with an APPROVED platform-sharing event. | Event exists. | |
| 2 | Set `EventStatus` to **ARCHIVED**. | Update succeeds. | |
| 3 | Verify persisted values. | Platform sharing is disabled; event is not platform visible; review history is retained. | |

#### Test 4.3: Cancel approved platform-sharing event
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Start with `IsSharedWithPlatform = True` and `PublicReviewStatusID = APPROVED`. | Event exists. | |
| 2 | Set `EventStatus` to **CANCELLED**. | Update succeeds. | |
| 3 | Verify behavior. | Event is not platform visible; any stakeholder notification behavior (if present) triggers without crashing. | |

---

### Category 5: Admin Review Workflow (Guard 3)

#### Test 5.1: Admin can view pending review queue
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Log in as **System Admin**. | Admin authenticated. | |
| 2 | Open admin review queue view. | List loads. | |
| 3 | Verify only eligible events appear. | Only events with `IsPublic=True`, `IsSharedWithPlatform=True`, `PublicReviewStatusID=PENDING`, and not archived/deleted appear. | |

#### Test 5.2: Approve a PENDING event
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Open a PENDING event for review. | Review details load. | |
| 2 | Click **Approve** (optional comment). | Approval succeeds. | |
| 3 | Verify persisted values. | `PublicReviewStatusID = APPROVED`; review audit fields populated (reviewed by/date); **EventStatus remains unchanged**. | |

#### Test 5.3: Reject a PENDING event requires comment
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Open a PENDING event for review. | Review details load. | |
| 2 | Click **Reject** with empty comment. | Rejection is blocked with a clear validation error. | |
| 3 | Reject with a comment. | Rejection succeeds. | |
| 4 | Verify persisted values. | `PublicReviewStatusID = REJECTED`; `IsSharedWithPlatform = False`; review fields populated; **EventStatus unchanged**. | |

#### Test 5.4: Only admins can approve/reject
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Log in as non-admin user. | User authenticated. | |
| 2 | Attempt to call approve/reject actions (via UI if visible or via direct URL). | Action is blocked/hidden; backend returns 403/unauthorized if called directly. | |

#### Test 5.5: Only PENDING events can be reviewed
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | As admin, attempt to approve/reject an event not in PENDING state. | Action is blocked. | |
| 2 | Verify error messaging. | Clear message: only PENDING events can be approved/rejected. | |

---

### Category 6: Visibility Queries

#### Test 6.1: Platform-wide visibility requires all conditions
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Ensure an event is `IsPublic=True`, `IsSharedWithPlatform=True`, `PublicReviewStatusID=APPROVED`, `EventStatusID=PUBLISHED`. | Event exists. | |
| 2 | Execute/observe platform-wide search/list endpoint. | Event appears in results. | |

#### Test 6.2: Platform-wide visibility excludes wrong combinations
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Create or identify events that fail exactly one condition each (e.g., not approved, not published, not shared). | Test data exists. | |
| 2 | Execute/observe platform-wide search/list endpoint. | None of those events appear in platform-wide results. | |

#### Test 6.3: Company network visibility shows public events
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Identify a company-network-only public event (`IsPublic=True`, `IsSharedWithPlatform=False`). | Event exists. | |
| 2 | Execute/observe company-network search/list endpoint (for creator’s company). | Event appears in company-network results. | |

---

### Category 7: Admin Review Queue Query Guards

#### Test 7.1: Queue excludes archived events
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Have a platform-sharing event in PENDING, then archive it. | Event is archived. | |
| 2 | Reload admin pending review queue. | Archived event does not appear. | |

#### Test 7.2: Queue excludes deleted events
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Mark an event deleted (or use an existing deleted event). | Deleted state exists. | |
| 2 | Reload admin pending review queue. | Deleted event does not appear. | |

---

### Category 8: Data Integrity Fixes

#### Test 8.1: Integrity script fixes archived + review-required inconsistencies
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Ensure there is (or create) an event in an invalid state (e.g., archived but pending review). | Invalid record exists. | |
| 2 | Run the data integrity fix process (per Story 2.7). | Script completes without errors. | |
| 3 | Verify corrected state. | Review-required flags and pending status are cleared appropriately; `IsSharedWithPlatform` disabled for invalid combos. | |

#### Test 8.2: Integrity script fixes IsPublic=true with NULL review status (platform-sharing)
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Ensure there is an event with `IsPublic=True`, `IsSharedWithPlatform=True`, but `PublicReviewStatusID=NULL`. | Invalid record exists. | |
| 2 | Run the integrity fix. | Script completes. | |
| 3 | Verify corrected state. | `PublicReviewStatusID` becomes `PENDING` (or the record is adjusted per workflow rules). | |

---

### Category 9: Frontend UX + Integration

#### Test 9.1: Progressive disclosure flow (public/private intent)
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Start Create Event flow. | Step 1 shows neutral Public/Private intent question. | |
| 2 | Choose Private and continue. | Full form appears; no platform sharing options shown. | |
| 3 | Restart and choose Public and continue. | Search/Skip step appears (public path). | |

#### Test 9.2: Public path – search existing event and join/participate
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Choose Public → Search existing events. | Search UI appears. | |
| 2 | Select an existing platform event. | Flow proceeds via “join/participate” behavior (no duplicate event created). | |
| 3 | Verify outcome. | User is linked as participant; event details reflect authoritative source; no duplicate event rows created for the same event. | |

#### Test 9.3: Public path – skip search → platform searchability question
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Choose Public → Skip create new. | Platform searchability question appears. | |
| 2 | Choose Company Network Only. | Event saves with `IsSharedWithPlatform=False` and no pending review. | |
| 3 | Choose Share with Platform (in a new attempt). | Event saves with `IsSharedWithPlatform=True` and `PublicReviewStatusID=PENDING`. | |

#### Test 9.4: Review status badges and feedback panels
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Open an event in PENDING. | Pending status badge and messaging are visible. | |
| 2 | Approve event as admin; reopen as creator. | Approved status shown; guidance indicates publish requirement (if applicable). | |
| 3 | Reject event as admin; reopen as creator. | Rejected status shown; feedback visible; resubmission guidance present. | |

---

### Category 10: Offline-first capability (if enabled in your environment)

#### Test 10.1: Offline indicator appears when offline
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Open app while online. | Offline indicator shows “online” or is hidden per design. | |
| 2 | Disconnect network (DevTools offline). | Offline indicator shows offline state. | |

#### Test 10.2: Create event while offline queues request
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | While offline, attempt to create an event. | UI does not crash; request is queued (or user gets clear offline messaging). | |
| 2 | Restore network. | Queue processes automatically; event is created successfully. | |

#### Test 10.3: Draft restoration
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|----------|
| 1 | Start creating an event and enter some fields. | Draft autosaves periodically. | |
| 2 | Refresh/reopen create modal. | Draft restore prompt appears and restores entered data. | |

---

## 📊 UAT Summary (To be completed by testers)

| Category | Tests | Pass | Fail | Notes |
|----------|------:|-----:|-----:|-------|
| 1. Event Creation (Guard 1) | 5 | | | |
| 2. Update IsPublic (Guard 2) | 3 | | | |
| 3. Update IsSharedWithPlatform (Guard 4A) | 4 | | | |
| 4. Update EventStatus (Guard 4B) | 3 | | | |
| 5. Admin Review (Guard 3) | 5 | | | |
| 6. Visibility Queries | 3 | | | |
| 7. Admin Queue Guards | 2 | | | |
| 8. Data Integrity | 2 | | | |
| 9. Frontend UX/Integration | 4 | | | |
| 10. Offline-first (optional) | 3 | | | |

---

## 📝 Notes for Testers

- **Admin approval is a quality gate:** approving/rejecting must not change `EventStatusID` (user-controlled).
- **Platform-wide visibility requires all conditions:** `IsPublic=True` AND `IsSharedWithPlatform=True` AND `PublicReviewStatusID=APPROVED` AND `EventStatusID=PUBLISHED`.
- **Safety:** broken/invalid state transitions must be blocked or corrected safely; no crashes.

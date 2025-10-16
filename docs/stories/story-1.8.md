# Story 1.8: Multi-Tenant Data Isolation & Testing

Status: Approved

## Story

As a platform administrator,
I want comprehensive data isolation and role-based access control testing,
so that I can ensure users only access their company's data and security is enforced.

## Acceptance Criteria

1. **AC-1.8.1**: All company-scoped queries filter by company_id from JWT
2. **AC-1.8.2**: Users cannot access other companies' data
3. **AC-1.8.3**: Company admins can only manage their own company
4. **AC-1.8.4**: Company users can only view their own company's data
5. **AC-1.8.5**: Role requirements enforced on all protected endpoints
6. **AC-1.8.6**: Comprehensive test suite validates data isolation
7. **AC-1.8.7**: Security tests verify users cannot bypass multi-tenancy
8. **AC-1.8.8**: Performance tests verify filtering doesn't impact queries
9. **AC-1.8.9**: Database helper functions enforce company filtering
10. **AC-1.8.10**: Audit logs capture all cross-company access attempts

## Tasks / Subtasks

- [ ] **Task 1: Create Multi-Tenant Query Helpers** (AC: 1.8.1, 1.8.9)
  - [ ] Create `backend/common/multi_tenant.py`
  - [ ] Implement filter_by_company(query, company_id) helper
  - [ ] Implement get_current_company_id() from request context
  - [ ] Auto-apply company filter to all company-scoped queries
  - [ ] Test: Query helpers work correctly

- [ ] **Task 2: Update All Company-Scoped Endpoints** (AC: 1.8.1, 1.8.2)
  - [ ] Review all existing endpoints
  - [ ] Add company_id filtering to queries
  - [ ] Verify company_id matches current user's company
  - [ ] Test: Company filtering applied correctly

- [ ] **Task 3: Create Data Isolation Tests** (AC: 1.8.2, 1.8.6)
  - [ ] Create test_multi_tenancy.py
  - [ ] Create two companies with test data
  - [ ] Test: User A cannot access Company B's data
  - [ ] Test: User B cannot access Company A's data
  - [ ] Test: API endpoints enforce company filtering
  - [ ] Test: Database queries enforce company filtering

- [ ] **Task 4: Create Role-Based Access Tests** (AC: 1.8.3, 1.8.4, 1.8.5)
  - [ ] Create test_rbac.py
  - [ ] Test: Company admin can invite team members
  - [ ] Test: Company user cannot invite team members
  - [ ] Test: Company admin can manage company settings
  - [ ] Test: Company user cannot manage company settings
  - [ ] Test: Role requirements enforced on all endpoints

- [ ] **Task 5: Create Security Tests** (AC: 1.8.7)
  - [ ] Create test_security.py
  - [ ] Test: Cannot forge JWT with different company_id
  - [ ] Test: Cannot manipulate company_id in request body
  - [ ] Test: Cannot access resources via direct ID manipulation
  - [ ] Test: Cannot escalate privileges via role manipulation

- [ ] **Task 6: Create Performance Tests** (AC: 1.8.8)
  - [ ] Create test_performance.py
  - [ ] Create large dataset (multiple companies, many records)
  - [ ] Benchmark query performance with company filtering
  - [ ] Verify indexes are used correctly
  - [ ] Test: Filtering adds minimal overhead

- [ ] **Task 7: Implement Cross-Company Access Logging** (AC: 1.8.10)
  - [ ] Log all denied access attempts
  - [ ] Include attempted company_id and user's actual company_id
  - [ ] Create alerts for suspicious patterns
  - [ ] Test: Denied access logged correctly

- [ ] **Task 8: Create Multi-Tenant Testing Utilities** (AC: 1.8.6)
  - [ ] Create test_utils.py
  - [ ] Implement create_test_company() helper
  - [ ] Implement create_test_user() helper
  - [ ] Implement create_test_data() helper
  - [ ] Make it easy to create multi-tenant test scenarios

- [ ] **Task 9: Database Constraints Review** (AC: 1.8.2)
  - [ ] Review all foreign keys
  - [ ] Verify referential integrity
  - [ ] Add additional constraints if needed
  - [ ] Test: Database constraints prevent data leaks

- [ ] **Task 10: Documentation** (AC: All)
  - [ ] Document multi-tenancy architecture
  - [ ] Document query patterns
  - [ ] Document testing strategies
  - [ ] Create security guidelines

## Dev Notes

### Multi-Tenant Query Pattern

**Standard Pattern:**
```python
# ❌ BAD: No company filtering
@router.get("/events")
async def get_events(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    events = db.query(Event).all()  # Returns ALL companies' events!
    return events

# ✅ GOOD: Company filtering
@router.get("/events")
async def get_events(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.company_id:
        raise HTTPException(status_code=403, detail="No company context")
    
    events = db.query(Event).filter(
        Event.CompanyID == current_user.company_id
    ).all()
    return events

# ✅ BEST: Using helper
@router.get("/events")
async def get_events(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Event)
    query = filter_by_company(query, current_user.company_id)
    events = query.all()
    return events
```

**Multi-Tenant Query Helper:**
```python
# backend/common/multi_tenant.py
from sqlalchemy.orm import Query
from fastapi import HTTPException, status

def filter_by_company(query: Query, company_id: int) -> Query:
    """
    Apply company filter to query.
    Ensures multi-tenant data isolation.
    """
    if not company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No company context. Please complete onboarding."
        )
    
    # Assuming model has CompanyID attribute
    return query.filter_by(CompanyID=company_id)

def verify_company_access(resource_company_id: int, user_company_id: int):
    """
    Verify user has access to resource's company.
    Raises 403 if companies don't match.
    """
    if resource_company_id != user_company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Resource belongs to different company."
        )
```

**Example Multi-Tenant Endpoint:**
```python
@router.get("/companies/{company_id}/events")
async def get_company_events(
    company_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify user belongs to company
    if current_user.company_id != company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access different company's data"
        )
    
    # Query with company filter
    events = db.query(Event).filter(
        Event.CompanyID == company_id
    ).all()
    
    return events
```

### Testing Multi-Tenancy

**Data Isolation Test:**
```python
def test_data_isolation_between_companies(client, db):
    # Create Company A with User A
    company_a = create_test_company(db, "Company A")
    user_a = create_test_user(db, "user_a@test.com", company_a.CompanyID)
    token_a = create_test_token(user_a)
    
    # Create Company B with User B
    company_b = create_test_company(db, "Company B")
    user_b = create_test_user(db, "user_b@test.com", company_b.CompanyID)
    token_b = create_test_token(user_b)
    
    # Create event for Company A
    event_a = create_test_event(db, company_a.CompanyID, "Event A")
    
    # User A can access their event
    response = client.get(
        f"/api/events/{event_a.EventID}",
        headers={"Authorization": f"Bearer {token_a}"}
    )
    assert response.status_code == 200
    
    # User B cannot access Company A's event
    response = client.get(
        f"/api/events/{event_a.EventID}",
        headers={"Authorization": f"Bearer {token_b}"}
    )
    assert response.status_code == 403
```

**Role-Based Access Test:**
```python
def test_company_admin_can_invite_company_user_cannot(client, db):
    # Create company
    company = create_test_company(db, "Test Company")
    
    # Create admin user
    admin = create_test_user(db, "admin@test.com", company.CompanyID, role="company_admin")
    admin_token = create_test_token(admin)
    
    # Create regular user
    user = create_test_user(db, "user@test.com", company.CompanyID, role="company_user")
    user_token = create_test_token(user)
    
    # Admin can invite
    response = client.post(
        f"/api/companies/{company.CompanyID}/invite",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"email": "new@test.com", "role": "company_user"}
    )
    assert response.status_code == 201
    
    # Regular user cannot invite
    response = client.post(
        f"/api/companies/{company.CompanyID}/invite",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"email": "another@test.com", "role": "company_user"}
    )
    assert response.status_code == 403
```

### Security Checklist

- [ ] All company-scoped endpoints filter by company_id
- [ ] Company_id extracted from JWT (not request body)
- [ ] Users cannot forge JWT tokens
- [ ] Users cannot access other companies' data via direct IDs
- [ ] Role requirements enforced on all protected endpoints
- [ ] Failed access attempts logged
- [ ] Database foreign keys enforce referential integrity
- [ ] Indexes support efficient company filtering

### References

- [Story 1.3: RBAC Middleware](docs/stories/story-1.3.md)
- [Story 1.5: First-Time Onboarding](docs/stories/story-1.5.md)
- [Story 1.6: Team Invitation System](docs/stories/story-1.6.md)
- [Story 1.7: Invited User Acceptance](docs/stories/story-1.7.md)

## Dev Agent Record

### Context Reference

- [Story Context 1.8](../story-context-1.8.xml) - To be generated

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List


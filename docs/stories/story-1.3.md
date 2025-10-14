# Story 1.3: First-Time User Onboarding (Company Creator)

Status: ContextReadyDraft

## Story

As a **verified EventLead Platform user**,
I want **to complete a multi-step onboarding process to set up my user profile and create my company**,
so that **I can become a Company Admin and start using the platform for event lead generation**.

## Acceptance Criteria

1. **AC-3.1:** User redirected to onboarding after email verification
2. **AC-3.2:** System presents 2-step onboarding flow with progress indicator
3. **AC-3.3:** **Step 1 - User Details:** User can enter first name, last name, role title (optional), phone (optional)
4. **AC-3.4:** System validates required fields and Australian phone format (+61)
5. **AC-3.5:** System saves user details and navigates to Step 2
6. **AC-3.6:** **Step 2 - Company Setup:** User can enter company name, ABN, billing address
7. **AC-3.7:** System provides enhanced company search with auto-detection (ABN/ACN/Name)
8. **AC-3.8:** System validates search results via ABR API with enterprise-grade caching (300x faster)
9. **AC-3.9:** System achieves ~90% search success rate (up from ~20%) with smart search UX
10. **AC-3.10:** System validates Australian address (state dropdown, 4-digit postcode)
11. **AC-3.11:** System saves company details and creates UserCompany relationship with Company Admin role
12. **AC-3.12:** System redirects to dashboard upon completion
13. **AC-3.13:** System logs all onboarding activities for audit trail
14. **AC-3.14:** User can save progress and resume later (auto-save functionality)

## Tasks / Subtasks

- [ ] **Backend Onboarding Service** (AC: 3.1, 3.5, 3.11, 3.13)
  - [ ] Create `backend/modules/users/router.py` with onboarding endpoints
  - [ ] Create `backend/modules/users/service.py` with onboarding business logic
  - [ ] Implement user details update endpoint
  - [ ] Implement company creation endpoint
  - [ ] Create UserCompany relationship with Company Admin role
  - [ ] Implement activity logging for onboarding events
  - [ ] Add auto-save functionality with draft state management

- [ ] **Enhanced ABR Search Integration** (AC: 3.7, 3.8, 3.9)
  - [ ] Create `backend/modules/companies/abr_client.py` for ABR API integration
  - [ ] Create `backend/modules/companies/cache_service.py` for enterprise-grade caching
  - [ ] Implement smart search detection (ABN/ACN/Company Name patterns)
  - [ ] Add search result caching with 30-day TTL
  - [ ] Implement search result validation and data enrichment
  - [ ] Add search analytics and success rate tracking

- [ ] **Company Management Service** (AC: 3.6, 3.10, 3.11)
  - [ ] Create `backend/modules/companies/router.py` with company endpoints
  - [ ] Create `backend/modules/companies/service.py` with company business logic
  - [ ] Implement company creation with validation
  - [ ] Add Australian address validation (state dropdown, postcode)
  - [ ] Implement ABN validation using ABR API
  - [ ] Create company audit trail and activity logging

- [ ] **Frontend Onboarding Flow** (AC: 3.2, 3.3, 3.4, 3.5)
  - [ ] Create `frontend/features/onboarding/components/OnboardingFlow.tsx`
  - [ ] Create `frontend/features/onboarding/components/OnboardingStep1.tsx` (User Details)
  - [ ] Implement form validation with react-hook-form
  - [ ] Add Australian phone format validation (+61)
  - [ ] Implement progress indicator component
  - [ ] Add loading states and error handling
  - [ ] Implement auto-save functionality with draft state

- [ ] **Frontend Company Setup** (AC: 3.6, 3.7, 3.9, 3.10)
  - [ ] Create `frontend/features/onboarding/components/OnboardingStep2.tsx` (Company Setup)
  - [ ] Create `frontend/features/companies/components/SmartCompanySearch.tsx`
  - [ ] Create `frontend/features/companies/components/CompanySearchResults.tsx`
  - [ ] Implement enhanced search UX with auto-detection
  - [ ] Add Australian address components (state dropdown, postcode validation)
  - [ ] Implement search result selection and confirmation
  - [ ] Add search success rate feedback and optimization

- [ ] **Database Schema Implementation** (AC: 3.11, 3.13)
  - [ ] Create User table with onboarding fields
  - [ ] Create Company table with audit trail
  - [ ] Create UserCompany junction table for role management
  - [ ] Create CompanyCustomerDetails, CompanyBillingDetails, CompanyOrganizerDetails tables
  - [ ] Create ABRSearchCache table for search optimization
  - [ ] Add proper foreign key relationships and constraints
  - [ ] Implement activity logging tables

- [ ] **Validation and Error Handling** (AC: 3.4, 3.10)
  - [ ] Implement Australian phone number validation
  - [ ] Implement Australian address validation
  - [ ] Add ABN format validation
  - [ ] Create comprehensive error handling for all validation scenarios
  - [ ] Implement user-friendly error messages
  - [ ] Add field-level validation feedback

- [ ] **Auto-Save and Progress Management** (AC: 3.14)
  - [ ] Implement auto-save functionality for onboarding steps
  - [ ] Create draft state management system
  - [ ] Add progress tracking and resume capability
  - [ ] Implement session management for onboarding flow
  - [ ] Add progress persistence across browser sessions

- [ ] **Testing Implementation** (All ACs)
  - [ ] Unit tests for onboarding service logic
  - [ ] Unit tests for ABR search integration and caching
  - [ ] Unit tests for company creation and validation
  - [ ] Integration tests for complete onboarding flow
  - [ ] Integration tests for ABR search and validation
  - [ ] E2E tests for browser onboarding flow
  - [ ] Performance tests for ABR search caching

## Dev Notes

### Architecture Patterns and Constraints
- **Multi-step Onboarding**: Progressive form completion with validation at each step
- **Enhanced ABR Search**: Enterprise-grade caching with 300x performance improvement
- **Multi-tenant Foundation**: Company creation establishes tenant boundary
- **Role-based Access**: First user becomes Company Admin automatically
- **Activity Logging**: Comprehensive audit trail for compliance and debugging
- **Auto-save Functionality**: User can save progress and resume later

### Project Structure Notes
- **Backend**: `backend/modules/users/` and `backend/modules/companies/` for business logic
- **Frontend**: `frontend/features/onboarding/` for onboarding flow components
- **Search Integration**: `backend/modules/companies/abr_client.py` and `cache_service.py`
- **Database**: User, Company, UserCompany, and related detail tables
- **Validation**: Country-specific validation rules via ValidationRule table

### Enhanced ABR Search Features
- **Smart Detection**: Automatically detects ABN, ACN, or Company Name patterns
- **Enterprise Caching**: 30-day TTL with 300x performance improvement
- **Search Analytics**: Success rate tracking and optimization
- **Data Enrichment**: ABR API integration for real-time validation

### Testing Standards Summary
- **Unit Tests**: 80%+ coverage for onboarding and company modules
- **Integration Tests**: Complete onboarding flow with ABR search
- **E2E Tests**: Browser onboarding flow with company creation
- **Performance Tests**: ABR search caching and response times
- **Search Tests**: ABR API integration and validation accuracy

### Onboarding Flow Structure
```
Step 1: User Details
├── First Name (required)
├── Last Name (required)
├── Role Title (optional)
└── Phone (optional, Australian format)

Step 2: Company Setup
├── Company Name (required)
├── ABN (optional, with validation)
├── Enhanced Search (ABR API integration)
└── Billing Address (Australian validation)
```

### References
- **Technical Specification**: [Source: docs/tech-spec-epic-1.md#AC-3-First-Time-User-Onboarding]
- **Enhanced ABR Search**: [Source: docs/tech-spec-epic-1.md#Enhanced-ABR-Search-Implementation]
- **Company Domain Schema**: [Source: docs/tech-spec-epic-1.md#Company-Domain-Schema]
- **UX Design**: [Source: docs/tech-spec-epic-1.md#UX-Design-Specifications]
- **Database Schema**: [Source: docs/tech-spec-epic-1.md#Database-Schema-Implementation]

## Dev Agent Record

### Context Reference
- docs/story-context-1.3.xml

### Agent Model Used
{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

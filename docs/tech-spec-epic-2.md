# Technical Specification: Epic 2 - Enhanced User Experience & Multi-Domain Integration

Date: 2025-01-15
Author: Anthony Keevy
Epic ID: Epic 2
Status: Draft

---

## Overview

Epic 2: Enhanced User Experience & Multi-Domain Integration represents the next phase of the EventLead Platform MVP, building on the solid Epic 1 foundation. This epic focuses on delivering personalized user experiences, streamlined approval workflows, comprehensive event management, and form foundation capabilities. The technical implementation emphasizes Anthony's learning journey while delivering production-ready features that prepare the platform for Epic 3's complex Form Builder.

The epic addresses the natural evolution of user needs: enhanced personalization through theme systems and user preferences, enterprise-grade approval workflows with external approver support, complete event lifecycle management with multi-tenant filtering, and foundational form management capabilities. These enhancements will significantly improve user satisfaction, enable enterprise customers with complex approval requirements, and establish the technical foundation for future form builder capabilities while maintaining the solid Epic 1 foundation.

## Objectives and Scope

**In Scope:**
- Enhanced user profile management with bio, theme preferences, layout density, and font size options
- Multiple industry associations through junction table system with primary/secondary industry support
- Comprehensive theme system (light/dark/high-contrast/system) with CSS custom properties
- Approval workflow extensions for form deployment costs with configurable thresholds
- External approver support via email without requiring platform accounts
- Complete event lifecycle management with multi-tenant filtering and public review process
- Form header creation and access control foundation for Epic 3 Form Builder
- Cross-domain integration ensuring seamless data flow between User, Company, Events, and Forms domains
- Enhanced diagnostic logging with request/response payloads, stack traces, and performance metrics
- Backward compatibility with all Epic 1 functionality
- Performance optimization maintaining or improving existing system performance

**Out of Scope:**
- Complete Form Builder implementation (deferred to Epic 3+)
- Form submission handling and response capture (deferred to Epic 3+)
- Advanced analytics and reporting features (deferred to Epic 3+)
- CRM integrations and third-party API access (deferred to Epic 4+)
- Mobile app development (deferred to Epic 4+)
- Advanced team permissions beyond Admin/User roles (deferred to Epic 4+)
- Multi-language support and internationalization (deferred to Epic 4+)

## System Architecture Alignment

Epic 2 builds upon the proven Epic 1 architecture while introducing enhanced patterns for cross-domain integration and user experience personalization. The architecture maintains the database-first approach that leverages Anthony's data engineering strengths while introducing frontend component patterns that support his learning journey.

**Core Architecture Components:**
- **Database Layer**: Extends Epic 1 schema with 15+ new tables maintaining naming conventions and audit patterns
- **Backend Services**: Domain-based service organization with repository patterns and event-driven cross-domain communication
- **Frontend Components**: React Context + useReducer for state management with domain-based component organization
- **API Layer**: RESTful endpoints maintaining Epic 1 patterns with enhanced error handling and audit logging
- **Integration Layer**: Event bus for cross-domain communication with polling-based real-time updates

**Key Architectural Constraints:**
- Maintain Epic 1 performance characteristics (dashboard < 2s, theme switching < 500ms)
- Preserve all existing Epic 1 functionality without breaking changes
- Support Epic 3 Form Builder preparation through component reusability and state management patterns
- Enable learning-focused development with detailed component relationships and data flow documentation

## Detailed Design

### Services and Modules

| Service/Module | Responsibility | Inputs | Outputs | Owner |
|----------------|----------------|--------|---------|-------|
| **UserService** | Profile management, preferences, industry associations | User profile data, theme preferences, industry IDs | Updated user entity, audit logs | User Domain |
| **CompanyService** | Approval workflows, external approvers, billing relationships | Approval requests, external approver data, billing info | Approval decisions, audit trails | Company Domain |
| **EventsService** | Event CRUD operations, multi-tenant filtering, public review | Event data, company context, review decisions | Event entities, filtered lists | Events Domain |
| **FormsService** | Form header management, access control, status tracking | Form metadata, access permissions, status updates | Form entities, access control lists | Forms Domain |
| **AuditService** | Cross-domain audit logging, compliance tracking | Action data, entity references, user context | Audit trail records | Cross-Domain |
| **ThemeService** | Theme system management, CSS custom properties | Theme preferences, layout density, font size | Applied themes, CSS variables | Frontend |
| **EventBus** | Cross-domain communication, real-time updates | Domain events, subscriber callbacks | Event notifications, state updates | Integration |
| **PollingService** | Real-time data synchronization, update notifications | Polling intervals, API endpoints | Updated data, UI refreshes | Frontend |

### Data Models and Contracts

**User Domain Extensions:**
```sql
-- User table extensions
ALTER TABLE dbo.User ADD
    Bio NVARCHAR(500) NULL,
    ThemePreferenceID BIGINT NULL,
    LayoutDensityID BIGINT NULL,
    FontSizeID BIGINT NULL,
    IsExternalApprover BIT NOT NULL DEFAULT 0;

-- User-Industry junction table
CREATE TABLE dbo.UserIndustry (
    UserIndustryID BIGINT IDENTITY(1,1) PRIMARY KEY,
    UserID BIGINT NOT NULL,
    IndustryID BIGINT NOT NULL,
    IsPrimary BIT NOT NULL DEFAULT 0,
    PriorityOrder INT NULL,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (UserID) REFERENCES dbo.User(UserID),
    FOREIGN KEY (IndustryID) REFERENCES dbo.Industry(IndustryID)
);
```

**Events Domain (New):**
```sql
-- Core Event table
CREATE TABLE dbo.Event (
    EventID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CompanyID BIGINT NOT NULL,
    Name NVARCHAR(200) NOT NULL,
    Description NVARCHAR(MAX) NULL,
    EventTypeID INT NOT NULL,
    EventStatusID INT NOT NULL,
    StartDateTime DATETIME2 NOT NULL,
    EndDateTime DATETIME2 NULL,
    VenueName NVARCHAR(200) NULL,
    City NVARCHAR(100) NULL,
    IsPublic BIT NOT NULL DEFAULT 0,
    CreatedBy BIGINT NOT NULL,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (CompanyID) REFERENCES dbo.Company(CompanyID),
    FOREIGN KEY (EventTypeID) REFERENCES ref.EventType(EventTypeID),
    FOREIGN KEY (EventStatusID) REFERENCES ref.EventStatus(EventStatusID),
    FOREIGN KEY (CreatedBy) REFERENCES dbo.User(UserID)
);
```

**Forms Domain (Foundation):**
```sql
-- Form header table
CREATE TABLE dbo.Form (
    FormID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CompanyID BIGINT NOT NULL,
    EventID BIGINT NULL,
    Name NVARCHAR(200) NOT NULL,
    Description NVARCHAR(1000) NULL,
    FormStatusID BIGINT NOT NULL,
    CreatedBy BIGINT NOT NULL,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (CompanyID) REFERENCES dbo.Company(CompanyID),
    FOREIGN KEY (EventID) REFERENCES dbo.Event(EventID),
    FOREIGN KEY (FormStatusID) REFERENCES ref.FormStatus(FormStatusID),
    FOREIGN KEY (CreatedBy) REFERENCES dbo.User(UserID)
);
```

**Pydantic Schemas:**
```python
# User Profile Schema
class UserProfileUpdate(BaseModel):
    bio: Optional[str] = None
    theme_preference_id: Optional[int] = None
    layout_density_id: Optional[int] = None
    font_size_id: Optional[int] = None

# Event Schema
class EventCreate(BaseModel):
    name: str
    description: Optional[str] = None
    event_type_id: int
    start_datetime: datetime
    end_datetime: Optional[datetime] = None
    venue_name: Optional[str] = None
    city: Optional[str] = None
    is_public: bool = False

# Form Header Schema
class FormHeaderCreate(BaseModel):
    name: str
    description: Optional[str] = None
    event_id: Optional[int] = None
    form_status_id: int
```

### APIs and Interfaces

**User Domain API:**
```python
# User Profile Management
GET    /api/v1/users/profile                    # Get current user profile
PUT    /api/v1/users/profile                    # Update user profile
GET    /api/v1/users/{user_id}                  # Get user by ID (team members)

# Theme and Preferences
GET    /api/v1/users/preferences                # Get user preferences
PUT    /api/v1/users/preferences                # Update user preferences
GET    /api/v1/users/preferences/themes         # Get available themes
GET    /api/v1/users/preferences/densities      # Get available layout densities
GET    /api/v1/users/preferences/font-sizes     # Get available font sizes

# Industry Management
GET    /api/v1/users/industries                 # Get user's industries
POST   /api/v1/users/industries                 # Add industry to user
PUT    /api/v1/users/industries/{industry_id}   # Update industry priority
DELETE /api/v1/users/industries/{industry_id}   # Remove industry from user
```

**Events Domain API:**
```python
# Event Management
GET    /api/v1/events                          # Get company events
POST   /api/v1/events                          # Create event
GET    /api/v1/events/{event_id}               # Get event details
PUT    /api/v1/events/{event_id}               # Update event
DELETE /api/v1/events/{event_id}               # Delete event

# Event Types and Status
GET    /api/v1/events/types                    # Get event types
GET    /api/v1/events/statuses                 # Get event statuses

# Event Forms
GET    /api/v1/events/{event_id}/forms         # Get forms for event
POST   /api/v1/events/{event_id}/forms         # Create form for event
```

**Forms Domain API:**
```python
# Form Header Management
GET    /api/v1/forms                           # Get company forms
POST   /api/v1/forms                           # Create form header
GET    /api/v1/forms/{form_id}                 # Get form details
PUT    /api/v1/forms/{form_id}                 # Update form header
DELETE /api/v1/forms/{form_id}                 # Delete form

# Form Access Control
GET    /api/v1/forms/{form_id}/access          # Get form access control
POST   /api/v1/forms/{form_id}/access          # Grant form access
PUT    /api/v1/forms/{form_id}/access/{id}     # Update form access
DELETE /api/v1/forms/{form_id}/access/{id}     # Revoke form access
```

**Error Response Format:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "name",
        "message": "Name is required"
      }
    ],
    "request_id": "req_12345",
    "timestamp": "2025-01-15T10:30:00Z"
  }
}
```

### Workflows and Sequencing

**User Profile Enhancement Workflow:**
1. User accesses profile settings page
2. System loads current user preferences and available options
3. User updates bio, theme preference, layout density, or font size
4. Frontend validates input and sends API request
5. Backend updates user record and logs audit trail
6. System applies theme changes immediately via CSS custom properties
7. Frontend polls for preference updates across all components

**Approval Workflow Sequence:**
1. User creates form with deployment cost calculation
2. System checks cost against company approval threshold
3. If threshold exceeded, creates approval request with audit trail
4. System routes to designated approver (internal or external)
5. Approver receives notification and reviews request
6. Approver makes decision with comments
7. System processes approval and enables form deployment
8. User receives notification of approval decision

**Event Creation and Management Workflow:**
1. User navigates to events section
2. System loads company-scoped event list with filtering
3. User creates new event with metadata and location details
4. System validates event data and applies multi-tenant filtering
5. If public event, triggers review process with admin notification
6. Event appears in company event list with appropriate status
7. User can create forms associated with approved events

**Cross-Domain Integration Flow:**
1. User changes theme preference in User domain
2. EventBus publishes theme_changed event
3. All domain components subscribe and update UI
4. AuditService logs user action across domains
5. PollingService updates real-time data for affected components
6. System maintains consistent state across all domains

## Non-Functional Requirements

### Performance

**Response Time Requirements:**
- Dashboard loading: < 2 seconds (maintain Epic 1 performance)
- Theme switching: < 500ms (immediate visual feedback)
- API response times: < 1 second for standard operations
- Real-time updates: 5-second polling interval with debounced updates

**Throughput Requirements:**
- Support same user load as Epic 1 (no degradation)
- Approval workflows: Handle 100+ concurrent approval requests
- Event management: Support 1000+ events per company
- Form operations: Maintain Epic 1 form creation performance

**Scalability Targets:**
- Database queries: Optimized with composite indexes for multi-tenant filtering
- Caching strategy: React Query for API responses, local storage for preferences
- Polling optimization: Intelligent intervals based on user activity
- Component rendering: Memoization for expensive operations

### Security

**Authentication and Authorization:**
- JWT token management with secure storage and refresh mechanism
- Role-based access control maintaining Epic 1 patterns
- Multi-tenant data isolation with company-scoped queries
- External approver email verification without platform accounts

**Data Protection:**
- Input validation with Pydantic schemas for all API endpoints
- SQL injection prevention through parameterized queries
- Audit trail immutability with secure log access
- Cross-tenant access prevention through repository patterns

**API Security:**
- Rate limiting for all API endpoints
- Request/response payload logging (sanitized for sensitive data)
- CORS configuration for frontend integration
- Error handling without information disclosure

### Reliability/Availability

**Availability Targets:**
- Maintain Epic 1 uptime (99.9% availability)
- Zero downtime deployment with database migration rollback capability
- Graceful degradation for non-critical features during maintenance

**Error Handling:**
- Comprehensive error boundaries in React components
- Graceful API error handling with user-friendly messages
- Database transaction rollback for failed operations
- Audit trail preservation during system errors

**Recovery Procedures:**
- Database migration rollback strategy for Epic 2 changes
- Epic 1 functionality preservation during Epic 2 deployment
- Real-time data synchronization recovery after network issues
- Theme system fallback to default settings on errors

### Observability

**Enhanced Diagnostic Logging:**
- Request/response payload logging for all API endpoints
- Stack trace logging for all application errors
- User action tracking for theme changes, preference updates, navigation
- Performance metrics logging for slow queries and API response times
- Cross-domain integration event logging for audit trails

**Monitoring Requirements:**
- Azure Application Insights integration for production monitoring
- Custom Epic 2 metrics (theme switching, approval workflows, event management)
- Real-time error correlation across domains
- Performance monitoring with alerting for degradation

**Logging Strategy:**
- Structured JSON logging with correlation IDs
- Log levels: DEBUG (development), INFO (operations), WARN (issues), ERROR (failures), CRITICAL (system failures)
- Audit trail immutability with secure access controls
- Diagnostic tool integration for BMAD agent debugging

## Dependencies and Integrations

**Backend Dependencies (Python 3.13):**
- **FastAPI 0.115.7**: Web framework for API endpoints
- **SQLAlchemy 2.0.40**: ORM for database operations
- **Alembic 1.14.1**: Database migration management
- **Pydantic 2.10.6**: Data validation and serialization
- **PyODBC 5.2.0**: MS SQL Server connectivity
- **Azure SDKs**: Storage blob and communication services
- **Structlog 24.4.0**: Enhanced logging capabilities

**Frontend Dependencies (React 18.2.0):**
- **React 18.2.0**: Core UI framework
- **TypeScript 5.2.2**: Type safety and development experience
- **Tailwind CSS 3.3.5**: Utility-first styling framework
- **Axios 1.6.2**: HTTP client for API communication
- **React Query 5.8.4**: Data fetching and caching
- **React Hook Form 7.48.2**: Form management
- **Framer Motion 10.16.5**: Animation and transitions
- **Zustand 4.4.6**: State management (alternative to Context)

**External Service Integrations:**
- **Azure App Service**: Hosting platform (Epic 1 foundation)
- **Azure SQL Database**: Primary database (Epic 1 foundation)
- **Azure Blob Storage**: File storage (Epic 1 foundation)
- **Azure Communication Services**: Email delivery (Epic 1 foundation)
- **Azure Application Insights**: Monitoring and observability

**Development Dependencies:**
- **Pytest 8.3.5**: Backend testing framework
- **Vitest 1.0.4**: Frontend testing framework
- **ESLint 8.54.0**: Code linting and quality
- **Prettier 3.1.0**: Code formatting
- **Black 24.10.0**: Python code formatting

## Acceptance Criteria (Authoritative)

1. **User Profile Enhancement**: Users can update bio, theme preferences, layout density, and font size with immediate UI updates
2. **Multiple Industry Support**: Users can associate with multiple industries with primary/secondary designation and priority ordering
3. **Theme System Implementation**: CSS custom properties enable seamless theme switching across all UI components
4. **Approval Workflow Extension**: Form deployment costs trigger approval workflows with configurable thresholds and external approver support
5. **Event Management**: Users can create, update, and manage events with multi-tenant filtering and public review process
6. **Form Header Foundation**: Users can create form headers with metadata and access control for Epic 3 preparation
7. **Cross-Domain Integration**: Theme changes and user actions propagate across all domains via event bus
8. **Enhanced Logging**: All API requests include payload logging, errors include stack traces, and user actions are tracked
9. **Backward Compatibility**: All Epic 1 functionality remains unchanged and fully operational
10. **Performance Maintenance**: Dashboard loads < 2 seconds, theme switching < 500ms, no performance degradation
11. **Audit Trail Compliance**: All approval decisions, user actions, and data changes are logged with complete audit trails
12. **Database Migration Safety**: Epic 2 migrations are reversible with zero data loss and Epic 1 preservation

## Traceability Mapping

| AC | Spec Section | Component/API | Test Idea |
|----|--------------|---------------|-----------|
| **AC1** | User Profile Enhancement | UserService, ProfileEditor.tsx, /api/v1/users/profile | Test bio update, theme switching, immediate UI updates |
| **AC2** | Multiple Industry Support | UserIndustry table, IndustrySelector.tsx, /api/v1/users/industries | Test primary/secondary industry assignment, priority ordering |
| **AC3** | Theme System Implementation | ThemeProvider.tsx, CSS custom properties, ThemeSelector.tsx | Test theme switching across all components, CSS variable updates |
| **AC4** | Approval Workflow Extension | CompanyService, ApprovalDashboard.tsx, /api/v1/companies/approvals | Test cost threshold triggering, external approver email flow |
| **AC5** | Event Management | EventsService, EventEditor.tsx, /api/v1/events | Test event CRUD, multi-tenant filtering, public review process |
| **AC6** | Form Header Foundation | FormsService, FormEditor.tsx, /api/v1/forms | Test form header creation, access control, Epic 3 preparation |
| **AC7** | Cross-Domain Integration | EventBus, PollingService, ThemeContext | Test theme propagation, real-time updates across domains |
| **AC8** | Enhanced Logging | AuditService, enhanced_diagnostic_logs.py | Test payload logging, stack traces, user action tracking |
| **AC9** | Backward Compatibility | All Epic 1 components and APIs | Test Epic 1 regression, no breaking changes |
| **AC10** | Performance Maintenance | All components, database queries, caching | Test response times, theme switching speed, load testing |
| **AC11** | Audit Trail Compliance | AuditService, ApprovalAuditTrail table | Test audit logging, compliance reporting, data integrity |
| **AC12** | Database Migration Safety | Alembic migrations, rollback procedures | Test migration rollback, data preservation, Epic 1 functionality |

## Risks, Assumptions, Open Questions

**Risks:**
- **Performance Degradation**: Adding theme system and real-time updates may impact Epic 1 performance
  - *Mitigation*: Comprehensive performance testing, caching strategies, component memoization
- **Database Migration Complexity**: Epic 2 schema changes may conflict with Epic 1 data
  - *Mitigation*: Thorough migration testing, rollback procedures, Epic 1 regression testing
- **Cross-Domain Integration Complexity**: Event bus and polling may introduce state synchronization issues
  - *Mitigation*: Simple polling strategy, comprehensive integration testing, fallback mechanisms

**Assumptions:**
- Epic 1 database schema and API patterns remain stable during Epic 2 development
- Azure services (App Service, SQL Database, Blob Storage) maintain Epic 1 performance characteristics
- Users will adopt new theme and preference features gradually without requiring extensive training
- External approvers will engage with email-based approval workflows without platform accounts

**Open Questions:**
- Should we implement WebSocket real-time updates in Epic 2 or defer to Epic 3?
- What is the optimal polling interval for real-time updates to balance performance and user experience?
- How should we handle theme conflicts when multiple users in the same company have different preferences?
- What is the expected volume of approval requests per company to optimize workflow performance?

## Test Strategy Summary

**Unit Testing:**
- **Frontend**: Component testing with React Testing Library, hook testing with custom utilities, service testing with mocked APIs
- **Backend**: Service testing with mocked repositories, API endpoint testing with FastAPI TestClient, repository testing with test database
- **Coverage Target**: 80% code coverage for new Epic 2 components and services

**Integration Testing:**
- **Cross-Domain**: Event bus integration testing, real-time update testing, cross-domain data synchronization testing
- **Database**: Migration testing with rollback, data integrity testing, performance testing with large datasets
- **API**: End-to-end API testing with real database, authentication flow testing, error handling validation

**End-to-End Testing:**
- **User Workflows**: Complete user journeys for profile enhancement, approval workflows, event management, form creation
- **Cross-Browser**: Chrome, Firefox, Safari compatibility testing
- **Mobile Responsiveness**: Tablet and mobile device testing for theme system and responsive layouts

**Performance Testing:**
- **Load Testing**: Realistic data volumes for approval workflows, event management, form operations
- **Theme Switching**: Performance testing for immediate theme changes across all components
- **Real-time Updates**: Polling performance testing with various user activity levels

**Epic 1 Regression Testing:**
- **Functionality**: All Epic 1 features must remain fully operational
- **Performance**: Epic 1 performance characteristics must be maintained
- **Data Integrity**: Epic 1 data must remain unchanged and accessible

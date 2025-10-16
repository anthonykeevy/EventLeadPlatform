# Solution Architecture - EventLeadPlatform

**Project:** EventLeadPlatform  
**Date:** 2025-10-12  
**Architect:** Winston (Architect Agent)  
**User:** Anthony Keevy  
**Status:** ✅ COMPLETE - Validated Against PRD and UX Specification  
**Cohesion Check:** docs/architecture-cohesion-check.md (100% Ready)

---

## Prerequisites and Scale Assessment

### Project Classification

- **Project Level:** 4 (Enterprise Platform)
- **Field Type:** Greenfield
- **Project Type:** Web Application
- **Has User Interface:** Yes
- **UI Complexity:** Complex (Advanced drag-and-drop form builder)

### Prerequisites Validation

✅ **Check 1: PRD Complete**
- Status: COMPLETE
- Location: `docs/prd.md`
- Includes: FRs, NFRs, epics, stories, data models, user flows

✅ **Check 2: UX Spec Complete (UI Project)**
- Status: COMPLETE
- Location: `docs/ux-specification.md`
- Includes: 50+ screens, design system, 20 components, 24 micro-interactions, responsive strategy, accessibility requirements

✅ **Check 3: All Prerequisites Met**
- PRD: Complete
- UX Spec: Complete
- **Proceeding with full solution architecture workflow for Level 4 enterprise platform**

### Workflow Path Determination

**Decision:** Proceed with full solution architecture workflow

**Rationale:**
- Level 4 project requires comprehensive architecture
- Complex multi-tenant SaaS with advanced form builder
- Enterprise data management requirements (audit tracking, data lineage)
- Multiple complex domains and integrations
- 60+ stories across 8-10 epics

---

## PRD and UX Analysis

### Primary Requirements Document

**Type:** Product Requirements Document (PRD)  
**Location:** `docs/prd.md`  
**Status:** Comprehensive Level 4 enterprise PRD

### Functional Requirements (FRs) - Core MVP Features

#### 1. User Authentication, Onboarding & RBAC
- Email-based signup/login with verification
- Multi-step onboarding flow (user details + company setup for first user, simplified for invited users)
- Three-role system: System Admin (backend only for MVP), Company Admin (full access), Company User (limited, no publish)
- Password reset flow
- Session management with JWT tokens
- RBAC middleware for authorization checks
- Invitation-based user signup (secure tokens, 7-day expiry, resend capability)

#### 2. Company Management (Multi-Tenant)
- Company profile: name, ABN (Australian Business Number - 11 digits), billing address, phone, industry
- Company Admin can update company details
- Company settings page
- Activity log (who created/edited what - comprehensive audit tracking)
- Data isolation per company (row-level security)
- Test threshold configuration (preview tests required before publish)

#### 3. Events Management & Domain Features
- Event CRUD operations
- Event details: name, date range, location, description, event type
- Event types: Trade Show, Conference, Expo, Community Event, Job Fair, Product Launch, Other
- Personal/Private events option (for non-event forms)
- Events contain multiple forms
- Form activation windows: Auto-activate 3 hours before event, auto-deactivate 3 hours after
- Override option for Company Admin (manual activate/deactivate)
- Event list view with filtering (upcoming, past, draft)
- Event dashboard showing all forms for an event
- Inline event creation during form creation (with quality review flag)

#### 4. Team Collaboration & Invitations
- Company Admin invites users via email (first name, last name, email, role)
- Invitation email with secure token link (7-day expiry)
- Pending invitations list with status tracking
- Expired invitation handling with resend capability
- Role assignment during invitation (Company Admin or Company User)
- User management screen (list users, change roles, remove users)
- Role-based UI rendering (show/hide features based on role)
- Activity tracking per user

#### 5. Drag-and-Drop Form Builder
**Canvas-Based Interface:**
- Fixed canvas dimensions: 1200x1600px (3:4 aspect ratio, iPad-optimized)
- Canvas vs Screen distinction: Screen is 80% rectangle within canvas
- Screen aspect ratio selector: Portrait (3:4), Square (1:1), Landscape (16:9)
- Component fencing: Components cannot be dragged outside screen rectangle

**Component Library (9 Field Types):**
- Name (first name, last name, full name variants)
- Email
- Phone
- Address (with GeoScape API for Australian address validation - Post-MVP)
- Text input (single line)
- Dropdown/select
- Checkbox
- Radio buttons
- Multi-line text area (textarea)

**Component Structure (3-Part System):**
Each component consists of:
1. Label - Field label text
2. Input Field - The actual input control
3. Validation Message - Error/helper text area

**Stacking Options (Per Component):**
- Horizontal Layout: Label left of input, validation below
- Vertical Layout (Default): Label above input, validation below

**Advanced Builder Features:**
- **Proportional Scaling:** Design at fixed canvas size, scale proportionally on publish
- **Component Framework:** Form-level default settings + per-component overrides (font family, font size, color, label position)
- **Undo/Redo System:** Track all actions (50 action history), Ctrl+Z/Ctrl+Shift+Z, clear on publish
- **Enhanced Drag Interactions:** Open/closed hand cursors, ghost preview, snap feedback, return to library if dropped outside
- **Component Overlap Prevention:** Collision detection, red outline on overlap, cannot release on top of another
- **Background Image Resize Mode:** Initial resize/reposition mode, locks after first component added
- **Tab Order Management:** Auto-assigned based on position, visual display toggle, drag to reorder
- **Real-time Preview:** Desktop, tablet, mobile views with device frames

#### 6. Custom Backgrounds + Template Library
**Option A: Upload Custom Background**
- Image upload (JPEG, PNG)
- Azure Blob Storage (production), local storage (development)
- Image optimization/resizing
- Preview with components overlaid

**Option B: Template Library**
- 5-10 pre-designed professional templates
- Industry-specific themes (tech, healthcare, retail, professional services)
- One-click apply
- Template JSON definitions

#### 7. Preview & Testing System
**Core Principle:** Preview uses same system as production - leads are flagged as preview vs production

**Preview Mode:**
- Toggle between "Preview" and "Production" mode in builder
- Preview URL: Same as production URL with ?preview=true parameter
- Preview leads: `submission.is_preview = true`
- Production leads: `submission.is_preview = false`

**Testing Requirements:**
- Minimum 5 preview tests required before publish
- Company Admin can set custom threshold per company (0-20 tests)
- Test counter visible in builder: "3 of 5 tests completed"
- Publish button disabled until threshold met
- Test audit log: track user, timestamp per test

**Approver Testing Requirement:**
- Company User requests publish → Company Admin must test before approving
- Exception: If Admin is also form creator and already tested
- Test button on review page opens preview URL

**Preview Data Management:**
- Preview leads visible in analytics with "Preview" badge
- Filter: Preview Only | Production Only | All Leads
- Export option: Include/Exclude preview leads
- Dashboard counts: "50 Production leads • 8 Preview leads"
- Delete individual or bulk delete all preview leads

#### 8. Form Publishing & Hosting
- "Publish" button triggers payment gate
- Stripe payment flow: $99 (includes 10% GST) - Standard tier only for MVP
- Generate unique public URL on publish: `forms.eventlead.com/{unique-id}`
- Forms hosted on Azure infrastructure
- Form never goes down (even if customer doesn't pay for next event)
- Unpublish option (takes form offline)
- Company User cannot publish - must request Admin approval
- Admin review page with "Publish & Pay" button

#### 9. Lead Collection & Storage
- Public forms accept submissions
- Store all form data in MS SQL Server
- Timestamp all submissions
- Associate submissions with form owner (company)
- Preview vs production flagging (`is_preview` boolean)
- No submission limits
- GDPR and Australian Privacy Principles compliant
- IP address hashing for privacy

#### 10. Data Validation
**Field-Level Validation Rules:**
- Email format validation
- Phone number format (Australian +61, international)
- Required field enforcement
- Min/max length for text fields
- Real-time validation feedback on form
- Frontend validation (React) + backend validation (FastAPI)
- Prevent >90% bad leads (quality = retention target)

#### 11. Minimalistic Analytics Dashboard
- Real-time lead count (split by Preview vs Production)
- Submission timeline chart (by hour/day)
- Basic demographics (if collected in form)
- List view of all submissions
- Search and filter submissions (by preview/production, date range, field values)
- Single-form view (drill into one form's data)
- Preview leads shown with "Preview" badge
- Production leads shown with "Production" badge
- Filter: Preview Only | Production Only | All Leads
- Delete preview leads (individual or bulk)
- Real-time updates (WebSocket or polling)

#### 12. Usage Analytics & Workflow Optimization (Post-MVP Core)
**Platform Usage Tracking:**
- Collect anonymous usage data for all workflows
- Track: clicks, page views, time on page, feature usage, workflow completion rates
- Purpose: Understand workflow success and efficiency
- Privacy-safe: aggregate data only, no PII, Australian Privacy Principles compliant
- Can opt-out in company settings
- PostHog or Plausible (privacy-focused analytics)

#### 13. CSV Export & Company Billing
**CSV Export:**
- Export all leads for a form to CSV
- Format options: Salesforce, Marketing Cloud, Emarsys, Generic CSV
- One-click download
- Include all fields + timestamp
- Include/exclude preview leads option

**Company Billing & Invoicing:**
- Generate Australian GST-compliant invoices
- Invoice details: Company name, ABN, billing address, line items (forms published)
- 10% GST included in all pricing ($90 ex GST + $9 GST = $99)
- Invoice PDF generation
- Email invoice to Company Admin
- Billing history view (list all invoices, download PDFs)
- Payment via Stripe (one-time payments per publish)
- Receipt emails after successful payment

### Non-Functional Requirements (NFRs)

#### Performance
- **Form Load Time:** <2 seconds on tablet (critical for event booth usage)
- **Form Creation Time:** <5 minutes average (key usability goal)
- **Uptime:** 99.5%+ (forms must stay live during events)
- **Real-time Updates:** Analytics dashboard updates without page refresh
- **Drag Performance:** Smooth 60fps interactions in form builder

#### Scalability
- Support 100 concurrent form submissions without errors
- No data loss (submissions persist reliably)
- Database design supports future growth (proper indexing, normalized schema)

#### Security
- SSL/TLS for all connections
- JWT token-based authentication
- RBAC enforced at every layer (middleware checks)
- Row-level security for multi-tenant data isolation
- Password hashing (secure algorithms)
- Secure invitation tokens (7-day expiry)
- Environment variable secrets (Azure Key Vault in production)

#### Data Quality & Compliance
- >90% valid leads (quality = retention driver)
- Field-level validation (frontend + backend)
- Australian Privacy Principles compliant
- GDPR-compatible practices
- Australian Business Number (ABN) validation (11 digits)
- GST-compliant invoicing (10% GST, proper invoice format)

#### Accessibility
- **Target:** WCAG 2.1 Level AA
- **Priority:** Public forms (customer-facing) must meet AA
- **Dashboard:** Most AA criteria met (acknowledge gaps for post-MVP)
- Color contrast ratios: ≥4.5:1 (normal text), ≥3:1 (large text, UI components)
- Keyboard navigation for all interactive elements
- Screen reader support
- Focus indicators clearly visible (3px teal outline)
- Alt text for images
- ARIA labels where appropriate

#### Responsive Design
- **Public Forms:** Tablet-first (768px-1024px primary, iPads at event booths)
- **Form Builder:** Desktop-first (1280px+ required, not supported <1024px)
- **Dashboard:** Responsive (works on desktop, tablet, mobile)
- Touch-friendly targets: 44x44px minimum for public forms

#### Enterprise Data Management (Critical NFRs)
**1. Full Audit Tracking:**
- Track ALL user actions (create, read, update, delete)
- Capture: who (user_id), what (action), when (timestamp), where (entity_type, entity_id)
- ActivityLog table with comprehensive logging
- Immutable audit records (append-only, no updates/deletes)

**2. Data Lineage:**
- Track data flow through system
- Parent-child relationships (Form → Submissions, Event → Forms)
- Transformation tracking (form design changes over time)
- Version history for critical entities (forms, company details)

**3. Data Quality:**
- Field-level validation (frontend + backend)
- Data integrity constraints (foreign keys, check constraints)
- Required field enforcement
- Format validation (email, phone, ABN)

**4. Enterprise Database Design:**
- Normalized schema with proper relationships
- Indexes for performance (query optimization)
- Row-level security for multi-tenant isolation
- Soft deletes (is_active flags, not hard deletes)
- Timestamps on all tables (created_at, updated_at)
- Proper data types (no stringly-typed fields)

### Epic Breakdown (8-10 Major Epics)

#### Epic 1: Authentication & Onboarding (6-8 stories)
- Email-based signup/login with verification
- Multi-step onboarding (user details + company setup)
- Password reset flow
- Session management with JWT tokens
- RBAC middleware

#### Epic 2: Company & Multi-Tenant Management (5-7 stories)
- Company profile management
- Multi-tenant data isolation
- Company settings
- Activity logging and audit tracking
- Data lineage tracking

#### Epic 3: Events Management & Domain Features (6-8 stories)
- Event CRUD operations
- Event types and categorization
- Private/personal events
- Form activation windows
- Event discovery and filtering

#### Epic 4: Team Collaboration & Invitations (5-7 stories)
- User invitation system with secure tokens
- Role assignment and management
- User management (add, remove, change roles)
- Expired invitation handling
- Activity tracking per user

#### Epic 5: Drag-and-Drop Form Builder (12-15 stories)
- Canvas-based interface with component library (9 field types)
- Drag-and-drop with freeform positioning
- Proportional scaling rendering system
- Canvas vs Screen distinction
- Component framework (form-level defaults + overrides)
- Undo/Redo system (50 action history)
- Enhanced drag interactions
- Component overlap prevention
- Background image resize mode
- Tab order management
- Custom backgrounds + template library
- Real-time preview

#### Epic 6: Preview, Testing & Publishing (6-8 stories)
- Preview mode toggle
- Preview test counter and enforcement (minimum 5 tests)
- Approver testing requirements
- Preview data management
- Publish workflow with payment gate
- Form hosting and public URL generation
- Activation/deactivation logic

#### Epic 7: Payment, Billing & Invoicing (6-8 stories)
- Stripe payment integration
- Company-based billing
- Australian GST-compliant invoicing (10% GST)
- Invoice PDF generation
- Invoice email delivery
- Billing history
- Payment receipts

#### Epic 8: Lead Collection & Analytics (7-9 stories)
- Form submission handling (preview vs production flagging)
- Real-time lead count dashboard
- Submissions timeline chart
- Leads list with search/filter
- Lead detail view
- CSV export (multiple formats)
- Preview lead management
- Data validation

#### Epic 9: Enterprise Data & Audit (5-7 stories)
- Comprehensive audit logging (all user actions)
- Data lineage tracking
- Enterprise-grade data quality controls
- Audit trail UI (for admins)
- Data retention policies

#### Epic 10: Usage Analytics & Optimization (Post-MVP) (4-6 stories)
- Platform usage tracking (PostHog/Plausible)
- Workflow completion metrics
- Feature adoption analytics
- A/B testing capability

**Total Story Estimate:** 62-83 stories across all epics

### Technical Constraints from PRD

**Technology Stack Specified:**
- Frontend: React (modern hooks-based)
- Backend: Python FastAPI
- Database: MS SQL Server (Azure SQL Database for production, local for dev)
- Hosting: Azure App Service (production), local (development)
- Storage: Azure Blob Storage (production), local file storage (development)
- Payments: Stripe (test mode dev, live mode production)
- Email: Azure Communication Services (production), MailHog containerized (development)

**Integrations Required:**
- Stripe (payment processing)
- Azure services (SQL Database, Blob Storage, Communication Services, App Service, CDN)
- MailHog (local email testing)
- GeoScape API (Address field validation - Post-MVP)
- SendGrid or Azure Communication Services (email)
- PostHog or Plausible (usage analytics - Post-MVP)

### UX Specification Analysis

**Location:** `docs/ux-specification.md`  
**Status:** Extremely comprehensive

#### Screen Count: 50+ Screens Mapped

**Main Areas:**
1. Public Marketing Site (5 screens)
2. Onboarding Flow - First-Time User (4 screens)
3. Onboarding Flow - Invited User (4 screens)
4. Main Dashboard (30+ screens across Events, Forms, Analytics, Team, Settings, Billing)
5. Form Builder (10+ screens/states)
6. Public Form View (3 states)

#### Navigation Complexity: Complex

**Top Navigation Bar:**
- Events | Forms | Analytics | Team* | Settings | [Profile▼]
- (*Team tab only visible to Company Admins - role-based rendering)

**Role-Based Navigation:**
- Company Admin: All nav items, Team tab, full Company Settings, Billing
- Company User: Events, Forms, Analytics, Settings (limited), NO Team tab, NO Billing

**Context Navigation:**
- Breadcrumbs for deep navigation
- Form Builder: Maximized workspace (no side navigation)
- Mobile: Hamburger menu for dashboard

#### UI Complexity: Complex

**Complex UI Indicators:**
✅ Complex wizards/multi-step forms (Onboarding, Publish workflow)
✅ Real-time updates/dashboards (Analytics with live lead counts)
✅ Complex state machines (Form builder states, approval workflows)
✅ Rich interactions (Drag-drop, animations, undo/redo)
✅ Advanced component positioning (Freeform canvas with collision detection)

**Most Complex Component:** Form Builder
- Drag-and-drop canvas with freeform positioning
- Undo/Redo with 50-action history
- Component overlap detection and prevention
- Proportional scaling rendering
- Tab order management
- Background image resize mode
- Real-time preview
- Multiple panel layout (Component Library, Canvas, Properties)

#### Component Patterns (20 Core Components Defined)

**Foundation Components:**
1. Button (variants: primary, secondary, ghost, danger)
2. Input Fields (types: text, email, password, tel, number, textarea)
3. Select/Dropdown (single, multi, searchable)
4. Checkbox & Radio
5. Modal/Dialog
6. Card
7. Table
8. Badge/Tag
9. Toast Notifications
10. Loading States (spinner, skeleton, progress bar)

**Form Builder Specific:**
11. DraggableComponent (canvas items with drag handles, resize, selection)
12. ComponentLibrary (left panel with collapsible sections)
13. PropertiesPanel (right panel, context-sensitive)
14. Canvas (drop zone with grid, snap-to-grid, zoom)
15. PreviewPane (desktop/tablet/mobile modes)

**Dashboard/Admin:**
16. EventCard
17. FormCard
18. StatsCard
19. NavigationTabs
20. UserAvatar

#### Design System Defined

**Colors:**
- Primary: Teal (teal-500 #14B8A6)
- Secondary: Violet (violet-500 #8B5CF6)
- Success: Emerald (emerald-500 #10B981)
- Warning: Amber (amber-500 #F59E0B)
- Error: Red (red-500 #EF4444)
- Info: Blue (blue-500 #3B82F6)

**Typography:**
- Font: Inter (primary), JetBrains Mono (monospace for technical)
- Scale: 12 sizes defined (from caption 12px to display 48px)

**Spacing:**
- Base unit: 4px
- Scale: 0, 4px, 8px, 12px, 16px (default), 20px, 24px, 32px, 40px, 48px, 64px, 80px

**Responsive Breakpoints:**
- sm: 640px (large phones)
- md: 768px (tablets portrait - PRIMARY for public forms)
- lg: 1024px (tablets landscape, small laptops)
- xl: 1280px (desktop/laptop - PRIMARY for form builder)
- 2xl: 1536px (large desktop)

#### Key User Flows Documented (7 Flows with Mermaid Diagrams)

1. New Company Sign Up & Onboarding (25+ steps)
2. Invited User Join Flow (21 steps)
3. Create Event & Publish Form (Company Admin) (30+ steps)
4. Company User Requests Admin to Publish Form (25+ steps)
5. View Analytics & Export Leads (15+ steps)
6. Password Reset (10+ steps)
7. Admin Invite Team Member (15+ steps)

#### Responsive Requirements

**Public Forms (Tablet-First):**
- Primary target: 768px-1024px (iPads at event booths)
- Full-width form with optimal touch targets (44px minimum)
- Background image scaled to fit viewport
- Generous spacing between fields

**Form Builder (Desktop-First):**
- Primary target: 1280px+ (three-panel layout)
- Minimum: 1024px (functional but cramped)
- Not supported: <1024px (show message: "Please use desktop for form builder")

**Dashboard (Responsive):**
- Desktop: 1280px+ (multi-column layouts)
- Tablet: 768px-1280px (responsive columns, collapsible nav)
- Mobile: 640px-768px (single column, hamburger menu)

#### Accessibility Requirements

**Target:** WCAG 2.1 Level AA

**Key Requirements:**
- Color contrast: ≥4.5:1 (normal text), ≥3:1 (large text)
- Keyboard navigation for all interactive elements
- Screen reader support (NVDA, VoiceOver, TalkBack)
- Focus indicators clearly visible (3px teal outline)
- Alt text for all images
- ARIA labels for icon buttons
- Touch targets: 44x44px minimum (tablet/mobile)

#### Micro-Interactions Defined (24 Animations)

**Key Animations:**
1. Email verification success (checkmark scale-in with bounce, 400ms)
2. Component drag & drop (lift effect, ghost preview, snap with bounce, 200ms)
3. Auto-save indicator (spinner → checkmark pulse, 200ms)
4. Payment success (checkmark burst, confetti, URL typewriter, 600ms)
5. Real-time lead counter (count-up animation, pulse, 400ms)
6. Form validation errors (shake animation, 300ms, 3 shakes)

**Animation Principles:**
- Fast but noticeable (100-600ms)
- Natural physics-based motion (easing curves)
- Purposeful, not decorative
- GPU-accelerated (transform, opacity)
- Reduced motion support (`prefers-reduced-motion`)

### PRD-UX Alignment Check

#### Epic-to-Screen Mapping

✅ **Epic 1: Authentication & Onboarding**
- Screens: Signup, Email Verification, Login, Onboarding (user details + company setup), Invitation acceptance
- User Flows: Fully documented (Flow 1, 2, 6)
- Components: Input fields, buttons, modals, progress indicators
- **Alignment:** COMPLETE

✅ **Epic 2: Company Management**
- Screens: Company Settings, Company Profile, Activity Log
- Components: Forms, cards, tables (activity log), user avatar
- **Alignment:** COMPLETE

✅ **Epic 3: Events Management**
- Screens: Events List, Event Dashboard, Create Event Modal, Event Details
- User Flows: Documented in Flow 3 (Create Event & Publish Form)
- Components: EventCard, modals, forms, filters
- **Alignment:** COMPLETE

✅ **Epic 4: Team Collaboration**
- Screens: Team Management, Invite User Modal, User Management, Pending Invitations
- User Flows: Fully documented (Flow 2, 7)
- Components: Tables, modals, badges (role badges), user avatar
- **Alignment:** COMPLETE

✅ **Epic 5: Form Builder**
- Screens: Form Builder Interface (left panel, canvas, right panel), Template Gallery, Preview Mode
- User Flows: Documented in Flow 3, 4
- Components: 15 specialized builder components defined (DraggableComponent, Canvas, PropertiesPanel, etc.)
- **Alignment:** COMPLETE - Most complex component with extensive UX detail

✅ **Epic 6: Preview & Publishing**
- Screens: Preview Mode Toggle, Publish Flow (payment screen, success), Publish Request (Company User)
- User Flows: Documented in Flow 3, 4
- Components: Modals, payment forms, preview pane
- **Alignment:** COMPLETE

✅ **Epic 7: Payment & Billing**
- Screens: Payment Screen, Payment Success, Billing History, Invoices List
- User Flows: Documented in Flow 3, 4
- Components: Stripe checkout, modals, tables (invoice list), PDF download buttons
- **Alignment:** COMPLETE

✅ **Epic 8: Analytics**
- Screens: Analytics Dashboard, Leads List, Lead Detail View, Export Modal
- User Flows: Fully documented (Flow 5)
- Components: StatsCard, charts (submissions timeline), tables, filters, badges (preview/production)
- **Alignment:** COMPLETE

✅ **Epic 9: Enterprise Data & Audit**
- Screens: Activity Log (within Company Settings), Audit Trail UI (admin)
- Components: Tables with search/filter, badges, timestamps
- **Alignment:** COMPLETE - ActivityLog component defined

#### Gaps Identified

**None identified.** PRD epics map cleanly to UX screens and user flows. All major features have corresponding UI designs.

### Project Characteristics Summary

**Project Type:** Web Application

**Architecture Style Hints:**
- Monolithic application (frontend + backend in coordinated deployment)
- Multi-tenant SaaS architecture
- RESTful API architecture (FastAPI backend, React frontend)

**Repository Strategy Hints:**
- Monorepo recommended (solo developer, coordinated deployments, shared types)
- Single repository with frontend/ and backend/ directories

**Special Needs:**
- **Real-time:** Analytics dashboard with live lead counts (WebSocket or Server-Sent Events)
- **Event-driven:** Form activation windows based on event times (scheduled jobs or cron)
- **Batch processing:** Invoice generation, email delivery (async background tasks)
- **Offline-first:** Not required (event forms require network for submission)

### Already Specified vs. Unknown

#### Known Technologies (From PRD):
✅ React (frontend)
✅ FastAPI (backend)
✅ MS SQL Server (database)
✅ Azure App Service (hosting)
✅ Azure Blob Storage (file storage)
✅ Stripe (payments)
✅ Azure Communication Services or SendGrid (email)
✅ MailHog (local email testing)

#### Known Patterns (From UX Spec):
✅ JWT token authentication
✅ Multi-tenant row-level security
✅ RBAC with 3 roles
✅ Drag-and-drop library (dnd-kit recommended in UX spec)
✅ Component library approach (20 components defined)

#### Unknowns (Need Architecture Decisions):

**Frontend:**
- ⚠️ State management library (React Context, Redux, Zustand, Jotai?)
- ⚠️ Form library (React Hook Form, Formik, or custom?)
- ⚠️ UI component library foundation (Headless UI, Radix UI, or fully custom with Tailwind?)
- ⚠️ Real-time library (WebSocket native, Socket.io, or Server-Sent Events?)
- ⚠️ Data fetching library (React Query, SWR, or fetch with custom hooks?)
- ⚠️ Build tooling (Vite, Create React App, or Next.js for SSR?)
- ⚠️ Testing framework (Jest, Vitest, React Testing Library, Playwright for E2E?)

**Backend:**
- ⚠️ ORM (SQLAlchemy, Tortoise ORM, or raw SQL?)
- ⚠️ Database migrations (Alembic?)
- ⚠️ Background task queue (Celery, Dramatiq, or FastAPI BackgroundTasks?)
- ⚠️ Real-time backend (WebSocket support in FastAPI, or separate service?)
- ⚠️ API documentation (FastAPI auto-docs, or additional Swagger/ReDoc?)
- ⚠️ Logging framework (structlog, loguru, or Python logging?)
- ⚠️ Testing framework (pytest, unittest?)

**Infrastructure:**
- ⚠️ Container strategy (Docker, Docker Compose for local dev?)
- ⚠️ CI/CD pipeline (GitHub Actions, Azure DevOps Pipelines?)
- ⚠️ Environment configuration management (python-decouple, pydantic BaseSettings?)
- ⚠️ Monitoring and observability (Application Insights, Sentry for error tracking?)

**Database:**
- ⚠️ Specific SQL Server version (SQL Server 2019, 2022?)
- ⚠️ Connection pooling strategy
- ⚠️ Migration approach (Alembic with autogenerate?)
- ⚠️ Seed data strategy for development

---

## User Skill Level and Technical Preferences

### Experience Level: Beginner (Detailed Explanations)

**Background:**
- Extensive data management experience (enterprise-grade database design)
- Team management experience (led development teams)
- Limited hands-on development (scripting experience)
- Months of experience with BMAD agentic tools (v4 projects completed)

**Architecture Approach:**
- Detailed explanations for all technology choices
- Expand all acronyms on first use
- Provide rationale for every decision
- Include examples and comparisons
- Educational tone (not just prescriptive)

### Technical Preferences

**Stack (Pre-selected from PRD):**
- Frontend: React 18+ (JavaScript UI library)
- Backend: FastAPI (Python web framework)
- Database: Microsoft SQL Server (enterprise relational database)
- Hosting: Azure (Microsoft cloud platform)
- Payments: Stripe (payment processing service)

**Technology Selection Approach:**
- Use architect's best judgment for library/module selection
- Prioritize: Solo developer productivity, enterprise-grade quality, learning curve
- Favor: Well-documented, widely-adopted, stable libraries
- Avoid: Cutting-edge/experimental, steep learning curves, niche solutions

**Key Constraints:**
- Solo founder (all development by Anthony)
- 5.5-month timeline (aggressive for Level 4 project)
- Local development → Azure production (smooth transition required)
- Enterprise data management (Anthony's strength - leverage this)

---

## Architecture Pattern Determination

### Architecture Style: Modular Monolith

**Decision: Modular Monolith** (single application with clear internal module boundaries)

**What is a Monolith?**
A monolith is a single, unified application where all functionality runs in one process. All features share the same database, codebase, and deployment.

**What are the alternatives?**
- **Microservices:** Multiple small applications, each with its own database and deployment (e.g., separate Auth Service, Payment Service, Form Service)
- **Serverless:** Individual functions deployed separately (e.g., AWS Lambda, Azure Functions)

**Why Monolith for EventLeadPlatform?**

✅ **Solo Developer Efficiency:**
- ONE codebase to understand and navigate
- ONE deployment process (simpler DevOps)
- NO network communication overhead between services
- FASTER development (no service coordination)
- EASIER debugging (all code in one place)

✅ **Shared Database Benefits:**
- Your database expertise is maximized
- ACID (Atomicity, Consistency, Isolation, Durability) transactions across all features
- NO eventual consistency problems
- Easier audit trail (all data in one database)
- Simpler backup/restore

✅ **Appropriate for Scale:**
- 100 concurrent users is well within monolith capability
- Vertical scaling (bigger server) easier than horizontal (more servers)
- Can split into microservices later IF needed (not now)

✅ **Timeline Pressure:**
- 5.5 months is aggressive
- Microservices add 30-40% overhead (service communication, deployment complexity)
- Focus time on features, not infrastructure

**What is "Modular" Monolith?**
Even though it's one application, we organize code into clear modules:
```
backend/
  modules/
    auth/         # Authentication and authorization
    companies/    # Company management
    events/       # Event management
    forms/        # Form builder and management
    payments/     # Stripe integration
    analytics/    # Lead analytics
```

Each module has:
- Clear boundaries (auth doesn't directly call payments)
- Own database tables (but shared database)
- Could be extracted to microservice later if needed

**Trade-offs:**
- ❌ Less scalable than microservices (but sufficient for MVP and beyond)
- ❌ Can't use different tech stacks per feature (but we don't need to)
- ✅ Simpler, faster, easier for solo developer
- ✅ Can refactor to microservices later if business grows significantly

---

### Repository Strategy: Monorepo

**Decision: Monorepo** (single Git repository with both frontend and backend)

**What is a Monorepo?**
One repository contains all code:
```
EventLeadPlatform/
  frontend/       # React application
  backend/        # FastAPI application
  database/       # Migration scripts
  docs/           # Documentation
```

**What is the alternative?**
- **Polyrepo:** Multiple repositories (e.g., `eventlead-frontend`, `eventlead-backend`, `eventlead-database`)

**Why Monorepo for EventLeadPlatform?**

✅ **Solo Developer Benefits:**
- ONE place to find all code
- ONE git clone to get started
- Atomic commits across frontend + backend
- NO version coordination between repos

✅ **Shared Types/Contracts:**
- TypeScript types can be shared between frontend and backend
- API (Application Programming Interface) contracts defined once
- Database schema changes visible to both frontend and backend

✅ **Simpler CI/CD (Continuous Integration/Continuous Deployment):**
- ONE pipeline builds and deploys everything
- NO coordination between multiple pipelines
- Easier to ensure frontend and backend stay in sync

✅ **Timeline Efficiency:**
- NO time wasted coordinating multiple repos
- Faster feature development (change frontend + backend together)
- Single source of truth

**Example Workflow:**
```bash
# ONE command gets everything
git clone eventleadplatform
cd eventleadplatform

# See all code together
ls
# → frontend/  backend/  database/  docs/

# Change frontend AND backend in one commit
git add frontend/components/EventCard.tsx
git add backend/api/routes/events.py
git commit -m "Add event filtering feature"
```

**Trade-offs:**
- ❌ Larger repository (but not a problem for one person)
- ❌ Can't have different access permissions for frontend vs backend (but not needed - you're solo)
- ✅ Simpler, faster, less coordination overhead
- ✅ Easier for solo developer

---

### Web Architecture Pattern: SPA (Single Page Application) + API

**Decision: SPA (Single Page Application) for Dashboard and Form Builder**

**What is an SPA?**
A Single Page Application loads once, then updates content dynamically without full page reloads. Think Gmail, Facebook, or Google Maps.

**How it works:**
1. Browser loads the React app (HTML + JavaScript)
2. React renders the UI (dashboard, form builder, etc.)
3. React calls backend API (Application Programming Interface) for data
4. React updates the UI without reloading the page

**What are the alternatives?**
- **SSR (Server-Side Rendering):** Server generates HTML for each page (e.g., traditional websites, Next.js)
- **MPA (Multi-Page Application):** Each page is a separate HTML file from the server

**Why SPA for EventLeadPlatform?**

✅ **Rich Interactions Required:**
- Form builder with drag-and-drop (needs JavaScript in browser)
- Real-time analytics updates (no page reload)
- Complex state management (undo/redo in form builder)

✅ **Desktop Application Feel:**
- Dashboard feels like an app, not a website
- Instant navigation between screens
- Smooth transitions and animations

✅ **API Reusability:**
- Same API (Application Programming Interface) serves web, mobile (future), integrations
- Clear separation: Frontend (React) ↔ API (FastAPI) ↔ Database (SQL Server)

**Architecture Diagram:**
```
User Browser
    ↓
React SPA (Single Page Application)
    ↓ (HTTP/HTTPS requests)
FastAPI Backend (RESTful API)
    ↓ (SQL queries)
MS SQL Server Database
```

**For Public Forms: Static/Simple Rendering**

Public forms (submitted by event attendees) use a simpler approach:
- Lighter JavaScript (not full SPA)
- Fast load time (critical for event booth tablets)
- Tablet-optimized

**Why?**
- Public form is simple (just show form, submit data)
- No need for complex SPA features
- Faster load = better user experience at events

**Trade-offs:**
- ❌ Initial load time slightly longer than SSR (but caching helps)
- ❌ SEO (Search Engine Optimization) harder (but not critical - platform is authenticated, not public marketing site)
- ✅ Better UX (User Experience) for authenticated users
- ✅ Simpler development (clear frontend/backend separation)

---

### API Architecture: RESTful JSON API

**Decision: RESTful API (Representational State Transfer)**

**What is REST?**
A standard way to design web APIs (Application Programming Interfaces) using HTTP (HyperText Transfer Protocol):
- `GET /api/events` - Get list of events
- `POST /api/events` - Create new event
- `PUT /api/events/123` - Update event 123
- `DELETE /api/events/123` - Delete event 123

**What are the alternatives?**
- **GraphQL:** Query language for APIs (more flexible but more complex)
- **gRPC (Google Remote Procedure Call):** Binary protocol (faster but harder to debug)
- **WebSockets:** Bidirectional real-time (we'll use this only for analytics updates)

**Why REST for EventLeadPlatform?**

✅ **Industry Standard:**
- Most widely used API pattern
- Huge ecosystem and tooling
- Easy to understand and debug
- FastAPI has excellent REST support

✅ **Solo Developer Friendly:**
- Simple to design and implement
- Browser tools (like Postman) work well
- Easy to test (just HTTP requests)
- Clear documentation (FastAPI auto-generates docs)

✅ **Sufficient for Requirements:**
- CRUD (Create, Read, Update, Delete) operations fit REST perfectly
- Form builder actions map to REST endpoints
- Real-time updates: Add WebSockets only where needed (analytics)

**Example REST Endpoints:**
```
Authentication:
  POST   /api/auth/signup
  POST   /api/auth/login
  POST   /api/auth/verify-email
  POST   /api/auth/reset-password

Events:
  GET    /api/events                    # List all events
  POST   /api/events                    # Create event
  GET    /api/events/123                # Get event 123
  PUT    /api/events/123                # Update event 123
  DELETE /api/events/123                # Delete event 123

Forms:
  GET    /api/events/123/forms          # Forms for event 123
  POST   /api/events/123/forms          # Create form for event 123
  GET    /api/forms/456                 # Get form 456
  PUT    /api/forms/456                 # Update form 456
  POST   /api/forms/456/publish         # Publish form (triggers payment)
```

**JSON (JavaScript Object Notation) Format:**
All data exchanged in JSON (text format for structured data):
```json
{
  "eventId": 123,
  "eventName": "Tech Summit 2026",
  "eventStartDate": "2026-01-15T09:00:00Z",
  "location": "Sydney Convention Centre",
  "isActive": true
}
```

**Trade-offs:**
- ❌ Less flexible than GraphQL (but don't need that flexibility)
- ❌ Can be "chatty" (multiple requests for related data) - but acceptable for our scale
- ✅ Simple, standard, well-understood
- ✅ Perfect for solo developer

---

### Real-Time Updates: WebSockets for Analytics Only

**Decision: REST for most features, WebSockets for real-time analytics**

**What are WebSockets?**
A persistent connection between browser and server for real-time updates:
- Server can push updates to browser instantly
- No polling (repeated requests)
- Used for: Chat apps, live dashboards, notifications

**Why limited use?**
Most features don't need real-time:
- Creating an event: Request → response (REST is fine)
- Editing a form: Save → response (REST is fine)
- Viewing analytics: MUST update in real-time (WebSocket)

**Where we'll use WebSockets:**
- ✅ Analytics dashboard (live lead count updates)
- ✅ Form submission notifications (optional: "New lead received!")

**Where we'll use REST:**
- ✅ Everything else (authentication, CRUD operations, payments)

**Why?**
- Simpler codebase (REST is easier than WebSockets)
- WebSockets only where truly needed
- Easier debugging and testing

---

### Architecture Risk Analysis & Mitigation Strategies

This section identifies potential risks with the chosen architecture patterns and defines mitigation strategies. As a Level 4 enterprise project with a solo developer and aggressive timeline, proactive risk management is critical.

#### Risk Category 1: Timeline & Complexity

**RISK: 5.5-month timeline too aggressive for Level 4 complexity**
- Solo developer building 60+ stories across 8-10 epics
- Complex form builder (undo/redo, collision detection, proportional scaling)
- Learning curve for unfamiliar frontend libraries and patterns

**Severity:** HIGH ⚠️

**Mitigations:**
1. ✅ BMAD v6 Just-In-Time approach (tech specs per epic, not all upfront)
2. ✅ Select libraries with excellent documentation (beginner-friendly)
3. ✅ Proof-of-concept form builder in Weeks 9-10 (validate complexity early)
4. ✅ Weekly progress reviews (catch slippage early)
5. ✅ Ruthless scope management (MVP focus, no feature creep)
6. Build in 1-week buffer (plan for 21 weeks, have 1 week contingency)
7. Foundation epics first (Weeks 1-8) - builds confidence before complex builder

**Monitoring:** Track story completion velocity weekly, adjust scope if falling behind

---

#### Risk Category 2: Monolith Scalability

**RISK: Monolith can't handle growth if platform succeeds**
- What if 1,000 concurrent users instead of 100?
- What if 10,000 published forms instead of 1,000?
- Single application becomes performance bottleneck

**Severity:** MEDIUM (Low immediate risk, higher long-term)

**Mitigations:**
1. ✅ Modular structure allows extraction to microservices later (clean boundaries)
2. ✅ Database-first design with proper indexing (Anthony's strength)
3. ✅ Azure App Service can scale vertically (bigger server) easily
4. ✅ Proper query optimization from start
5. Design stateless API (no server-side sessions) - easier to add more servers later
6. Use caching strategy (Redis layer can be added when needed)
7. CDN (Content Delivery Network) for public forms (Azure CDN)

**Decision Point:** If platform reaches 500+ concurrent users OR performance degrades, THEN consider microservices (not before)

**Why this is acceptable:**
- MVP needs speed to market, not infinite scale
- Can refactor later with paying customers (validates need)
- Premature optimization wastes time

---

#### Risk Category 3: Solo Developer Burnout

**RISK: Anthony trying to do everything alone for 5.5 months**
- DevOps, frontend, backend, database, testing, documentation
- No team for code review or knowledge sharing
- Mental exhaustion or quality degradation

**Severity:** HIGH ⚠️

**Mitigations:**
1. ✅ BMAD agents act as "virtual team" (code review via review-story workflow)
2. ✅ Monorepo/Monolith reduces cognitive overhead (simpler than distributed systems)
3. ✅ Focus on YOUR strength (database/data management) - let agents assist with frontend
4. Weekly retrospectives (even solo) to catch burnout signs early
5. Define "good enough" standards (don't over-engineer for MVP)
6. Use managed services (Azure handles infrastructure, Stripe handles payments)
7. Take weekends off (sustainable pace beats sprint-to-burnout)

**Recommendation:** Consider 1-2 beta testers after Week 16 (external validation, fresh perspective)

---

#### Risk Category 4: Frontend Complexity (Limited Development Experience)

**RISK: Limited hands-on frontend development experience**
- Complex drag-and-drop form builder is most challenging feature (Epic 5)
- State management, real-time updates, animations
- Undo/Redo system requires sophisticated state tracking
- 12-15 stories in Epic 5 alone

**Severity:** HIGH ⚠️

**Mitigations:**
1. ✅ Select beginner-friendly libraries with excellent documentation
2. ✅ UX spec provides detailed component definitions (clear guidance)
3. ✅ BMAD Developer agent generates code (review and learn, not write from scratch)
4. Build foundation components FIRST (buttons, inputs, modals) - Weeks 1-8 builds React skills
5. Form builder is Epic 5 (Weeks 9-14) - 8 weeks of React experience before tackling complexity
6. Proof-of-concept drag-and-drop in Week 9 (validate feasibility early)
7. Select dnd-kit library (best documentation for beginners, widely adopted)
8. Educational architecture document (detailed explanations, not just decisions)

**Contingency Plan:** If form builder proves too complex:
- Fallback 1: Template-only approach (no custom backgrounds/freeform positioning)
- Fallback 2: Simplified positioning (grid-based instead of freeform)
- Fallback 3: Hire contractor for Epic 5 only (outsource complexity)

**Decision Point:** Week 10 POC results determine if pivot needed

---

#### Risk Category 5: Database Migration Errors

**RISK: Database schema changes break existing data or violate naming standards**
- Alembic (migration tool) auto-generates migrations that may not follow PascalCase standards
- Migration fails in production (data loss or downtime)
- BMAD agents generate SQL that violates your conventions (v4 experience)

**Severity:** MEDIUM-HIGH ⚠️

**Mitigations:**
1. ✅ Database standards documented in architecture (authoritative reference)
2. ✅ All migrations reviewed manually before execution
3. Create custom Alembic templates that follow your naming conventions (PascalCase)
4. Database validation script (checks naming before migration runs)
5. Use BMad Builder to create "Database Migration Validator Agent" (automates standards checking)
6. Always test migrations on local database first (never test in production)
7. Backup database before EVERY migration (even in dev environment)
8. Story-context XML includes database standards for EVERY story touching database

**Recommendation:** 
- Create Database Migration Validator Agent (using Builder) BEFORE Epic 1 implementation starts
- Validator runs as pre-commit hook (blocks git commit if standards violated)

---

#### Risk Category 6: Multi-Tenant Data Isolation Failures (CRITICAL)

**RISK: Company A sees Company B's data (catastrophic security breach)**
- Row-level security must be enforced EVERYWHERE
- One missed `WHERE CompanyID = @current_company_id` clause = data breach
- Audit logging must be bulletproof (detect breaches immediately)
- Regulatory compliance failure (Australian Privacy Principles)

**Severity:** CRITICAL 🚨 (Business-ending if occurs)

**Mitigations:**
1. ✅ Anthony's database expertise (multi-tenant design is a known pattern)
2. SQL Server Row-Level Security (RLS) as primary defense layer (database enforces isolation)
3. EVERY API endpoint MUST filter by CompanyID (no exceptions)
4. ORM (Object-Relational Mapping) middleware auto-adds CompanyID filter to ALL queries
5. Integration tests for multi-tenancy:
   - Simulate Company A user trying to access Company B event/form/submission
   - Test MUST fail with 403 Forbidden error
6. Audit log EVERY data access (read operations, not just writes)
7. Security code review checklist in EVERY story-context XML
8. Penetration testing after Epic 2 complete (try to breach multi-tenancy)

**Critical Success Factor:**
- Epic 2 (Company & Multi-Tenant Management) MUST be 100% complete and tested before other epics
- All subsequent epics inherit multi-tenant patterns from Epic 2
- NO shortcuts or exceptions to CompanyID filtering

**Architecture Decision:**
- Use SQL Server Row-Level Security (RLS) feature (database-level enforcement)
- Application layer ALSO enforces (defense in depth - two layers of protection)

---

#### Risk Category 7: Environment Abstraction Layer Complexity

**RISK: Local development → Azure production transition breaks**
- Local: MailHog (email), local file system (storage)
- Production: Azure Communication Services (email), Azure Blob Storage
- Different APIs, different configurations
- Code works locally but fails in production ("works on my machine" syndrome)

**Severity:** MEDIUM ⚠️

**Mitigations:**
1. ✅ Design abstraction layers from Day 1 (not retrofitted later)
2. Create `StorageProvider` interface (local file system vs Azure Blob use same code interface)
3. Create `EmailProvider` interface (MailHog vs Azure Communication Services use same code interface)
4. Environment-specific configuration files (`.env.local` vs `.env.production`)
5. Docker Compose for local environment (closer to production parity)
6. Test environment switching EARLY (Week 4) - don't wait until Week 22 deployment
7. Smoke tests that run in BOTH environments (validate abstraction works)

**Example Abstraction Pattern:**
```python
# Abstraction interface (same for both environments)
class StorageProvider:
    def upload_file(self, file, path):
        pass
    def download_file(self, path):
        pass

# Local implementation
class LocalStorageProvider(StorageProvider):
    def upload_file(self, file, path):
        # Save to ./local_storage/path

# Azure implementation  
class AzureBlobStorageProvider(StorageProvider):
    def upload_file(self, file, path):
        # Upload to Azure Blob Storage

# Application code uses interface (doesn't know which implementation)
storage = get_storage_provider()  # Returns Local or Azure based on ENV
storage.upload_file(background_image, "uploads/bg123.jpg")  # Works in both!
```

**Recommendation:** Architecture document will include abstraction layer patterns with code examples

---

#### Risk Category 8: Form Builder Performance (Client-Side)

**RISK: Drag-and-drop interactions feel sluggish on user's device**

**Why this matters:**
- Form builder runs in user's browser (client-side JavaScript)
- Performance depends on user's device (fast laptop vs older tablet)
- 60fps (frames per second) = smooth; <30fps = laggy/stuttering
- Users expect desktop app responsiveness

**Severity:** MEDIUM-HIGH ⚠️

**What affects performance:**
- **Collision detection:** Runs on EVERY mouse move while dragging (CPU intensive)
- **Undo/Redo state:** Tracking 50 actions (memory intensive)
- **Real-time preview:** Re-rendering form on every change
- **Component overlap prevention:** Checking all components on every drag

**Mitigations:**

**1. Performant Library Selection:**
- ✅ dnd-kit (optimized for 60fps, uses CSS transforms, GPU-accelerated)

**2. React Optimization Techniques:**
- React.memo() for components (prevents re-rendering if props unchanged)
- useMemo() for expensive calculations (cache results)
- useCallback() for event handlers (prevents function recreation)

**3. Debounce/Throttle Expensive Operations:**
- Collision detection: Check every 16ms (60fps), not every 1ms
- Auto-save: Debounce 500ms (wait for user to stop typing)
- Preview updates: Throttle 100ms (smooth but not every keystroke)

**4. Web Workers (Advanced):**
- Run collision detection in separate thread (doesn't block UI)
- Main thread: Handle drag interactions (smooth)
- Worker thread: Calculate collisions (in parallel)

**5. Device Emulation & Testing Strategy:**

**Chrome DevTools CPU Throttling:**
```
1. Open Chrome DevTools (F12)
2. Performance tab → Gear icon (⚙️)
3. CPU throttling:
   - 4x slowdown = mid-range tablet simulation
   - 6x slowdown = older/budget tablet simulation
```

**Performance Budgets (Maximum allowed time):**
- Component drag response: <16ms (for 60fps smoothness)
- Collision detection: <5ms per check
- Undo operation: <100ms (feels instant)
- Auto-save: <500ms (background operation)

**Real Device Testing:**
- iPad (10th gen or older) - PRIMARY target device
- Surface tablet (mid-range Windows tablet)
- Budget Android tablet (Samsung Galaxy Tab A)

**Testing Checklist (Week 9-10 POC):**
- [ ] Drag component at 4x CPU throttling (must be smooth)
- [ ] Collision detection at 6x throttling (acceptable lag <100ms)
- [ ] Undo/Redo at 4x throttling (must feel instant)
- [ ] Real iPad testing (Week 12) - physical device, not emulation

**Measurement Tools:**
```javascript
// Measure operation performance
console.time('collision-check');
checkCollisions(component, allComponents);
console.timeEnd('collision-check');
// Target: <5ms
```

**Contingency Plan:**
- If 4x throttling fails: Optimize algorithms (spatial indexing, early exit)
- If optimization insufficient: Simplify feature (disable collision detection, or grid-based positioning)
- If still fails: Fallback to template-only approach (no freeform drag)

**Decision Point:** Week 10 POC results determine if form builder is feasible as designed

---

#### Risk Category 9: Payment Integration Failures

**RISK: Stripe payment succeeds but form doesn't publish (or vice versa)**
- Data inconsistency: `form.status = published` but `payment.status = failed`
- Customer charged but form doesn't go live (angry customer)
- Form goes live but payment didn't process (lost revenue)
- Refund/dispute complexity

**Severity:** HIGH ⚠️ (Revenue impact + customer trust)

**Mitigations:**
1. ✅ Transaction pattern (only mark published AFTER payment succeeds)
2. Database transaction: `BEGIN → process payment → IF success THEN publish ELSE rollback`
3. Idempotent publish endpoint (can retry safely if payment succeeds but publish fails)
4. Stripe webhooks for payment confirmation (async double-check)
5. Manual reconciliation tool (admin can fix payment ↔ form mismatches)
6. Comprehensive logging (every step of payment flow logged)
7. Test payment failure scenarios (declined card, network timeout, webhook delay)

**Implementation Pattern:**
```python
# Pseudo-code showing transaction safety
async def publish_form(form_id, payment_details):
    async with database.transaction():
        # Step 1: Process payment
        payment = await stripe.charge(payment_details)
        
        if payment.status != "succeeded":
            # Payment failed - rollback transaction
            raise PaymentFailedError()
        
        # Step 2: Only if payment succeeded, publish form
        form.status = "published"
        form.public_url = generate_url()
        form.published_at = utcnow()
        
        # Step 3: Save payment record
        save_payment(payment)
        
        # Transaction commits - all or nothing (ACID guarantee)
```

**Recommendation:** Include payment reconciliation workflow in Epic 7 (Payments & Billing)

---

#### Risk Category 10: Data Quality Degradation

**RISK: >90% valid lead target not met**
- Forms collect bad data (invalid emails, fake phone numbers, spam)
- Customers churn due to poor lead quality (retention driver)
- Validation not strict enough or easily bypassed

**Severity:** HIGH ⚠️ (Core value proposition)

**Mitigations:**
1. ✅ Field-level validation (frontend + backend double-check)
2. ✅ Preview testing requirement (5 tests minimum before publish)
3. Email verification service (check if email exists, not just format)
4. Phone validation service (Australian number format validation)
5. Honeypot fields (invisible fields that catch bots)
6. Rate limiting (prevent spam submissions: max 10 submissions per IP per hour)
7. Quality metrics dashboard (track % valid leads per form)
8. Customer feedback on lead quality (post-event survey)
9. CAPTCHA for public forms (optional, if spam becomes issue)

**Quality Metrics to Track:**
- Email bounce rate (invalid emails)
- Phone number format failures
- Duplicate submissions (same person multiple times)
- Suspicious patterns (bot-like behavior)

**Recommendation:** Data quality monitoring as part of Epic 8 (Analytics)

---

#### Risk Category 11: BMAD Agent Violating Database Standards

**RISK: BMAD agents generate code that violates your naming conventions**
- Alembic auto-generates migrations using snake_case instead of PascalCase
- Agents forget `Is` prefix for boolean columns
- Column names don't follow `[ReferencedTableName]ID` pattern
- Constant manual fixes required (your v4 experience)

**Severity:** MEDIUM-HIGH ⚠️ (Quality of life + data integrity)

**Mitigations:**
1. ✅ Database standards documented in architecture (authoritative reference)
2. ✅ Standards included in EVERY story-context XML (agents see rules every time)
3. Create Database Migration Validator Agent (using BMad Builder)
4. Pre-commit hooks (validate migrations before git commit allowed)
5. Custom Alembic templates (auto-generate PascalCase by default)
6. Story acceptance criteria MUST include "Database standards validated"
7. Example migrations in architecture (show correct patterns)
8. Migration checklist (manual review against standards)

**Example Validator Agent:**
```
Agent: Database Migration Validator
Menu: *validate-migration

Workflow:
1. Load database standards from architecture.md
2. Parse SQL migration file
3. Check: Table names PascalCase? ✓
4. Check: Column names PascalCase? ✓
5. Check: Boolean fields have Is/Has prefix? ✓
6. Check: Foreign keys follow [TableName]ID pattern? ✓
7. Check: All text fields use NVARCHAR? ✓
8. Report: PASS or list violations
```

**Recommendation:** 
- Use BMad Builder to create Database Migration Validator BEFORE Epic 1 implementation
- Integrate validator into story-context workflow (automatic validation)

---

#### Risk Category 12: Epic Boundary Violations (Cross-Epic Contamination)

**RISK: Epic 2 agents modify Epic 1 code (your v4 experience)**
- Developer agent changes authentication code while building events feature
- "Completed" Epic 1 code requires re-testing
- Timeline slippage from rework
- Regression bugs introduced

**Severity:** HIGH ⚠️ (Your specific pain point from v4)

**Mitigations:**
1. ✅ Story-context XML with forbidden zones (v6 feature)
2. Each tech-spec defines EXACT file boundaries (what this epic touches, what it doesn't)
3. Story-context includes `<forbidden-zones>` list:
   ```xml
   <forbidden-zones>
     <zone>backend/modules/auth/ - Epic 1 COMPLETE - DO NOT MODIFY</zone>
     <zone>frontend/components/Auth/ - Epic 1 COMPLETE - DO NOT MODIFY</zone>
     <zone>database/migrations/001-005_*.sql - Epic 1 - READ ONLY</zone>
   </forbidden-zones>
   ```
4. Git pre-commit hook (blocks commits that touch forbidden zones)
5. Epic Boundary Guardian Agent (using BMad Builder) - validates no cross-epic changes
6. Fresh context window for each story review (no context bleed-over)
7. Epic retrospective captures learnings WITHOUT changing Epic 1 code

**Example Story-Context Pattern:**
```xml
<story-context epic="3" story="3.2">
  <title>Create Event CRUD endpoints</title>
  
  <allowed-files>
    - backend/modules/events/routes.py (NEW - create this file)
    - backend/modules/events/models.py (NEW)
    - database/migrations/006_create_event_table.sql (NEW)
  </allowed-files>
  
  <read-only-dependencies>
    - backend/modules/auth/middleware.py (USE, don't modify)
    - backend/modules/companies/models.py (REFERENCE, don't modify)
  </read-only-dependencies>
  
  <forbidden-zones>
    - backend/modules/auth/ (Epic 1 COMPLETE - DO NOT TOUCH)
    - backend/modules/companies/ (Epic 2 COMPLETE - DO NOT TOUCH)
    - frontend/components/Auth/ (Epic 1 COMPLETE - DO NOT TOUCH)
  </forbidden-zones>
</story-context>
```

**Recommendation:** 
- Create Epic Boundary Guardian Agent (using Builder) BEFORE Epic 2 starts
- Guardian validates git commits before they're allowed
- Include boundary validation in review-story workflow

---

#### Risk Category 13: Multi-Tenant Data Breach via Query

**RISK: SQL injection or ORM bypass exposes cross-company data**
- Malicious user crafts request to see other company's data
- ORM query doesn't include CompanyID filter
- Direct SQL queries bypass row-level security

**Severity:** CRITICAL 🚨

**Mitigations:**
1. SQL Server Row-Level Security (RLS) policies on ALL tenant tables
2. Parameterized queries ONLY (prevents SQL injection)
3. ORM query builder (SQLAlchemy) - never raw SQL from user input
4. FastAPI dependency injection for current company (auto-included in all endpoints)
5. Security testing: Attempt to access other company's data (must fail)
6. Input validation (sanitize all user inputs)
7. API rate limiting (prevent brute-force attacks)

**SQL Server RLS Example:**
```sql
-- Create security policy for Form table
CREATE SECURITY POLICY FormSecurityPolicy
ADD FILTER PREDICATE dbo.fn_SecurityPredicate(CompanyID)
ON dbo.Form
WITH (STATE = ON);

-- Function checks current user's company
CREATE FUNCTION dbo.fn_SecurityPredicate(@CompanyID BIGINT)
RETURNS TABLE
AS RETURN
    SELECT 1 AS result
    WHERE @CompanyID = CAST(SESSION_CONTEXT(N'CompanyID') AS BIGINT);
```

**Recommendation:** Multi-tenant security patterns defined in architecture, enforced in Epic 2

---

#### Risk Category 14: WebSocket Connection Failures (Analytics Real-Time Updates)

**RISK: WebSocket connection drops, analytics stop updating**
- Network interruption at event (unreliable event venue WiFi)
- User thinks system is broken (no new leads showing)
- Loss of "real-time" value proposition

**Severity:** MEDIUM ⚠️

**Mitigations:**
1. WebSocket reconnection logic (auto-retry on disconnect)
2. Fallback to polling (if WebSocket fails, poll every 5 seconds)
3. Visual indicator (shows connection status: "Live" or "Reconnecting...")
4. Optimistic updates (show submission immediately, confirm via WebSocket)
5. Manual refresh button (user can force update)
6. Graceful degradation (if real-time fails, still functional with manual refresh)

**Why this is acceptable:**
- Analytics is "nice to have" real-time, not critical
- Manual refresh is acceptable fallback
- REST API always works (WebSocket is enhancement)

---

#### Risk Category 15: Stripe Payment Service Outage

**RISK: Stripe is down when customer tries to publish form**
- Customer can't publish form (blocked at payment)
- Lost revenue
- Frustrated customer (urgent event deadline)

**Severity:** MEDIUM (Rare but impactful)

**Mitigations:**
1. Stripe has 99.99% uptime (very reliable)
2. Clear error message: "Payment service temporarily unavailable. Please try again in a few minutes."
3. Retry mechanism (user can attempt payment again)
4. Email notification to admin (Stripe outage detected)
5. Status page link (users can check Stripe status)

**Why this is acceptable:**
- Stripe outages are rare (<1 hour per year)
- No alternative payment processor for MVP (Stripe is industry standard)
- Can add PayPal in Phase 2 if needed (backup payment method)

---

#### Risk Category 16: Azure Service Outages (Production Downtime)

**RISK: Azure App Service, SQL Database, or Blob Storage unavailable**
- Published forms don't load (event booth disaster)
- Dashboard unavailable (can't create forms)
- Data loss if database unavailable

**Severity:** HIGH ⚠️ (Violates 99.5% uptime requirement)

**Mitigations:**
1. ✅ Azure has 99.9% SLA (Service Level Agreement)
2. Azure SQL Database with geo-redundancy (automatic backup)
3. Azure Blob Storage with geo-replication (images replicated)
4. Health check endpoints (monitor service availability)
5. Status page for customers (communicate outages)
6. Database backups (daily automated, can restore)

**Monitoring:**
- Azure Application Insights (real-time health monitoring)
- Uptime monitoring (ping forms every 60 seconds)
- Alert system (email/SMS if downtime detected)

**Why this is acceptable:**
- Azure reliability is high (Microsoft-managed infrastructure)
- MVP budget can't afford multi-cloud redundancy
- 99.5% target achievable with Azure SLA (99.9%)

---

### Risk Prioritization Matrix

| Risk | Severity | Likelihood | Priority | Mitigation Timing |
|------|----------|------------|----------|-------------------|
| Multi-Tenant Data Breach | CRITICAL | Medium | **P0** | Epic 2 (Week 5) |
| SQL Injection / Query Bypass | CRITICAL | Low-Medium | **P0** | Epic 2 (Week 5) |
| Solo Developer Burnout | HIGH | Medium-High | **P1** | Ongoing |
| Frontend Complexity | HIGH | Medium | **P1** | POC Week 9 |
| Epic Boundary Violations | HIGH | Medium | **P1** | Before Epic 2 |
| Payment Integration Failures | HIGH | Low-Medium | **P1** | Epic 7 (Week 7) |
| Data Quality Issues | HIGH | Medium | **P1** | Epic 8 (Week 19) |
| Database Migration Errors | MEDIUM-HIGH | Medium | **P2** | Before Epic 1 |
| Form Builder Performance | MEDIUM-HIGH | Medium | **P2** | POC Week 9-10 |
| Azure Service Outages | HIGH | Low | **P2** | Week 21 (monitoring) |
| Environment Abstraction | MEDIUM | Medium | **P2** | Week 4 (early test) |
| Monolith Scalability | MEDIUM | Low | **P3** | Monitor post-launch |
| WebSocket Failures | MEDIUM | Medium | **P3** | Epic 8 (Week 19) |
| Stripe Outages | MEDIUM | Very Low | **P3** | Monitoring only |
| Timeline Pressure | HIGH | High | **P1** | Now + Weekly reviews |

**P0 = Critical (Must address before Epic 2)**  
**P1 = High (Address during respective epic)**  
**P2 = Medium (Include in architecture, validate during development)**  
**P3 = Low (Monitor, acceptable risk)**

---

### Critical Pre-Implementation Actions (Before Epic 1 Starts)

Based on risk analysis, complete these BEFORE starting implementation:

**Week 0 (Before Epic 1):**
1. **Create Database Migration Validator Agent** (using BMad Builder)
   - Validates all migrations against your naming standards
   - Integrated into story-context workflow

2. **Setup Environment Abstraction Layers** (architecture patterns defined)
   - StorageProvider interface (local vs Azure Blob)
   - EmailProvider interface (MailHog vs Azure Communication Services)
   - Configuration management (environment-specific settings)

3. **Define Multi-Tenant Security Patterns** (Epic 2 foundation)
   - SQL Server Row-Level Security (RLS) design
   - CompanyID filtering strategy
   - Security testing checklist

4. **Create Epic Boundary Guardian Agent** (using BMad Builder) - BEFORE Epic 2
   - Validates no cross-epic modifications
   - Forbidden zones enforcement

**Week 4 (Early Validation):**
5. **Test Environment Switching** (local → Azure transition)
   - Deploy simple endpoint to Azure
   - Validate abstraction layers work
   - Catch environment issues early

**Week 9-10 (Form Builder POC):**
6. **Validate Form Builder Feasibility**
   - Drag-and-drop performance at 4x CPU throttling
   - Collision detection performance
   - Undo/Redo memory usage
   - Decision: Proceed or pivot to simpler approach

---

### Technology Selection from First Principles

This section validates our technology choices by rebuilding from fundamental truths rather than assumptions or industry trends.

#### Methodology: Strip Away Assumptions

Rather than accepting "best practices" or "industry standards," we validate each decision against the project's fundamental constraints and requirements.

**Fundamental Truths (Non-Negotiable):**
1. Solo developer (Anthony) with data management expertise, limited frontend experience
2. 5.5-month maximum timeline (aggressive for Level 4 project)
3. Bootstrap budget (no team, no contractors unless critical)
4. Multi-tenant SaaS with complex form builder (60+ stories, 8-10 epics)
5. Azure + SQL Server infrastructure already available
6. Local development required (can't pay for cloud during development)
7. Must differentiate from Google Forms (custom backgrounds, freeform positioning)
8. "Form live in 5 minutes" value proposition (speed is competitive advantage)
9. Enterprise-grade data management (audit, lineage, quality - non-negotiable)

#### Question 1: Should we use Monolith or Microservices?

**Testing from First Principles:**

**Microservices would require:**
- Managing 5-8 separate services (Auth Service, Form Service, Payment Service, etc.)
- Inter-service communication (network calls between services)
- Distributed transactions (payment in one service, form publish in another)
- 5-8 separate deployments
- Service discovery and orchestration
- More complex local development (Docker Compose with 8+ containers)

**From Truth 1 (solo developer):**
- Microservices = 30-40% more complexity
- One person managing 8 services vs 1 application
- More moving parts = more potential failures

**From Truth 2 (5.5-month timeline):**
- Time spent on infrastructure vs features
- Microservices coordination takes weeks away from feature development

**From Truth 5 (Azure infrastructure):**
- Monolith = ONE Azure App Service instance
- Microservices = 5-8 App Service instances = higher cost

**CONCLUSION: Modular Monolith is the ONLY choice that satisfies constraints**
- NOT because "it's simpler" (abstract claim)
- BUT because: Solo developer + 5.5 months + bootstrap budget = cannot afford microservices overhead

**Mathematical Reality:**
- Microservices overhead: 30-40% (documented industry standard)
- 22 weeks × 40% = 9 weeks of overhead
- 22 - 9 = 13 weeks remaining for features
- 60 stories ÷ 13 weeks = 4.6 stories/week (unsustainable for solo dev)

**Validation:** ✅ Modular Monolith is not just "better" - it's the ONLY viable option

---

#### Question 2: Should we use Monorepo or Polyrepo?

**Testing from First Principles:**

**Polyrepo would require:**
- Separate repos: `eventlead-frontend`, `eventlead-backend`, `eventlead-database`
- Version coordination (ensure frontend v1.2.3 works with backend v1.2.3)
- Separate git clones (3 directories on local machine)
- Cross-repo changes (change API contract = update both repos)

**From Truth 1 (solo developer):**
- No team = no need for separate permissions
- No team = no parallel development across repos
- Context switching already hard (frontend brain → backend brain) - multiple repos makes worse

**From Truth 3 (tight frontend-backend coupling):**
- Form builder API calls: Frontend needs backend endpoints
- TypeScript types shared between layers
- API contract changes affect both layers simultaneously

**Example Feature: "Add event filtering"**
```
Monorepo (ONE commit):
  - frontend/components/EventFilter.tsx
  - backend/api/routes/events.py (add filter params)
  - database/migrations/007_add_event_indexes.sql
  git commit -m "Add event filtering" → DONE

Polyrepo (THREE commits, THREE repos):
  1. eventlead-database: Add migration → commit → version 1.2.3
  2. eventlead-backend: Add filter endpoint → update to db 1.2.3 → commit → version 1.4.5
  3. eventlead-frontend: Add UI component → update to backend 1.4.5 → commit → version 2.1.1
  → 3x coordination overhead
```

**CONCLUSION: Monorepo is the ONLY choice that meets timeline**
- Polyrepo would add 20-30% coordination overhead
- 22 weeks × 25% = 5.5 weeks wasted on coordination
- Solo developer cannot afford this waste

**Validation:** ✅ Monorepo is not preference - it's mathematical necessity

---

#### Question 3: Must form builder run Client-Side (browser)?

**Testing the assumption:** Could server-side work?

**Server-Side Form Builder (hypothetical):**
```
User drags component:
  1. Browser sends: "Move component 47 to position x:245, y:380"
  2. Network round-trip to server: 100-500ms
  3. Server calculates new layout
  4. Server sends preview image back
  5. Browser displays preview
  Total time: 200-700ms per interaction
```

**From Truth 8 ("form live in 5 minutes" value proposition):**
- User builds form with ~100 interactions (drag, resize, style)
- 100 interactions × 500ms = 50 seconds of waiting
- 50 seconds of lag = frustrating, not "5 minutes"

**From Truth 7 (differentiation from Google Forms):**
- Google Forms = instant feedback (client-side)
- Our server-side approach = laggy feedback
- We'd be WORSE than competitor (unacceptable)

**Physics Reality:**
- 60fps (frames per second) = 16.67ms per frame
- Network round-trip = 100-500ms (minimum)
- 500ms ÷ 16.67ms = 30 frames of lag
- Human perception: >100ms lag = noticeable, >200ms = frustrating

**CONCLUSION: Client-side is NOT a choice - it's a physical requirement**
- Server-side violates fundamental physics (network latency)
- Client-side is the ONLY way to achieve 60fps interactions

**Validation:** ✅ Client-side is correct - no viable alternative exists

---

#### Question 4: Do we REALLY need Freeform Drag-Drop? (First Principles Challenge)

**Testing the core assumption:** Is freeform positioning REQUIRED for differentiation?

**From Truth 7 (differentiation from Google Forms):**
- Google Forms = generic templates
- Our value = custom backgrounds + positioned components

**From Truth 4 (competitive speed):**
- "Form live in 5 minutes" vs "$200 contractor, 2-3 days"

**Alternative Approaches:**

**Option A: Freeform Positioning (Current Design)**
- Drag components anywhere on canvas
- Collision detection, snap-to-grid, undo/redo
- Complexity: HIGH (12-15 stories)
- Risk: HIGH (Week 10 POC validates feasibility)

**Option B: Grid-Based Positioning**
- Components snap to grid (like PowerPoint)
- Still custom backgrounds
- Still drag-and-drop (simpler)
- Complexity: MEDIUM (8-10 stories)
- Risk: MEDIUM (proven pattern, less complex)

**First Principles Test: Does Grid-Based achieve differentiation?**

✅ **Custom backgrounds:** YES (same as freeform)
✅ **Better than Google Forms:** YES (still branded and visual)
✅ **Faster than contractor:** YES (still 5 minutes)
✅ **Beautiful forms:** YES (background + styling enough for "beautiful")

⚠️ **Less than freeform:** YES (some positioning constraints)

**INSIGHT: Grid-based provides 80% of value with 50% of complexity**

**Architecture Decision:**
- **Primary approach:** Freeform positioning (as designed in PRD/UX spec)
- **Contingency:** Grid-based positioning (if Week 10 POC shows freeform too complex)
- **Architecture design:** Modular form renderer (supports BOTH approaches without major refactor)

**Modular Renderer Design:**
```typescript
// Form Renderer Interface (abstraction)
interface FormRenderer {
  renderComponent(component: FormComponent): JSX.Element;
  handleDrag(component: FormComponent, position: Position): void;
  validatePosition(position: Position): boolean;
}

// Freeform Implementation (Option A)
class FreeformRenderer implements FormRenderer {
  handleDrag(component, position) {
    // Allow any position within bounds
    // Check collision detection
    // Allow placement if no overlap
  }
}

// Grid-Based Implementation (Option B - Contingency)
class GridRenderer implements FormRenderer {
  handleDrag(component, position) {
    // Snap to nearest grid cell
    // Simpler collision (grid cells occupied or not)
    // Much simpler logic
  }
}

// Application uses interface (can swap implementations)
const renderer = useFormRenderer(); // Returns Freeform or Grid based on config
renderer.handleDrag(component, newPosition); // Works with either!
```

**Decision Point: Week 10 POC**
- Test freeform at 4x CPU throttling
- If smooth (60fps): Proceed with freeform ✅
- If laggy (<30fps): Switch to grid-based ⚠️
- Architecture supports BOTH (low switching cost)

**Recommendation:** Include "Modular Form Renderer" section in architecture

---

## **Form Builder Data Loss Prevention Strategy**

Now addressing your auto-save concern:

### **Hybrid Auto-Save Architecture**

**Strategy: Local Storage + Database (Dual-Layer Safety)**

**Layer 1: Local Storage (Browser-Based, Offline-Safe)**
- **Frequency:** Every 5 seconds
- **Storage:** Browser's localStorage API (5-10MB available)
- **Survives:** Browser crash, tab close, power outage, network issues
- **Does NOT survive:** Browser data clear, switching devices, different browser

**Layer 2: Database Auto-Save (Server-Based, Persistent)**
- **Frequency:** Every 30 seconds
- **Storage:** Form table in SQL Server (DesignJSON column)
- **Survives:** Everything (browser clear, device switch, browser crash)
- **Requires:** Network connection

**Recovery Logic:**

```
On Form Builder Load:
  1. Fetch database draft (latest server-side save)
  2. Check local storage for draft (latest client-side save)
  3. Compare timestamps:
     - IF local storage newer: Show recovery prompt
     - IF database newer: Load database version
     - IF timestamps equal: Load normally
  4. User choice: "Restore" or "Discard" unsaved changes
```

**Maximum Data Loss:**
- Best case: 0 seconds (both layers saved)
- Typical case: <5 seconds (local storage interval)
- Worst case: <30 seconds (if network down + local storage cleared)
- Catastrophic case: Never (database always has last save)

**User-Visible Indicators:**

```
Top bar save status:
┌─────────────────────────────────────────────────┐
│ [Form Name] | Saved 3 seconds ago ● | [Publish] │
└─────────────────────────────────────────────────┘

States:
- "Saving..." (gray dot pulsing) → Currently saving to local storage
- "Saved 3 seconds ago ●" (green dot) → Local storage saved
- "Saving to cloud..." (cloud icon) → Database save in progress
- "All changes saved ☁✓" (cloud + check) → Both local and database saved
- "Offline - saving locally only ⚠" (warning) → Network down, local only
```

**Implementation Details:**

**Local Storage Schema:**
```javascript
// Browser localStorage key-value store
Key: `form-draft-${formId}`
Value: {
  formId: 456,
  timestamp: 1697123456789,  // Unix timestamp
  version: 1,  // Schema version (for future migrations)
  formState: {
    components: [...],  // All dragged components
    background: {...},  // Background image settings
    canvas: {...},      // Canvas dimensions, grid settings
    history: [...],     // Undo/redo stack (last 50 actions)
  }
}
```

**Database Schema (Already in PRD):**
```sql
Form table:
  - FormID (PK)
  - DesignJSON (NVARCHAR(MAX)) -- Auto-saved form state
  - UpdatedAt (DATETIME2) -- Last auto-save timestamp
  - UpdatedBy (BIGINT FK) -- User who last edited
```

**Recovery Flow:**
```javascript
async function checkForRecovery(formId) {
  // 1. Get database version
  const dbDraft = await api.getFormDraft(formId);
  const dbTime = dbDraft?.updatedAt || 0;
  
  // 2. Get local storage version
  const localKey = `form-draft-${formId}`;
  const localDraft = localStorage.getItem(localKey);
  const localData = localDraft ? JSON.parse(localDraft) : null;
  const localTime = localData?.timestamp || 0;
  
  // 3. Compare timestamps
  if (localTime > dbTime) {
    const timeDiff = formatTimeDiff(localTime - dbTime);
    const userChoice = await showRecoveryModal({
      message: `Restore unsaved changes from ${timeDiff} ago?`,
      options: ['Restore', 'Discard'],
    });
    
    if (userChoice === 'Restore') {
      return localData.formState;  // Use local storage (newer)
    } else {
      localStorage.removeItem(localKey);  // Clear outdated local storage
      return dbDraft.designJSON;  // Use database version
    }
  }
  
  // 4. Database is newer or equal - use it
  return dbDraft?.designJSON || createNewForm();
}
```

**Network Failure Handling:**
```javascript
async function autoSaveToDatabase(formState) {
  try {
    await api.saveDraft(formId, formState);
    updateIndicator('All changes saved ☁✓');
  } catch (networkError) {
    // Network down - local storage still working
    updateIndicator('Offline - saving locally only ⚠');
    // Auto-retry every 60 seconds
    scheduleRetry();
  }
}
```

**Benefits Summary:**
1. ✅ **User Confidence:** Visible save indicators build trust
2. ✅ **Data Safety:** Dual-layer protection (near-zero data loss)
3. ✅ **Offline Support:** Can build forms without network (local storage)
4. ✅ **Cross-Device:** Database sync allows device switching
5. ✅ **Recovery UX:** Clear prompts, user control over recovery

**Architecture Impact:**
- Add "Auto-Save Strategy" section to architecture
- Include in Epic 5 (Form Builder) tech spec
- Story acceptance criteria: "Auto-save works offline and online"

---

### Technology Stack Validation (From First Principles)

#### Frontend: Why React 18+?

**From fundamental requirements:**
- Complex state management (form builder with undo/redo, drag-drop)
- Component-based UI (20 components defined in UX spec)
- Large ecosystem needed (drag-drop library, charts, form library)
- BMAD agent support (better code generation for popular frameworks)

**Alternatives Considered:**

**Vue.js:**
- Pros: Simpler learning curve, good documentation
- Cons: Smaller ecosystem (fewer drag-drop libraries), less BMAD training data
- Conclusion: Not enough ecosystem for complex form builder

**Angular:**
- Pros: Full framework, TypeScript native, enterprise-grade
- Cons: Steepest learning curve, very opinionated, heavier
- Conclusion: Learning curve violates Truth 1 (limited frontend experience) + Truth 2 (timeline)

**Svelte:**
- Pros: Simpler syntax, compiled (smaller bundle)
- Cons: Smaller ecosystem, fewer drag-drop libraries, newer (less mature)
- Conclusion: Not enough mature libraries for enterprise form builder

**Vanilla JavaScript (No Framework):**
- Pros: No framework learning curve, full control
- Cons: Must build everything from scratch (state management, routing, components)
- Conclusion: Would take 12+ months (violates Truth 2)

**CONCLUSION: React 18+ emerges as ONLY viable option**
- Largest ecosystem: dnd-kit (drag-drop), React Hook Form, Recharts (analytics)
- Best BMAD support: More training data = better code generation
- Huge community: More Stack Overflow answers when stuck
- Component model: Matches UX spec design (20 components)

**Specific Version: React 18.2.0**
- Latest stable (as of 2025-10-12)
- Concurrent rendering (better performance for drag-drop)
- Automatic batching (fewer re-renders = smoother UX)

**Validation:** ✅ React is not preference - it's the only option that satisfies all constraints

---

#### Backend: Why FastAPI?

**From fundamental requirements:**
- Async operations needed (WebSockets for real-time analytics, background tasks)
- Auto-generated API documentation (reduces solo developer burden)
- Modern Python typing (better editor support for beginner)
- Must integrate with SQL Server

**Alternatives Considered:**

**Django:**
- Pros: Mature, full-featured, excellent ORM, large community
- Cons: Synchronous by default (not async-first), heavier, admin UI we don't need
- From Truth 3 (WebSocket real-time): Django async support is newer, less mature

**Flask:**
- Pros: Lightweight, flexible, minimalist
- Cons: No async support, no auto-generated docs, requires many extensions
- From Truth 1 (solo developer): Too many decisions (which ORM? which validation? which async?)

**FastAPI:**
- Pros: **Async-first, auto-generates OpenAPI docs, modern typing, lightweight**
- Cons: Newer than Django/Flask (but stable since 2019)
- From Truth 3 (WebSocket): Native async support, excellent WebSocket integration
- From Truth 1 (solo dev): Auto-docs reduce documentation burden

**CONCLUSION: FastAPI emerges from async requirement**
- NOT because "it's modern"
- BUT because: Real-time analytics + background tasks = async framework required
- Auto-docs = solo developer productivity multiplier

**Specific Version: FastAPI 0.104.1**
- Latest stable (as of 2025-10-12)
- Python 3.11+ support (better performance)
- Pydantic v2 (10x faster validation)

**Validation:** ✅ FastAPI is not trend-following - it's requirement-driven

---

#### Database: Why MS SQL Server?

**From Truth 5 (existing infrastructure):**
- Already have Azure SQL Database configured
- Already have local SQL Server OR can use Docker container
- Zero setup cost (already available)

**From Truth 1 (Anthony's expertise):**
- Extensive experience with SQL Server
- Knows enterprise features (Row-Level Security, audit tracking, indexing)
- Can leverage existing knowledge (fast development)

**From Truth 9 (enterprise data management):**
- Row-Level Security (RLS) for multi-tenant isolation
- Advanced indexing (query performance)
- Audit tracking capabilities
- ACID transactions

**Alternatives Considered:**

**PostgreSQL:**
- Pros: Open source, excellent features, similar to SQL Server
- Cons: Anthony has SQL Server expertise (learning curve), Azure setup needed
- From Truth 2 (timeline): Switching databases = 2-3 weeks learning + migration

**MySQL:**
- Pros: Popular, simple
- Cons: Less enterprise features (weaker RLS, less robust JSON support)
- From Truth 9 (enterprise data): MySQL insufficient for audit/lineage requirements

**MongoDB (NoSQL):**
- Pros: Flexible schema, JSON native
- Cons: Not relational (bad fit for normalized schema), Anthony's expertise is relational
- From Truth 1 (expertise): Would waste Anthony's strongest skill

**CONCLUSION: SQL Server is not just available - it's strategically correct**
- Leverages Anthony's expertise (productivity multiplier)
- Enterprise features match requirements
- Azure integration seamless

**Specific Version: SQL Server 2022**
- Latest stable
- JSON functions improved
- Better performance
- Azure SQL Database runs 2022

**Validation:** ✅ SQL Server leverages expertise + meets requirements

---

### Client-Side vs Server-Side Processing Strategy

Based on first principles analysis, here's what MUST run where:

#### Client-Side Processing (Browser)

**MUST run client-side (physics requirement):**
- ✅ Drag-and-drop interactions (60fps requires <16ms latency - network is 100-500ms)
- ✅ Collision detection (real-time feedback during drag)
- ✅ Undo/Redo operations (instant response expected)
- ✅ Component resizing (real-time visual feedback)
- ✅ Form preview rendering (instant updates)
- ✅ Client-side validation (instant error feedback before submission)

**Why?**
Network round-trip (100-500ms) is 10-30x slower than client processing (<16ms). For 60fps interactions, client-side is the ONLY option that satisfies physics.

#### Server-Side Processing (Backend)

**MUST run server-side (security/business logic requirement):**
- ✅ Payment processing (Stripe API calls - NEVER expose keys to client)
- ✅ Database operations (security - client cannot query database directly)
- ✅ Server-side validation (security - never trust client)
- ✅ Email sending (credentials must stay server-side)
- ✅ PDF generation (invoices - server has resources)
- ✅ Authentication (JWT token generation - server holds secrets)
- ✅ Multi-tenant filtering (CompanyID checks - security layer)

**Why?**
Security and business logic MUST be server-controlled. Client-side code can be inspected/modified by users (browser dev tools). Secrets, payments, and data access MUST stay server-side.

#### Could Be Either (Choose Based on Trade-offs)

**Image Processing (Background uploads):**
- **Client-side:** Instant feedback, reduce server load
- **Server-side:** Consistent results, more powerful processing
- **Decision:** Hybrid approach
  - Client: Resize for preview (instant feedback)
  - Server: Optimize for storage (consistent quality)

**Form Validation:**
- **Client-side:** Instant user feedback (UX improvement)
- **Server-side:** Security enforcement (never trust client)
- **Decision:** BOTH (client for UX, server for security)

---

### Minimum Viable Architecture (Core vs Enhancement)

From first principles: What's TRULY needed for MVP vs nice-to-have?

#### CORE (Cannot Ship Without)

**Must Have (Ordered by Value Delivery):**

**1. ✅ LEAD COLLECTION (Epic 8 - CORE VALUE)**
   - **Why #1:** This IS the product value - quality leads for customers
   - Public forms accept submissions
   - Store lead data (no data loss tolerance = 0)
   - Field validation (>90% valid leads = retention driver)
   - **Without this:** No product value at all

**2. ✅ CSV EXPORT (Epic 8 - VALUE REALIZATION)**
   - **Why #2:** Customers must USE leads (import to Salesforce, Marketing Cloud)
   - Salesforce format minimum (most common CRM)
   - **Without this:** Leads trapped in platform (no value realization)

**3. ✅ LEAD ANALYTICS (Epic 8 - VALUE VISIBILITY)**
   - **Why #3:** Customers must SEE leads collected (real-time proof of value)
   - Lead count, submissions list
   - **Without this:** Can't prove value during event

**4. ✅ Form Builder (Epic 5 - Value Creation Tool)**
   - **Why #4:** Creates the forms that collect leads
   - Even simplified version acceptable (grid-based positioning fallback)
   - **Without this:** No way to create lead collection forms

**5. ✅ Form Hosting (Epic 6 - Value Delivery)**
   - **Why #5:** Public URL for event attendees to submit leads
   - **Without this:** Forms can't be accessed at events

**6. ✅ Payment Integration (Epic 7 - Monetization)**
   - **Why #6:** Revenue model ($99 per publish)
   - **Without this:** No business model

**7. ✅ Events Management (Epic 3 - Organization)**
   - **Why #7:** Organize forms by event (customer mental model)
   - **Without this:** Poor UX (forms not organized)

**8. ✅ Company + Multi-Tenant (Epic 2 - Foundation)**
   - **Why #8:** Enables team collaboration, data isolation
   - **Without this:** Not a SaaS platform

**9. ✅ Authentication + Onboarding (Epic 1 - Access)**
   - **Why #9:** Access control, user accounts
   - **Without this:** No secure access

**10. ✅ Database with Audit Tracking (Epic 9 - Quality & Compliance)**
   - **Why #10:** Data quality, compliance, debugging
   - **Without this:** No enterprise credibility

**Why this order matters:**
- **Leads are #1** (the product's value)
- **Export is #2** (value realization - use leads in CRM)
- **Analytics is #3** (value visibility - see leads during event)
- Everything else enables these three core capabilities

#### ENHANCEMENTS (Could Cut If Timeline Pressure)

**Nice to Have (Can Add Post-MVP):**
1. ⚠️ Collision detection (forms work without it - just allow overlap)
2. ⚠️ Undo/Redo (users can manually fix mistakes)
3. ⚠️ Multiple CSV formats (start with Salesforce only)
4. ⚠️ Real-time analytics (polling fallback acceptable)
5. ⚠️ Template library (start with custom backgrounds only)
6. ⚠️ Advanced drag cursors (standard cursor works)
7. ⚠️ Preview test enforcement (trust users initially)
8. ⚠️ Company User role (start with Admin-only, add Users in Phase 2)

**Fallback Priority (If Week 16 shows timeline risk):**
1. First cut: Collision detection (save 1 week)
2. Second cut: Undo/Redo (save 1.5 weeks)
3. Third cut: Template library (save 0.5 weeks)
4. Fourth cut: Company User role (save 1 week)

**Total fallback capacity: 4 weeks** (covers timeline contingency)

**Architecture Principle: Design for Full, Build for MVP, Cut If Needed**
- Architecture supports full vision (collision detection, undo/redo, etc.)
- Implementation prioritizes core features first
- Enhancements added if time permits

---

### Modular Form Renderer Design (Contingency Architecture)

To support freeform vs grid-based contingency:

**Design Pattern: Strategy Pattern (Swappable Rendering Engines)**

```typescript
// Renderer Interface (abstraction)
interface IFormRenderer {
  // Position validation
  validatePosition(component: FormComponent, position: Position): boolean;
  
  // Drag handling
  handleDragStart(component: FormComponent): void;
  handleDragMove(component: FormComponent, position: Position): Position;
  handleDragEnd(component: FormComponent, position: Position): void;
  
  // Collision detection
  checkCollisions(component: FormComponent, allComponents: FormComponent[]): boolean;
  
  // Rendering
  renderComponent(component: FormComponent): JSX.Element;
}

// Freeform Implementation (Primary)
class FreeformRenderer implements IFormRenderer {
  validatePosition(component, position) {
    // Can be anywhere within screen bounds
    return isWithinBounds(position, this.screenBounds);
  }
  
  checkCollisions(component, allComponents) {
    // Bounding box overlap detection
    return allComponents.some(other => 
      boxesOverlap(component.bounds, other.bounds)
    );
  }
  
  handleDragMove(component, position) {
    // Freeform - any position allowed
    // Check collision and show warning
    return position;
  }
}

// Grid-Based Implementation (Contingency)
class GridRenderer implements IFormRenderer {
  validatePosition(component, position) {
    // Must align to grid
    return isOnGrid(position, this.gridSize);
  }
  
  checkCollisions(component, allComponents) {
    // Simpler: Check if grid cell occupied
    const gridCell = positionToGridCell(component.position);
    return this.occupiedCells.has(gridCell);
  }
  
  handleDragMove(component, position) {
    // Snap to nearest grid cell
    return snapToGrid(position, this.gridSize);
  }
}

// Factory: Returns appropriate renderer
function createFormRenderer(config: RendererConfig): IFormRenderer {
  if (config.renderMode === 'freeform') {
    return new FreeformRenderer(config);
  } else {
    return new GridRenderer(config);
  }
}

// Form Builder uses interface (doesn't know implementation)
const renderer = useFormRenderer(); // Config determines which
renderer.handleDragMove(component, newPosition); // Works with either!
```

**Benefits:**
- ✅ Week 10 POC tests freeform performance
- ✅ If fails: Switch to grid-based (change config, not code)
- ✅ Low switching cost (1-2 days vs 2-3 weeks rewrite)
- ✅ Both approaches share: Component library, styling, save logic, preview

**Architecture Decision:** Include modular renderer in form builder architecture section

---

### Integration Risk Management (Addressing v4 Lessons)

This section addresses the meta-risk of "unknown unknowns" - conflicts between features that aren't apparent in initial risk assessment but emerge during development or library updates.

#### Problem Statement

**From v4 Experience:**
- Initial architecture appeared sound
- Library update introduced unexpected conflict with existing features
- Conflict wasn't in original risk assessment
- Required rework and timeline slippage

**Common Integration Conflicts:**
- Auto-save interrupts undo/redo operations
- Auto-save captures temporary drag state (component "mid-air")
- Batch operations saved in partial state (inconsistent data)
- Library updates break saved state schema (incompatible versions)
- Preview mode state saved when edit mode expected

**Why this happens:**
- Features developed in isolation don't reveal integration issues
- Library updates change internal behavior
- Complex state interactions hard to predict upfront

---

#### Prevention Strategy

**1. POC (Proof of Concept) Validates Integrations Early**

**Week 9-10 POC Scope:**
Build minimal form builder with ALL complex features working TOGETHER:
- ✅ Drag-and-drop (dnd-kit)
- ✅ Auto-save (local storage + database)
- ✅ Undo/Redo (history stack)
- ✅ Collision detection (overlap prevention)
- ✅ Component framework (form-level defaults)

**What we're testing:**
- Do auto-save and undo/redo conflict?
- Does auto-save interrupt drag operations?
- Does collision detection affect performance with auto-save?
- Do all features work together smoothly?

**Decision Point:**
- If all features integrate smoothly: Proceed with full Epic 5 ✅
- If conflicts found: Redesign integration before building 12-15 stories ⚠️
- If performance fails: Switch to grid-based renderer 🔄

**Why this matters:**
- Catch integration issues with 2-week POC, not 6-week epic
- Fix architecture issues before building all stories
- Lower risk, faster iteration

---

**2. Dependency Pinning (Exact Versions)**

**Strategy: Pin EXACT library versions in package.json**

**Example:**
```json
{
  "dependencies": {
    "react": "18.2.0",           // EXACT (not "^18.2.0")
    "@dnd-kit/core": "6.0.8",    // EXACT version
    "react-hook-form": "7.48.2", // EXACT version
    "tailwindcss": "3.3.5"       // EXACT version
  }
}
```

**What this means:**
- `"react": "^18.2.0"` = "any version 18.x.x" (could auto-update to 18.9.0 with breaking changes)
- `"react": "18.2.0"` = "ONLY this version" (won't auto-update)

**Benefits:**
- ✅ No surprise updates
- ✅ We control when updates happen
- ✅ Test updates before applying
- ✅ Reproducible builds (same versions on all machines)

**Update Process:**
```bash
# We decide to update React 18.2.0 → 18.3.0
1. Read React 18.3.0 changelog (understand breaking changes)
2. Create feature branch: "update-react-18.3.0"
3. Update package.json to exact version "18.3.0"
4. Run full test suite
5. Test integration points (auto-save, undo/redo, drag-drop)
6. If all pass → merge to main
7. If conflicts → fix on branch before merging
```

---

**3. Integration Testing (Not Isolation Testing)**

**Traditional approach (risky):**
```
Test auto-save in isolation ✓
Test undo/redo in isolation ✓
Test drag-drop in isolation ✓
Ship → Features conflict in production ✗
```

**Our approach (safer):**
```
Test auto-save + undo/redo together ✓
Test auto-save + drag-drop together ✓
Test undo/redo + drag-drop together ✓
Test all three together ✓
Ship → Features work together ✓
```

**Integration Test Examples:**
```javascript
describe('Auto-Save Integration Tests', () => {
  test('Auto-save preserves undo/redo stack', async () => {
    // 1. Make 10 changes
    // 2. Auto-save happens
    // 3. Simulate crash and recovery
    // 4. Verify: Can undo all 10 changes
  });

  test('Auto-save does not trigger during drag', async () => {
    // 1. Start dragging component
    // 2. Auto-save interval triggers
    // 3. Verify: Save was skipped (isDragging flag blocked it)
    // 4. Complete drag
    // 5. Verify: Immediate save happened after drag end
  });

  test('Batch operations complete before auto-save', async () => {
    // 1. Apply defaults to 20 components (batch)
    // 2. Auto-save triggers mid-batch
    // 3. Verify: Save was blocked until batch complete
    // 4. Verify: Final save has all 20 components updated
  });
});
```

---

**4. Staged Library Update Process**

**Process:**
```
1. Monitor library changelogs (check monthly for security updates)
2. Review breaking changes (read migration guide)
3. Create feature branch (e.g., "update-dnd-kit-7.0")
4. Update package.json to new EXACT version
5. Run automated tests
6. Manual testing of integration points:
   - Auto-save + new library version
   - Undo/redo + new library version
   - Saved forms load correctly (state migration if needed)
7. If issues: Fix on branch or defer update
8. If clean: Merge to main
9. Update architecture document (note version change)
```

**When to update:**
- Security vulnerabilities: Immediately (highest priority)
- Breaking changes with value: Evaluate (cost vs benefit)
- Minor updates: Low priority (only if needed)

---

**5. Epic Retrospectives Capture New Risks**

**After each epic completion:**
```markdown
Epic 5 Retrospective Template:

**What integration conflicts did we discover?**
- Auto-save + undo/redo interaction issue?
- Drag-drop + collision detection performance problem?
- Library update broke saved state?

**How did we resolve it?**
- Migration function added
- Integration contract updated
- Testing added

**What should future epics know?**
- Update architecture document (add new risk)
- Update story-context template (include new rules)
- Share learning (don't repeat issue)
```

**Living Architecture:**
- Architecture document is updated after each epic
- New risks discovered → added to architecture
- Next epic's tech-spec includes lessons learned
- Continuous improvement (not static document)

---

#### Auto-Save Integration Contract (Formal Rules)

All form builder features MUST follow these rules:

**Rule 1: Signal Active State**
```javascript
// Features that shouldn't be interrupted MUST set flag
let isDragging = false;
let isResizing = false;
let isProcessingBatch = false;
let isEditingText = false;

// Auto-save checks ALL flags
const shouldAutoSave = !isDragging && 
                       !isResizing && 
                       !isProcessingBatch &&
                       !isEditingText;
```

**Rule 2: Complete State Atomicity**
- Save COMPLETE state or NOTHING
- No partial saves (all components or none)
- Batch operations complete before save

**Rule 3: Data vs UI Separation**
```javascript
// SAVE (permanent data)
const dataState = {
  components: [{position, size, style}],  // Data
  background: {url, scale, position},      // Data
};

// DON'T SAVE (temporary UI)
// - component.hasCollisionWarning (recalculate on load)
// - component.isHovered (recalculate on load)
// - component.isSelected (recalculate on load)
```

**Rule 4: Version All State**
```javascript
const savedState = {
  version: 1,  // Schema version
  libraryVersions: {
    dndKit: "6.0.0",
    react: "18.2.0"
  },
  formState: {...}
};
```

**Rule 5: Immediate Save After User Actions**
```javascript
function handleDragEnd() {
  // User completed action
  isDragging = false;
  
  // Immediate save (don't wait for interval)
  saveToLocalStorage();
  debouncedDatabaseSave();
}
```

---

#### Integration Testing Requirements

**Epic 5 (Form Builder) Acceptance Criteria MUST Include:**

**Integration Test Suite:**
```
✓ Auto-save preserves undo/redo stack
✓ Auto-save does not trigger during drag
✓ Auto-save does not trigger during batch operations
✓ Recovery restores complete undo/redo history
✓ Collision warnings recalculated on load (not saved)
✓ Preview mode does not persist on recovery
✓ Batch operations complete atomically (all or nothing)
✓ Library update migration preserves user data
✓ State schema versioning works correctly
✓ Immediate save after drag-end completes
```

**POC Validation (Week 9-10):**
```
✓ Drag component, auto-save triggers, undo works
✓ Undo/redo, auto-save triggers, history preserved
✓ Batch apply defaults, auto-save blocked, completes atomically
✓ Crash during drag, recovery shows last completed position
✓ All features work together smoothly
```

---

#### Potential Future Conflicts (Monitor During Development)

**Features Not Yet Built (Watch For Conflicts):**

**1. Tab Order Management + Auto-Save**
- Risk: User reordering tabs, auto-save mid-reorder
- Mitigation: Block auto-save during tab reorder (same pattern as drag)

**2. Background Resize Mode + Auto-Save**
- Risk: Background unlocked state saved permanently
- Mitigation: Save mode state explicitly (isLocked boolean)

**3. Component Properties Panel + Auto-Save**
- Risk: User editing text field, auto-save mid-edit
- Mitigation: Block auto-save while typing, save on blur

**4. Template Application + Auto-Save**
- Risk: Template loading, auto-save captures partial template
- Mitigation: Block auto-save during template load, save after complete

**Recommendation:** As each feature is implemented, update integration contract with new rules

---

### Summary: Integration Risk Mitigation

**How we prevent v4-style surprises:**

1. ✅ **POC Early (Week 9-10):** All complex features together, not isolated
2. ✅ **Exact Version Pinning:** No surprise library updates
3. ✅ **Integration Contract:** Formal rules all features follow
4. ✅ **Integration Testing:** Test features together, not separately
5. ✅ **Staged Updates:** Test library updates before applying
6. ✅ **Living Architecture:** Retrospectives update architecture with new risks
7. ✅ **Epic Boundary Protection:** Prevent changes to completed epics

**Your v4 concern directly addressed:**
- Won't update libraries without testing
- Won't build features in isolation
- Will validate integrations in POC
- Will capture new risks in retrospectives

---

## Epic Analysis and Component Boundaries

This section analyzes each epic to identify natural component/module boundaries, data operations, and integration points. This defines the modular structure within our monolith architecture.

### Value Delivery Architecture (Lead-Centric View)

**Core Insight:** The platform's entire purpose is to **collect quality leads at events**. All features serve this goal.

**Value Chain:**
```
┌────────────────────────────────────────────────────────────┐
│                    CORE VALUE                               │
│              Quality Leads Collected                        │
│         (Event attendee data in customer's CRM)             │
└──────────────────────┬─────────────────────────────────────┘
                       ↑
         ┌─────────────┴─────────────┐
         │   Lead Submission Flow     │
         │  (Public Form at Event)    │
         └─────────────┬───────────────┘
                       ↑
         ┌─────────────┴─────────────┐
         │    Published Form          │
         │  (Beautiful, Branded)      │
         └─────────────┬───────────────┘
                       ↑
         ┌─────────────┴─────────────┐
         │   Payment ($99)            │
         │  (Monetization Point)      │
         └─────────────┬───────────────┘
                       ↑
         ┌─────────────┴─────────────┐
         │   Form Builder             │
         │  (Create Beautiful Form)   │
         └─────────────┬───────────────┘
                       ↑
         ┌─────────────┴─────────────┐
         │   Event + Team Setup       │
         │  (Organization)            │
         └─────────────┬───────────────┘
                       ↑
         ┌─────────────┴─────────────┐
         │   Company + Auth           │
         │  (Foundation)              │
         └────────────────────────────┘
```

**Every feature serves lead collection:**
- **Authentication (Epic 1):** Enables user to access platform → Build forms → Collect leads
- **Company Management (Epic 2):** Enables team collaboration → More forms → More leads
- **Events (Epic 3):** Organizes lead collection by event → Contextual data
- **Team (Epic 4):** Enables collaboration → Faster form creation → More leads
- **Form Builder (Epic 5):** Creates beautiful forms → Better conversion → More leads
- **Preview/Publishing (Epic 6):** Ensures form quality → Valid leads → Customer retention
- **Payments (Epic 7):** Monetizes lead collection capability
- **Analytics (Epic 8):** **DELIVERS the value** → Leads exported to CRM → Customer success
- **Audit (Epic 9):** Ensures lead data quality and compliance

**Architecture Implication:**
- Lead collection and export must be BULLETPROOF (no data loss)
- Lead quality must be VALIDATED (>90% valid - retention driver)
- CSV export must be RELIABLE (customers must trust data)
- Real-time visibility must work (customers see value during event)

---

### Epic-to-Module Mapping

Based on domain analysis, we identify **9 core backend modules** and **corresponding frontend modules**:

```
Backend Modules:
  1. auth/          - Authentication & authorization (Epic 1)
  2. companies/     - Company management & multi-tenancy (Epic 2)
  3. events/        - Event management (Epic 3)
  4. team/          - Team collaboration & invitations (Epic 4)
  5. forms/         - Form builder & management (Epic 5, 6)
  6. payments/      - Stripe integration, billing, invoicing (Epic 7)
  7. analytics/     - Lead collection & analytics (Epic 8)
  8. audit/         - Enterprise audit & data lineage (Epic 9)
  9. images/        - Image management, storage-database alignment (Shared)

Frontend Modules:
  1. auth/          - Login, signup, onboarding components
  2. dashboard/     - Main dashboard, navigation
  3. events/        - Event list, event dashboard components
  4. team/          - Team management, invitations
  5. builder/       - Form builder (canvas, components, properties panel)
  6. analytics/     - Analytics dashboard, charts, export
  7. settings/      - Company settings, billing, user profile

Shared:
  1. components/    - Reusable UI components (20 foundation components)
  2. common/        - Shared utilities, types, constants
  3. database/      - Migrations, seed data, scripts
  4. images/        - Image upload, optimization, cleanup (backend module)
  5. storage/       - Storage abstraction layer (local vs Azure Blob)
  6. email/         - Email abstraction layer (MailHog vs Azure Communication)
```

---

### Epic 1: Authentication & Onboarding

**Domain Capabilities:**
- User signup with email verification
- Login with JWT token generation
- Password reset flow
- Multi-step onboarding (user details + company setup)
- Session management
- RBAC (Role-Based Access Control) middleware

**Data Operations:**
- **Creates:** User, Company (for first-time users)
- **Reads:** User (login validation)
- **Updates:** User (email verification, password reset, onboarding completion)
- **Deletes:** None (users soft-deleted via IsActive flag)

**Database Tables:**
- User (primary)
- Company (created during onboarding)
- PasswordResetToken (temporary tokens)
- EmailVerificationToken (temporary tokens)

**Integrations:**
- Email service (verification emails, password reset emails)
- JWT library (token generation and validation)
- Password hashing library (bcrypt or argon2)

**Backend Module:** `backend/modules/auth/`
```
auth/
  __init__.py
  routes.py              # API endpoints (/api/auth/signup, /login, /verify-email)
  models.py              # User model, token models
  schemas.py             # Pydantic request/response schemas
  dependencies.py        # JWT verification, current user dependency
  middleware.py          # RBAC middleware (checks user role)
  services/
    auth_service.py      # Business logic (signup, login, verify)
    token_service.py     # JWT generation, validation
    password_service.py  # Hashing, reset logic
  utils.py               # Helper functions
```

**Frontend Module:** `frontend/modules/auth/`
```
auth/
  components/
    SignupForm.tsx       # Email + password signup
    LoginForm.tsx        # Email + password login
    OnboardingFlow.tsx   # Multi-step wizard
    PasswordReset.tsx    # Reset password form
  hooks/
    useAuth.tsx          # Authentication state management
  contexts/
    AuthContext.tsx      # Global auth state
  services/
    authApi.ts           # API calls to backend
```

**Component Boundaries:**
- **Isolated:** Auth module does NOT call other modules directly
- **Dependencies:** None (foundational module)
- **Used By:** ALL other modules (auth middleware protects all endpoints)

---

### Epic 2: Company & Multi-Tenant Management

**Domain Capabilities:**
- Company profile management (CRUD)
- Multi-tenant data isolation (row-level security)
- Company settings
- Activity logging (comprehensive audit tracking)
- Data lineage tracking

**Data Operations:**
- **Creates:** Company (during onboarding by Epic 1)
- **Reads:** Company (all endpoints filter by CompanyID)
- **Updates:** Company profile (name, ABN, billing address, settings)
- **Deletes:** None (soft delete via IsActive)

**Database Tables:**
- Company (primary)
- ActivityLog (audit tracking - all user actions)
- CompanySettings (test threshold, analytics opt-out)

**Integrations:**
- Auth module (gets current user's CompanyID)
- ALL modules (provide multi-tenant filtering)

**Backend Module:** `backend/modules/companies/`
```
companies/
  __init__.py
  routes.py              # API endpoints (/api/companies/{id}, /settings)
  models.py              # Company, ActivityLog, CompanySettings models
  schemas.py             # Request/response schemas
  dependencies.py        # current_company dependency (auto-filter by CompanyID)
  services/
    company_service.py   # Business logic
    audit_service.py     # Audit logging (track all actions)
    lineage_service.py   # Data lineage tracking
  middleware/
    tenant_middleware.py # Row-level security enforcement
  utils.py
```

**Frontend Module:** `frontend/modules/dashboard/`
```
dashboard/
  components/
    CompanySettings.tsx   # Company profile editing
    ActivityLog.tsx       # Audit trail table
  hooks/
    useCompany.tsx        # Company state management
  contexts/
    CompanyContext.tsx    # Global company state
```

**Component Boundaries:**
- **Isolated:** Company module manages tenant context
- **Dependencies:** Auth (current user)
- **Used By:** ALL modules (tenant filtering via middleware)

**Critical Pattern: Multi-Tenant Filtering**
```python
# EVERY query MUST include CompanyID filter
async def get_current_company(
    current_user: User = Depends(get_current_user)
) -> Company:
    return await db.query(Company).filter(
        Company.CompanyID == current_user.CompanyID
    ).first()

# Dependency injection ensures ALL endpoints filter by company
@router.get("/api/events")
async def get_events(
    company: Company = Depends(get_current_company)  # ← Auto-filters
):
    # This query is automatically filtered to current company
    return await db.query(Event).filter(
        Event.CompanyID == company.CompanyID
    ).all()
```

---

### Epic 3: Events Management & Domain Features

**Domain Capabilities:**
- Event CRUD operations
- Event types (Trade Show, Conference, Expo, etc.)
- Private/personal events
- Form activation windows (auto-activate 3hrs before/after event)
- Event discovery and filtering

**Data Operations:**
- **Creates:** Event
- **Reads:** Event (filtered by company, date range, type)
- **Updates:** Event details, activation status
- **Deletes:** Soft delete (IsActive flag)

**Database Tables:**
- Event (primary)
- EventType (lookup table: Trade Show, Conference, etc.)

**Integrations:**
- Companies module (tenant filtering)
- Forms module (events contain forms)
- Scheduled jobs (activation window management)

**Backend Module:** `backend/modules/events/`
```
events/
  __init__.py
  routes.py              # API endpoints (/api/events, /api/events/{id})
  models.py              # Event, EventType models
  schemas.py             # Request/response schemas
  services/
    event_service.py     # Business logic (CRUD, filtering)
    activation_service.py # Activation window management
  tasks/
    check_activations.py # Scheduled job (check event times, activate/deactivate forms)
```

**Frontend Module:** `frontend/modules/events/`
```
events/
  components/
    EventsList.tsx       # Grid/list of events
    EventCard.tsx        # Individual event display
    EventDashboard.tsx   # Single event detail view
    CreateEventModal.tsx # Event creation form
    EventFilters.tsx     # Filter by type, date, location
  hooks/
    useEvents.tsx        # Event state management
```

**Component Boundaries:**
- **Isolated:** Event logic separate from forms
- **Dependencies:** Companies (tenant context), Auth (current user)
- **Used By:** Forms module (forms belong to events)

---

### Epic 4: Team Collaboration & Invitations

**Domain Capabilities:**
- User invitation system (secure tokens, 7-day expiry)
- Role assignment (Company Admin, Company User)
- User management (list, change roles, remove)
- Expired invitation handling (resend)
- Activity tracking per user

**Data Operations:**
- **Creates:** Invitation, User (when invitation accepted)
- **Reads:** Invitation (pending list), User (team members list)
- **Updates:** Invitation status (accepted, expired), User role
- **Deletes:** Invitation (cancel), User (soft delete)

**Database Tables:**
- Invitation (primary)
- User (updated when invitation accepted)
- ActivityLog (track invitation actions)

**Integrations:**
- Auth module (create user accounts from invitations)
- Companies module (invitations scoped to company)
- Email service (send invitation emails)

**Backend Module:** `backend/modules/team/`
```
team/
  __init__.py
  routes.py              # API endpoints (/api/team/invitations, /api/team/members)
  models.py              # Invitation model
  schemas.py             # Request/response schemas
  services/
    invitation_service.py # Create, send, validate invitations
    team_service.py       # User management (role changes, removal)
  tasks/
    check_expired.py      # Scheduled job (mark expired invitations)
```

**Frontend Module:** `frontend/modules/team/`
```
team/
  components/
    TeamMembersList.tsx   # Active users table
    InviteUserModal.tsx   # Invitation form
    PendingInvitations.tsx # Pending invites list
    UserManagement.tsx    # Change roles, remove users
  hooks/
    useTeam.tsx           # Team state management
```

**Component Boundaries:**
- **Isolated:** Team management logic
- **Dependencies:** Auth (user creation), Companies (tenant scope), Email
- **Used By:** Dashboard (team tab)

---

### Epic 5: Drag-and-Drop Form Builder

**Domain Capabilities:**
- Canvas-based interface (1200x1600px, 3:4 aspect ratio)
- Component library (9 field types)
- Drag-and-drop with freeform positioning
- Proportional scaling rendering
- Component framework (form-level defaults + overrides)
- Undo/Redo system (50 action history)
- Enhanced drag interactions (collision detection, snap, fencing)
- Background image resize mode
- Tab order management
- Template library
- Real-time preview (desktop/tablet/mobile)

**Data Operations:**
- **Creates:** Form (draft)
- **Reads:** Form (load existing), Template (library)
- **Updates:** Form (design JSON - auto-save every 30 seconds)
- **Deletes:** Form component, Form draft

**Database Tables:**
- Form (primary - stores DesignJSON)
- Template (pre-designed templates)

**Integrations:**
- Events module (forms belong to events)
- Storage service (background image uploads)
- Companies module (tenant filtering)

**Backend Module:** `backend/modules/forms/`
```
forms/
  __init__.py
  routes.py              # API endpoints (/api/forms, /api/forms/{id}/draft)
  models.py              # Form, Template models
  schemas.py             # Request/response schemas
  services/
    form_service.py      # CRUD operations, draft management
    template_service.py  # Template library management
    rendering_service.py # Proportional scaling logic
```

**Frontend Module:** `frontend/modules/builder/` (MOST COMPLEX)
```
builder/
  components/
    FormBuilder.tsx           # Main builder container (3-panel layout)
    
    # Left Panel - Component Library
    ComponentLibrary.tsx      # Component palette
    ComponentPalette.tsx      # Draggable field types
    TemplateGallery.tsx       # Pre-designed templates
    
    # Center - Canvas
    Canvas.tsx                # Drop zone, grid, zoom
    DraggableComponent.tsx    # Draggable form field
    BackgroundImage.tsx       # Custom background display
    SelectionOutline.tsx      # Shows selected component
    
    # Right Panel - Properties
    PropertiesPanel.tsx       # Context-sensitive properties
    ComponentProperties.tsx   # Label, validation, styling
    FormSettings.tsx          # Form-level defaults
    
    # Preview
    PreviewPane.tsx           # Desktop/tablet/mobile preview
    
  rendering/
    FreeformRenderer.ts       # Freeform positioning engine
    GridRenderer.ts           # Grid-based positioning (contingency)
    RendererFactory.ts        # Factory pattern (selects renderer)
    
  state/
    formBuilderStore.ts       # State management (Zustand recommended)
    undoRedoManager.ts        # Undo/redo history (50 actions)
    autoSaveManager.ts        # Dual-layer auto-save (localStorage + database)
    
  collision/
    collisionDetector.ts      # Bounding box overlap detection
    spatialIndex.ts           # Optimize collision checks (performance)
    
  hooks/
    useFormBuilder.tsx        # Form builder state
    useDragDrop.tsx           # Drag-and-drop logic (dnd-kit wrapper)
    useAutoSave.tsx           # Auto-save orchestration
    useUndoRedo.tsx           # Undo/redo logic
```

**Component Boundaries:**
- **Isolated:** Form builder is self-contained (most complex module)
- **Dependencies:** Events (forms belong to events), Storage (image uploads), Companies (tenant)
- **Used By:** Publishing module (Epic 6)

**Key Architectural Decisions:**
1. **State Management:** Zustand (lightweight, beginner-friendly, less boilerplate than Redux)
2. **Drag-Drop Library:** dnd-kit (performant, accessible, modern)
3. **Modular Renderer:** Strategy pattern supports freeform or grid-based
4. **Auto-Save:** Dual-layer (localStorage 5s + database 30s)
5. **Undo/Redo:** Immutable state history (50 actions)

---

### Epic 6: Preview, Testing & Publishing

**Domain Capabilities:**
- Preview mode toggle (?preview=true URL parameter)
- Preview test counter and enforcement (minimum 5 tests)
- Approver testing requirements (Company User → Admin approval)
- Preview data management (filtering, deletion)
- Publish workflow with payment gate
- Form hosting and public URL generation
- Activation/deactivation logic

**Data Operations:**
- **Creates:** PublishRequest (Company User requests admin to publish)
- **Reads:** Form (preview), Submission (preview leads)
- **Updates:** Form status (draft → pending_admin_review → published)
- **Deletes:** Preview submissions (bulk delete)

**Database Tables:**
- Form (status field)
- PublishRequest (Company User → Admin approval workflow)
- Submission (is_preview flag)

**Integrations:**
- Forms module (publish forms)
- Payments module (triggers payment before publish)
- Email service (notify admin of publish request)
- Companies module (test threshold settings)

**Backend Module:** `backend/modules/forms/` (extends forms module)
```
forms/
  services/
    publish_service.py    # Publish workflow, approval logic
    preview_service.py    # Preview mode, test tracking
    hosting_service.py    # Public URL generation, CDN deployment
```

**Frontend Module:** `frontend/modules/builder/` (extends builder)
```
builder/
  components/
    PreviewToggle.tsx     # Preview mode switch
    PublishButton.tsx     # Publish workflow trigger
    PublishModal.tsx      # Payment screen, approval workflow
    TestCounter.tsx       # "3 of 5 tests completed" indicator
```

**Component Boundaries:**
- **Isolated:** Publishing logic in forms module
- **Dependencies:** Forms, Payments (publish requires payment), Email
- **Used By:** Dashboard (publish status displayed)

---

### Epic 7: Payment, Billing & Invoicing

**Domain Capabilities:**
- Stripe payment integration
- Company-based billing
- Australian GST-compliant invoicing (10% GST)
- Invoice PDF generation
- Invoice email delivery
- Billing history
- Payment receipts

**Data Operations:**
- **Creates:** Payment, Invoice
- **Reads:** Payment history, Invoice list
- **Updates:** Payment status (pending → succeeded/failed)
- **Deletes:** None (financial records immutable)

**Database Tables:**
- Payment (primary)
- Invoice (GST-compliant invoices)

**Integrations:**
- Stripe API (payment processing)
- PDF generation library (invoice PDFs)
- Email service (invoice delivery)
- Forms module (payment unlocks publish)

**Backend Module:** `backend/modules/payments/`
```
payments/
  __init__.py
  routes.py              # API endpoints (/api/payments, /api/invoices)
  models.py              # Payment, Invoice models
  schemas.py             # Request/response schemas
  services/
    stripe_service.py    # Stripe API integration
    invoice_service.py   # Invoice generation, PDF creation
    billing_service.py   # Billing history, receipts
  templates/
    invoice_template.html # Invoice PDF template (GST-compliant)
```

**Frontend Module:** `frontend/modules/settings/`
```
settings/
  components/
    PaymentForm.tsx       # Stripe checkout integration
    BillingHistory.tsx    # Invoices list
    InvoiceView.tsx       # Invoice PDF viewer
```

**Component Boundaries:**
- **Isolated:** Payment logic separate from business logic
- **Dependencies:** Companies (billing scoped to company), Forms (payment for publish)
- **Used By:** Forms module (publish triggers payment)

---

### Epic 8: Lead Collection & Analytics (CORE VALUE DELIVERABLE)

**THIS IS THE CORE VALUE - Everything else serves this purpose**

**Why This Epic Is Central:**
- Form builder exists to CREATE lead collection forms
- Payments exist to MONETIZE lead collection capability  
- Events exist to ORGANIZE lead collection at physical events
- Analytics exist to VIEW and USE the collected leads
- **The leads themselves are the product's value** - without quality leads, nothing else matters

**Domain Capabilities:**
- **Lead submission handling** (the core transaction - event attendee submits form)
- **Preview vs production flagging** (ensure lead quality via testing)
- **Real-time lead count dashboard** (prove value during event)
- **Submissions timeline chart** (show lead flow over time)
- **Leads list with search/filter** (find specific leads)
- **Lead detail view** (see individual lead data)
- **CSV export** (Salesforce, Marketing Cloud, Emarsys formats - USE the leads in CRM)
- **Preview lead management** (delete test leads)
- **Data validation** (field-level rules - ensure >90% valid leads)

**Data Operations:**
- **Creates:** Submission (public form submissions)
- **Reads:** Submission (analytics queries, filtering)
- **Updates:** None (submissions immutable)
- **Deletes:** Preview submissions only (IsPreview = true)

**Database Tables:**
- Submission (primary - stores form data JSON)

**Integrations:**
- Forms module (submissions belong to forms)
- WebSocket service (real-time updates)
- CSV generation library

**Backend Module:** `backend/modules/analytics/`
```
analytics/
  __init__.py
  routes.py              # API endpoints (/api/submissions, /api/analytics)
  models.py              # Submission model
  schemas.py             # Request/response schemas
  services/
    submission_service.py  # Store submissions, retrieve data
    analytics_service.py   # Aggregate data, charts
    export_service.py      # CSV generation (multiple formats)
    validation_service.py  # Field-level validation
  websocket/
    analytics_socket.py    # Real-time updates (new submission events)
```

**Frontend Module:** `frontend/modules/analytics/`
```
analytics/
  components/
    AnalyticsDashboard.tsx  # Main analytics view
    StatsCards.tsx          # Lead count, preview/production split
    SubmissionsChart.tsx    # Timeline chart (Recharts library)
    LeadsList.tsx           # Table with search/filter
    LeadDetail.tsx          # Individual lead view
    ExportModal.tsx         # CSV format selection
  hooks/
    useAnalytics.tsx        # Analytics state
    useWebSocket.tsx        # Real-time updates
```

**Component Boundaries:**
- **Isolated:** Analytics logic separate
- **Dependencies:** Forms (submissions belong to forms), WebSocket
- **Used By:** Dashboard (analytics tab)

---

### Epic 9: Enterprise Data & Audit

**Domain Capabilities:**
- Comprehensive audit logging (all user actions)
- Data lineage tracking (parent-child relationships, transformations)
- Enterprise-grade data quality controls
- Audit trail UI (for admins)
- Data retention policies

**Data Operations:**
- **Creates:** ActivityLog entries (every action)
- **Reads:** ActivityLog (audit trail queries), Data lineage queries
- **Updates:** None (audit log is append-only, immutable)
- **Deletes:** None (retain all audit data)

**Database Tables:**
- ActivityLog (comprehensive audit trail - already exists in Companies module)
- DataLineage (optional - tracks data transformations)

**Integrations:**
- ALL modules (every module logs actions to audit)
- Companies module (audit service)

**Backend Module:** `backend/modules/audit/` (extends companies/audit)
```
audit/
  __init__.py
  routes.py              # API endpoints (/api/audit/trail, /api/audit/lineage)
  models.py              # DataLineage model (if separate from ActivityLog)
  services/
    audit_query_service.py  # Complex audit queries
    lineage_service.py      # Data lineage tracking
    retention_service.py    # Data retention policies
```

**Frontend Module:** `frontend/modules/settings/`
```
settings/
  components/
    AuditTrail.tsx        # Audit log table with search/filter
    LineageView.tsx       # Data lineage visualization
```

**Component Boundaries:**
- **Isolated:** Audit is cross-cutting (used by all modules)
- **Dependencies:** ALL modules (provide audit data)
- **Used By:** Admin UI (audit trail viewing)

**Audit Integration Pattern:**
```python
# EVERY module action logs to audit
from modules.companies.services.audit_service import log_action

async def create_event(event_data, current_user):
    # 1. Create event
    event = await db.create(Event(**event_data))
    
    # 2. Log action (audit trail)
    await log_action(
        user_id=current_user.UserID,
        action="created",
        entity_type="event",
        entity_id=event.EventID,
        details={"event_name": event.EventName}
    )
    
    return event
```

---

### Module Dependency Graph

Visual representation of how modules depend on each other:

```
┌─────────────────────────────────────────────────────┐
│                      Auth (Epic 1)                   │
│         (Foundational - no dependencies)             │
└───────────────────────┬─────────────────────────────┘
                        │ (provides: current_user)
                        ↓
┌─────────────────────────────────────────────────────┐
│             Companies (Epic 2) + Audit (Epic 9)      │
│         (Foundational - multi-tenant context)        │
└───────────────────────┬─────────────────────────────┘
                        │ (provides: current_company, audit_log)
          ┌─────────────┼─────────────┬───────────────┐
          ↓             ↓             ↓               ↓
    ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌──────────┐
    │ Events  │   │  Team   │   │  Forms  │   │ Payments │
    │ (Epic 3)│   │ (Epic 4)│   │ (Epic 5)│   │ (Epic 7) │
    └────┬────┘   └─────────┘   └────┬────┘   └────┬─────┘
         │                            │             │
         │ (events contain forms)     │             │
         └────────────────────────────┘             │
                                      │             │
                                      │ (publish requires payment)
                                      └─────────────┘
                                                    │
                        ┌───────────────────────────┘
                        ↓
                 ┌─────────────┐
                 │  Analytics  │
                 │  (Epic 8)   │
                 │ (submissions)│
                 └─────────────┘
```

**Dependency Rules:**
1. **Auth (Epic 1):** No dependencies (foundational)
2. **Companies (Epic 2):** Depends on Auth only
3. **Events (Epic 3):** Depends on Companies, Auth
4. **Team (Epic 4):** Depends on Companies, Auth, Email
5. **Forms (Epic 5):** Depends on Events, Companies, Storage
6. **Payments (Epic 7):** Depends on Companies, Email, PDF generation
7. **Analytics (Epic 8):** Depends on Forms, WebSocket
8. **Audit (Epic 9):** Used by ALL modules (cross-cutting)

**Critical Rule: Epic Boundaries**
- Epic 2 code CANNOT modify Epic 1 code
- Epic 3 code CANNOT modify Epic 1 or Epic 2 code
- Dependencies are READ-ONLY (can call, cannot modify)

---

### Shared Infrastructure Components

**Component:** Storage Abstraction Layer
- **Purpose:** Abstract local storage vs Azure Blob Storage
- **Used By:** Forms module (background images), Templates module, Image Management
- **Pattern:** Provider interface (same API for both environments)

**Component:** Image Management Service (NEW - Critical Addition)
- **Purpose:** Ensure storage and database alignment for uploaded images
- **Used By:** Forms module (background images), Template module (template thumbnails)
- **Responsibilities:**
  - Upload images to storage (via Storage Abstraction Layer)
  - Create database records (Image table) tracking metadata
  - Associate images with forms (Form.BackgroundImageID FK)
  - Orphan cleanup (delete images not referenced by any form)
  - Duplicate detection (avoid storing same image twice)
  - Multi-tenant isolation (CompanyID on all images)
  - Image optimization (resize, compress, generate thumbnails)

**Component:** Email Abstraction Layer
- **Purpose:** Abstract MailHog vs Azure Communication Services
- **Used By:** Auth (verification emails), Team (invitation emails), Payments (invoices)
- **Pattern:** Provider interface (same API for both environments)

**Component:** WebSocket Service
- **Purpose:** Real-time updates for analytics dashboard
- **Used By:** Analytics module
- **Pattern:** FastAPI WebSocket endpoint with connection management

**Component:** Background Task Queue
- **Purpose:** Async operations (email sending, PDF generation, activation windows)
- **Used By:** Email service, Payments (invoice generation), Events (activation checks)
- **Technology:** FastAPI BackgroundTasks (simple) or Celery (advanced - if needed)

**Component:** Validation Library
- **Purpose:** Field-level validation rules (email, phone, ABN formats)
- **Used By:** Auth (email validation), Forms (submission validation), Companies (ABN validation)
- **Pattern:** Shared validation functions (frontend + backend use same rules)

**Component:** Logging & Observability Service (NEW - Critical for Development & Operations)
- **Purpose:** Comprehensive logging of ALL system activity (API requests, auth events, database queries, errors)
- **Used By:** ALL modules (every API call, every auth attempt, every database query logged)
- **Capabilities:**
  - API request/response logging (every endpoint call)
  - Authentication event logging (login, logout, failures, token generation)
  - Database query logging (SQL queries, execution time, row counts)
  - Error logging (exceptions, stack traces, context)
  - Performance logging (slow operations, bottlenecks)
  - Security logging (failed auth, suspicious activity, multi-tenant violations)
  - Structured logging (JSON format for analysis)
  - Environment-specific verbosity (verbose in dev, filtered in prod)

---

### Data Flow Examples (Cross-Module Interactions)

#### Example 1: Create Event Flow
```
User (Frontend)
  ↓ POST /api/events {eventName, dates, location}
Auth Middleware (validates JWT token)
  ↓ extracts current_user
Companies Middleware (validates CompanyID)
  ↓ extracts current_company
Events Module (routes.py)
  ↓ calls event_service.create_event()
Events Service (business logic)
  ↓ validates dates, creates Event record with CompanyID
Database (Event table)
  ↓ INSERT INTO Event
Audit Service (log action)
  ↓ INSERT INTO ActivityLog (user created event)
Response to Frontend
  ↓ {eventId, eventName, createdAt}
Frontend Updates UI
  ↓ Adds event to events list
```

#### Example 2: Publish Form Flow (Multi-Module)
```
User clicks "Publish" (Frontend)
  ↓ POST /api/forms/{id}/publish
Auth Middleware (validates JWT, role = Company Admin)
  ↓
Forms Module (check preview tests completed)
  ↓ IF tests < threshold: REJECT
  ↓ IF tests OK: Proceed
Payments Module (initiate Stripe payment)
  ↓ Stripe.create_payment_intent($99)
User Completes Stripe Checkout (Frontend)
  ↓ Payment succeeds
Payments Webhook (Stripe confirms payment)
  ↓ POST /api/webhooks/stripe
Payments Module (verify payment)
  ↓ Database Transaction BEGIN
  ↓ 1. Create Payment record
  ↓ 2. Update Form.Status = "published"
  ↓ 3. Generate Form.PublicURL
  ↓ 4. Create Invoice record
  ↓ Database Transaction COMMIT (all or nothing)
Background Task (async)
  ↓ 1. Generate invoice PDF
  ↓ 2. Email invoice to Company Admin
Audit Service (log publish action)
  ↓ INSERT INTO ActivityLog
Response to Frontend
  ↓ {publicURL, invoiceNumber}
Frontend Shows Success
  ↓ Display QR code, copy URL
```

**Notice:** Multiple modules coordinate, but transaction ensures consistency

---

### Component Boundary Rules

**Rule 1: Modules Communicate via API Contracts**
- Forms module calls Payments module via service interface (not direct database access)
- Clean interfaces between modules
- Can extract to microservice later if needed

**Rule 2: Shared Database, Separate Tables**
- Each module "owns" its tables (Forms owns Form table, Events owns Event table)
- Other modules query via service layer (not direct SQL)
- Foreign keys enforce relationships

**Rule 3: Cross-Module Dependencies are Read-Only**
- Epic 3 can READ Epic 1 code (auth middleware)
- Epic 3 CANNOT MODIFY Epic 1 code
- Story-context enforces with forbidden zones

**Rule 4: Shared Components in Common Module**
- Reusable UI components (Button, Input, Modal) in `/frontend/components/`
- Shared utilities (date formatting, validation) in `/common/`
- DRY (Don't Repeat Yourself) principle

---

### Epic Implementation Order (Based on Dependencies)

**Phase 1: Foundation (Weeks 1-8)**
```
Epic 1: Auth → Epic 2: Companies → Epic 3: Events → Epic 4: Team
         ↓              ↓                ↓              ↓
    (Week 1-4)     (Week 5-6)       (Week 7)      (Week 8)
```

**Phase 2: Form Builder (Weeks 9-14)**
```
Epic 5: Form Builder
  ↓
POC (Week 9-10) → Full Build (Week 11-14)
```

**Phase 3: Publishing & Payments (Weeks 15-18)**
```
Epic 6: Preview & Publishing → Epic 7: Payments
         ↓                          ↓
    (Week 15-16)               (Week 17-18)
```

**Phase 4: Analytics & Launch (Weeks 19-22)**
```
Epic 8: Analytics → Epic 9: Audit (enhance) → Polish & Launch
       ↓                  ↓                         ↓
  (Week 19-20)       (Week 20)                (Week 21-22)
```

**Why this order:**
- Foundation epics first (Auth, Companies, Events, Team)
- Form builder after foundation (requires events)
- Payments after forms exist
- Analytics after submissions flow complete

---

### Image Management Architecture (Detailed)

#### Why This Is Critical

**Problem Without Image Management:**
- User uploads background image → Stored in Azure Blob → Database has NO record → Orphaned file
- Form references ImageID 123 → Database record exists → Image deleted from storage → Broken link
- Company A uploads image → Stored as "bg-123.jpg" → Company B uploads same image → Stored as "bg-124.jpg" → Wasted storage
- Images accumulate over time → Storage costs grow → No cleanup strategy

**Solution: Image Management Service**
Ensures **storage and database are always in sync** (your core concern).

---

#### Database Schema: Image Table

**New Table: Image**
```sql
CREATE TABLE Image (
    ImageID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CompanyID BIGINT NOT NULL,  -- Multi-tenant isolation
    OriginalFileName NVARCHAR(255) NOT NULL,  -- User's original filename
    StoragePath NVARCHAR(500) NOT NULL,  -- Path in storage (local or Azure Blob)
    BlobURL NVARCHAR(2048) NULL,  -- Full Azure Blob URL (production only)
    FileSize INT NOT NULL,  -- Bytes (for storage tracking)
    MimeType NVARCHAR(50) NOT NULL,  -- image/jpeg, image/png
    Width INT NOT NULL,  -- Original width in pixels
    Height INT NOT NULL,  -- Original height in pixels
    ContentHash VARBINARY(32) NOT NULL,  -- SHA-256 hash (for duplicate detection)
    ThumbnailPath NVARCHAR(500) NULL,  -- Thumbnail for gallery view
    OptimizedPath NVARCHAR(500) NULL,  -- Optimized version for web
    IsDeleted BIT NOT NULL DEFAULT 0,  -- Soft delete
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,  -- User who uploaded
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    
    -- Foreign Keys
    CONSTRAINT FK_Image_Company_CompanyID FOREIGN KEY (CompanyID) 
        REFERENCES Company(CompanyID),
    CONSTRAINT FK_Image_User_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [User](UserID),
    
    -- Indexes
    CONSTRAINT UQ_Image_ContentHash UNIQUE (ContentHash, CompanyID),  -- Prevent duplicates per company
    INDEX IX_Image_CompanyID (CompanyID),
    INDEX IX_Image_ContentHash (ContentHash)
);
```

**Updated: Form Table (Add Foreign Key)**
```sql
ALTER TABLE Form
ADD BackgroundImageID BIGINT NULL;

ALTER TABLE Form
ADD CONSTRAINT FK_Form_Image_BackgroundImageID 
    FOREIGN KEY (BackgroundImageID) REFERENCES Image(ImageID);
```

**Why ContentHash?**
- Detects duplicate images (same file uploaded twice)
- SHA-256 hash of file contents
- Prevents wasting storage on duplicates

---

#### Image Upload Flow (Storage + Database Aligned)

**Step-by-Step Process:**

```
User selects image file (Frontend)
  ↓
1. Client-side validation
   - Check file size (<5MB)
   - Check format (JPEG, PNG, WebP only)
   - Calculate preview (show user before upload)
   ↓
2. POST /api/images/upload (with file)
   ↓
Backend Image Service:
  ↓
3. Calculate ContentHash (SHA-256 of file)
   ↓
4. Check for duplicate:
   SELECT * FROM Image 
   WHERE ContentHash = @hash 
   AND CompanyID = @companyID 
   AND IsDeleted = 0
   ↓
5a. IF duplicate found:
    - Return existing ImageID
    - Increment reference count (optional)
    - SKIP storage upload (reuse existing)
    ↓
5b. IF new image:
    - Database Transaction BEGIN
    - Upload to storage (via StorageProvider)
      → Local: ./local_storage/images/company-{id}/img-{uuid}.jpg
      → Azure: container/company-{id}/img-{uuid}.jpg
    - Create Image record in database
    - Generate thumbnail (async background task)
    - Generate optimized version (async)
    - Database Transaction COMMIT
    ↓
6. Return ImageID to frontend
   ↓
7. Frontend stores ImageID with form
   ↓
8. When saving form:
   POST /api/forms/{id} 
   { ..., backgroundImageID: 123 }
   ↓
9. Database enforces FK constraint
   Form.BackgroundImageID → Image.ImageID ✓
```

**Result:**
- ✅ Storage has file
- ✅ Database has Image record
- ✅ Form references Image (FK enforced)
- ✅ Duplicates detected and reused
- ✅ Multi-tenant isolation (CompanyID on Image)

---

#### Image Cleanup Strategy (Orphan Prevention)

**Problem:** User uploads image but never uses it in a form
- Image stored in storage ✓
- Image record in database ✓
- No Form references it → Orphan (wastes storage)

**Solution: Scheduled Cleanup Job**

```python
# Scheduled task (runs daily at 2 AM)
async def cleanup_orphaned_images():
    """
    Delete images not referenced by any form and older than 7 days
    """
    # Find orphaned images
    orphaned_images = await db.query(Image).filter(
        Image.ImageID.not_in(
            db.query(Form.BackgroundImageID)
            .filter(Form.BackgroundImageID.is_not(None))
        ),
        Image.CreatedDate < (utcnow() - timedelta(days=7)),
        Image.IsDeleted == False
    ).all()
    
    for image in orphaned_images:
        # 1. Delete from storage
        await storage_provider.delete_file(image.StoragePath)
        
        # 2. Soft delete in database
        image.IsDeleted = True
        image.DeletedDate = utcnow()
        
        # 3. Log action (audit trail)
        await log_action(
            user_id=None,  # System action
            action="deleted_orphan",
            entity_type="image",
            entity_id=image.ImageID
        )
    
    await db.commit()
```

**Why 7-day grace period?**
- User might upload image, get distracted, return next day
- Grace period allows for "I'll use it later" workflow
- After 7 days, likely abandoned (safe to clean)

---

#### Storage-Database Alignment Validation

**Validation Script (Run Weekly):**

```python
async def validate_storage_database_alignment():
    """
    Ensure storage and database are in sync
    Reports:
    - Images in database but missing from storage (broken links)
    - Images in storage but missing from database (orphans)
    """
    
    # 1. Get all image records from database
    db_images = await db.query(Image).filter(
        Image.IsDeleted == False
    ).all()
    
    # 2. Check each exists in storage
    missing_from_storage = []
    for image in db_images:
        if not await storage_provider.exists(image.StoragePath):
            missing_from_storage.append(image)
            # Alert: Database has record but storage missing!
    
    # 3. List all files in storage
    storage_files = await storage_provider.list_all()
    
    # 4. Check each has database record
    missing_from_database = []
    for file_path in storage_files:
        if not await db.query(Image).filter(
            Image.StoragePath == file_path
        ).first():
            missing_from_database.append(file_path)
            # Alert: Storage has file but database missing!
    
    # 5. Generate alignment report
    return {
        "aligned": len(missing_from_storage) == 0 and len(missing_from_database) == 0,
        "missing_from_storage": missing_from_storage,
        "missing_from_database": missing_from_database,
        "total_images": len(db_images),
        "storage_usage_mb": calculate_storage_usage()
    }
```

**When to run:**
- Weekly scheduled job (proactive monitoring)
- Before deployment (validate migration)
- After storage migration (local → Azure validation)

---

#### Image Management Service Implementation

**Backend Module:** `backend/modules/images/`
```
images/
  __init__.py
  routes.py                  # API endpoints (/api/images/upload, /api/images/{id})
  models.py                  # Image model
  schemas.py                 # Request/response schemas
  services/
    image_service.py         # Upload, retrieve, delete
    optimization_service.py  # Resize, compress, thumbnail generation
    cleanup_service.py       # Orphan detection and removal
    validation_service.py    # Alignment validation (storage ↔ database)
  utils/
    hash_utils.py            # SHA-256 content hashing
    image_utils.py           # PIL/Pillow image processing
  tasks/
    cleanup_orphans.py       # Scheduled job (daily cleanup)
    validate_alignment.py    # Scheduled job (weekly validation)
```

**Image Upload Endpoint:**
```python
from fastapi import UploadFile, Depends
from modules.images.services.image_service import ImageService
from modules.companies.dependencies import get_current_company

@router.post("/api/images/upload")
async def upload_image(
    file: UploadFile,
    current_user: User = Depends(get_current_user),
    current_company: Company = Depends(get_current_company),
    image_service: ImageService = Depends()
):
    """
    Upload background image with storage-database alignment
    
    Process:
    1. Validate file (size, format)
    2. Calculate content hash (duplicate detection)
    3. Check for existing image (same hash, same company)
    4. If duplicate: Return existing ImageID
    5. If new: Upload to storage + create database record (transactional)
    6. Generate thumbnail (async background task)
    7. Return ImageID
    """
    # 1. Validate
    if file.size > 5_000_000:  # 5MB limit
        raise HTTPException(400, "File too large")
    
    # 2. Calculate hash
    content = await file.read()
    content_hash = hashlib.sha256(content).digest()
    
    # 3. Check duplicate
    existing = await db.query(Image).filter(
        Image.ContentHash == content_hash,
        Image.CompanyID == current_company.CompanyID,
        Image.IsDeleted == False
    ).first()
    
    if existing:
        return {"imageID": existing.ImageID, "duplicate": True}
    
    # 4. Upload to storage + create database record (atomic)
    async with db.transaction():
        # Upload to storage
        storage_path = f"company-{current_company.CompanyID}/img-{uuid4()}.jpg"
        await storage_provider.upload(storage_path, content)
        
        # Create database record
        image = Image(
            CompanyID=current_company.CompanyID,
            OriginalFileName=file.filename,
            StoragePath=storage_path,
            BlobURL=storage_provider.get_url(storage_path),
            FileSize=file.size,
            MimeType=file.content_type,
            ContentHash=content_hash,
            CreatedBy=current_user.UserID
        )
        db.add(image)
        await db.commit()
        
        # 5. Background tasks (async - don't block response)
        background_tasks.add_task(generate_thumbnail, image.ImageID)
        background_tasks.add_task(generate_optimized, image.ImageID)
    
    return {"imageID": image.ImageID, "url": image.BlobURL}
```

---

#### Storage-Database Alignment Patterns

**Pattern 1: Transactional Upload (Storage + Database Together)**

```python
async def upload_with_transaction(file, company_id, user_id):
    """
    Upload to storage and database in single transaction
    If either fails, both rollback
    """
    async with db.transaction():
        try:
            # 1. Upload to storage first
            storage_path = await storage_provider.upload(file)
            
            # 2. Create database record
            image = Image(
                CompanyID=company_id,
                StoragePath=storage_path,
                ...
            )
            db.add(image)
            await db.commit()
            
            return image
            
        except StorageError as e:
            # Storage failed - rollback database
            await db.rollback()
            raise
        except DatabaseError as e:
            # Database failed - delete from storage
            await storage_provider.delete(storage_path)
            raise
```

**Pattern 2: Soft Delete with Cleanup (Two-Phase Delete)**

```python
async def delete_image(image_id):
    """
    Phase 1: Soft delete (mark IsDeleted = True)
    Phase 2: Cleanup job deletes from storage later
    
    Why two-phase?
    - Immediate database delete (user sees image gone)
    - Storage cleanup happens async (safer, can retry)
    - Grace period for accidental deletion recovery
    """
    # Phase 1: Soft delete in database (immediate)
    image = await db.get(Image, image_id)
    image.IsDeleted = True
    image.DeletedDate = utcnow()
    await db.commit()
    
    # Phase 2: Storage cleanup (background task, runs daily)
    # Scheduled job finds IsDeleted = True images older than 24 hours
    # Deletes from storage
    # This gives 24-hour recovery window for mistakes
```

**Pattern 3: Reference Counting (Track Usage)**

```python
# Optional: Track how many forms use each image
async def get_image_reference_count(image_id):
    """
    Count how many forms reference this image
    Used for: Orphan detection, storage optimization
    """
    count = await db.query(Form).filter(
        Form.BackgroundImageID == image_id,
        Form.IsActive == True
    ).count()
    
    return count

# Cleanup only images with zero references
async def cleanup_unused_images():
    images = await db.query(Image).all()
    
    for image in images:
        ref_count = await get_image_reference_count(image.ImageID)
        
        if ref_count == 0 and image.CreatedDate < (utcnow() - timedelta(days=7)):
            # No forms use this image and it's old → safe to delete
            await soft_delete_image(image.ImageID)
```

---

#### Duplicate Detection Strategy

**Problem:** Company uploads same image multiple times
- Wastes storage
- Increases costs
- Slower uploads

**Solution: Content Hash Deduplication**

```python
async def handle_upload_with_dedup(file, company_id):
    # 1. Calculate hash of file contents
    content = await file.read()
    content_hash = hashlib.sha256(content).digest()
    
    # 2. Check if image already exists for this company
    existing = await db.query(Image).filter(
        Image.ContentHash == content_hash,
        Image.CompanyID == company_id,
        Image.IsDeleted == False
    ).first()
    
    if existing:
        # Duplicate found - return existing image
        return {
            "imageID": existing.ImageID,
            "url": existing.BlobURL,
            "duplicate": True,
            "message": "This image was already uploaded. Using existing copy."
        }
    
    # 3. New image - proceed with upload
    return await upload_new_image(file, company_id, content_hash)
```

**Benefits:**
- ✅ Same image uploaded twice → Uses same file (no duplicate storage)
- ✅ Different companies upload same image → Each gets own copy (multi-tenant isolation)
- ✅ User sees: "This image was already uploaded" (saves time)

---

#### Multi-Tenant Image Isolation

**Critical Rule: Images are Company-Scoped**

```python
# Company A uploads image
image_a = Image(
    CompanyID=1,  # Company A
    StoragePath="company-1/img-abc.jpg",
    ...
)

# Company B uploads SAME image (same ContentHash)
image_b = Image(
    CompanyID=2,  # Company B
    StoragePath="company-2/img-xyz.jpg",  # Different storage path
    ContentHash=<same as Company A>,  # Same hash
    ...
)

# Result: Each company has own copy
# Why? Multi-tenant isolation (Company A deletes image, shouldn't affect Company B)
```

**Storage Path Structure:**
```
Local Development:
  ./local_storage/
    company-1/
      img-uuid-1.jpg
      img-uuid-2.jpg
    company-2/
      img-uuid-3.jpg

Azure Blob Storage (Production):
  Container: eventlead-images
    company-1/
      img-uuid-1.jpg
      img-uuid-2.jpg
    company-2/
      img-uuid-3.jpg
```

**Why company-scoped folders?**
- ✅ Clear separation (Company A can't access Company B's folder)
- ✅ Easy cleanup (delete entire company folder if company deleted)
- ✅ Storage-level isolation (Azure access policies per folder)

---

#### Image Optimization Pipeline

**Three Versions of Each Image:**

```
Original Upload:
  - user-background.jpg (2048x1536, 2.4MB)
    ↓
Backend Processing:

1. Original (Stored As-Is):
   - company-1/img-abc-original.jpg (2048x1536, 2.4MB)
   - Used for: High-quality preview, download

2. Optimized (Web-Optimized):
   - company-1/img-abc-optimized.jpg (1600x1200, 400KB)
   - Compressed for web (quality: 85%)
   - Used for: Form builder canvas, public forms

3. Thumbnail (Gallery View):
   - company-1/img-abc-thumb.jpg (320x240, 40KB)
   - Small preview
   - Used for: Template gallery, image selection UI
```

**Database Records:**
```sql
Image record:
  - StoragePath: "company-1/img-abc-original.jpg"
  - OptimizedPath: "company-1/img-abc-optimized.jpg"
  - ThumbnailPath: "company-1/img-abc-thumb.jpg"
```

**Background Processing:**
```python
async def generate_optimized_versions(image_id):
    """
    Background task: Generate thumbnail and optimized version
    Runs async after upload (doesn't block user)
    """
    image = await db.get(Image, image_id)
    
    # Download original
    original = await storage_provider.download(image.StoragePath)
    
    # Generate thumbnail (320x240)
    thumbnail = resize_image(original, width=320, height=240)
    thumb_path = image.StoragePath.replace('.jpg', '-thumb.jpg')
    await storage_provider.upload(thumb_path, thumbnail)
    
    # Generate optimized (1600x1200, 85% quality)
    optimized = optimize_image(original, max_width=1600, quality=85)
    opt_path = image.StoragePath.replace('.jpg', '-optimized.jpg')
    await storage_provider.upload(opt_path, optimized)
    
    # Update database
    image.ThumbnailPath = thumb_path
    image.OptimizedPath = opt_path
    await db.commit()
```

---

#### Image Management Service API

**Endpoints:**

```python
POST   /api/images/upload              # Upload new image
GET    /api/images/{id}                # Get image metadata
GET    /api/images/{id}/download       # Download original
DELETE /api/images/{id}                # Soft delete image
GET    /api/images                     # List company's images
POST   /api/images/validate-alignment  # Run alignment check (admin)
```

**Service Interface:**
```python
class ImageService:
    async def upload(self, file: UploadFile, company_id: int, user_id: int) -> Image:
        """Upload image with storage-database alignment"""
        
    async def get(self, image_id: int, company_id: int) -> Image:
        """Get image (filtered by company)"""
        
    async def delete(self, image_id: int, company_id: int) -> None:
        """Soft delete image (two-phase delete)"""
        
    async def list_images(self, company_id: int) -> List[Image]:
        """List all company's images"""
        
    async def cleanup_orphans(self) -> CleanupReport:
        """Remove orphaned images (scheduled job)"""
        
    async def validate_alignment(self) -> AlignmentReport:
        """Validate storage and database are in sync"""
```

---

#### Integration with Forms Module

**Updated Form Creation Flow:**

```
User creates form:
  ↓
1. User clicks "Upload Background"
   ↓
2. Frontend calls: POST /api/images/upload
   ↓
3. Image Service:
   - Validates file
   - Uploads to storage
   - Creates Image record
   - Returns ImageID
   ↓
4. Frontend stores ImageID in form state
   formState.backgroundImageID = 123
   ↓
5. User continues building form (drag components, etc.)
   ↓
6. Auto-save (every 30 seconds):
   PUT /api/forms/{formID}/draft
   {
     designJSON: {...},
     backgroundImageID: 123  ← Links to Image table
   }
   ↓
7. Database enforces FK constraint:
   Form.BackgroundImageID → Image.ImageID ✓
```

**Result:**
- ✅ Image in storage (via ImageService)
- ✅ Image record in database (Image table)
- ✅ Form references image (Form.BackgroundImageID FK)
- ✅ All aligned and traceable

---

#### Architecture Additions Summary

**New Components Added:**
1. ✅ **Image Table** (database schema with ContentHash for deduplication)
2. ✅ **Image Management Service** (backend/modules/images/)
3. ✅ **Upload with alignment** (transactional: storage + database together)
4. ✅ **Duplicate detection** (ContentHash prevents duplicate storage)
5. ✅ **Orphan cleanup** (scheduled job removes unused images after 7 days)
6. ✅ **Alignment validation** (weekly check: storage ↔ database sync)
7. ✅ **Multi-tenant isolation** (CompanyID on all images, company-scoped storage folders)
8. ✅ **Image optimization pipeline** (original + optimized + thumbnail)

**Updated Form Schema:**
```sql
Form:
  - FormID (PK)
  - BackgroundImageID (FK → Image.ImageID)  -- NEW
  - DesignJSON (form components)
  - ...
```

**Benefits:**
- ✅ Storage and database ALWAYS aligned (your concern addressed)
- ✅ No orphaned files (cleanup job)
- ✅ No broken links (FK constraint enforces)
- ✅ Duplicate prevention (saves storage costs)
- ✅ Multi-tenant safe (CompanyID on images)
- ✅ Audit trail (track who uploaded, when)

---

**This architectural pattern is integrated into:**
- ✅ Shared Infrastructure section (Image Management Service)
- ✅ Epic 5 tech-spec (Form Builder integrates with Image Service)
- ✅ Database schema section (Image table)
- ✅ Story-context for image-related stories (upload, cleanup, validation)

---

### Logging & Observability Architecture

**Purpose:** Comprehensive logging of ALL system activity for development debugging, security monitoring, performance optimization, and operational visibility.

**Core Principle:** Log everything in development, filter intelligently in production.

---

#### What Gets Logged

**1. API Request/Response Logging (EVERY endpoint)**

**What to capture:**
```json
{
  "timestamp": "2025-10-12T14:23:45.123Z",
  "level": "INFO",
  "category": "api.request",
  "method": "POST",
  "path": "/api/events",
  "status_code": 201,
  "duration_ms": 45,
  "request": {
    "headers": {
      "authorization": "Bearer ***" (masked),
      "content-type": "application/json"
    },
    "body": {
      "eventName": "Tech Summit 2026",
      "eventStartDate": "2026-01-15T09:00:00Z"
    },
    "query_params": {},
    "client_ip": "192.168.1.100"
  },
  "response": {
    "status": 201,
    "body": {
      "eventId": 123,
      "eventName": "Tech Summit 2026"
    }
  },
  "user": {
    "userId": 456,
    "companyId": 789,
    "role": "company_admin"
  },
  "performance": {
    "db_queries": 2,
    "db_time_ms": 12,
    "total_time_ms": 45
  }
}
```

**What gets masked:**
- Passwords (NEVER logged)
- JWT tokens (show "Bearer ***")
- Credit card numbers (PCI compliance)
- Sensitive PII (Personal Identifiable Information)

**Implementation:**
```python
# FastAPI middleware (logs EVERY request automatically)
from fastapi import Request, Response
import structlog

logger = structlog.get_logger()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Start timer
    start_time = time.time()
    
    # Log request
    logger.info(
        "api.request.started",
        method=request.method,
        path=request.url.path,
        client_ip=request.client.host
    )
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = (time.time() - start_time) * 1000  # milliseconds
    
    # Log response
    logger.info(
        "api.request.completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_ms=duration
    )
    
    return response
```

---

**2. Authentication Event Logging (Security Critical)**

**What to capture:**
```json
{
  "timestamp": "2025-10-12T14:23:45.123Z",
  "level": "INFO",
  "category": "auth.login.success",
  "user_id": 456,
  "company_id": 789,
  "email": "anthony@example.com",
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "session_id": "sess_abc123",
  "mfa_used": false
}
```

**Events to log:**
- ✅ Signup attempts (success, failure with reason)
- ✅ Login attempts (success, failure, lockout)
- ✅ Email verification (sent, clicked, failed)
- ✅ Password reset (requested, completed, failed)
- ✅ Token generation (JWT created, refreshed, revoked)
- ✅ Logout (session ended)
- ✅ Authorization failures (user tried to access forbidden resource)
- ✅ Role changes (user promoted/demoted)
- ✅ Suspicious activity (multiple failed logins, token manipulation)

**Security Events:**
```json
{
  "timestamp": "2025-10-12T14:25:10.456Z",
  "level": "WARNING",
  "category": "auth.login.failed",
  "email": "anthony@example.com",
  "reason": "invalid_password",
  "ip_address": "192.168.1.100",
  "attempt_count": 3,  // 3rd failed attempt
  "lockout_triggered": false
}
```

**Implementation:**
```python
async def login(credentials: LoginRequest):
    logger.info(
        "auth.login.attempt",
        email=credentials.email,
        ip=request.client.host
    )
    
    user = await get_user_by_email(credentials.email)
    
    if not user or not verify_password(credentials.password, user.password_hash):
        logger.warning(
            "auth.login.failed",
            email=credentials.email,
            reason="invalid_credentials",
            ip=request.client.host
        )
        raise HTTPException(401, "Invalid credentials")
    
    # Generate JWT
    token = create_jwt(user)
    
    logger.info(
        "auth.login.success",
        user_id=user.UserID,
        company_id=user.CompanyID,
        email=user.Email,
        ip=request.client.host
    )
    
    return {"token": token}
```

---

**3. Database Query Logging (Performance & Debugging)**

**What to capture:**
```json
{
  "timestamp": "2025-10-12T14:23:45.150Z",
  "level": "DEBUG",
  "category": "database.query",
  "sql": "SELECT * FROM Event WHERE CompanyID = @p0 AND IsActive = 1",
  "params": {"p0": 789},
  "duration_ms": 12,
  "rows_returned": 5,
  "user_id": 456,
  "company_id": 789,
  "endpoint": "/api/events"
}
```

**What to log:**
- ✅ SQL queries executed (parameterized, not with actual values for security)
- ✅ Execution time (identify slow queries)
- ✅ Row counts (returned, affected)
- ✅ Connection pool stats (active connections, wait time)
- ✅ Slow query warnings (>100ms flagged for optimization)

**SQLAlchemy Integration:**
```python
import logging
from sqlalchemy import event
from sqlalchemy.engine import Engine

# Enable query logging
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop()
    
    logger.debug(
        "database.query",
        sql=statement,
        duration_ms=total * 1000,
        rows=cursor.rowcount
    )
    
    # Warn on slow queries
    if total > 0.1:  # 100ms threshold
        logger.warning(
            "database.slow_query",
            sql=statement,
            duration_ms=total * 1000,
            threshold_ms=100
        )
```

---

**4. Error Logging (Exceptions & Stack Traces)**

**What to capture:**
```json
{
  "timestamp": "2025-10-12T14:25:30.789Z",
  "level": "ERROR",
  "category": "error.exception",
  "exception_type": "ValidationError",
  "message": "Invalid ABN format",
  "stack_trace": "Traceback (most recent call last):\n  File...",
  "context": {
    "endpoint": "/api/companies",
    "user_id": 456,
    "company_id": 789,
    "request_id": "req_xyz789"
  },
  "user_input": {
    "abn": "12345"  // Invalid (should be 11 digits)
  }
}
```

**FastAPI Error Handler:**
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log full exception details
    logger.error(
        "error.exception",
        exception_type=type(exc).__name__,
        message=str(exc),
        stack_trace=traceback.format_exc(),
        endpoint=request.url.path,
        method=request.method,
        user_id=getattr(request.state, "user_id", None)
    )
    
    # Return user-friendly error (don't expose internals)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )
```

---

**5. Performance Logging (Optimization & Bottlenecks)**

**What to capture:**
```json
{
  "timestamp": "2025-10-12T14:23:45.200Z",
  "level": "INFO",
  "category": "performance.endpoint",
  "endpoint": "/api/forms/456/publish",
  "duration_ms": 1250,
  "breakdown": {
    "validation": 50,
    "stripe_payment": 800,
    "database_transaction": 350,
    "pdf_generation": 50
  },
  "user_id": 456,
  "company_id": 789
}
```

**Identify bottlenecks:**
- Stripe payment took 800ms (external API call - expected)
- Database transaction 350ms (could optimize?)
- Total 1250ms (acceptable for publish flow)

---

**6. Security Logging (Threat Detection)**

**What to capture:**
```json
{
  "timestamp": "2025-10-12T14:30:15.456Z",
  "level": "CRITICAL",
  "category": "security.multi_tenant_violation_attempt",
  "user_id": 456,
  "company_id": 789,
  "attempted_resource": "form",
  "attempted_resource_id": 999,
  "resource_owner_company_id": 123,  // Different company!
  "action": "blocked",
  "ip_address": "192.168.1.100"
}
```

**Security events:**
- ✅ Multi-tenant violation attempts (Company A tries to access Company B data)
- ✅ SQL injection attempts (suspicious query patterns)
- ✅ Brute force login attempts (multiple failures from same IP)
- ✅ Invalid JWT tokens (manipulation attempts)
- ✅ Privilege escalation attempts (User tries Admin-only endpoint)
- ✅ Unusual API patterns (rapid requests, scraping behavior)

---

#### Logging Architecture Design

**Log Levels (Environment-Specific):**

**Development Environment:**
```
DEBUG:    ALL database queries, detailed request/response bodies
INFO:     API calls, auth events, user actions
WARNING:  Slow queries, validation failures, retry attempts
ERROR:    Exceptions, failed operations
CRITICAL: Security violations, data integrity issues
```

**Production Environment:**
```
INFO:     API calls (summary only), auth events, user actions
WARNING:  Slow queries, validation failures, security concerns
ERROR:    Exceptions, failed operations
CRITICAL: Security violations, data integrity issues, system failures
```

**What changes dev → prod:**
- Database queries: DEBUG in dev (see every query), NOT logged in prod (too verbose)
- Request bodies: Full in dev, sanitized in prod (remove PII)
- Response bodies: Full in dev, summary in prod

---

#### Structured Logging (JSON Format)

**Why JSON?**
- Machine-readable (can query logs with tools)
- Structured fields (filter by user_id, company_id, endpoint, etc.)
- Integration with log analysis tools (ELK stack, Azure Log Analytics)

**Library: structlog (Python)**

**Configuration:**
```python
import structlog

# Configure structlog for JSON output
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),  # ISO 8601 timestamps
        structlog.stdlib.add_log_level,               # Add log level
        structlog.processors.JSONRenderer()           # Output as JSON
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

# Get logger
logger = structlog.get_logger()

# Usage
logger.info(
    "auth.login.success",
    user_id=456,
    company_id=789,
    email="anthony@example.com"
)

# Output (JSON):
# {"event": "auth.login.success", "timestamp": "2025-10-12T14:23:45.123Z", "level": "info", "user_id": 456, "company_id": 789, "email": "anthony@example.com"}
```

---

#### Environment-Specific Configuration

**Development (.env.local):**
```bash
LOG_LEVEL=DEBUG
LOG_API_REQUESTS=true
LOG_API_RESPONSES=true
LOG_REQUEST_BODY=true
LOG_RESPONSE_BODY=true
LOG_DATABASE_QUERIES=true
LOG_SQL_PARAMS=true
LOG_PERFORMANCE_BREAKDOWN=true
```

**Production (.env.production):**
```bash
LOG_LEVEL=INFO
LOG_API_REQUESTS=true
LOG_API_RESPONSES=false  # Only log on errors
LOG_REQUEST_BODY=false   # Privacy - don't log user data
LOG_RESPONSE_BODY=false  # Privacy
LOG_DATABASE_QUERIES=false  # Too verbose
LOG_SQL_PARAMS=false     # Security - don't log query params
LOG_PERFORMANCE_BREAKDOWN=true  # Still useful for optimization
```

**Conditional Logging:**
```python
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_REQUEST_BODY = os.getenv("LOG_REQUEST_BODY", "false") == "true"

async def log_request(request: Request):
    # Always log basic info
    logger.info("api.request", method=request.method, path=request.url.path)
    
    # Conditionally log request body (only in dev)
    if LOG_REQUEST_BODY:
        body = await request.json()
        logger.debug("api.request.body", body=body)
```

---

#### Log Categories & Examples

**Category 1: API Requests (api.request.*)**

```python
# Request started
logger.info(
    "api.request.started",
    request_id="req_abc123",
    method="POST",
    path="/api/forms/456/publish",
    user_id=456,
    company_id=789
)

# Request completed
logger.info(
    "api.request.completed",
    request_id="req_abc123",
    status_code=200,
    duration_ms=1250
)

# Request failed
logger.error(
    "api.request.failed",
    request_id="req_abc123",
    status_code=500,
    error="Database connection timeout"
)
```

---

**Category 2: Authentication (auth.*)**

```python
# Login success
logger.info(
    "auth.login.success",
    user_id=456,
    company_id=789,
    email="anthony@example.com",
    ip="192.168.1.100"
)

# Login failure
logger.warning(
    "auth.login.failed",
    email="anthony@example.com",
    reason="invalid_password",
    ip="192.168.1.100",
    attempt_count=3
)

# JWT token created
logger.info(
    "auth.token.created",
    user_id=456,
    token_type="access",
    expires_in=3600  # seconds
)

# Authorization denied
logger.warning(
    "auth.authorization.denied",
    user_id=456,
    role="company_user",
    attempted_action="publish_form",
    required_role="company_admin"
)
```

---

**Category 3: Database (database.*)**

```python
# Query execution
logger.debug(
    "database.query",
    sql="SELECT * FROM Event WHERE CompanyID = %(company_id)s",
    params={"company_id": 789},
    duration_ms=12,
    rows_returned=5
)

# Slow query warning
logger.warning(
    "database.slow_query",
    sql="SELECT * FROM Submission WHERE FormID = %(form_id)s",
    duration_ms=450,  # Over 100ms threshold
    threshold_ms=100,
    optimization_needed=True
)

# Transaction started/committed
logger.debug("database.transaction.begin", transaction_id="tx_xyz")
logger.debug("database.transaction.commit", transaction_id="tx_xyz", duration_ms=350)

# Connection pool stats
logger.info(
    "database.pool.stats",
    active_connections=5,
    idle_connections=3,
    waiting_requests=0,
    max_connections=20
)
```

---

**Category 4: Business Logic (business.*)**

```python
# Form published
logger.info(
    "business.form.published",
    form_id=456,
    event_id=123,
    company_id=789,
    user_id=456,
    public_url="https://forms.eventlead.com/abc123",
    payment_amount=9900  # cents
)

# Lead collected
logger.info(
    "business.lead.collected",
    submission_id=789,
    form_id=456,
    event_id=123,
    company_id=789,
    is_preview=false,
    timestamp="2025-10-12T14:23:45.123Z"
)

# Invoice generated
logger.info(
    "business.invoice.generated",
    invoice_id=101,
    company_id=789,
    amount=9900,
    gst_amount=900,
    invoice_number="INV-2025-001"
)
```

---

**Category 5: Performance (performance.*)**

```python
# Slow operation detected
logger.warning(
    "performance.slow_operation",
    operation="generate_invoice_pdf",
    duration_ms=2500,  # 2.5 seconds
    threshold_ms=1000,
    optimization_candidate=True
)

# Memory usage
logger.info(
    "performance.memory",
    usage_mb=450,
    threshold_mb=1000,
    available_mb=550
)

# Form builder drag performance
logger.debug(
    "performance.drag",
    operation="collision_check",
    duration_ms=3.5,  # Under 5ms budget ✓
    component_count=20
)
```

---

**Category 6: Security (security.*)**

```python
# Multi-tenant violation attempt
logger.critical(
    "security.tenant_violation",
    user_id=456,
    user_company_id=789,
    attempted_resource="form",
    resource_id=999,
    resource_company_id=123,  # Different company!
    action="blocked",
    ip="192.168.1.100"
)

# SQL injection attempt detected
logger.critical(
    "security.sql_injection_attempt",
    user_id=456,
    endpoint="/api/events",
    malicious_input="'; DROP TABLE Event; --",
    action="blocked",
    ip="192.168.1.100"
)

# Brute force detected
logger.warning(
    "security.brute_force",
    email="anthony@example.com",
    failed_attempts=10,
    time_window_minutes=5,
    action="account_locked",
    ip="192.168.1.100"
)
```

---

#### Logging vs Audit Trail (Two Different Systems)

**Important Distinction:**

**Operational Logs (Logging Service):**
- **Purpose:** Development debugging, performance monitoring, error tracking
- **Retention:** 7-30 days (logs are temporary)
- **Storage:** Log files, Azure Log Analytics (for querying)
- **Audience:** Developers, DevOps, Anthony
- **Volume:** VERY HIGH (thousands of log entries per minute)

**Audit Trail (ActivityLog table in database):**
- **Purpose:** Compliance, business audit, customer transparency
- **Retention:** PERMANENT (regulatory requirement)
- **Storage:** ActivityLog table in SQL Server
- **Audience:** Auditors, customers (via audit trail UI), regulators
- **Volume:** MEDIUM (only user actions, not every API call)

**What goes in Audit Trail (ActivityLog):**
- ✅ User created event
- ✅ User published form
- ✅ User invited team member
- ✅ Admin changed user role
- ✅ Form was deleted
- ❌ NOT: Every API call (too verbose)
- ❌ NOT: Database queries (operational, not business events)

**What goes in Operational Logs:**
- ✅ EVERY API call
- ✅ EVERY database query (dev only)
- ✅ EVERY authentication attempt
- ✅ EVERY error/exception
- ✅ Performance metrics
- ✅ Security events

**Both systems work together:**
- Operational logs: Debugging and monitoring
- Audit trail: Compliance and business tracking

---

#### Log Storage & Retention

**Development Environment:**
```
Local Files:
  ./logs/
    app.log              # All logs (rotated daily)
    api.log              # API-specific logs
    database.log         # Database query logs
    error.log            # Errors only
    
  Retention: 7 days (development logs cleared weekly)
```

**Production Environment:**
```
Azure Log Analytics:
  - All logs sent to Azure (centralized)
  - Query language (KQL - Kusto Query Language)
  - Retention: 30 days for INFO/DEBUG, 90 days for ERROR/CRITICAL
  - Alerting rules (email on CRITICAL errors)

Local Files (Backup):
  /var/log/eventlead/
    app.log              # Rotated daily, kept 7 days
    error.log            # Rotated daily, kept 30 days
```

---

#### Log Filtering & Privacy

**PII (Personal Identifiable Information) Masking:**

```python
def sanitize_for_logging(data: dict) -> dict:
    """
    Mask sensitive fields before logging
    """
    sensitive_fields = ['password', 'creditCard', 'ssn', 'token']
    
    sanitized = data.copy()
    
    for key, value in sanitized.items():
        if key.lower() in sensitive_fields:
            sanitized[key] = "***MASKED***"
        elif isinstance(value, dict):
            sanitized[key] = sanitize_for_logging(value)
    
    return sanitized

# Usage
logger.info(
    "api.request",
    body=sanitize_for_logging(request_body)
)
```

**IP Address Hashing (Privacy):**
```python
import hashlib

def hash_ip(ip_address: str) -> str:
    """
    Hash IP for privacy while maintaining uniqueness
    Used for: Rate limiting, abuse detection (don't need actual IP)
    """
    return hashlib.sha256(ip_address.encode()).hexdigest()[:16]

logger.info(
    "auth.login",
    user_id=456,
    ip_hash=hash_ip("192.168.1.100")  # Hash for privacy
)
```

---

#### Logging Service Implementation

**Backend Module:** `backend/common/logging/`
```
logging/
  __init__.py
  config.py              # structlog configuration
  middleware.py          # Request logging middleware
  formatters.py          # JSON formatting, PII masking
  filters.py             # Environment-specific filtering
  handlers.py            # File handlers, Azure handlers
  utils/
    sanitizer.py         # PII masking functions
    performance.py       # Performance measurement decorators
```

**Example Performance Decorator:**
```python
from functools import wraps
import time

def log_performance(operation_name: str):
    """
    Decorator: Logs operation duration
    Usage: @log_performance("generate_invoice_pdf")
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.time()
            
            try:
                result = await func(*args, **kwargs)
                duration = (time.time() - start) * 1000
                
                logger.info(
                    "performance.operation",
                    operation=operation_name,
                    duration_ms=duration,
                    status="success"
                )
                
                return result
                
            except Exception as e:
                duration = (time.time() - start) * 1000
                
                logger.error(
                    "performance.operation",
                    operation=operation_name,
                    duration_ms=duration,
                    status="failed",
                    error=str(e)
                )
                
                raise
        
        return wrapper
    return decorator

# Usage
@log_performance("publish_form")
async def publish_form(form_id, payment_details):
    # Function logic
    pass

# Automatically logs: "performance.operation" with duration
```

---

#### Integration with Existing Audit Trail

**Two-Layer Strategy:**

**Layer 1: Operational Logs (Temporary, Verbose)**
- Every API call logged
- Every auth attempt logged
- Every database query logged (dev)
- Retention: 7-30 days

**Layer 2: Business Audit Trail (Permanent, Selective)**
- User actions logged to ActivityLog table
- Retention: Permanent
- Queryable via UI (audit trail screen)

**How they work together:**
```python
async def create_event(event_data, current_user):
    # 1. Operational log (temporary)
    logger.info(
        "api.create_event.started",
        user_id=current_user.UserID,
        company_id=current_user.CompanyID
    )
    
    # 2. Create event (business logic)
    event = await db.create(Event(**event_data))
    
    # 3. Business audit trail (permanent - ActivityLog table)
    await log_action(
        user_id=current_user.UserID,
        action="created",
        entity_type="event",
        entity_id=event.EventID,
        details={"event_name": event.EventName}
    )
    
    # 4. Operational log (temporary)
    logger.info(
        "api.create_event.completed",
        event_id=event.EventID,
        duration_ms=45
    )
    
    return event
```

**Result:**
- ✅ Operational logs: Full technical detail for debugging
- ✅ Audit trail: Business-level actions for compliance
- ✅ Both provide value, serve different purposes

---

#### Request Tracing (Correlation IDs)

**Problem:** Track single request across multiple logs

**Solution: Request ID (Correlation ID)**

```python
import uuid

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    # Generate unique ID for this request
    request_id = str(uuid.uuid4())
    
    # Store in request state
    request.state.request_id = request_id
    
    # Add to all logs
    with structlog.contextvars.bound_contextvars(request_id=request_id):
        response = await call_next(request)
    
    # Add to response headers (client can reference in bug reports)
    response.headers["X-Request-ID"] = request_id
    
    return response

# Now ALL logs for this request have same request_id
logger.info("api.request")           # request_id: req_abc123
logger.debug("database.query")       # request_id: req_abc123
logger.error("error.exception")      # request_id: req_abc123

# Can filter logs: "Show me ALL logs for request req_abc123"
```

**User reports bug:**
```
User: "I got an error when publishing form"
Anthony: "What was the Request ID shown in error?"
User: "req_abc123"
Anthony: Filter logs by request_id="req_abc123"
         → See ENTIRE flow: request → validation → payment → database → error
```

---

#### Logging Architecture Summary

**Components:**
1. ✅ **structlog** (Python structured logging library)
2. ✅ **FastAPI middleware** (automatic request/response logging)
3. ✅ **SQLAlchemy event listeners** (database query logging)
4. ✅ **Environment-specific configuration** (verbose dev, filtered prod)
5. ✅ **PII sanitization** (mask sensitive data)
6. ✅ **Request correlation IDs** (trace requests across logs)
7. ✅ **Performance decorators** (measure operation duration)
8. ✅ **Azure Log Analytics integration** (production log storage)

**Benefits:**
- ✅ **Development:** See EVERYTHING (debug easily)
- ✅ **Production:** See IMPORTANT events (performance, not noise)
- ✅ **Security:** Detect threats (multi-tenant violations, brute force)
- ✅ **Performance:** Find bottlenecks (slow queries, slow endpoints)
- ✅ **Privacy:** Mask PII (compliance with Australian Privacy Principles)
- ✅ **Tracing:** Follow requests end-to-end (correlation IDs)

**Integration Points:**
- ✅ Epic 1 (Auth): Login/logout/signup logging
- ✅ Epic 2 (Companies): Audit trail + operational logs
- ✅ Epic 5 (Forms): Form builder interactions, auto-save events
- ✅ Epic 7 (Payments): Payment flow logging, Stripe webhook events
- ✅ Epic 8 (Analytics): Lead submission logging, export events
- ✅ ALL Epics: API request/response logging

**Story Acceptance Criteria:**
- Every story MUST include logging for key operations
- No story complete without appropriate log statements
- Integration tests verify logs generated correctly

---

## Project-Type-Specific Architecture Decisions (Web Application)

Based on web application requirements, these technology decisions complete our stack:

### Database Layer

**ORM (Object-Relational Mapping): SQLAlchemy 2.0**

**What is an ORM?**
An ORM lets Python code work with databases using objects instead of raw SQL:
```python
# With ORM (SQLAlchemy):
user = await db.query(User).filter(User.Email == "anthony@example.com").first()

# Without ORM (Raw SQL):
cursor.execute("SELECT * FROM [User] WHERE Email = ?", ("anthony@example.com",))
user = cursor.fetchone()
```

**Decision: SQLAlchemy 2.0.23**

**Why SQLAlchemy?**
- ✅ Industry standard (most popular Python ORM)
- ✅ Excellent SQL Server support (mature driver: pyodbc)
- ✅ Migration tool included (Alembic - version-controlled schema changes)
- ✅ BMAD agent training (more code generation data)
- ✅ Type hints support (Python 3.11+ typing - better editor support)
- ✅ Async support (works with FastAPI async endpoints)
- ✅ Can write raw SQL when needed (doesn't prevent you from using SQL expertise)

**Benefits for Anthony:**
- Leverages your SQL expertise (you understand what ORM generates)
- Migration tool (Alembic) with your custom templates (PascalCase naming)
- Can drop to raw SQL for complex queries (best of both worlds)

**Migration Tool: Alembic 1.12.1**
- Generates migration files (version-controlled schema changes)
- Auto-detect model changes (compares models to database)
- Can customize templates (enforce your PascalCase naming standards)
- Rollback capability (undo migrations if needed)

---

### CI/CD (Continuous Integration / Continuous Deployment)

**Pipeline: GitHub Actions**

**What is CI/CD?**
Automated testing and deployment:
- **CI (Continuous Integration):** Every code push runs tests automatically
- **CD (Continuous Deployment):** If tests pass, deploy to Azure automatically

**Decision: GitHub Actions (implemented before production deployment)**

**Why GitHub Actions?**
- ✅ Free for public/private repos (unlimited minutes for public, 2000 min/month for private)
- ✅ Built into GitHub (where code lives)
- ✅ Simple YAML configuration
- ✅ Huge ecosystem (pre-built actions for Azure deployment)
- ✅ Can start simple, add complexity later

**Timeline:**
- Weeks 1-20: Manual deployment (focus on features, not DevOps)
- Week 21: Implement GitHub Actions (before production launch)
- Post-launch: Automated deployment for updates

**Why delayed implementation?**
- ✅ Saves time early (manual deployment acceptable for local dev)
- ✅ Focus on features first (shipping > automation)
- ✅ Less complexity during development (one less thing to maintain)
- ✅ Still have CI/CD before customers (production-ready)

**Simple GitHub Actions Pipeline (Week 21):**
```yaml
name: Deploy to Azure

on:
  push:
    branches: [ main ]

jobs:
  test-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Run tests
        run: |
          pytest backend/tests/
          npm test --prefix frontend/
      
      - name: Deploy to Azure
        if: success()  # Only deploy if tests pass
        uses: azure/webapps-deploy@v2
        with:
          app-name: eventlead-platform
```

---

### Monitoring & Observability

**Service: Azure Application Insights (Free Tier)**

**What is Application Insights?**
Azure's monitoring service that tracks:
- API performance (response times, success rates)
- Errors and exceptions (with stack traces)
- Dependencies (database, Stripe API, email service)
- Availability (uptime monitoring)
- Custom metrics (lead collection rate, form publish rate)

**Decision: Azure Application Insights**

**Why Application Insights?**
- ✅ Free tier: 5GB/month data ingestion (sufficient for MVP)
- ✅ Built into Azure (zero setup - just enable)
- ✅ Integrates with FastAPI (Python SDK available)
- ✅ Integrates with React (JavaScript SDK)
- ✅ Automatic dashboards (no configuration needed)
- ✅ Alerting built-in (email on errors)
- ✅ Query language (KQL - Kusto Query Language - powerful filtering)

**What you get:**
```
Application Insights Dashboard:
- Request rate: 45 req/min
- Average response time: 120ms
- Failed requests: 2 in last hour (both Stripe card declines)
- Dependencies: SQL Server (12ms avg), Stripe API (450ms avg)
- Exceptions: 0 in last 24 hours ✓
- Availability: 99.8% (last 30 days)
```

**Integration with Our Logging:**
- structlog (our logging) → Sends logs to Application Insights
- Application Insights → Visualizes and alerts
- Both work together (structured logs + Azure dashboards)

**Setup:**
```python
# Add Application Insights to FastAPI
from applicationinsights import TelemetryClient

# Initialize (one line)
tc = TelemetryClient(os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"))

# Logs automatically flow to Application Insights
logger.error("error.exception", ...)  # → Shows in App Insights dashboard
```

**Cost:**
- Free tier: 5GB/month (enough for 100K requests/month)
- MVP will be well under this limit
- If exceed: $2.30 per GB (very affordable)

---

## Technology Stack and Library Decisions

**CRITICAL:** This table contains ALL technologies with SPECIFIC versions. No vagueness allowed.

| Category | Technology | Version | Rationale |
|----------|------------|---------|-----------|
| **Frontend Framework** | React | 18.2.0 | Largest ecosystem for complex UI, best BMAD support, component model matches UX spec, concurrent rendering for performance |
| **Frontend Build Tool** | Vite | 5.0.0 | Fastest dev server, excellent React support, simpler than Webpack, hot module replacement |
| **Frontend Language** | TypeScript | 5.2.2 | Type safety (catches bugs early), better editor support, shared types with backend |
| **CSS Framework** | Tailwind CSS | 3.3.5 | Utility-first (rapid development), defined in UX spec, smaller bundle than alternatives |
| **State Management** | Zustand | 4.4.6 | Lightweight (minimal boilerplate), beginner-friendly, less complex than Redux, sufficient for app needs |
| **Form Library** | React Hook Form | 7.48.2 | Performant (uncontrolled components), excellent validation, TypeScript support, widely adopted |
| **Drag-and-Drop** | dnd-kit | 6.0.8 | 60fps performance, accessible, modern, best docs for beginners, modular architecture |
| **Data Fetching** | TanStack Query (React Query) | 5.8.4 | Caching, automatic refetching, optimistic updates, industry standard for data fetching |
| **Charts/Visualization** | Recharts | 2.10.1 | React-native charts, composable, good docs, sufficient for analytics dashboard |
| **Date Handling** | date-fns | 2.30.0 | Lightweight, tree-shakeable, functional API, better than Moment.js |
| **HTTP Client** | Axios | 1.6.2 | Interceptors (auth token injection), request/response transformation, better DX than fetch |
| **Icons** | Lucide React | 0.294.0 | Modern, consistent, tree-shakeable, large icon set, better than Font Awesome |
| **UI Primitives** | Radix UI | 1.3.0 | Unstyled accessible components (modals, dropdowns), works with Tailwind, WCAG compliant |
| **Animation** | Framer Motion | 10.16.5 | Declarative animations, gesture handling, 24 micro-interactions from UX spec |
| **Image Processing (Client)** | Browser Image Compression | 2.0.2 | Client-side image resize/compress before upload, reduces server load |
| **Backend Framework** | FastAPI | 0.104.1 | Async-first (WebSocket support), auto-generated docs, modern typing, perfect for real-time analytics |
| **Backend Language** | Python | 3.11.6 | Scripting background matches Anthony's experience, type hints, async/await, excellent libraries |
| **ORM** | SQLAlchemy | 2.0.23 | Industry standard, SQL Server support, async capabilities, migration tool (Alembic) |
| **Database Migrations** | Alembic | 1.12.1 | Version-controlled schema changes, auto-generation, rollback support, customizable templates |
| **Database Driver** | pyodbc | 5.0.1 | Microsoft-recommended SQL Server driver for Python, ODBC standard |
| **Database** | MS SQL Server | 2022 | Anthony's expertise, enterprise features (RLS, audit), Azure SQL Database compatible |
| **Validation (Backend)** | Pydantic | 2.5.0 | FastAPI native, type validation, data parsing, v2 performance (10x faster) |
| **Password Hashing** | passlib + bcrypt | 1.7.4 / 4.1.1 | Industry standard, secure hashing (bcrypt with cost factor 12), future-proof |
| **JWT Tokens** | python-jose | 3.3.0 | JWT generation/validation, HS256/RS256 algorithms, FastAPI ecosystem |
| **HTTP Client (Backend)** | httpx | 0.25.2 | Async HTTP client (Stripe API calls), better than requests for async |
| **Structured Logging** | structlog | 23.2.0 | JSON logging, context binding, request correlation IDs, production-ready |
| **Logging Integration** | opencensus-ext-azure | 1.1.13 | Application Insights integration, automatic telemetry, Azure-native |
| **Environment Config** | python-decouple | 3.8 | Environment variable management, .env file support, type conversion |
| **Task Queue** | FastAPI BackgroundTasks | (built-in) | Simple async background tasks (email, PDF), sufficient for MVP (can upgrade to Celery later) |
| **WebSocket** | FastAPI WebSocket | (built-in) | Real-time analytics updates, native FastAPI support, simple for solo dev |
| **PDF Generation** | ReportLab | 4.0.7 | Invoice PDF generation, GST-compliant templates, mature library |
| **Image Processing (Server)** | Pillow (PIL) | 10.1.0 | Image resize, optimization, thumbnail generation, Python standard |
| **CSV Generation** | pandas | 2.1.3 | Multiple format support (Salesforce, Marketing Cloud, Emarsys), data transformation |
| **Testing (Backend)** | pytest | 7.4.3 | Python testing standard, fixtures, async support, excellent plugin ecosystem |
| **Testing (Frontend)** | Vitest | 1.0.4 | Vite-native (fast), Jest-compatible API, modern testing framework |
| **E2E Testing** | Playwright | 1.40.0 | Cross-browser testing, auto-wait (no flaky tests), excellent developer experience |
| **Payments** | Stripe Python SDK | 7.6.0 | Payment processing, webhooks, Australian merchant support, industry standard |
| **Email (Production)** | Azure Communication Services SDK | 1.2.0 | Azure-native email, transactional emails, SMTP alternative |
| **Email (Dev)** | MailHog | 1.0.1 | Local email testing (containerized), catches emails without sending, web UI for viewing |
| **Storage (Production)** | azure-storage-blob | 12.19.0 | Azure Blob Storage SDK, file upload/download, SAS tokens |
| **Storage (Dev)** | aiofiles | 23.2.1 | Async local file operations, mimics cloud storage interface |
| **Monitoring** | Azure Application Insights | (service) | Error tracking, performance monitoring, dependency tracking, alerting (Free tier: 5GB/month) |
| **Containerization** | Docker | 24.0.7 | Local development (MailHog, SQL Server), Docker Compose for multi-container setup |
| **CI/CD** | GitHub Actions | (service) | Automated testing and Azure deployment (implemented Week 21 before production) |
| **Hosting (Production)** | Azure App Service | (service) | Web app hosting, auto-scaling, SSL included, Azure-native |
| **Database (Production)** | Azure SQL Database | (service) | Managed SQL Server, automatic backups, geo-redundancy, enterprise SLA 99.99% |
| **CDN** | Azure CDN | (service) | Public form hosting, low latency, global distribution, caching |
| **Secrets Management** | Azure Key Vault | (service) | API keys, connection strings, certificates (production only - .env for dev) |

**Total Technologies: 43 specific tools with exact versions**

**No vagueness:** Every technology has specific version number (workflow requirement satisfied)

---

### Technology Selection Rationale Summary

**Why these specific choices?**

**Frontend:**
- React 18: Only option for complex drag-drop form builder (ecosystem requirement)
- Vite: Fastest build tool (developer productivity)
- TypeScript: Type safety (reduce bugs for beginner developer)
- Tailwind: UX spec requirement (design system defined with Tailwind)
- Zustand: Lightweight state (less learning curve than Redux)
- dnd-kit: Performance requirement (60fps drag interactions)

**Backend:**
- FastAPI: Async requirement (WebSocket for real-time analytics)
- SQLAlchemy: Industry standard ORM (BMAD support, SQL Server compatibility)
- Python 3.11: Anthony's scripting background + modern async features

**Infrastructure:**
- Azure: Existing infrastructure (already have SQL Server, hosting)
- Docker: Local development (MailHog, consistent environments)
- GitHub Actions: Free CI/CD (automated before production)

**Services:**
- Stripe: Payment industry standard (Australian merchant support)
- Application Insights: Free Azure monitoring (comprehensive observability)

**Philosophy:**
- Boring technology (proven, stable, widely adopted)
- Optimize for: Solo developer productivity, beginner-friendly docs, BMAD agent support
- Avoid: Cutting-edge (risky), niche (poor docs), over-engineered (complex)

---

## Technology Dependency Mapping

This section visualizes how all 43 technologies interconnect, identifies critical dependency chains, and analyzes impact if any component fails.

### Dependency Layer Architecture

**Layer 1: Foundation (Language & Runtime)**
```
TypeScript 5.2.2 (Frontend language)
Python 3.11.6 (Backend language)

No dependencies - these are the foundation everything else builds on
```

**Layer 2: Core Frameworks**
```
React 18.2.0
  ├─→ Depends on: TypeScript 5.2.2
  └─→ Built by: Vite 5.0.0

FastAPI 0.104.1
  ├─→ Depends on: Python 3.11.6
  └─→ Uses: Pydantic 2.5.0 (validation)
```

**Layer 3: Framework Extensions**
```
React Ecosystem (all depend on React 18):
  ├─→ Zustand 4.4.6 (state management)
  ├─→ React Hook Form 7.48.2 (forms)
  ├─→ dnd-kit 6.0.8 (drag-and-drop)
  ├─→ TanStack Query 5.8.4 (data fetching)
  ├─→ Recharts 2.10.1 (charts)
  ├─→ Framer Motion 10.16.5 (animations)
  ├─→ Radix UI 1.3.0 (accessible primitives)
  └─→ Lucide React 0.294.0 (icons)

FastAPI Ecosystem (all depend on FastAPI):
  ├─→ SQLAlchemy 2.0.23 (ORM)
  ├─→ python-jose 3.3.0 (JWT)
  ├─→ passlib 1.7.4 (password hashing)
  └─→ structlog 23.2.0 (logging)
```

**Layer 4: Integration SDKs**
```
External Service Integration:
  ├─→ Stripe Python SDK 7.6.0 (uses httpx 0.25.2)
  ├─→ azure-storage-blob 12.19.0
  ├─→ Azure Communication Services SDK 1.2.0
  └─→ opencensus-ext-azure 1.1.13 (Application Insights)
```

**Layer 5: External Services**
```
Cloud Services (no code dependencies):
  ├─→ Azure App Service (hosting)
  ├─→ Azure SQL Database (database)
  ├─→ Azure Blob Storage (file storage)
  ├─→ Azure CDN (public forms)
  ├─→ Stripe (payments)
  └─→ GitHub Actions (CI/CD)
```

---

### Critical Dependency Chains

**Chain 1: Form Builder → Lead Collection (Core Value Chain)**

```
User Browser
  └─→ React 18.2.0 (UI rendering)
       └─→ dnd-kit 6.0.8 (drag components onto canvas)
            └─→ Zustand 4.4.6 (stores form state: components, background, undo history)
                 └─→ Auto-save Manager:
                      ├─→ localStorage (browser) every 5 seconds (offline-safe)
                      └─→ Axios 1.6.2 → FastAPI every 30 seconds
                           └─→ FastAPI /api/forms/{id}/draft endpoint
                                └─→ SQLAlchemy 2.0.23 (ORM)
                                     └─→ pyodbc 5.0.1 (driver)
                                          └─→ SQL Server 2022 (Form table, DesignJSON column)
                                               
On Publish:
  Form.Status = "published"
  └─→ Public URL generated: forms.eventlead.com/{unique-id}
       └─→ Azure CDN hosts public form
            └─→ Event attendee visits URL
                 └─→ Submits form data
                      └─→ FastAPI /api/submissions endpoint
                           └─→ SQLAlchemy → SQL Server (Submission table)
                                └─→ LEAD COLLECTED ✓
                                     └─→ pandas 2.1.3 (CSV export)
                                          └─→ Customer imports to Salesforce
                                               └─→ VALUE REALIZED ✓
```

**Impact Analysis:**
- If **React** fails: Frontend down → Cannot create forms
- If **dnd-kit** fails: Form builder unusable → Fallback to grid renderer
- If **Zustand** fails: State management breaks → Fallback to React Context
- If **localStorage** fails: Auto-save degrades → Database auto-save still works
- If **Axios** fails: API calls fail → Use fetch API (browser native)
- If **FastAPI** fails: Backend down → Platform down (CRITICAL)
- If **SQLAlchemy** fails: Database access fails → Drop to raw SQL (Anthony's expertise)
- If **SQL Server** fails: Data storage down → Platform down (CRITICAL)
- If **pandas** fails: CSV export breaks → VALUE NOT REALIZED (HIGH impact)

**Mitigation Priority:**
- CRITICAL: FastAPI, SQL Server, pandas (core value chain)
- HIGH: React, dnd-kit, SQLAlchemy (user-facing features)
- MEDIUM: Zustand, Axios (have fallbacks)
- LOW: localStorage (database auto-save backup)

---

**Chain 2: Payment Flow (Revenue Chain)**

```
User clicks "Publish" Button
  └─→ React (PublishButton.tsx component)
       └─→ Axios POST /api/forms/{id}/publish
            └─→ FastAPI publish endpoint
                 └─→ Preview test validation (check Form.PreviewTestCount >= threshold)
                      └─→ Stripe Python SDK 7.6.0
                           └─→ httpx 0.25.2 (async HTTP client)
                                └─→ Stripe API (external - payment processing)
                                     └─→ Payment succeeds
                                          └─→ SQLAlchemy async transaction:
                                               ├─→ 1. INSERT Payment (PaymentID, StripeID, Amount)
                                               ├─→ 2. UPDATE Form SET Status='published', PublicURL='...'
                                               ├─→ 3. INSERT Invoice (InvoiceNumber, GST breakdown)
                                               └─→ 4. COMMIT (all or nothing - ACID)
                                                    └─→ Background Tasks (async):
                                                         ├─→ ReportLab 4.0.7 (generate invoice PDF)
                                                         │    └─→ azure-storage-blob (save PDF to Blob Storage)
                                                         │
                                                         └─→ Azure Communication Services SDK 1.2.0
                                                              └─→ Email invoice to Company Admin
                                                                   └─→ REVENUE CAPTURED ✓
```

**Impact Analysis:**
- If **Stripe SDK** fails: Payment processing down → No revenue (CRITICAL)
- If **httpx** fails: External API calls fail → Stripe unreachable (CRITICAL)
- If **SQLAlchemy transaction** fails: Data inconsistency → Rollback ensures no partial state
- If **ReportLab** fails: No PDF invoice → Generate CSV invoice (fallback)
- If **Azure Blob** fails: PDF not stored → Email plain invoice text (fallback)
- If **Email service** fails: Invoice not delivered → User can download from dashboard (acceptable)

**Dependencies with NO fallback (must work):**
- Stripe SDK + httpx (payment processing)
- SQLAlchemy transaction (data consistency)

---

**Chain 3: Multi-Tenant Security (Security Chain)**

```
API Request: GET /api/forms
  └─→ FastAPI middleware stack:
       ├─→ 1. Request ID middleware (generate correlation ID)
       ├─→ 2. Logging middleware (structlog - log request)
       ├─→ 3. Auth middleware:
       │      └─→ python-jose 3.3.0 (verify JWT token)
       │           ├─→ Extract user_id from token
       │           └─→ SQLAlchemy: SELECT * FROM [User] WHERE UserID = @id
       │                └─→ pyodbc → SQL Server
       │                     └─→ Returns user with CompanyID
       │
       └─→ 4. Tenant middleware:
            └─→ Set session context: CompanyID = user.CompanyID
                 └─→ EVERY subsequent query auto-filtered:
                      └─→ SQLAlchemy WHERE clauses: CompanyID = @current_company
                           └─→ SQL Server Row-Level Security (RLS):
                                └─→ Database-level enforcement (defense in depth)
                                     └─→ ONLY returns rows where CompanyID matches
                                          └─→ MULTI-TENANT ISOLATION ✓
```

**Impact Analysis:**
- If **python-jose** fails: JWT verification breaks → Auth fails (platform down)
- If **SQLAlchemy** filter skipped: Multi-tenant breach → CRITICAL security failure
- If **SQL Server RLS** misconfigured: Backup security layer missing → Still have app-level filtering
- If **BOTH** fail: Data breach (catastrophic)

**Defense in Depth:**
- Layer 1: Application (SQLAlchemy WHERE CompanyID)
- Layer 2: Database (SQL Server RLS policies)
- Both must fail for breach to occur (very unlikely)

---

### Single Points of Failure (SPOF) Analysis

**Critical SPOFs (No fallback, platform stops working):**

**SPOF 1: SQL Server 2022**
- **Impact:** Database down → ALL data operations fail → Platform unusable
- **Mitigation:** Azure SQL Database 99.99% SLA, automatic backups, geo-redundancy
- **Recovery:** Azure auto-failover to secondary region (minimal downtime)
- **Likelihood:** Very low (<1 hour/year based on Azure SLA)

**SPOF 2: FastAPI 0.104.1**
- **Impact:** Backend framework fails → All API endpoints down → Platform unusable
- **Mitigation:** Mature framework (stable), pin exact version (no surprise updates)
- **Recovery:** Rollback to previous version if update causes issue
- **Likelihood:** Very low (FastAPI is stable, well-tested)

**SPOF 3: React 18.2.0**
- **Impact:** Frontend framework fails → UI doesn't render → Platform unusable
- **Mitigation:** Mature framework (stable), pin exact version
- **Recovery:** Rollback to previous version
- **Likelihood:** Very low (React 18 is production-proven)

**SPOF 4: Stripe (Payment Processing)**
- **Impact:** Payments fail → No revenue → Business impact (not platform down)
- **Mitigation:** Stripe 99.99% uptime, clear error messages, retry logic
- **Recovery:** Wait for Stripe (usually <15 min), or manual payment (Phase 2)
- **Likelihood:** Very low (<1 hour/year)

**Medium SPOFs (Degraded mode possible):**

**SPOF 5: dnd-kit 6.0.8**
- **Impact:** Drag-and-drop breaks → Form builder unusable
- **Mitigation:** Modular renderer design → Switch to grid-based (contingency)
- **Recovery:** Deploy grid renderer (1-2 days)
- **Likelihood:** Low (dnd-kit is stable)

**SPOF 6: Azure Blob Storage**
- **Impact:** Image uploads fail → Cannot add custom backgrounds
- **Mitigation:** Fallback to template library (templates already in database)
- **Recovery:** Wait for Azure (usually <30 min)
- **Likelihood:** Low (Azure 99.9% SLA)

**SPOF 7: pandas 2.1.3 (CSV Export)**
- **Impact:** CSV export fails → Leads trapped in platform → VALUE NOT REALIZED
- **Mitigation:** Manual CSV generation (write Python script), or simple export (basic format)
- **Recovery:** Deploy fix within hours
- **Likelihood:** Very low (pandas is stable)

**Low-Risk SPOFs (Enhancements only):**

**SPOF 8: Framer Motion** (Animations)
- **Impact:** Animations don't work → Slightly less polished UX
- **Fallback:** CSS transitions (basic animations)

**SPOF 9: Recharts** (Analytics charts)
- **Impact:** Charts don't render → Show table only (data still accessible)
- **Fallback:** Simple HTML tables

**SPOF 10: ReportLab** (PDF invoices)
- **Impact:** Invoice PDFs don't generate → Email plain text invoice
- **Fallback:** CSV invoice or plain text

---

### Dependency Count by Category

**Frontend: 15 dependencies**
- **Core (3):** React, Vite, TypeScript - Platform-critical
- **UI (4):** Tailwind, Radix UI, Lucide, Framer Motion - Important for UX
- **State/Data (4):** Zustand, React Hook Form, TanStack Query, Axios - Core functionality
- **Specialized (4):** dnd-kit, Recharts, date-fns, Browser Image Compression - Feature-specific

**Backend: 17 dependencies**
- **Core (3):** Python, FastAPI, Pydantic - Platform-critical
- **Database (3):** SQLAlchemy, Alembic, pyodbc - Data layer critical
- **Auth (3):** python-jose, passlib, bcrypt - Security critical
- **External SDKs (3):** Stripe, Azure Blob, Azure Communication - Service integration
- **Processing (3):** Pillow, ReportLab, pandas - Feature-specific
- **Infrastructure (4):** structlog, python-decouple, httpx, opencensus - Cross-cutting

**Services: 8 dependencies**
- **Azure (6):** App Service, SQL Database, Blob, CDN, Key Vault, App Insights
- **External (2):** Stripe, GitHub Actions

**Development Only: 3 dependencies**
- Docker, MailHog, aiofiles (local development, not in production)

**Total: 43 technologies (manageable for solo developer)**

---

### Critical Path Dependencies (MVP Launch Requirements)

**Tier 0: Platform-Critical (Cannot Function Without)**

1. **React 18.2.0** → Frontend won't render
2. **FastAPI 0.104.1** → Backend won't run
3. **SQL Server 2022** → No data storage
4. **Azure App Service** → No hosting
5. **TypeScript 5.2.2** → Code won't compile
6. **Python 3.11.6** → Backend won't execute

**Impact if any fails:** Platform completely unusable

---

**Tier 1: Business-Critical (Core Value Delivery)**

7. **dnd-kit 6.0.8** → Form builder doesn't work
8. **SQLAlchemy 2.0.23** → Database access fails
9. **Stripe SDK 7.6.0** → No payments = no revenue
10. **pandas 2.1.3** → No CSV export = leads trapped (value not realized)
11. **Axios 1.6.2** → Frontend can't call backend APIs
12. **Zustand 4.4.6** → State management breaks

**Impact if any fails:** Core business value cannot be delivered

---

**Tier 2: Important (Degraded Mode Possible)**

13. **TanStack Query 5.8.4** → Fallback to basic fetch (no caching)
14. **Azure Blob Storage** → Fallback to local storage or templates
15. **Application Insights** → Fallback to file logs only
16. **ReportLab 4.0.7** → Fallback to plain text invoices
17. **Azure Communication Services** → Fallback to MailHog or manual email

**Impact if any fails:** Features degrade but platform still functional

---

**Tier 3: Enhancements (Can Ship Without)**

18. **Framer Motion** → CSS transitions (less polished animations)
19. **Recharts** → Simple HTML tables (no charts)
20. **Radix UI** → Custom-built components (more work)
21. **Lucide Icons** → Unicode symbols or Font Awesome fallback
22. **date-fns** → Native JavaScript Date (less elegant)

**Impact if any fails:** Slightly worse UX but acceptable for MVP

---

### Development vs Production Dependencies

**Development ONLY:**
```
Docker 24.0.7
  └─→ Runs containers:
       ├─→ MailHog 1.0.1 (email testing)
       └─→ (Optional) SQL Server container

aiofiles 23.2.1 (local file storage)
  └─→ Mimics: Azure Blob Storage interface
  └─→ Replaced by: azure-storage-blob in production

Environment:
  .env.local
  └─→ Contains: Local database connection, local storage paths
```

**Production ONLY:**
```
Azure Services:
  ├─→ Azure App Service (hosting - replaces local server)
  ├─→ Azure SQL Database (managed DB - replaces local SQL Server)
  ├─→ Azure Blob Storage (replaces local file system)
  ├─→ Azure Communication Services (replaces MailHog)
  ├─→ Azure CDN (public forms)
  ├─→ Azure Key Vault (secrets - replaces .env file)
  └─→ Azure Application Insights (monitoring)

GitHub Actions
  └─→ CI/CD pipeline (Week 21+ only)

Environment:
  .env.production
  └─→ Contains: Azure connection strings, Stripe live keys
```

**Both Environments:**
```
Core Stack (identical in dev and prod):
  - React, FastAPI, SQLAlchemy, all libraries
  - SAME CODE runs in both environments
  - ONLY configuration changes (env variables)
```

**Abstraction Layers Handle Differences:**
```python
# StorageProvider interface (same code, different implementation)
if ENV == "production":
    storage = AzureBlobStorageProvider()  # Uses azure-storage-blob
else:
    storage = LocalStorageProvider()      # Uses aiofiles

# EmailProvider interface
if ENV == "production":
    email = AzureCommunicationProvider()  # Uses Azure SDK
else:
    email = MailHogProvider()             # Uses SMTP to MailHog
```

---

### Dependency Update Strategy

**Update Frequency by Layer:**

**Layer 5 (External Services):**
- **Azure services:** Auto-updated by Microsoft (no action required)
- **Stripe API:** Versioned API (use stable version, optional upgrades)
- **GitHub Actions:** Auto-updated (safe, no code changes)
- **Frequency:** Managed by service providers

**Layer 3-4 (Frameworks & SDKs):**
- **React, FastAPI, SQLAlchemy:** Update quarterly (after testing)
- **Security patches:** Update immediately (within 24 hours)
- **Breaking changes:** Evaluate cost/benefit, test on feature branch
- **Process:** Changelog review → feature branch → full test suite → merge
- **Frequency:** Quarterly (or as needed for security)

**Layer 1-2 (Libraries & Utilities):**
- **Utility libraries:** Update semi-annually (low risk)
- **Tailwind, Axios, date-fns:** Stable, infrequent breaking changes
- **Security vulnerabilities:** Update immediately
- **Frequency:** Semi-annually (or as needed)

**Version Pinning (EXACT versions in package files):**
```json
// package.json
{
  "dependencies": {
    "react": "18.2.0",           // EXACT (no ^ or ~)
    "zustand": "4.4.6",
    "@dnd-kit/core": "6.0.8"
  }
}
```

```python
# requirements.txt
fastapi==0.104.1        # EXACT (no >= or ~=)
sqlalchemy==2.0.23
stripe==7.6.0
```

**Benefits:**
- ✅ No surprise updates (prevents integration conflicts from v4)
- ✅ Reproducible builds (same on all machines)
- ✅ Controlled updates (test before applying)

---

### Dependency Update Impact Matrix

| Technology | Update Frequency | Breaking Change Risk | Testing Required | Impact if Breaks | Fallback Available |
|------------|------------------|---------------------|------------------|------------------|--------------------|
| **React** | Quarterly | Medium | Full regression, visual tests | Platform down | None |
| **FastAPI** | Quarterly | Low | API integration tests | Backend down | None |
| **SQLAlchemy** | Quarterly | Low | Database tests, migration tests | Data access fails | Raw SQL (Anthony's expertise) |
| **dnd-kit** | Semi-annually | Medium | Form builder POC, drag tests | Builder unusable | Grid renderer |
| **Stripe SDK** | Annually | Low | Payment flow tests | No revenue | None (wait for fix) |
| **Tailwind** | Annually | Low | Visual regression tests | Styling breaks | None |
| **Zustand** | Annually | Low | State tests | State breaks | React Context |
| **TanStack Query** | Semi-annually | Medium | Data fetching tests | Caching breaks | Basic fetch |
| **pandas** | Annually | Low | CSV export tests | Export fails | Manual CSV generation |
| **Pydantic** | Quarterly | Low (v2 stable) | Validation tests | Validation breaks | None |
| **Azure SDKs** | As released | Low | Integration tests | Service access fails | None |
| **All utilities** | Semi-annually | Low | Unit tests | Localized impact | Varies |

**Update Priority:**
1. **Security patches:** Immediate (all technologies)
2. **Major frameworks:** Quarterly with testing (React, FastAPI, SQLAlchemy)
3. **Specialized libs:** Semi-annually (dnd-kit, TanStack Query)
4. **Utilities:** Annually or as needed (Tailwind, date-fns, etc.)

---

### Dependency Conflict Prevention

**Known Compatibility Matrix:**

| Technology A | Technology B | Compatibility | Notes |
|--------------|--------------|---------------|-------|
| React 18.2.0 | dnd-kit 6.0.8 | ✅ Compatible | dnd-kit designed for React 18+ |
| FastAPI 0.104.1 | Pydantic 2.5.0 | ✅ Compatible | FastAPI 0.100+ supports Pydantic v2 |
| FastAPI | SQLAlchemy 2.0.23 | ✅ Compatible | Both support async/await |
| Python 3.11.6 | All Azure SDKs | ✅ Compatible | All SDKs support Python 3.11 |
| SQLAlchemy 2.0 | pyodbc 5.0.1 | ✅ Compatible | Standard ODBC driver |
| Tailwind 3.3.5 | Radix UI 1.3.0 | ✅ Compatible | Unstyled components work with any CSS |
| Vite 5.0.0 | React 18.2.0 | ✅ Compatible | Vite optimized for React |
| structlog | Azure App Insights | ✅ Compatible | opencensus-ext-azure bridges |

**Potential Future Conflicts (Monitor):**

| Upgrade Path | Risk | Monitor For |
|--------------|------|-------------|
| React 18 → 19 | Medium | Breaking changes in concurrent rendering |
| Pydantic 2 → 3 | Medium | Major version likely has breaking changes |
| dnd-kit 6 → 7 | Medium | API changes, performance regressions |
| Python 3.11 → 3.12 | Low | Azure SDK compatibility |
| Tailwind 3 → 4 | Medium | Class name changes, config changes |

**Before ANY major version upgrade:**
1. Read full changelog
2. Create feature branch
3. Run full test suite
4. Test integration points (auto-save + undo/redo + drag-drop)
5. If tests pass → merge
6. If conflicts → fix or defer upgrade

---

### Dependency Installation & Management

**Frontend Installation:**
```bash
# One command installs all 15 frontend dependencies
npm install

# Installs from package.json with exact versions
# Creates node_modules/ directory
# Updates package-lock.json (lockfile for reproducibility)
```

**Backend Installation:**
```bash
# One command installs all 17 backend dependencies
pip install -r requirements.txt

# Installs exact versions specified in requirements.txt
# Creates virtual environment isolation
```

**Development Environment Setup:**
```bash
# Install Docker (for MailHog container)
# Pull MailHog image
docker pull mailhog/mailhog

# Run MailHog (email testing)
docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog

# Total setup time: ~10 minutes
```

**Dependency Files (Version Control):**
```
Checked into Git:
  ├─→ package.json (frontend dependencies with exact versions)
  ├─→ package-lock.json (lockfile - ensures reproducible builds)
  ├─→ requirements.txt (backend dependencies with exact versions)
  ├─→ docker-compose.yml (local environment setup)
  └─→ .env.example (template for environment variables)

NOT in Git:
  ├─→ node_modules/ (installed via npm install)
  ├─→ venv/ (Python virtual environment)
  ├─→ .env.local (contains secrets - listed in .gitignore)
  └─→ .env.production (contains secrets - listed in .gitignore)
```

---

### Summary: Dependency Management

**Total: 43 technologies, all interconnected**

**Dependency Layers:**
1. Foundation: TypeScript, Python (2 dependencies)
2. Core Frameworks: React, FastAPI (2 dependencies)
3. Framework Extensions: 23 libraries
4. Integration SDKs: 5 SDKs
5. External Services: 8 services
6. Development Tools: 3 tools

**Critical Chains Identified:**
- Form Builder → Lead Collection (11 dependencies)
- Payment Flow (8 dependencies)
- Multi-Tenant Security (6 dependencies)

**Single Points of Failure:**
- Critical (4): SQL Server, FastAPI, React, Stripe
- Medium (3): dnd-kit, Azure Blob, pandas
- Low (3): Framer Motion, Recharts, ReportLab

**Management Strategy:**
- Pin EXACT versions (prevent surprises)
- Update quarterly with testing (controlled process)
- Security patches immediate (GitHub Dependabot)
- Feature branch testing (staged updates)

**Your v4 Concern Addressed:**
- No auto-updates (exact version pinning)
- Integration testing before merge (prevent conflicts)
- Fallbacks identified (know what to do if dependency fails)

---

## Database Architecture

This section defines the complete database schema with Anthony's enterprise naming standards, multi-tenant isolation strategy, audit tracking, and data lineage architecture.

### Database Design Philosophy

**Core Principles:**
1. **Database-First Approach:** Schema drives API design (leverages Anthony's data management expertise)
2. **Self-Documenting Schema:** Table and column names reveal relationships (foreign keys named after referenced tables)
3. **Enterprise Standards:** PascalCase naming, comprehensive audit fields, soft deletes, proper data types
4. **Multi-Tenant Isolation:** CompanyID on all tenant tables, Row-Level Security (RLS) enforcement
5. **Data Quality:** Constraints, validations, indexes for performance
6. **Audit Everything:** ActivityLog tracks all user actions, immutable records

---

### Database Standards (Authoritative - MANDATORY)

**CRITICAL RULES (Must Never Be Violated):**

**1. Unicode Support:**
- ✅ ALL text fields MUST be `NVARCHAR` (never `VARCHAR`)
- Why: International platform requires Unicode (Chinese, Arabic, emoji, special characters)
- SQLAlchemy: Configure `type_annotation_map = {str: NVARCHAR}` in Base class

**2. Primary Keys:**
- ✅ MUST be `[TableName]ID` (e.g., `UserID`, `CompanyID`, `FormID`)
- Never use generic `id`, `ID`, or custom names
- Type: `BIGINT IDENTITY(1,1)` (preferred) or `INT IDENTITY(1,1)`

**3. Foreign Keys:**
- ✅ MUST be `[ReferencedTableName]ID` (e.g., `CompanyID`, `EventID`)
- Must match the PK name exactly
- Creates self-documenting schema (column name reveals relationship)
- Example: `UserRoleID` tells you `UserRole` table exists

**4. Boolean Fields:**
- ✅ MUST use `Is` or `Has` prefix (e.g., `IsActive`, `IsEmailVerified`, `HasAccess`)
- Type: `BIT` in SQL Server, `Boolean` in SQLAlchemy
- Never: `Active`, `EmailVerified`, `Verified` (missing prefix)

**5. PascalCase:**
- ✅ ALL table and column names use PascalCase
- Tables: `User`, `Company`, `Event`, `Form`, `Submission`
- Columns: `UserID`, `CompanyName`, `CreatedDate`, `IsActive`
- Never: snake_case, camelCase, lowercase

**6. Timestamps (All in UTC):**
- ✅ ALL timestamps stored in UTC using `GETUTCDATE()`
- Type: `DATETIME2` (more precise than DATETIME)
- Default: `DEFAULT GETUTCDATE()` for CreatedDate fields
- Conversion: Use `fn_ConvertToTimezone()` function for display

**Standard Audit Columns (ALL tables MUST have):**
```sql
CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE()
CreatedBy BIGINT NULL  -- FK to User.UserID (can be NULL for system actions)

-- For mutable tables (tables that can be updated):
LastUpdated DATETIME2 NULL
UpdatedBy BIGINT NULL  -- FK to User.UserID

-- For soft delete (no hard deletes - retain history):
IsDeleted BIT NOT NULL DEFAULT 0
DeletedDate DATETIME2 NULL
DeletedBy BIGINT NULL  -- FK to User.UserID
```

**7. SQL Server Schemas (Logical Organization):**
- ✅ Use schemas to organize tables by purpose (NOT just default `dbo`)
- ✅ Schema names: lowercase, single word (`dbo`, `log`, `audit`, `ref`, `config`, `cache`)
- ✅ Table reference: `[SchemaName].[TableName]` (e.g., `log.ApiRequest`, `ref.Country`)
- ✅ Schemas provide: logical organization, security boundaries, lifecycle management

---

### Schema Organization Strategy

**Why Use Schemas?**
- **Clarity:** Instantly understand table purpose from schema name
- **Security:** Grant permissions at schema level (not table-by-table)
- **Lifecycle:** Different retention policies per schema (logs vs business data)
- **Maintenance:** Easier backups, archiving, and operations
- **Self-Documenting:** Queries reveal data type (business vs logging vs reference)

---

#### Schema Definitions

**1. `dbo` Schema - Core Business Entities**
- **Purpose:** Primary business data customers pay for
- **Retention:** Permanent (soft delete only, never hard delete)
- **Backup Priority:** CRITICAL (hourly backups)
- **Write Volume:** Medium
- **Tables:**
  - `dbo.User` - User accounts
  - `dbo.Company` - Company profiles
  - `dbo.CompanyCustomerDetails` - Customer-specific company data
  - `dbo.CompanyBillingDetails` - Billing information
  - `dbo.CompanyOrganizerDetails` - Organizer-specific company data
  - `dbo.Event` - Events (domain features)
  - `dbo.Form` - Form builder designs
  - `dbo.Submission` - Lead capture data
  - `dbo.Image` - Uploaded images
  - `dbo.Payment` - Payment transactions
  - `dbo.Invoice` - Billing invoices
  - `dbo.Invitation` - Team invitations
  - `dbo.UserCompany` - User-company relationships
  - `dbo.EmailVerificationToken` - Email verification tokens
  - `dbo.PasswordResetToken` - Password reset tokens

---

**2. `log` Schema - Technical Logging**
- **Purpose:** Application logging for debugging, monitoring, diagnostics
- **Retention:** 90 days, then archive or delete
- **Backup Priority:** MEDIUM (can be rebuilt from application logs)
- **Write Volume:** VERY HIGH (every API request logged)
- **Tables:**
  - `log.ApiRequest` - HTTP request/response logging
  - `log.AuthEvent` - Authentication events (login, logout, token refresh)
  - `log.ApplicationError` - Application errors and exceptions
  - `log.Performance` - Slow query tracking, operation timing
  - `log.EmailDelivery` - Email delivery tracking
  - `log.WebSocketConnection` - WebSocket connection events (future)

**Characteristics:**
- High write volume (every request)
- Rarely queried (only for debugging)
- Can be on separate filegroup (different disk for I/O performance)
- Simpler indexes (optimized for writes)

---

**3. `ref` Schema - Reference/Lookup Data**
- **Purpose:** Static or slowly-changing reference data
- **Retention:** Permanent
- **Backup Priority:** MEDIUM (changes rarely)
- **Write Volume:** VERY LOW (admin changes only)
- **Tables:**
  - `ref.Country` - Country lookup
  - `ref.Language` - Language lookup
  - `ref.Industry` - Industry lookup
  - `ref.UserRole` - User role definitions (if table-based, otherwise enum in code)
  - `ref.InvitationStatus` - Invitation status lookup (if table-based)
  - `ref.UserStatus` - User status lookup (if table-based)

**Characteristics:**
- Very low write volume
- High read volume (every query)
- Excellent candidate for in-memory caching
- Small tables (10-1000 rows max)

---

**4. `audit` Schema - Compliance Audit Trail** *(Added Epic 2+)*
- **Purpose:** Immutable audit trail for compliance (who did what when)
- **Retention:** 7 years (regulatory compliance)
- **Backup Priority:** CRITICAL (legal/compliance requirement)
- **Write Volume:** Medium (business actions only, not every API call)
- **Tables:**
  - `audit.ActivityLog` - All user actions (CRUD operations)
  - `audit.User` - User record changes (before/after snapshots)
  - `audit.Company` - Company record changes
  - `audit.Form` - Form design changes
  - `audit.Role` - RBAC role changes

**Characteristics:**
- Append-only (NEVER update or delete)
- Queried for compliance reports
- May need legal hold capability
- Different from logging (compliance vs debugging)

---

**5. `config` Schema - Configuration Management** *(Added Epic 1)*
- **Purpose:** Runtime application configuration
- **Retention:** Permanent with change history
- **Backup Priority:** HIGH (critical for app behavior)
- **Write Volume:** VERY LOW (admin changes only)
- **Tables:**
  - `config.AppSetting` - Runtime business rules
  - `config.ValidationRule` - Country-specific validation
  - `config.FeatureFlag` - Feature toggles (future)
  - `config.PricingTier` - Subscription pricing (future)

**Characteristics:**
- Critical for application behavior
- Changes require careful audit trail
- Cached in application layer
- Admin-only modifications

---

**6. `cache` Schema - External API Cache** *(Added Epic 3+)*
- **Purpose:** Cache for external API results (safe to delete/rebuild)
- **Retention:** 30-90 days, then delete
- **Backup Priority:** LOW (can be rebuilt from source API)
- **Write Volume:** Medium
- **Tables:**
  - `cache.ABRSearch` - ABR API lookup cache
  - `cache.Geocoding` - Address geocoding cache (future)
  - `cache.EmailValidation` - Email validation cache (future)

**Characteristics:**
- Can be truncated without data loss
- Improves performance but not critical
- May not need full audit columns

---

#### Schema Organization Summary Table

| Schema | Purpose | Retention | Backup | Write Volume | Example Tables |
|--------|---------|-----------|--------|--------------|----------------|
| **dbo** | Core business data | Permanent | CRITICAL | Medium | User, Company, Form, Submission |
| **log** | Technical logging | 90 days | MEDIUM | Very High | ApiRequest, AuthEvent, ApplicationError |
| **ref** | Reference data | Permanent | MEDIUM | Very Low | Country, Language, Industry |
| **audit** | Compliance trail | 7 years | CRITICAL | Medium | ActivityLog, User changes, Role changes |
| **config** | Runtime config | Permanent | HIGH | Very Low | AppSetting, ValidationRule, FeatureFlag |
| **cache** | External API cache | 30-90 days | LOW | Medium | ABRSearch, Geocoding |

---

#### SQLAlchemy Schema Configuration

**Models must specify schema:**
```python
# Core business entity (dbo schema)
class User(Base):
    __tablename__ = 'User'
    __table_args__ = {'schema': 'dbo'}
    
    UserID = Column(BIGINT, primary_key=True)
    Email = Column(NVARCHAR(255), nullable=False)
    # ... columns

# Logging table (log schema)
class ApiRequest(Base):
    __tablename__ = 'ApiRequest'
    __table_args__ = {'schema': 'log'}
    
    ApiRequestID = Column(BIGINT, primary_key=True)
    RequestPath = Column(NVARCHAR(500), nullable=False)
    # ... columns

# Reference data (ref schema)
class Country(Base):
    __tablename__ = 'Country'
    __table_args__ = {'schema': 'ref'}
    
    CountryID = Column(BIGINT, primary_key=True)
    CountryName = Column(NVARCHAR(100), nullable=False)
    # ... columns

# Configuration (config schema)
class AppSetting(Base):
    __tablename__ = 'AppSetting'
    __table_args__ = {'schema': 'config'}
    
    AppSettingID = Column(BIGINT, primary_key=True)
    SettingKey = Column(NVARCHAR(100), nullable=False)
    # ... columns
```

---

#### Alembic Migration Schema Support

**Create schema first:**
```python
def upgrade():
    # Create schemas (only once, in initial migration)
    op.execute("CREATE SCHEMA log;")
    op.execute("CREATE SCHEMA ref;")
    op.execute("CREATE SCHEMA config;")
    
    # Create tables in appropriate schemas
    op.create_table(
        'ApiRequest',
        sa.Column('ApiRequestID', sa.BIGINT(), nullable=False),
        sa.Column('RequestPath', sa.NVARCHAR(500), nullable=False),
        # ... columns
        sa.PrimaryKeyConstraint('ApiRequestID'),
        schema='log'  # Specify schema here
    )
    
    op.create_table(
        'Country',
        sa.Column('CountryID', sa.BIGINT(), nullable=False),
        sa.Column('CountryName', sa.NVARCHAR(100), nullable=False),
        # ... columns
        schema='ref'
    )
```

---

#### Cross-Schema Foreign Keys

**Tables can reference across schemas:**
```sql
-- log.ApiRequest references dbo.User
CREATE TABLE [log].[ApiRequest] (
    ApiRequestID BIGINT IDENTITY(1,1) PRIMARY KEY,
    UserID BIGINT NULL,  -- FK to dbo.User
    RequestPath NVARCHAR(500) NOT NULL,
    -- ... columns
    CONSTRAINT FK_ApiRequest_User 
        FOREIGN KEY (UserID) REFERENCES [dbo].[User](UserID)
);

-- config.ValidationRule references ref.Country
CREATE TABLE [config].[ValidationRule] (
    ValidationRuleID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CountryID BIGINT NOT NULL,  -- FK to ref.Country
    RuleType NVARCHAR(50) NOT NULL,
    -- ... columns
    CONSTRAINT FK_ValidationRule_Country 
        FOREIGN KEY (CountryID) REFERENCES [ref].[Country](CountryID)
);
```

---

#### Query Examples with Schemas

**Self-documenting queries:**
```sql
-- Query business data with logging
SELECT 
    u.Email,
    ar.RequestPath,
    ar.StatusCode,
    ar.CreatedDate
FROM dbo.User u  -- Business entity
INNER JOIN log.ApiRequest ar ON ar.UserID = u.UserID  -- Logging data
WHERE ar.CreatedDate > GETUTCDATE() - 1;

-- Query with reference data
SELECT 
    u.FirstName,
    u.LastName,
    c.CompanyName,
    ctry.CountryName
FROM dbo.User u  -- Business entity
INNER JOIN dbo.Company c ON c.CompanyID = u.CompanyID  -- Business entity
INNER JOIN ref.Country ctry ON ctry.CountryID = c.CountryID  -- Reference data
WHERE u.IsDeleted = 0;
```

---

**Complete Database Schema:** Core tables organized by schema:

**`dbo` Schema (Core Business):**
- User, UserCompany - User accounts and relationships
- Company, CompanyCustomerDetails, CompanyBillingDetails, CompanyOrganizerDetails
- Event - Domain features
- Form, Submission, FormField - Form builder & lead capture
- Image, Payment, Invoice, Invitation, PublishRequest
- EmailVerificationToken, PasswordResetToken

**`log` Schema (Technical Logging):**
- ApiRequest, AuthEvent, ApplicationError, Performance, EmailDelivery, WebSocketConnection

**`ref` Schema (Reference/Lookup):**
- Country, Language, Industry
- UserRole, InvitationStatus, UserStatus (if table-based)

**`audit` Schema (Compliance Trail):**
- ActivityLog, User, Company, Form, Role (audit history tables)

**`config` Schema (Configuration):**
- AppSetting, ValidationRule
- FeatureFlag, PricingTier (future)

**`cache` Schema (External API Cache):**
- ABRSearch, Geocoding, EmailValidation (future)

**All tables follow enterprise standards:** PascalCase, NVARCHAR text, UTC timestamps, audit columns, soft deletes, multi-tenant CompanyID, Row-Level Security enforcement.

---

### Configuration Management Architecture

**Design Philosophy:**
- **Right-Sized for Current Needs:** Only what authentication & onboarding requires
- **Clear Separation:** Database for business rules, `.env` for infrastructure secrets, code for static logic
- **Runtime Flexibility:** Change business rules without code deployment
- **Standards Compliant:** All tables follow [TableName]ID pattern and Solomon's standards
- **Type-Safe:** Service layer provides type conversion and defaults

---

#### Configuration Distribution Strategy

**Configuration belongs in THREE places:**

**1. `.env` Files (Infrastructure & Secrets)**
- Database connection strings
- JWT secret keys (NEVER in database)
- API keys (email service, payment gateway)
- Environment identifiers (development, staging, production)
- Frontend URLs (environment-specific)

**Example `.env`:**
```env
# Environment
ENVIRONMENT=development

# Database
DATABASE_URL=mssql+pyodbc://localhost/EventLeadPlatform?driver=ODBC+Driver+18...

# JWT Secrets (from Azure Key Vault)
JWT_SECRET_KEY=<secret>
JWT_ALGORITHM=HS256

# Email Service
EMAIL_API_KEY=<from Key Vault>
EMAIL_FROM_ADDRESS=noreply@eventlead.com

# Frontend
FRONTEND_URL=https://app.eventlead.com
```

**2. Database Tables (Runtime Business Rules)**
- JWT token expiry times (changeable without deployment)
- Password validation rules
- Email verification token expiry
- Team invitation expiry
- Country-specific validation rules (phone, postal code, tax ID)
- Test threshold settings (preview tests required)

**Example: AppSetting Table**
- `jwt_access_token_expiry_minutes` → 15 minutes
- `password_min_length` → 8 characters
- `email_verification_token_expiry_hours` → 24 hours
- `invitation_token_expiry_days` → 7 days

**3. Code Constants (Static Logic)**
- Enum definitions (UserRole, InvitationStatus, UserStatus)
- Physical limits (max file upload size, max form fields)
- Default fallback values
- Regex patterns (email format validation)

---

#### AppSetting Table (Runtime Business Rules)

**Purpose:** Store runtime-changeable application settings

**Schema:** `config.AppSetting` (config schema for configuration tables)

**Table Definition:**
```sql
CREATE TABLE [config].[AppSetting] (
    AppSettingID BIGINT IDENTITY(1,1) PRIMARY KEY,
    SettingKey NVARCHAR(100) NOT NULL UNIQUE,
    SettingValue NVARCHAR(MAX) NOT NULL,
    SettingCategory NVARCHAR(50) NOT NULL,  -- 'authentication', 'validation', 'email'
    SettingType NVARCHAR(20) NOT NULL,      -- 'integer', 'boolean', 'string', 'json'
    Description NVARCHAR(500) NOT NULL,
    DefaultValue NVARCHAR(MAX) NOT NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 999,
    -- Standard audit columns
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    CONSTRAINT FK_AppSetting_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_AppSetting_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_AppSetting_DeletedBy FOREIGN KEY (DeletedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT CK_AppSetting_SettingType CHECK (SettingType IN ('integer', 'boolean', 'string', 'json', 'decimal')),
    CONSTRAINT CK_AppSetting_Category CHECK (SettingCategory IN ('authentication', 'validation', 'email', 'invitation', 'security'))
);
```

**Epic 1 Settings:**
| SettingKey | Value | Category | Type | Purpose |
|------------|-------|----------|------|---------|
| `jwt_access_token_expiry_minutes` | 15 | authentication | integer | JWT access token expiry |
| `jwt_refresh_token_expiry_days` | 7 | authentication | integer | JWT refresh token expiry |
| `password_min_length` | 8 | authentication | integer | Minimum password length |
| `max_failed_login_attempts` | 5 | security | integer | Login attempts before lockout |
| `account_lockout_minutes` | 15 | security | integer | Account lockout duration |
| `email_verification_token_expiry_hours` | 24 | validation | integer | Email verification expiry |
| `password_reset_token_expiry_hours` | 1 | validation | integer | Password reset expiry |
| `invitation_token_expiry_days` | 7 | invitation | integer | Team invitation expiry |

---

#### ValidationRule Table (Country-Specific Validation)

**Purpose:** Store country-specific validation rules for phone numbers, postal codes, tax IDs

**Schema:** `config.ValidationRule` (config schema for configuration tables)

**Table Definition:**
```sql
CREATE TABLE [config].[ValidationRule] (
    ValidationRuleID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CountryID BIGINT NOT NULL,
    RuleType NVARCHAR(50) NOT NULL,         -- 'phone', 'postal_code', 'tax_id'
    RuleName NVARCHAR(100) NOT NULL,
    ValidationPattern NVARCHAR(500) NOT NULL,  -- Regex pattern
    ErrorMessage NVARCHAR(200) NOT NULL,
    MinLength INT NULL,
    MaxLength INT NULL,
    ExampleValue NVARCHAR(100) NULL,
    SortOrder INT NOT NULL DEFAULT 999,
    IsActive BIT NOT NULL DEFAULT 1,
    -- Standard audit columns
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    CONSTRAINT FK_ValidationRule_Country FOREIGN KEY (CountryID) REFERENCES [ref].[Country](CountryID),
    CONSTRAINT FK_ValidationRule_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_ValidationRule_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_ValidationRule_DeletedBy FOREIGN KEY (DeletedBy) REFERENCES [dbo].[User](UserID),
    CONSTRAINT CK_ValidationRule_RuleType CHECK (RuleType IN ('phone', 'postal_code', 'tax_id', 'email', 'address'))
);
```

**Australia Examples (CountryID = 1):**
| RuleType | RuleName | ValidationPattern | ErrorMessage |
|----------|----------|-------------------|--------------|
| phone | Australian Mobile | `^\+61[4-5][0-9]{8}$` | Mobile must be +61 followed by 4 or 5 and 8 digits |
| phone | Australian Landline | `^\+61[2-8][0-9]{8}$` | Landline must be +61 followed by area code |
| postal_code | Australian Postcode | `^[0-9]{4}$` | Postcode must be 4 digits |
| tax_id | Australian ABN | `^[0-9]{11}$` | ABN must be 11 digits |

---

#### Configuration Service (Backend)

**Purpose:** Centralized service for retrieving configuration with type conversion and caching

**File:** `backend/common/config_service.py`

**Key Features:**
- In-memory caching for performance
- Type conversion (string → integer/boolean/json)
- Fallback to code defaults
- Type-safe convenience methods

**Example Usage:**
```python
from backend.common.config_service import ConfigurationService

# In authentication endpoint
config = ConfigurationService(db)
jwt_expiry = config.get_jwt_access_expiry_minutes()  # Returns 15 (integer)

# In password validation
min_length = config.get_password_min_length()  # Returns 8 (integer)
if len(password) < min_length:
    raise ValueError(f"Password must be at least {min_length} characters")

# Country-specific validation
rules = config.get_validation_rules(country_id=1, rule_type='phone')
for rule in rules:
    if re.match(rule.ValidationPattern, phone):
        return True  # Valid
```

---

#### Configuration API Endpoints

**Get Application Configuration:**
```
GET /api/config
Response: {
  passwordMinLength: 8,
  jwtAccessExpiryMinutes: 15,
  emailVerificationExpiryHours: 24,
  invitationExpiryDays: 7
}
```

**Get Country-Specific Validation Rules:**
```
GET /api/config/validation-rules?country_id=1&rule_type=phone
Response: [
  {
    ruleType: "phone",
    ruleName: "Australian Mobile",
    validationPattern: "^\\+61[4-5][0-9]{8}$",
    errorMessage: "Mobile must be +61 followed by 4 or 5 and 8 digits",
    exampleValue: "+61412345678"
  }
]
```

---

#### Frontend Configuration Hooks

**File:** `frontend/src/hooks/useAppConfig.ts`

**React Query Hooks:**
```typescript
// Get application settings
const { config } = useAppConfig();
// Returns: { passwordMinLength: 8, jwtAccessExpiryMinutes: 15, ... }

// Get country validation rules
const { rules } = useValidationRules(countryId, 'phone');
// Returns: [{ ruleName: "Australian Mobile", validationPattern: "...", ... }]
```

**Usage in Components:**
```typescript
const SignupForm = () => {
  const { config } = useAppConfig();
  
  return (
    <input 
      type="password"
      minLength={config?.passwordMinLength || 8}
      placeholder={`Password (min ${config?.passwordMinLength || 8} characters)`}
    />
  );
};
```

---

#### Configuration Design Benefits

**1. Right-Sized for Epic 1:**
- Only what authentication & onboarding needs
- No speculative future features
- Simple single-table queries (no complex hierarchy)

**2. Standards Compliant:**
- AppSettingID (follows [TableName]ID pattern) ✅
- ValidationRuleID (follows [TableName]ID pattern) ✅
- Full audit trail (CreatedBy, UpdatedBy, IsDeleted) ✅
- NVARCHAR for all text ✅

**3. Clear for Developers:**
- Obvious where configuration belongs (`.env` vs database vs code)
- Type-safe service methods with descriptive names
- No confusion about resolution order (single source of truth)

**4. Runtime Flexibility:**
- Change JWT expiry without code deployment
- Update password rules via database
- Add new country validation rules without code changes

**5. Performance:**
- In-memory caching in backend service
- React Query caching in frontend (5-10 minute stale time)
- Single table queries (no joins required)

---

**Configuration Evolution Path:**

**Epic 1 (Current):**
- AppSetting: Simple key-value for runtime settings
- ValidationRule: Country-specific validation

**Future Epics (When Needed):**
- **Epic 3 (Feature Flags):** Add `FeatureFlag` table for gradual rollouts
- **Epic 4 (Pricing Tiers):** Add `PricingTier` table for subscription plans
- **Epic 9+ (Enterprise):** Add per-tenant configuration overrides

**Key Principle:** Start simple, add complexity only when requirements demand it.

---

## API Architecture

This section defines the RESTful API design, endpoint patterns, request/response formats, authentication flow, and error handling strategy.

### API Design Philosophy

**Core Principles:**
1. **RESTful JSON API:** Standard HTTP methods (GET, POST, PUT, DELETE), JSON request/response bodies
2. **Resource-Oriented:** URLs represent resources (`/api/forms`, `/api/events`), not actions
3. **Stateless:** Every request contains auth token (JWT), no server-side session state
4. **Consistent Patterns:** Predictable URL structure, standard error formats, uniform pagination
5. **Multi-Tenant Aware:** CompanyID injected from JWT token, automatic filtering in every query
6. **Versioned (Future):** `/api/v1/` prefix for API versioning (not needed for MVP, but structure allows it)

---

### Authentication Flow

**JWT Token-Based Authentication:**

**1. Signup Flow:**
```
POST /api/auth/signup
Request: {email, password, firstName, lastName}
Response: {message: "Please verify your email", userId}

→ Backend: Create User (IsEmailVerified = false, OnboardingComplete = false)
→ Send verification email with token
→ User clicks email link

GET /api/auth/verify-email?token={token}
Response: Redirect to login (email verified ✓)

→ Backend: Update User.IsEmailVerified = true
```

**2. Login Flow:**
```
POST /api/auth/login
Request: {email, password}
Response: {
  accessToken: "eyJhbGci...",
  user: {userId, email, firstName, lastName, role, companyId, onboardingComplete}
}

→ Backend: Verify password, generate JWT token
→ JWT contains: {userId, companyId, role, email}
→ Frontend: Store token in memory (Zustand state) + localStorage
```

**3. Onboarding Flow (First-time User):**
```
POST /api/companies (create company)
Request: {companyName, abn, billingAddress, industry}
Response: {companyId, message: "Company created"}

→ Backend: Create Company, update User.CompanyID, User.OnboardingComplete = true
→ Frontend: Redirect to dashboard
```

**4. Protected Endpoint Access:**
```
GET /api/forms
Headers: Authorization: Bearer {accessToken}

→ Middleware: Verify JWT token
→ Extract: {userId, companyId, role}
→ Inject: CompanyID into query filter
→ Response: Only forms for user's company
```

**JWT Token Structure:**
```json
{
  "sub": 456,  // userId (subject)
  "company_id": 789,
  "role": "company_admin",
  "email": "anthony@example.com",
  "exp": 1697865600,  // Expiration (1 hour)
  "iat": 1697862000   // Issued at
}
```

---

### API Endpoint Patterns

**Standard RESTful Patterns:**

| HTTP Method | Endpoint | Purpose | Request Body | Response |
|-------------|----------|---------|--------------|----------|
| POST | `/api/resources` | Create new resource | Resource data | `{id, ...fields}` 201 Created |
| GET | `/api/resources` | List all resources (paginated) | None | `{data: [], total, page}` 200 OK |
| GET | `/api/resources/{id}` | Get single resource | None | `{id, ...fields}` 200 OK |
| PUT | `/api/resources/{id}` | Update entire resource | Full resource data | `{id, ...fields}` 200 OK |
| PATCH | `/api/resources/{id}` | Partial update | Changed fields only | `{id, ...fields}` 200 OK |
| DELETE | `/api/resources/{id}` | Soft delete resource | None | `{message}` 204 No Content |

---

### Complete API Endpoint Reference

**Authentication (`/api/auth`):**
```
POST   /api/auth/signup               - Create new user account
POST   /api/auth/login                - Login (returns JWT token)
POST   /api/auth/logout               - Logout (client-side token removal)
GET    /api/auth/verify-email         - Verify email (from email link)
POST   /api/auth/resend-verification  - Resend verification email
POST   /api/auth/forgot-password      - Request password reset
POST   /api/auth/reset-password       - Reset password (with token)
GET    /api/auth/me                   - Get current user info
```

**Companies (`/api/companies`):**
```
POST   /api/companies                 - Create company (onboarding)
GET    /api/companies/{id}            - Get company details
PUT    /api/companies/{id}            - Update company
PATCH  /api/companies/{id}/settings   - Update company settings (test threshold, analytics opt-out)
```

**Events (`/api/events`):**
```
POST   /api/events                    - Create event
GET    /api/events                    - List company's events (filtered by CompanyID)
GET    /api/events/{id}               - Get event details
PUT    /api/events/{id}               - Update event
DELETE /api/events/{id}               - Soft delete event
GET    /api/events/{id}/forms         - List forms for event
```

**Forms (`/api/forms`):**
```
POST   /api/forms                     - Create form
GET    /api/forms                     - List company's forms
GET    /api/forms/{id}                - Get form design
PUT    /api/forms/{id}                - Update form design
POST   /api/forms/{id}/draft          - Auto-save draft (every 30s)
POST   /api/forms/{id}/publish        - Publish form (payment required)
POST   /api/forms/{id}/unpublish      - Unpublish form
POST   /api/forms/{id}/test           - Submit preview test
DELETE /api/forms/{id}                - Soft delete form
GET    /api/forms/{id}/submissions    - List submissions for form
```

**Images (`/api/images`):**
```
POST   /api/images/upload             - Upload background image
GET    /api/images                    - List company's images (gallery)
GET    /api/images/{id}               - Get image metadata
DELETE /api/images/{id}               - Soft delete image
```

**Team/Invitations (`/api/team`):**
```
GET    /api/team                      - List company team members
POST   /api/team/invite               - Invite team member (send invitation)
PATCH  /api/team/{userId}/role        - Change user role (Admin only)
DELETE /api/team/{userId}             - Remove user from company
GET    /api/invitations               - List pending invitations
POST   /api/invitations/{id}/accept   - Accept invitation (from email link)
DELETE /api/invitations/{id}          - Cancel invitation
```

**Publish Requests (`/api/publish-requests`):**
```
POST   /api/publish-requests          - Request publish approval (User → Admin)
GET    /api/publish-requests          - List pending requests (Admin sees all, User sees own)
POST   /api/publish-requests/{id}/approve  - Approve request (Admin only)
POST   /api/publish-requests/{id}/decline  - Decline request (Admin only)
```

**Payments (`/api/payments`):**
```
POST   /api/payments/create-intent    - Create Stripe payment intent (before publish)
POST   /api/payments/confirm          - Confirm payment succeeded (webhook)
GET    /api/payments                  - List company's payment history
GET    /api/payments/{id}             - Get payment details
GET    /api/payments/{id}/invoice     - Download invoice PDF
```

**Submissions/Analytics (`/api/submissions`):**
```
POST   /api/submissions               - Submit form (public endpoint - no auth)
GET    /api/submissions               - List company's submissions (filtered)
GET    /api/submissions/{id}          - Get submission details
GET    /api/submissions/export        - Export submissions as CSV (Salesforce, etc.)
DELETE /api/submissions/{id}          - Delete preview submissions only
```

**WebSocket (`/ws/analytics/{eventId}`):**
```
WS     /ws/analytics/{eventId}        - Real-time lead count updates
```

**Activity Log (`/api/activity`):**
```
GET    /api/activity                  - List company's activity log (audit trail)
GET    /api/activity/{entityType}/{entityId}  - Get activity for specific entity
```

**Templates (`/api/templates`):**
```
GET    /api/templates                 - List available templates (platform-wide)
GET    /api/templates/{id}            - Get template design
POST   /api/forms/{id}/apply-template - Apply template to form
```

---

### Request/Response Format Standards

**Standard Success Response:**
```json
// Single resource
{
  "formId": 123,
  "formName": "Lead Capture",
  "status": "published",
  "createdDate": "2025-10-12T14:23:45Z"
}

// List response (paginated)
{
  "data": [
    {"formId": 123, "formName": "..."},
    {"formId": 124, "formName": "..."}
  ],
  "total": 45,
  "page": 1,
  "pageSize": 20,
  "totalPages": 3
}
```

**Standard Error Response:**
```json
{
  "error": "Validation failed",
  "message": "Form name is required",
  "code": "VALIDATION_ERROR",
  "details": {
    "field": "formName",
    "constraint": "required"
  },
  "requestId": "req-abc123"  // For support/debugging
}
```

**HTTP Status Codes Used:**
```
200 OK                - Successful GET, PUT, PATCH
201 Created           - Successful POST (resource created)
204 No Content        - Successful DELETE
400 Bad Request       - Validation error, malformed request
401 Unauthorized      - Missing or invalid JWT token
403 Forbidden         - Valid token, but insufficient permissions (User trying Admin endpoint)
404 Not Found         - Resource doesn't exist or doesn't belong to company (multi-tenant filtering)
409 Conflict          - Business rule violation (e.g., "Cannot publish without 5 tests")
422 Unprocessable     - Semantic error (valid request, but can't be processed)
500 Internal Server   - Server error (logged with full context)
```

---

### Multi-Tenant API Filtering

**Automatic CompanyID Injection:**

```python
# FastAPI dependency: Extract company from JWT
async def get_current_company(
    current_user: User = Depends(get_current_user)
) -> int:
    return current_user.CompanyID

# Endpoint automatically filtered by company
@router.get("/api/forms")
async def list_forms(
    company_id: int = Depends(get_current_company),
    db: AsyncSession = Depends(get_db)
):
    # EVERY query auto-filtered by CompanyID
    forms = await db.query(Form).filter(Form.CompanyID == company_id).all()
    return forms

# Result: User only sees their company's forms (multi-tenant isolation)
```

**System Admin Bypass (Special Case):**
```python
async def list_forms(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # System admins can see ALL companies (no filter)
    if current_user.Role == "system_admin":
        forms = await db.query(Form).all()
    else:
        forms = await db.query(Form).filter(Form.CompanyID == current_user.CompanyID).all()
    
    return forms
```

---

### Pagination Pattern

**Query Parameters:**
```
GET /api/forms?page=2&pageSize=20&sortBy=createdDate&sortOrder=desc&status=published
```

**Implementation:**
```python
from fastapi import Query

@router.get("/api/forms")
async def list_forms(
    page: int = Query(1, ge=1),  # Default page 1, minimum 1
    page_size: int = Query(20, ge=1, le=100),  # Default 20, max 100
    sort_by: str = Query("createdDate"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    status: Optional[str] = None,  # Optional filter
    company_id: int = Depends(get_current_company),
    db: AsyncSession = Depends(get_db)
):
    # Base query (filtered by company)
    query = db.query(Form).filter(Form.CompanyID == company_id)
    
    # Optional filters
    if status:
        query = query.filter(Form.Status == status)
    
    # Count total (before pagination)
    total = await query.count()
    
    # Sort
    if sort_order == "asc":
        query = query.order_by(asc(getattr(Form, sort_by)))
    else:
        query = query.order_by(desc(getattr(Form, sort_by)))
    
    # Paginate
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    
    forms = await query.all()
    
    return {
        "data": forms,
        "total": total,
        "page": page,
        "pageSize": page_size,
        "totalPages": (total + page_size - 1) // page_size
    }
```

---

### Validation Patterns

**Pydantic Request Schemas:**
```python
from pydantic import BaseModel, Field, validator

class CreateEventRequest(BaseModel):
    eventName: str = Field(..., min_length=3, max_length=255)
    eventType: str = Field(..., regex="^(trade_show|conference|expo|other)$")
    eventStartDate: datetime
    eventEndDate: datetime
    location: Optional[str] = Field(None, max_length=255)
    timezoneName: Optional[str] = "Australia/Sydney"
    
    @validator('eventEndDate')
    def end_after_start(cls, v, values):
        if 'eventStartDate' in values and v < values['eventStartDate']:
            raise ValueError('Event end date must be after start date')
        return v

# Usage in endpoint
@router.post("/api/events")
async def create_event(
    request: CreateEventRequest,  # Automatically validated
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # If validation fails, FastAPI returns 422 with error details
    event = Event(**request.dict(), CompanyID=current_user.CompanyID)
    db.add(event)
    await db.commit()
    return event
```

**Common Validation Rules:**
- Email: RFC 5322 format validation
- ABN: Exactly 11 digits
- Phone: Australian format (+61)
- Dates: ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
- URLs: Valid HTTP/HTTPS format
- File uploads: MIME type, size limits (5MB for images)

---

### Error Handling Strategy

**Global Exception Handler:**
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log full error details
    logger.error(
        "error.exception",
        exception_type=type(exc).__name__,
        message=str(exc),
        stack_trace=traceback.format_exc(),
        endpoint=request.url.path,
        user_id=getattr(request.state, "user_id", None),
        request_id=request.state.request_id
    )
    
    # Return user-friendly error
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "Something went wrong. Our team has been notified.",
            "requestId": request.state.request_id
        }
    )

# Business logic exceptions
class BusinessRuleViolation(Exception):
    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code

@app.exception_handler(BusinessRuleViolation)
async def business_rule_handler(request: Request, exc: BusinessRuleViolation):
    return JSONResponse(
        status_code=409,  # Conflict
        content={
            "error": "Business rule violation",
            "message": exc.message,
            "code": exc.code,
            "requestId": request.state.request_id
        }
    )

# Usage:
if form.PreviewTestCount < company.TestThreshold:
    raise BusinessRuleViolation(
        message=f"Form must be tested {company.TestThreshold} times before publishing",
        code="INSUFFICIENT_TESTS"
    )
```

---

### API Security

**1. JWT Token Security:**
- Tokens signed with HS256 algorithm (shared secret) or RS256 (public/private key)
- Short expiration (1 hour for access tokens)
- Refresh token pattern (future enhancement - Week 12+)
- Token stored in memory (Zustand) + localStorage (reload persistence)

**2. Rate Limiting (Future Enhancement):**
```python
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

# Limit: 100 requests per minute per IP
@router.post("/api/auth/login", dependencies=[Depends(RateLimiter(times=5, minutes=1))])
async def login(...):
    # Prevent brute force attacks
    pass
```

**3. CORS Configuration:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Dev frontend
        "https://eventlead.com",  # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**4. Input Sanitization:**
- Pydantic validates all input types
- SQLAlchemy uses parameterized queries (prevents SQL injection)
- HTML escaping for user-generated content (prevent XSS)

---

### WebSocket API (Real-Time Analytics)

**Connection:**
```typescript
// Frontend: Connect to WebSocket
const ws = new WebSocket(`ws://localhost:8000/ws/analytics/${eventId}?token=${jwtToken}`);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // {type: "lead_submitted", count: 45, formId: 123}
  updateLeadCount(data.count);
};
```

**Backend:**
```python
from fastapi import WebSocket

@app.websocket("/ws/analytics/{event_id}")
async def websocket_analytics(
    websocket: WebSocket,
    event_id: int,
    token: str  # JWT token from query param
):
    # Verify token
    user = verify_jwt(token)
    
    await websocket.accept()
    
    try:
        while True:
            # Send updates when new submission arrives
            message = await submission_queue.get()
            await websocket.send_json({
                "type": "lead_submitted",
                "count": message["count"],
                "formId": message["formId"]
            })
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected", event_id=event_id)
```

---

### API Documentation

**Auto-Generated Docs (FastAPI):**
- **Swagger UI:** `http://localhost:8000/docs` (interactive API testing)
- **ReDoc:** `http://localhost:8000/redoc` (clean documentation)
- **OpenAPI Schema:** `http://localhost:8000/openapi.json` (machine-readable)

**Benefits:**
- Automatic documentation from code
- Interactive testing (send requests from browser)
- Always up-to-date (generated from code)
- No manual documentation needed

---

## Backend Abstraction Layer Architecture

This section defines the critical abstraction layer that isolates database naming conventions from frontend code, enabling independent evolution of each layer while maintaining type safety and developer productivity.

### Design Philosophy

**Core Principle:** Each layer of the application stack should use its native naming convention, with automatic transformation between layers.

```
Database (SQL Server)    →    Backend (Python)    →    Frontend (TypeScript)
PascalCase               →    snake_case          →    camelCase
UserID                   →    user_id             →    userId
FirstName                →    first_name          →    firstName
CompanyName              →    company_name        →    companyName
```

**Why This Matters:**
- ✅ **Database refactoring never breaks frontend** - Change column names without touching frontend code
- ✅ **Each layer uses its own convention** - SQL Server standards, Python PEP 8, JavaScript conventions
- ✅ **Type-safe at every layer** - SQLAlchemy ORM + Pydantic validation + TypeScript types
- ✅ **Clean separation of concerns** - Clear boundaries between persistence, business logic, and presentation
- ✅ **Better developer experience** - No mixing of naming conventions in any single file

---

### The Problem Without Abstraction

**Without proper abstraction:**

```python
# BAD: Database naming leaked into API response
@router.get("/api/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.UserID == id).first()
    return {
        "UserID": user.UserID,           # ❌ SQL naming in JSON response
        "FirstName": user.FirstName,     # ❌ Frontend gets PascalCase
        "EmailAddress": user.Email       # ❌ Tight coupling to database
    }
```

```typescript
// BAD: Frontend coupled to database schema
const userName = user.FirstName + " " + user.LastName;  // ❌ SQL naming in JavaScript
const email = user.EmailAddress;                         // ❌ Inconsistent with JS conventions

// If you rename database column, frontend breaks! 🚨
```

**Problems:**
- ❌ Frontend tightly coupled to database schema
- ❌ Database refactoring requires frontend changes
- ❌ Inconsistent naming conventions across codebase
- ❌ Violates separation of concerns principle
- ❌ Poor developer experience (cognitive load of switching conventions)

---

### The Solution: 3-Layer Abstraction

**Layer 1: SQLAlchemy Models (Database → Python)**

Map SQL Server columns (PascalCase) to Python properties (snake_case):

```python
# backend/models/user.py
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """
    SQLAlchemy model - Maps SQL Server columns to Python properties
    Database columns: PascalCase (UserID, FirstName)
    Python properties: snake_case (user_id, first_name)
    """
    __tablename__ = 'User'
    __table_args__ = {'schema': 'dbo'}
    
    # Column name mapping: python_property = Column('SQLServerColumnName', ...)
    user_id = Column('UserID', BigInteger, primary_key=True, autoincrement=True)
    email = Column('Email', String(255), nullable=False, unique=True)
    password_hash = Column('PasswordHash', String(500), nullable=False)
    
    # Profile fields
    first_name = Column('FirstName', String(100), nullable=False)
    last_name = Column('LastName', String(100), nullable=False)
    phone = Column('Phone', String(20), nullable=True)
    role_title = Column('RoleTitle', String(100), nullable=True)
    profile_picture_url = Column('ProfilePictureUrl', String(500), nullable=True)
    timezone_identifier = Column('TimezoneIdentifier', String(50), nullable=False, default='Australia/Sydney')
    
    # Status & account state
    status_id = Column('StatusID', BigInteger, nullable=False)
    is_email_verified = Column('IsEmailVerified', Boolean, nullable=False, default=False)
    email_verified_at = Column('EmailVerifiedAt', DateTime, nullable=True)
    is_locked = Column('IsLocked', Boolean, nullable=False, default=False)
    locked_until = Column('LockedUntil', DateTime, nullable=True)
    
    # Session management
    session_token = Column('SessionToken', String(255), nullable=True)
    access_token_version = Column('AccessTokenVersion', Integer, nullable=False, default=1)
    refresh_token_version = Column('RefreshTokenVersion', Integer, nullable=False, default=1)
    
    # Audit trail
    created_date = Column('CreatedDate', DateTime, nullable=False, default=datetime.utcnow)
    created_by = Column('CreatedBy', BigInteger, nullable=True)
    updated_date = Column('UpdatedDate', DateTime, nullable=False, default=datetime.utcnow)
    updated_by = Column('UpdatedBy', BigInteger, nullable=True)
    is_deleted = Column('IsDeleted', Boolean, nullable=False, default=False)
    deleted_date = Column('DeletedDate', DateTime, nullable=True)
    deleted_by = Column('DeletedBy', BigInteger, nullable=True)
```

**Key Benefits:**
- Python code uses Pythonic `user.user_id`, `user.first_name` (snake_case)
- Database stores in `UserID`, `FirstName` columns (PascalCase)
- SQLAlchemy handles translation automatically
- No SQL naming conventions visible in Python code

---

**Layer 2: Pydantic Schemas (Python → JSON API)**

Auto-convert Python properties (snake_case) to JSON fields (camelCase):

```python
# backend/modules/auth/schemas.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional

def to_camel_case(string: str) -> str:
    """Convert snake_case to camelCase"""
    components = string.split('_')
    return components[0] + ''.join(x.capitalize() for x in components[1:])

# Reusable config for all schemas
CamelCaseConfig = ConfigDict(
    alias_generator=to_camel_case,
    populate_by_name=True,  # Allow both camelCase and snake_case
    from_attributes=True    # Allow ORM model conversion
)

class UserResponse(BaseModel):
    """API Response Schema - Outputs camelCase for frontend"""
    model_config = CamelCaseConfig
    
    # Define fields in Python snake_case
    # API outputs them in camelCase automatically
    user_id: int = Field(..., description="Unique user identifier")
    email: EmailStr = Field(..., description="User email address")
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    role_title: Optional[str] = Field(None, max_length=100)
    profile_picture_url: Optional[str] = Field(None, max_length=500)
    timezone_identifier: str = Field(default='Australia/Sydney')
    
    is_email_verified: bool = Field(..., description="Email verification status")
    email_verified_at: Optional[datetime] = None
    is_locked: bool = Field(..., description="Account lock status")
    
    onboarding_complete: bool
    onboarding_step: int = Field(..., ge=1)
    
    created_date: datetime
    last_login_date: Optional[datetime] = None


class UserCreateRequest(BaseModel):
    """API Request Schema - Accepts camelCase from frontend"""
    model_config = CamelCaseConfig
    
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    timezone_identifier: str = Field(default='Australia/Sydney')


class UserUpdateRequest(BaseModel):
    """API Update Schema - Partial updates with camelCase"""
    model_config = CamelCaseConfig
    
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    role_title: Optional[str] = Field(None, max_length=100)
    profile_picture_url: Optional[str] = Field(None, max_length=500)
    timezone_identifier: Optional[str] = None
```

**API Response Example:**
```json
{
  "userId": 123,
  "email": "john@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "isEmailVerified": true,
  "emailVerifiedAt": "2025-10-16T10:30:00Z",
  "onboardingComplete": true,
  "createdDate": "2025-10-01T08:15:00Z"
}
```

**Key Benefits:**
- Frontend receives camelCase (JavaScript convention)
- Python code still uses snake_case (PEP 8 convention)
- Automatic conversion via `alias_generator`
- Type safety with Pydantic validation

---

**Layer 3: Service Layer (Business Logic)**

Clean Python code with snake_case throughout:

```python
# backend/modules/auth/service.py
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.modules.auth.schemas import UserResponse, UserCreateRequest
from backend.common.security import hash_password
from datetime import datetime
from typing import Optional

class UserService:
    """Service layer - Business logic with Pythonic naming"""
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreateRequest) -> UserResponse:
        """Create new user - Notice clean Python naming throughout"""
        # Hash password
        password_hash = hash_password(user_data.password)
        
        # Create SQLAlchemy model (Python snake_case)
        new_user = User(
            email=user_data.email,
            password_hash=password_hash,
            first_name=user_data.first_name,      # ✅ Python snake_case
            last_name=user_data.last_name,
            phone=user_data.phone,
            timezone_identifier=user_data.timezone_identifier,
            status_id=2,  # 'pending' status
            is_email_verified=False,
            onboarding_complete=False,
            onboarding_step=1,
            created_date=datetime.utcnow()
        )
        
        # Save to database (SQLAlchemy maps to PascalCase columns)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Return Pydantic schema (converts to camelCase for API)
        return UserResponse.model_validate(new_user)
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[UserResponse]:
        """Get user by ID - Notice Python naming in code"""
        user = db.query(User).filter(User.user_id == user_id).first()
        
        if user:
            return UserResponse.model_validate(user)
        return None
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdateRequest) -> Optional[UserResponse]:
        """Update user - Notice Python naming throughout"""
        user = db.query(User).filter(User.user_id == user_id).first()
        
        if not user:
            return None
        
        # Update fields (Python snake_case)
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        user.updated_date = datetime.utcnow()
        
        db.commit()
        db.refresh(user)
        
        return UserResponse.model_validate(user)
```

**Key Benefits:**
- All Python code uses snake_case (PEP 8)
- No SQL naming conventions visible
- Clean, Pythonic code
- Database mapping handled by SQLAlchemy layer

---

**Layer 4: API Router (HTTP Endpoints)**

```python
# backend/modules/auth/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.common.database import get_db
from backend.modules.auth.schemas import UserResponse, UserCreateRequest, UserUpdateRequest
from backend.modules.auth.service import UserService

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreateRequest, db: Session = Depends(get_db)):
    """
    Create new user
    
    Request (camelCase from frontend):
    {
      "email": "john@example.com",
      "password": "SecurePass123!",
      "firstName": "John",
      "lastName": "Doe",
      "phone": "+61412345678",
      "timezoneIdentifier": "Australia/Sydney"
    }
    
    Response (camelCase to frontend):
    {
      "userId": 123,
      "email": "john@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "isEmailVerified": false,
      "onboardingComplete": false,
      "createdDate": "2025-10-16T10:30:00Z"
    }
    """
    return UserService.create_user(db, user_data)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID - Returns camelCase to frontend"""
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdateRequest, db: Session = Depends(get_db)):
    """Update user profile - Accepts camelCase from frontend"""
    user = UserService.update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
```

---

### Frontend Consumption

**TypeScript Types (Auto-generated from Pydantic):**

```typescript
// frontend/src/types/user.ts
/**
 * User type - camelCase (JavaScript convention)
 * Matches backend UserResponse schema
 */
export interface User {
  userId: number;
  email: string;
  firstName: string;
  lastName: string;
  phone: string | null;
  roleTitle: string | null;
  profilePictureUrl: string | null;
  timezoneIdentifier: string;
  isEmailVerified: boolean;
  emailVerifiedAt: string | null;
  isLocked: boolean;
  lockedUntil: string | null;
  onboardingComplete: boolean;
  onboardingStep: number;
  createdDate: string;
  lastLoginDate: string | null;
}

export interface CreateUserRequest {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  phone?: string;
  timezoneIdentifier?: string;
}

export interface UpdateUserRequest {
  firstName?: string;
  lastName?: string;
  phone?: string;
  roleTitle?: string;
  profilePictureUrl?: string;
  timezoneIdentifier?: string;
}
```

**React Component:**

```typescript
// frontend/src/features/auth/UserProfile.tsx
import React, { useEffect, useState } from 'react';
import { User } from '@/types/user';
import { api } from '@/lib/api';

export const UserProfile: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  
  useEffect(() => {
    // Fetch user from API (receives camelCase)
    api.get<User>('/api/v1/users/123')
      .then(response => {
        setUser(response.data);
        
        // Notice: Clean JavaScript naming, no SQL conventions!
        console.log('User ID:', response.data.userId);
        console.log('Full Name:', `${response.data.firstName} ${response.data.lastName}`);
        console.log('Email Verified:', response.data.isEmailVerified);
      });
  }, []);
  
  if (!user) return <div>Loading...</div>;
  
  return (
    <div className="profile-card">
      <img src={user.profilePictureUrl || '/default-avatar.png'} alt="Profile" />
      
      <h2>{user.firstName} {user.lastName}</h2>
      
      {user.roleTitle && <p className="role-title">{user.roleTitle}</p>}
      
      <p className="email">{user.email}</p>
      
      {user.isEmailVerified ? (
        <span className="badge badge-success">✓ Email Verified</span>
      ) : (
        <span className="badge badge-warning">⚠ Email Not Verified</span>
      )}
      
      <div className="onboarding-progress">
        <p>Onboarding: Step {user.onboardingStep}</p>
        {user.onboardingComplete && <span>✅ Complete</span>}
      </div>
    </div>
  );
};
```

---

### Data Flow Summary

```
┌──────────────────────────────────────────────────────────────────┐
│                   DATA TRANSFORMATION FLOW                        │
└──────────────────────────────────────────────────────────────────┘

Database (SQL Server):
  Column: UserID (PascalCase)
  Storage: BIGINT IDENTITY(1,1)
      ↓
SQLAlchemy Model (Python):
  Property: user_id (snake_case)
  Mapping: user_id = Column('UserID', BigInteger)
  Code: user = db.query(User).filter(User.user_id == 123).first()
      ↓
Service Layer (Python):
  Variable: user.user_id (snake_case)
  Code: new_user = User(first_name=data.first_name, ...)
      ↓
Pydantic Schema (JSON API):
  Field: userId (camelCase)
  Alias: alias_generator converts snake_case → camelCase
  Response: {"userId": 123, "firstName": "John"}
      ↓
Frontend (TypeScript):
  Property: user.userId (camelCase)
  Code: console.log(user.userId, user.firstName)
```

---

### Benefits of This Architecture

**1. Separation of Concerns**
- ✅ Database schema changes don't affect frontend
- ✅ Each layer uses its own naming convention
- ✅ Clear boundaries between persistence, logic, and presentation

**2. Flexibility**
- ✅ Rename database columns without breaking frontend
- ✅ Change API response format without database migration
- ✅ Support multiple API versions with different naming

**3. Developer Experience**
- ✅ Backend developers use Pythonic snake_case
- ✅ Frontend developers use JavaScript camelCase
- ✅ Database follows SQL Server standards (PascalCase)
- ✅ No mixing of conventions in any single layer

**4. Maintainability**
- ✅ Each layer is independently testable
- ✅ Clear transformation rules at layer boundaries
- ✅ Type safety at every layer (SQLAlchemy + Pydantic + TypeScript)

**5. Compliance with Standards**
- ✅ Database: SQL Server naming standards (Anthony's rules - PascalCase)
- ✅ Python: PEP 8 naming conventions (snake_case)
- ✅ JavaScript/TypeScript: Industry standard (camelCase)
- ✅ REST API: JSON convention (camelCase)

---

### Implementation Checklist

**For Each Database Table:**

1. **Create SQLAlchemy model** with column name mapping
   ```python
   user_id = Column('UserID', BigInteger, primary_key=True)
   first_name = Column('FirstName', String(100), nullable=False)
   is_email_verified = Column('IsEmailVerified', Boolean, default=False)
   ```

2. **Create Pydantic response schema** with camelCase alias
   ```python
   class UserResponse(BaseModel):
       model_config = CamelCaseConfig
       user_id: int      # API outputs: "userId"
       first_name: str   # API outputs: "firstName"
   ```

3. **Create Pydantic request schema** for API input
   ```python
   class UserCreateRequest(BaseModel):
       model_config = CamelCaseConfig
       email: EmailStr
       first_name: str  # API accepts: "firstName"
   ```

4. **Create service layer methods** with Python naming
   ```python
   def create_user(db: Session, user_data: UserCreateRequest) -> UserResponse:
       new_user = User(first_name=user_data.first_name)
       # All code uses snake_case
   ```

5. **Create API routes** with proper response models
   ```python
   @router.post("/users", response_model=UserResponse)
   def create_user(user_data: UserCreateRequest):
       return UserService.create_user(db, user_data)
   ```

6. **Generate TypeScript types** from Pydantic schemas
   ```bash
   # Use pydantic2ts or similar tool
   pydantic2ts --module backend.modules.auth.schemas --output frontend/src/types/
   ```

---

### Naming Convention Reference

| Layer | Convention | Example | When to Use |
|-------|-----------|---------|-------------|
| **SQL Server** | PascalCase | `UserID`, `FirstName`, `CompanyName` | Table/column definitions, constraints |
| **SQLAlchemy** | snake_case | `user_id`, `first_name`, `company_name` | Python model properties, queries |
| **Pydantic** | snake_case | `user_id: int`, `first_name: str` | Schema field definitions (internal) |
| **JSON API** | camelCase | `{"userId": 123, "firstName": "John"}` | API request/response bodies |
| **TypeScript** | camelCase | `user.userId`, `user.firstName` | Frontend code, React components |
| **URL Params** | kebab-case | `/api/users/user-id` | REST API endpoints (optional) |

---

## Security Architecture

This section defines the comprehensive security strategy for EventLeadPlatform, covering authentication, authorization, session management, data protection, and threat mitigation.

### Security Design Philosophy

**Core Principles:**
1. **Defense in Depth:** Multiple layers of security (application, middleware, database)
2. **Least Privilege:** Users only access what they need for their role
3. **Secure by Default:** Security controls enabled out of the box
4. **Fail Securely:** Security failures deny access, not grant it
5. **Audit Everything:** Complete trail of authentication and authorization events

---

### Authentication & Session Management

**JWT-Based Authentication:**

**Token Strategy:**
```
Access Token:  Short-lived (15 minutes), used for API requests
Refresh Token: Long-lived (7 days), used to get new access tokens
Session Token: User-specific, invalidates all tokens when rotated
```

**Token Structure:**
```json
// Access Token (JWT)
{
  "sub": 123,                    // User ID (subject)
  "company_id": 456,              // Current company
  "role": "company_admin",        // User role for authorization
  "email": "user@example.com",
  "session_token": "abc123...",   // Current session identifier
  "token_version": 1,             // Token version for invalidation
  "exp": 1697865600,              // Expiration (15 minutes from now)
  "iat": 1697862000               // Issued at timestamp
}
```

**Session Management Features:**

**1. Token Versioning (Logout All Devices)**
```python
# Stored in User table
class User:
    session_token: str                    # Current session identifier
    access_token_version: int = 1         // Increment to invalidate all access tokens
    refresh_token_version: int = 1        // Increment to invalidate all refresh tokens

# Token validation
def validate_token(token: str, user: User) -> bool:
    claims = jwt.decode(token)
    
    # Check session token matches current session
    if claims['session_token'] != user.session_token:
        return False  # User logged out or password reset
    
    # Check token version matches current version
    if claims['token_version'] != user.access_token_version:
        return False  # All tokens invalidated (security event)
    
    return True
```

**Use Cases:**
- **Password Reset:** Increment `session_token` + both version numbers → All devices logged out
- **Logout All Devices:** User clicks "Log out everywhere" → Increment `session_token`
- **Security Event:** Suspicious activity detected → Increment `access_token_version`

**2. Email Verification**
```sql
-- EmailVerificationToken table
CREATE TABLE [dbo].[UserEmailVerificationToken] (
    UserEmailVerificationTokenID BIGINT PRIMARY KEY,
    UserID BIGINT NOT NULL,
    Token NVARCHAR(500) NOT NULL UNIQUE,  -- Cryptographically secure random token
    ExpiresAt DATETIME2 NOT NULL,         -- 24-hour expiry
    IsUsed BIT NOT NULL DEFAULT 0,
    UsedAt DATETIME2 NULL,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE()
);
```

**Flow:**
1. User signs up → `IsEmailVerified = false`
2. System generates secure token, sends email
3. User clicks link → Token validated → `IsEmailVerified = true`
4. User can now login

**3. Password Reset**
```sql
-- PasswordResetToken table
CREATE TABLE [dbo].[UserPasswordResetToken] (
    UserPasswordResetTokenID BIGINT PRIMARY KEY,
    UserID BIGINT NOT NULL,
    Token NVARCHAR(500) NOT NULL UNIQUE,  -- Cryptographically secure
    ExpiresAt DATETIME2 NOT NULL,         -- 1-hour expiry (shorter than email verification)
    IsUsed BIT NOT NULL DEFAULT 0,
    UsedAt DATETIME2 NULL,
    IPAddress NVARCHAR(50) NULL,          -- Track where reset was requested
    UserAgent NVARCHAR(500) NULL,         -- Track device/browser
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE()
);
```

**Flow:**
1. User forgets password → Requests reset
2. System generates secure token (1-hour expiry), sends email
3. User clicks link → Provides new password
4. System validates token → Updates password → Increments `session_token` → All devices logged out

---

### Authorization & Role-Based Access Control (RBAC)

**Three-Role System:**

| Role | Scope | Capabilities | Implementation |
|------|-------|--------------|----------------|
| **System Admin** | Platform-wide | Manage all companies, access all data, configure system | `User.UserRoleID` (system-level role) |
| **Company Admin** | Single company | Manage company, invite users, publish forms, view all company data | `UserCompany.UserCompanyRoleID = 'company_admin'` |
| **Company User** | Single company | Create forms, request publish approval, view own data | `UserCompany.UserCompanyRoleID = 'company_user'` |

**Authorization Middleware:**
```python
# FastAPI dependency
def require_role(required_role: str):
    async def dependency(current_user: User = Depends(get_current_user)):
        # Extract role from JWT token (already validated)
        if current_user.role != required_role and current_user.role != "system_admin":
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return dependency

# Usage
@router.post("/api/team/invite")
async def invite_user(
    invitation_data: InvitationRequest,
    current_user: User = Depends(require_role("company_admin"))  # Only admins can invite
):
    # ... invitation logic
```

**Multi-Tenant Data Isolation:**
```python
# EVERY query automatically filtered by company
async def get_current_company(current_user: User = Depends(get_current_user)) -> int:
    return current_user.company_id  # From JWT token

@router.get("/api/forms")
async def list_forms(
    company_id: int = Depends(get_current_company),
    db: Session = Depends(get_db)
):
    # Automatic company filtering
    forms = db.query(Form).filter(Form.company_id == company_id).all()
    return forms
```

**Database-Level Security (SQL Server Row-Level Security):**
```sql
-- Create security function (checks session context)
CREATE FUNCTION dbo.fn_TenantAccessPredicate(@CompanyID BIGINT)
RETURNS TABLE
AS RETURN
    SELECT 1 AS AccessAllowed
    WHERE @CompanyID = CAST(SESSION_CONTEXT(N'CompanyID') AS BIGINT)
    OR CAST(SESSION_CONTEXT(N'Role') AS NVARCHAR(50)) = 'system_admin';

-- Apply security policy to Form table
CREATE SECURITY POLICY FormSecurityPolicy
ADD FILTER PREDICATE dbo.fn_TenantAccessPredicate(CompanyID)
ON dbo.Form
WITH (STATE = ON);
```

**Defense in Depth:**
- Layer 1: Application (FastAPI dependency injection)
- Layer 2: ORM (SQLAlchemy automatic filtering)
- Layer 3: Database (SQL Server RLS policies)

---

### Password Security

**Password Policies:**
- Minimum length: 8 characters (configurable via `AppSetting`)
- Character requirements (configurable):
  - Uppercase letter (optional)
  - Lowercase letter (optional)
  - Number (optional)
  - Special character (optional)
- No common passwords (e.g., "password123")
- Password history: Cannot reuse last 3 passwords (future enhancement)

**Password Hashing:**
```python
# bcrypt with salt rounds = 12
import bcrypt

def hash_password(plain_password: str) -> str:
    """Hash password using bcrypt (industry standard)"""
    salt = bcrypt.gensalt(rounds=12)  # Higher = more secure, slower
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )
```

**Why bcrypt?**
- ✅ Designed for password hashing (slow by design)
- ✅ Built-in salt generation
- ✅ Adaptive (can increase rounds as hardware improves)
- ✅ Industry standard (OWASP recommended)

**Failed Login Protection:**
```python
# Track failed attempts in User table
class User:
    failed_login_attempts: int = 0
    locked_until: datetime | None = None
    is_locked: bool = False

# Login logic
async def login(email: str, password: str):
    user = await get_user_by_email(email)
    
    # Check if account is locked
    if user.is_locked and user.locked_until > datetime.utcnow():
        raise HTTPException(status_code=423, detail="Account locked. Try again later.")
    
    # Verify password
    if not verify_password(password, user.password_hash):
        # Increment failed attempts
        user.failed_login_attempts += 1
        
        # Lock after 5 failed attempts
        if user.failed_login_attempts >= 5:
            user.is_locked = True
            user.locked_until = datetime.utcnow() + timedelta(minutes=15)
            await send_security_alert(user.email, "Account locked due to failed login attempts")
        
        await db.commit()
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Successful login - reset counter
    user.failed_login_attempts = 0
    user.is_locked = False
    user.locked_until = None
    await db.commit()
    
    return generate_tokens(user)
```

---

### API Security

**Rate Limiting:**
```python
# Rate limit configuration (per IP address)
RATE_LIMITS = {
    "/api/auth/login": "5/minute",         # Max 5 login attempts per minute
    "/api/auth/signup": "3/hour",          # Max 3 signups per hour
    "/api/auth/forgot-password": "3/hour", # Max 3 password reset requests per hour
    "/api/*": "100/minute"                 # General API limit
}

# Implementation using SlowAPI (FastAPI middleware)
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/api/auth/login")
@limiter.limit("5/minute")
async def login(request: Request, credentials: LoginRequest):
    # ... login logic
```

**CORS (Cross-Origin Resource Sharing):**
```python
# Production configuration
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://app.eventlead.com",      # Production frontend
        "https://forms.eventlead.com"     # Public form hosting
    ],
    allow_credentials=True,               # Allow cookies/auth headers
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["X-Total-Count"],     # For pagination
    max_age=3600                          // Cache preflight requests
)

# Development configuration
if settings.ENVIRONMENT == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],  # Vite dev server
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
```

**SQL Injection Prevention:**
```python
# ✅ CORRECT: Parameterized queries (SQLAlchemy ORM)
user = db.query(User).filter(User.email == user_email).first()

# ✅ CORRECT: Parameterized raw SQL
result = db.execute(
    text("SELECT * FROM User WHERE Email = :email"),
    {"email": user_email}
)

# ❌ WRONG: String concatenation (SQL injection risk)
query = f"SELECT * FROM User WHERE Email = '{user_email}'"  # NEVER DO THIS
```

**Input Validation:**
```python
# Pydantic models enforce validation
class SignupRequest(BaseModel):
    email: EmailStr                                   # Valid email format
    password: str = Field(min_length=8, max_length=100)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    
    @validator('email')
    def email_must_not_be_temp(cls, v):
        """Reject temporary email providers"""
        temp_domains = ['tempmail.com', 'guerrillamail.com']
        if any(domain in v for domain in temp_domains):
            raise ValueError('Temporary email addresses not allowed')
        return v
```

---

### Data Protection

**Encryption:**

**1. Data in Transit (TLS/HTTPS)**
- All API requests over HTTPS (TLS 1.2+)
- HTTP Strict Transport Security (HSTS) header
- Azure Front Door or CloudFlare for TLS termination

**2. Data at Rest**
- Database: Transparent Data Encryption (TDE) in SQL Server
- File Storage: Azure Blob Storage encryption (Microsoft-managed keys)
- Backups: Encrypted before upload to backup storage

**3. Sensitive Data**
```python
# Password hashing (bcrypt)
password_hash = bcrypt.hashpw(plain_password, salt)

# JWT tokens (HMAC-SHA256 signature)
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# IP address hashing (privacy compliance)
hashed_ip = hashlib.sha256(ip_address.encode()).hexdigest()[:16]
```

**Audit Trail:**
```sql
-- ActivityLog tracks all user actions
CREATE TABLE [audit].[ActivityLog] (
    ActivityLogID BIGINT PRIMARY KEY,
    UserID BIGINT NOT NULL,
    CompanyID BIGINT NOT NULL,
    Action NVARCHAR(100) NOT NULL,       -- 'user.login', 'form.publish', 'team.invite'
    EntityType NVARCHAR(50) NULL,        -- 'Form', 'User', 'Company'
    EntityID BIGINT NULL,                -- ID of affected entity
    IPAddress NVARCHAR(50) NOT NULL,     -- Hashed IP for privacy
    UserAgent NVARCHAR(500) NULL,        -- Browser/device info
    RequestID NVARCHAR(100) NULL,        -- Correlation ID for debugging
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE()
);
```

**Compliance:**
- ✅ GDPR (EU): Right to access, right to erasure, data portability
- ✅ Australian Privacy Principles: Consent, security, access, correction
- ✅ Data retention: 7 years for audit logs (compliance requirement)

---

### Threat Mitigation

**Common Threats & Mitigations:**

| Threat | Mitigation | Implementation |
|--------|-----------|----------------|
| **SQL Injection** | Parameterized queries | SQLAlchemy ORM (never raw SQL string concatenation) |
| **XSS (Cross-Site Scripting)** | Input sanitization, CSP headers | React escapes by default, Content-Security-Policy header |
| **CSRF (Cross-Site Request Forgery)** | JWT tokens in headers (not cookies) | Authorization: Bearer token (not cookie-based auth) |
| **Brute Force Login** | Rate limiting + account lockout | 5 attempts → 15-minute lockout + rate limit (5/minute) |
| **Session Hijacking** | Short-lived tokens + HTTPS only | 15-minute access tokens, secure transport |
| **Privilege Escalation** | RBAC + multi-layer authorization | FastAPI dependencies + SQL RLS + audit logging |
| **Data Breach** | Multi-tenant isolation + RLS | Company filtering at every layer + database policies |
| **DDoS** | Rate limiting + CDN | CloudFlare/Azure Front Door + API rate limits |

**Security Headers:**
```python
# FastAPI middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    
    # Prevent clickjacking
    response.headers["X-Frame-Options"] = "DENY"
    
    # Prevent MIME sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"
    
    # XSS protection
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    # Content Security Policy
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:;"
    )
    
    # HSTS (force HTTPS)
    if request.url.scheme == "https":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    return response
```

---

### Security Monitoring & Incident Response

**Logging Security Events:**
```python
# Log all authentication events
logger.info(
    "auth.login.success",
    user_id=user.user_id,
    company_id=user.company_id,
    ip_address=hashed_ip,
    user_agent=request.headers.get("User-Agent")
)

logger.warning(
    "auth.login.failed",
    email=email,
    ip_address=hashed_ip,
    reason="invalid_password",
    failed_attempts=user.failed_login_attempts
)

logger.critical(
    "auth.account.locked",
    user_id=user.user_id,
    failed_attempts=5,
    locked_until=user.locked_until
)
```

**Alerting:**
- Failed login spike (>10 failures in 1 minute) → Alert security team
- Account lockout → Email user + security team
- Suspicious activity (multiple IP addresses, unusual access patterns) → Flag for review
- Database query performance degradation → May indicate SQL injection attempt

**Incident Response:**
1. **Detection:** Automated alerts + log monitoring
2. **Containment:** Lock affected accounts, revoke tokens
3. **Investigation:** Analyze logs, identify scope
4. **Recovery:** Reset credentials, patch vulnerabilities
5. **Post-Mortem:** Document incident, update security controls

---

### Security Checklist (Development)

**Every API Endpoint MUST:**
- [ ] Require authentication (JWT token validation)
- [ ] Enforce authorization (role check)
- [ ] Filter by `CompanyID` (multi-tenant isolation)
- [ ] Validate input (Pydantic schemas)
- [ ] Use parameterized queries (no raw SQL)
- [ ] Log security events (authentication, authorization failures)
- [ ] Return appropriate HTTP status codes (401, 403, 404)
- [ ] Not expose sensitive data in error messages

**Every Database Table MUST:**
- [ ] Have `CompanyID` column (if tenant-specific)
- [ ] Have audit columns (`CreatedDate`, `CreatedBy`, etc.)
- [ ] Use soft delete (`IsDeleted` flag, not hard delete)
- [ ] Have appropriate indexes (performance)
- [ ] Enforce referential integrity (foreign keys)

---

## Proposed Source Tree Structure

**Monorepo Structure (Single Repository):**

```
eventlead-platform/
├── frontend/                          # React SPA
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/                # Shared UI components
│   │   │   ├── common/               # Button, Input, Card, Modal
│   │   │   ├── layout/               # Header, Sidebar, Footer
│   │   │   └── forms/                # FormField, FormLabel, FormError
│   │   ├── features/                  # Feature-specific components (by Epic)
│   │   │   ├── auth/                 # Login, Signup, OnboardingForm
│   │   │   ├── events/               # EventList, EventCard, CreateEventModal
│   │   │   ├── forms/                # FormBuilder (Epic 5 - largest feature)
│   │   │   │   ├── components/       # Canvas, ComponentPalette, PropertiesPanel
│   │   │   │   ├── renderers/        # FreeformRenderer, GridRenderer
│   │   │   │   ├── hooks/            # useFormBuilder, useAutoSave, useUndo
│   │   │   │   └── types/            # FormComponent, FormState, RendererConfig
│   │   │   ├── analytics/            # Dashboard, LeadsList, ExportButton
│   │   │   ├── team/                 # TeamList, InviteModal
│   │   │   └── payments/             # PaymentModal, InvoiceList
│   │   ├── lib/                       # Utilities and helpers
│   │   │   ├── api/                  # API client (Axios setup, interceptors)
│   │   │   ├── hooks/                # Custom React hooks (useAuth, useCompany)
│   │   │   ├── utils/                # Date formatting, validation, helpers
│   │   │   └── constants/            # API URLs, config values
│   │   ├── store/                     # Zustand state management
│   │   │   ├── authStore.ts          # User, token, login/logout
│   │   │   ├── companyStore.ts       # Company context
│   │   │   ├── formBuilderStore.ts   # Form builder state
│   │   │   └── index.ts              # Export all stores
│   │   ├── pages/                     # Route components
│   │   │   ├── Auth/                 # Login.tsx, Signup.tsx
│   │   │   ├── Onboarding/           # CompanySetup.tsx
│   │   │   ├── Dashboard/            # Dashboard.tsx
│   │   │   ├── Events/               # EventsPage.tsx, EventDetails.tsx
│   │   │   ├── Forms/                # FormsPage.tsx, FormBuilder.tsx
│   │   │   ├── Analytics/            # AnalyticsPage.tsx
│   │   │   └── Settings/             # SettingsPage.tsx, TeamPage.tsx
│   │   ├── App.tsx                    # Root component, routing
│   │   ├── main.tsx                   # Entry point
│   │   └── index.css                  # Tailwind CSS imports
│   ├── package.json                   # Frontend dependencies
│   ├── tsconfig.json                  # TypeScript configuration
│   ├── vite.config.ts                 # Vite build configuration
│   └── tailwind.config.js             # Tailwind CSS configuration
│
├── backend/                           # FastAPI Python backend
│   ├── main.py                        # FastAPI application entry point
│   ├── config.py                      # Environment configuration
│   ├── database.py                    # SQLAlchemy setup, connection pool
│   ├── models/                        # SQLAlchemy ORM models (database tables)
│   │   ├── base.py                   # Base class (PascalCase config)
│   │   ├── user.py                   # User model
│   │   ├── company.py                # Company model
│   │   ├── event.py                  # Event model
│   │   ├── form.py                   # Form model
│   │   ├── submission.py             # Submission model
│   │   ├── payment.py                # Payment model
│   │   ├── invoice.py                # Invoice model
│   │   ├── image.py                  # Image model
│   │   ├── invitation.py             # Invitation model
│   │   ├── activity_log.py           # ActivityLog model
│   │   └── __init__.py               # Export all models
│   ├── modules/                       # Business logic modules (by Epic)
│   │   ├── auth/                     # Epic 1: Authentication
│   │   │   ├── routes.py             # Auth endpoints
│   │   │   ├── schemas.py            # Pydantic request/response schemas
│   │   │   ├── services/             # Business logic
│   │   │   │   ├── auth_service.py   # Login, signup, token generation
│   │   │   │   └── email_service.py  # Verification emails
│   │   │   └── dependencies.py       # get_current_user, require_role
│   │   ├── companies/                # Epic 2: Company Management
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   │   │   └── services/
│   │   │       └── company_service.py
│   │   ├── events/                   # Epic 3: Events
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   │   │   └── services/
│   │   │       └── event_service.py
│   │   ├── team/                     # Epic 4: Team Management
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   │   │   └── services/
│   │   │       ├── team_service.py
│   │   │       └── invitation_service.py
│   │   ├── forms/                    # Epic 5 & 6: Form Builder & Publishing
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   │   │   └── services/
│   │   │       ├── form_service.py
│   │   │       └── publish_service.py
│   │   ├── payments/                 # Epic 7: Payments
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   │   │   └── services/
│   │   │       ├── stripe_service.py
│   │   │       └── invoice_service.py
│   │   ├── analytics/                # Epic 8: Lead Collection & Analytics
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   │   │   └── services/
│   │   │       ├── submission_service.py
│   │   │       └── export_service.py
│   │   ├── images/                   # Image Management
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   │   │   └── services/
│   │   │       ├── upload_service.py
│   │   │       └── optimization_service.py
│   │   └── audit/                    # Epic 9: Audit Trail
│   │       ├── routes.py
│   │       ├── schemas.py
│   │       └── services/
│   │           └── audit_service.py
│   ├── common/                        # Shared infrastructure
│   │   ├── logging/                  # structlog configuration
│   │   │   ├── config.py
│   │   │   └── middleware.py
│   │   ├── middleware/               # FastAPI middleware
│   │   │   ├── auth.py               # JWT verification
│   │   │   ├── tenant.py             # Multi-tenant filtering
│   │   │   ├── cors.py               # CORS configuration
│   │   │   └── error_handler.py      # Global exception handling
│   │   ├── providers/                # Abstraction layers (dev vs prod)
│   │   │   ├── storage/              # StorageProvider interface
│   │   │   │   ├── base.py
│   │   │   │   ├── local.py          # aiofiles (dev)
│   │   │   │   └── azure_blob.py     # Azure Blob Storage (prod)
│   │   │   └── email/                # EmailProvider interface
│   │   │       ├── base.py
│   │   │       ├── mailhog.py        # MailHog (dev)
│   │   │       └── azure_comm.py     # Azure Communication (prod)
│   │   └── utils/                    # Shared utilities
│   │       ├── validators.py         # ABN, phone, email validation
│   │       ├── timezone.py           # UTC conversion helpers
│   │       └── hashing.py            # Password hashing
│   ├── tests/                         # Backend tests
│   │   ├── unit/                     # Unit tests (services, utilities)
│   │   ├── integration/              # Integration tests (API endpoints)
│   │   └── conftest.py               # pytest fixtures
│   ├── requirements.txt               # Backend dependencies
│   └── .env.example                   # Environment variables template
│
├── database/                          # Database management
│   ├── migrations/                    # Alembic migration files
│   │   ├── versions/
│   │   │   ├── 001_initial_schema.py
│   │   │   ├── 002_add_image_table.py
│   │   │   └── ...
│   │   ├── env.py                    # Alembic environment config
│   │   └── script.py.mako            # Migration template (PascalCase)
│   ├── seeds/                         # Seed data scripts
│   │   ├── dev_seed.py               # Development data
│   │   └── prod_seed.py              # Production data (templates)
│   └── scripts/                       # Database utility scripts
│       ├── create_rls_policies.sql   # Row-Level Security setup
│       └── backup.sh                 # Database backup script
│
├── docs/                              # Project documentation
│   ├── prd.md                        # Product Requirements (this file)
│   ├── ux-specification.md           # UX/UI Specification
│   ├── solution-architecture.md      # This document
│   ├── api-reference.md              # API documentation (generated from OpenAPI)
│   └── deployment-guide.md           # Production deployment steps
│
├── .github/                           # GitHub Actions CI/CD
│   └── workflows/
│       └── deploy.yml                # Azure deployment pipeline (Week 21)
│
├── docker-compose.yml                 # Local development environment
├── .gitignore                         # Git ignore rules
├── README.md                          # Project overview and setup
└── package.json                       # Root package.json (optional - for Nx monorepo tools)
```

**Total Structure:**
- Frontend: ~40 files (components, pages, features)
- Backend: ~50 files (modules, models, services)
- Database: ~15 files (migrations, seeds)
- Configuration: ~10 files
- **Total: ~115 source files** (manageable for solo developer)

---

## Implementation Roadmap (Quick Reference)

**Epic Implementation Order:**

```
Week 1-2:   Epic 1 (Auth) → Foundation
Week 2-3:   Epic 2 (Companies) → Multi-tenant setup
Week 3-4:   Epic 3 (Events) → Core domain
Week 4-5:   Epic 4 (Team) → Collaboration
Week 5-14:  Epic 5 (Form Builder) → Complex feature (9 weeks)
Week 15-16: Epic 6 (Publishing) → Activation logic
Week 16-18: Epic 7 (Payments) → Revenue
Week 18-20: Epic 8 (Analytics) → Core value delivery
Week 20-21: Epic 9 (Audit) → Compliance
Week 21:    CI/CD Pipeline → Deployment automation
Week 22:    Production Launch → Go-live

Total: 22 weeks (5.5 months)
```

---

## Architecture Summary

**What We've Defined:**

✅ **1. Architecture Patterns**
- Modular Monolith (simple, maintainable for solo dev)
- Monorepo (frontend + backend in single repo)
- SPA + REST API (React frontend, FastAPI backend)
- Multi-tenant with Row-Level Security (CompanyID isolation)

✅ **2. Technology Stack**
- 43 technologies with exact versions
- All dependencies mapped with fallback strategies
- Exact version pinning (prevents v4 integration conflicts)

✅ **3. Database Architecture**
- 13 core tables with enterprise naming standards
- PascalCase, NVARCHAR, UTC timestamps, audit columns
- Multi-tenant isolation (CompanyID + RLS)
- Data lineage tracking (ActivityLog)

✅ **4. API Architecture**
- RESTful JSON API (standard HTTP methods)
- 60+ endpoints defined (8 resource groups)
- JWT authentication, pagination, validation patterns
- WebSocket for real-time analytics

✅ **5. Risk Mitigation Strategies**
- Form builder data loss prevention (hybrid auto-save)
- Integration risk management (POC, dependency pinning)
- Image management (storage-database alignment)
- Logging & observability (comprehensive error tracking)
- Multi-tenant security (defense in depth)

✅ **6. Development Approach**
- Environment abstraction (local dev to Azure prod)
- Database migrations (Alembic version control)
- Monorepo structure (~115 source files)
- GitHub Actions CI/CD (Week 21)

---

## Next Steps

**Immediate Actions (Week 0):**

1. **Review & Approve Architecture**
   - Read complete solution architecture
   - Identify any unclear sections or concerns
   - Confirm technology choices align with experience level

2. **Environment Setup (Local Development)**
   - Install tools: Python 3.11, Node.js 18+, SQL Server, Docker
   - Clone repository structure
   - Install dependencies (`npm install`, `pip install -r requirements.txt`)
   - Configure `.env.local` file
   - Run MailHog container (email testing)
   - Create local database
   - Run Alembic migrations
   - Seed development data

3. **BMAD Planning Workflow**
   - Run `plan-project` workflow (generate project breakdown)
   - Review epic breakdown and story estimates
   - Confirm 22-week timeline is realistic
   - Adjust if needed based on your availability

**BMad Builder Integration (After Architecture Approval):**

If you want to create custom agents for database standards enforcement:

1. **Database Migration Validator Agent**
   - Validates Alembic migrations follow PascalCase
   - Checks NVARCHAR usage, audit columns, constraints
   - Runs before migration applied (prevents standards violations)

2. **Story Context Generator Agent**
   - Generates `story-context.xml` with forbidden zones
   - Injects database standards into every story
   - Prevents epic boundary violations

**To Create These Agents:**
```
@bmad/bmb/agents/bmad-builder create-agent
Agent Name: database-migration-validator
Purpose: Enforce database naming standards in Alembic migrations
Base Template: validator
```

---

## Architecture Cohesion Check

**Quality Gates (Must Pass Before Implementation):**

✅ **1. Database Schema Completeness**
- All 13 core tables defined with exact column specifications
- Foreign key relationships mapped correctly
- Indexes defined for common queries
- RLS policies documented

✅ **2. API Endpoint Coverage**
- All epics have corresponding API endpoints
- CRUD operations defined for all entities
- Authentication flow complete (signup → login → onboarding)
- Multi-tenant filtering in every endpoint

✅ **3. Technology Stack Validation**
- No version conflicts detected (compatibility matrix validated)
- Dependency chains mapped (11 critical chains identified)
- Single points of failure mitigated (10 SPOFs with strategies)
- Update strategy defined (quarterly with testing)

✅ **4. Epic Boundary Definition**
- 9 epics mapped to backend modules
- Component boundaries clear (no overlap)
- Integration points documented
- Forbidden zones defined (prevent cross-epic contamination)

✅ **5. Risk Mitigation Completeness**
- 16 risk categories analyzed with mitigations
- P0-P3 priority matrix defined
- Critical pre-implementation actions identified (Week 0, 4, 9-10)
- Fallback strategies for key dependencies

✅ **6. Anthony's v4 Pain Points Addressed**
- Epic boundary violations: story-context XML with forbidden zones
- Database naming: Standards embedded in architecture + validation agent
- Integration conflicts: Exact version pinning + POC validation + integration testing
- Auto-update surprises: No auto-updates (controlled quarterly updates)

**Architecture Status: ✅ READY FOR IMPLEMENTATION**

**Recommendation:** Proceed to `plan-project` workflow to generate detailed epic breakdown and story estimates.

---


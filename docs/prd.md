# PRD — Event Lead Platform (MVP)

**Status:** Active - Comprehensive MVP Scope Defined  
**Date:** 2025-10-11 (Major Update)  
**Realistic Target Launch:** 5.5 months (2026-04-25)  
**Brainstorming Session:** `docs/brainstorming-session-results-2025-10-10.md`  
**UX Specification:** `docs/ux-specification.md`

**Change Log:**
- **2025-10-11 Update 1:** Added multi-tenant company model, RBAC (3 roles), Events as containers for forms, team collaboration/invitations, company billing & invoicing, Australian compliance requirements, onboarding flows, and updated all data models and user flows.
- **2025-10-11 Update 2:** Added advanced form builder features (undo/redo, component framework, enhanced drag UX, canvas/screen distinction), preview/testing system, event domain features (private events, event types, activation windows), proportional scaling rendering approach, and revised timeline to realistic 5.5 months.

---

## Executive Summary

**Event Lead Platform** is a multi-tenant SaaS platform that helps businesses collect leads at events using beautiful, branded forms with custom backgrounds and drag-and-drop design. Companies create events, build multiple forms per event, and pay only when they publish forms for their events.

**Target Market:** Businesses exhibiting at trade shows, conferences, expos, and community events  
**Initial Focus:** Australian market (Sydney events ~40+ events/month)  
**Business Model:** "Create Free, Pay to Publish" - freemium builder with company-based billing and invoicing  
**Differentiator:** Custom backgrounds + freeform placement (not generic form templates) + event-based organization

**Platform Model:**
- **Multi-tenant:** Companies with multiple team members collaborating
- **Role-Based Access:** System Admin, Company Admin, Company User roles
- **Event-Centric:** Events contain multiple forms, pay per published form
- **Australian Compliance:** Adheres to Australian legal and privacy requirements

**MVP Goal:** Launch in 3 months with full company, event, and team collaboration features

---

## Business Model

### Create Free, Pay to Publish (Company-Based Billing)

**Core Principle:** Zero barrier to entry. Companies and their teams create events and build forms for free, paying only when they publish forms for their events.

**Company Flow:**
1. First user signs up (free, email-based authentication)
2. Complete onboarding (user details + company setup)
3. First user becomes Company Admin automatically
4. Admin invites team members (Company Users)
5. Team creates events and builds unlimited draft forms
6. Pay to publish forms ($99 per form per event)
7. Company receives invoices (Australian GST-compliant)
8. Forms go live, collect leads, view analytics, export CSV

**Why This Works:**
- No friction to try the product (individuals or teams)
- Company-based billing matches B2B purchasing workflows
- Team collaboration enables multiple stakeholders (marketing, events, sales)
- Emotional investment (pride in creation) increases conversion
- Event-based organization aligns with customer mental model
- Australian invoicing builds trust with local businesses

### Pricing

**MVP Pricing:**
- **$99 per published form per event**
  - Create unlimited draft forms (free)
  - Pay only when publishing a form for an event
  - Multiple forms per event possible (each charged separately)
  - Includes all features:
    - Custom form with backgrounds OR templates
    - Drag-and-drop builder
    - Hosting and public URL
    - Lead collection and storage
    - Minimalistic analytics dashboard
    - CSV export (Salesforce, Marketing Cloud, Emarsys formats)
    - Data validation
    - Tablet-responsive forms

**Company Billing:**
- Invoices sent to Company Admin email
- Australian GST-compliant invoicing (10% GST included in pricing)
- Payment via Stripe (credit card, debit card)
- Billing history available in company dashboard

**Post-MVP Pricing (Phase 2):**
- **Premium: $199 per event**
  - Everything in Standard PLUS:
  - Gamified prize draw (spin wheel, countdown)
  - SMS reminders 30min before draw
  - Winner announcement and notifications
  - Multiple draws per event (additional fee)

**Rationale:**
- $99 vs $200 contractor baseline = compelling value
- Positions as premium service, not commodity
- Need 70-94 events/month to reach $14k breakeven (realistic)
- "Form live in 5 minutes" vs 2-3 day contractor turnaround

---

## Multi-Tenant Architecture & RBAC

### Company Model

**Platform is multi-tenant at the company level:**
- Each company is a separate tenant with isolated data
- Companies have multiple users (team members)
- First user to sign up for a company becomes Company Admin
- Company Admin can invite additional users
- All company data (events, forms, submissions, billing) is shared among company users

### Role-Based Access Control (RBAC)

**Three user roles:**

**1. System Admin** (Platform-level - Post-MVP UI)
- Full platform access across all companies
- Manage platform settings and configurations
- Monitor system health and usage
- Handle customer support escalations
- Access to admin-only backend tools
- **Note:** System Admin screens/UI are out of scope for MVP (backend access only)

**2. Company Admin** (Company-level)
- Full access to company dashboard and all features
- Manage company details (name, billing address, ABN, contact info)
- Invite and remove team members
- Assign roles to users (promote to Admin, demote to User)
- View and manage billing/invoices
- Create/edit/delete events
- Create/edit/delete/publish forms
- View analytics for all company forms
- Export data

**3. Company User** (Company-level - Limited)
- Access to company dashboard (read-only for company settings)
- Create/edit/delete events
- Create/edit/delete forms (CANNOT publish - draft only)
- **Request Admin to publish** forms (Admin handles payment)
- View analytics for forms they created or have been shared with
- Export data from their forms
- Cannot publish forms or trigger payments
- Cannot manage billing or invite users
- Cannot modify company details

### Authentication & Onboarding Flow

**First-Time User (Company Creator):**

**Phase 1 - Sign Up & Email Verification (Public, Unauthenticated):**
1. User visits signup page
2. Enters email and password
3. Submits signup form
4. System sends verification email with secure token link
5. User checks email, clicks verification link
6. Redirected to login page with "Email verified" confirmation
7. User logs in with email/password
8. System generates JWT token for session

**Phase 2 - Onboarding (Authenticated, Inside App):**
9. After successful login, check if user has completed onboarding
10. If not complete, show onboarding flow (cannot skip, required to use platform)
11. **Onboarding Step 1 - User Details:**
    - First Name (required)
    - Last Name (required)
    - Role/Title (optional, e.g., "Marketing Manager")
    - Phone Number (optional, Australian format +61)
    - Click "Next"
12. **Onboarding Step 2 - Company Setup:**
    - Company Name (required)
    - ABN (Australian Business Number - validated format, 11 digits)
    - Billing Address (required, Australian address with validation)
      - Street Address
      - City
      - State (dropdown: NSW, VIC, QLD, SA, WA, TAS, NT, ACT)
      - Postcode (4 digits)
    - Company Phone (optional)
    - Industry (dropdown, optional)
    - Click "Complete Setup"
13. User automatically assigned Company Admin role
14. Onboarding complete flag set in database
15. Redirect to dashboard with welcome overlay/tutorial
16. Dashboard shows "Create Your First Event" prompt

**Invited User (Joining Existing Company):**

**Phase 1 - Invitation & Verification (Public, Unauthenticated):**
1. Company Admin sends invitation with:
   - Invitee's First Name (required)
   - Invitee's Last Name (required)
   - Invitee's Email (required)
   - Assigned Role: Company Admin OR Company User
2. Invitee receives invitation email with:
   - Welcome message
   - Company name they're joining
   - Role they'll have
   - Secure invitation token link (expires in 7 days)
3. Invitee clicks invitation link
4. Lands on invitation acceptance page showing:
   - "Join [Company Name] as [Role]"
   - Email pre-filled (read-only)
   - Password field (set new password)
5. Invitee sets password and submits
6. Email automatically marked as verified (invitation email = verification)
7. System generates JWT token for session

**Phase 2 - Onboarding (Authenticated, Inside App):**
8. After successful signup/login, check if user has completed onboarding
9. **Onboarding Step 1 - User Details:**
   - First Name (pre-filled from invitation, editable)
   - Last Name (pre-filled from invitation, editable)
   - Role/Title (optional)
   - Phone Number (optional, Australian format)
10. NO Company Setup step (joining existing company)
11. Role already assigned by Admin
12. Onboarding complete flag set
13. Redirect to company dashboard (sees existing events/forms)
14. Company Admin notified that invitee has joined

**Password Reset Flow:**
1. User clicks "Forgot Password" on login page
2. Enters email address
3. System sends password reset email with secure token link
4. User clicks link, lands on reset page
5. Enters new password (with confirmation)
6. Password updated
7. Redirect to login with success message
8. User logs in with new password

### Team Collaboration

- Company Admin can invite unlimited users (for MVP - no seat limits)
- Invitation via email address
- Pending invitations tracked (can be cancelled)
- Users see company name during invitation signup
- All users share access to company events and forms
- Activity log shows which user created/edited/published each form

---

## MVP Scope (3 Months)

### Core Features (Must Build)

#### 1. User Authentication, Onboarding & RBAC
- Email-based signup/login with verification
- Multi-step onboarding flow (user details + company setup)
- Role assignment (System Admin, Company Admin, Company User)
- User profile management
- Password reset flow
- Session management with JWT tokens
- RBAC middleware for authorization checks

**Tech:** FastAPI + JWT tokens, MS SQL Server (users, companies, roles, invitations tables)

---

#### 2. Company Management
- Company profile (name, ABN, billing address, phone, industry)
- Company Admin can update company details
- Company settings page
- Activity log (who created/edited what)
- Data isolation per company (multi-tenant)

**Tech:** MS SQL Server company table with foreign keys, row-level security patterns

---

#### 3. Events Management & Domain Features
**Core Event Management:**
- Create/edit/delete events
- Event details: name, date range, location, description, event type
- Events contain multiple forms
- Event list view (upcoming, past, draft)
- Event dashboard (shows all forms for an event)
- Pay per published form within an event

**Event Domain & Discovery:**
- **Event selection during form creation:**
  - Dropdown with all company events
  - Filter by location, date range, event type
  - Search by event name
  - "Add New Event" inline option (modal within form creation flow)
- **Event Types** (for differential pricing and categorization):
  - Trade Show
  - Conference
  - Expo
  - Community Event
  - Job Fair
  - Product Launch
  - Other
  - Each type can have different base pricing (configured in admin)
- **Personal/Private Events:**
  - Option to mark event as "Personal/Private"
  - Used for non-event forms (ongoing lead collection, surveys, etc.)
  - Only requires start/end date (location optional)
  - Doesn't appear in any public listings
  - Same form creation workflow
- **New Event Quality Review:**
  - Events created inline during form creation flagged for review
  - System Admin reviews and approves new events (post-MVP UI)
  - Prevents spam/abuse at scale
  - Auto-approved for MVP (manual review via database)
- **Form Activation Windows:**
  - Forms automatically activate 3 hours before event start time
  - Forms automatically deactivate 3 hours after event end time
  - Outside activation window: Form shows "This event has ended" message
  - Override option for Company Admin (manual activate/deactivate)
  - Personal/Private events: Use custom start/end dates for activation

**Tech:** MS SQL Server events table with event_type, is_private, activation logic in form rendering

---

#### 4. Team Collaboration & Invitations
- Company Admin invites users via email (first name, last name, email, role)
- Invitation email with secure token link
- Pending invitations list (can cancel)
- Assign role during invitation (Company Admin or Company User)
- User management screen (list users, change roles, remove users)
- Role-based UI rendering (show/hide features based on role)
- **Expired invitation handling:**
  - Invitations expire after 7 days
  - Expired status shown in pending invitations list
  - "Resend Invitation" button generates fresh 7-day invite
  - New token generated, new email sent
  - Original invitation marked as expired, new one created

**Tech:** MS SQL Server invitations table with expiry logic, email service (SendGrid), role-based UI components

---

#### 4A. Preview & Testing System

**Core Principle:** Preview uses same system as production - no separate environment. Leads are simply flagged as preview vs production.

**Preview Mode:**
- Toggle between "Preview" and "Production" mode in form builder
- Preview URL: Same as production URL with ?preview=true parameter
- Preview leads flagged in database: `submission.is_preview = true`
- Production leads flagged: `submission.is_preview = false`
- Both types stored in same table, same validation rules

**Testing Requirements:**
- **Minimum 5 preview tests** required before form can be published
- Each test = complete form submission in preview mode
- Test counter visible in builder: "3 of 5 tests completed"
- Publish button disabled until threshold met
- **Company Admin override:**
  - Admin can set custom test threshold per company (0-20 tests)
  - Stored in company settings
  - Default: 5 tests
- **Test audit log:**
  - Track which user completed each test
  - Timestamp of each test submission
  - Stored in ActivityLog table
  - Visible to Company Admins

**Approver Testing Requirement:**
- When Company User requests publish, Company Admin must test before approving
- **Exception:** If Admin is also the form creator and already completed required tests
- Admin review page shows: "You must complete X tests before publishing"
- Test button on review page opens preview URL
- After completing tests, "Publish & Pay" button enabled

**Preview Data Management:**
- Preview leads visible in analytics with "Preview" badge
- Filter: Show Preview Only | Production Only | All Leads
- Export option: Include/Exclude preview leads
- Dashboard counts: "50 Production leads • 8 Preview leads"
- Preview leads help customers test CRM import workflows
- Can delete individual preview leads or bulk delete all preview leads

**Tech:** Submission table with `is_preview` boolean flag, preview test counter in Form table, ActivityLog for test auditing

---

#### 5. Drag-and-Drop Form Builder

**Canvas-based interface with freeform component placement**

**Component Library:**
- Name (first name, last name, full name variants)
- Email
- Phone
- **Address** (integrated with GeoScape API for Australian address validation)
- Text input (single line)
- Dropdown/select
- Checkbox
- Radio buttons
- Multi-line text area (textarea)

**Component Structure (3-Part System):**

Each form component consists of three parts:
1. **Label** - Field label text
2. **Input Field** - The actual input control
3. **Validation Message** - Error/helper text area

**Stacking Options (Configurable per component):**
- **Horizontal Layout:**
  - Label to the left of Input Field
  - Validation message below (spans full width)
  - Good for compact forms, side-by-side layout
- **Vertical Layout:** (Default)
  - Label above Input Field
  - Input Field below label
  - Validation message below input
  - Good for mobile, clearer hierarchy
- Toggle setting in component properties panel

**Tab Order Management:**
- Each component automatically assigned tab order when added to form
- Tab order based on visual top-to-bottom, left-to-right positioning
- **Visual tab order display:**
  - Toggle in Form Settings: "Show Tab Order"
  - Numbers appear on each component (1, 2, 3...)
  - Drag components to reorder (updates tab order automatically)
  - Manual tab order editing available (advanced mode)
- Ensures keyboard navigation follows logical flow
- Critical for accessibility compliance

**Drag and Position:**
- Drag components onto canvas, position anywhere within screen rectangle
- Resize and style components
- Real-time preview
- Aspect ratio maintenance when published (proportional scaling)

**Tech:** React frontend, drag-and-drop library (react-dnd or dnd-kit), responsive rendering engine

**Advanced Builder Features (Integrated):**

**A. Proportional Scaling Rendering System**
- Design on fixed canvas (1200x1600px - 3:4 aspect ratio, iPad-optimized)
- Components positioned in absolute pixels during design
- On publish: Entire form scales proportionally to fit target device
- CSS transform: scale() maintains design proportions
- Letterbox/crop handling for different aspect ratios
- Designer sees exact WYSIWYG (what they design = what renders)
- **Rationale:** Simpler than percentage positioning (1-2 weeks vs 3-4 weeks), works well for 90% of tablets

**B. Canvas vs Screen Distinction**
- **Canvas:** Full editing area between left/right panels
- **Screen:** 80% rectangle within canvas (represents target device screen)
- Screen rectangle shows form boundaries (prevents designs that exceed viewport)
- Screen aspect ratio selector: Portrait (3:4), Square (1:1), Landscape (16:9)
- Components must be placed within screen rectangle
- Visual fence prevents dragging outside screen boundaries

**C. Component Framework (Form-level Defaults + Overrides)**
- Form-level default settings: font family, font size, color, label position
- Apply defaults to all components automatically
- Each component can override form-level settings individually
- Last updated timestamp determines precedence
- "Reset to form defaults" option on components
- "Apply to all components" option from form settings

**D. Undo/Redo System**
- Track all designer actions (add, move, resize, style, delete component)
- Undo: Ctrl+Z (or button), reverses last action
- Redo: Ctrl+Shift+Z (or button), re-applies undone action
- History limit: 50 actions (balance memory vs utility)
- Clear history on publish (fresh start for edits)
- Visual indicator: "X actions available to undo"

**E. Enhanced Drag Interactions**
- **Cursor states:**
  - Hover over component library: Open hand cursor
  - Click and hold: Closed hand cursor
  - Dragging: Closed hand moves with component ghost
- **Fencing:** Components cannot be dragged outside screen rectangle
- **Return to library:** If released outside screen, component returns to library (smooth animation)
- **Snap feedback:** Visual/haptic feedback when snapping to grid or other components
- **Ghost preview:** Semi-transparent preview shows where component will land

**F. Component Overlap Prevention**
- Collision detection when dragging/resizing components
- Red outline shows if component would overlap existing component
- Cannot release component on top of another (must find open space)
- Nudge suggestion: "Move 20px right to avoid overlap"
- Option to allow overlap (advanced mode toggle)

**G. Background Image Resize Mode**
- Initial mode: Background image can be resized/repositioned
- Scale background larger/smaller than screen rectangle
- Pan background within screen to get desired portion visible
- **Mode lock:** After adding first component, background edit mode disabled
- Prevents accidental background moves while placing components
- "Edit Background" button re-enables if needed (shows warning: "Components may shift")

---

#### 6. Custom Backgrounds + Template Library
- **Option A:** Upload custom background image
  - Image upload (JPEG, PNG)
  - Azure Blob Storage
  - Image optimization/resizing
  - Preview with components overlaid
  
- **Option B:** Choose from template library
  - 5-10 pre-designed professional templates
  - Industry-specific themes (tech, healthcare, retail, professional services)
  - One-click apply
  
- **Best of Both:** Start with template, then customize OR start blank with custom background

**Tech:** Azure Blob Storage for images, image processing library, template JSON definitions

---

#### 7. Form Publishing & Hosting
- "Publish" button triggers payment gate
- Stripe payment flow ($99 Standard tier only for MVP)
- Generate unique public URL on publish (e.g., `forms.eventlead.com/{unique-id}`)
- Forms hosted on reliable Azure infrastructure
- Form never goes down (even if customer doesn't pay for next event)
- Unpublish option (takes form offline)

**Tech:** Azure App Service or Static Web Apps, Stripe SDK, URL generation logic

---

#### 8. Lead Collection & Storage
- Public forms accept submissions
- Store all form data in MS SQL Server
- Timestamp all submissions
- Associate submissions with form owner
- No submission limits
- GDPR-compliant data handling

**Tech:** MS SQL Server submissions table, API endpoints for form submission

---

#### 9. Data Validation
- Field-level validation rules:
  - Email format validation
  - Phone number format (Australian +61, international)
  - Required field enforcement
  - Min/max length for text fields
- Real-time validation feedback on form
- Prevent >90% bad leads (quality = retention)

**Tech:** Frontend validation (React), backend validation (FastAPI), validation library

---

#### 10. Minimalistic Analytics Dashboard
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

**Tech:** React dashboard, Chart.js or Recharts for visualization, real-time data fetch, WebSocket or polling for real-time updates

---

#### 10A. Usage Analytics & Workflow Optimization

**Platform Usage Tracking:**
- Collect anonymous usage data for all user workflows
- Track: clicks, page views, time on page, feature usage, workflow completion rates
- Purpose: Understand if workflows are successful and efficient
- Identify friction points and optimize UX
- A/B testing capability (future)

**Metrics Collected:**
- Form builder usage: time to create form, components used, features utilized
- Onboarding completion rate and drop-off points
- Event creation patterns
- Preview testing behavior
- Payment conversion rates
- Feature adoption (undo usage, template vs custom background, etc.)

**Privacy-Safe:**
- Aggregate data only (no PII)
- Company-level analytics (not individual user tracking for external analytics)
- Australian Privacy Principles compliant
- Can opt-out in company settings

**Tech:** PostHog or Plausible (privacy-focused analytics), custom event tracking, dashboard for Anthony to review platform health

---

#### 11. CSV Export & Company Billing
**CSV Export:**
- Export all leads for a form to CSV
- Format options:
  - Salesforce format
  - Marketing Cloud format
  - Emarsys format
  - Generic CSV
- One-click download
- Include all fields + timestamp

**Company Billing & Invoicing:**
- Generate Australian GST-compliant invoices
- Invoice details: Company name, ABN, billing address, line items (forms published)
- 10% GST included in all pricing
- Invoice PDF generation
- Email invoice to Company Admin
- Billing history view (list all invoices, download PDFs)
- Payment via Stripe (one-time payments per publish)
- Receipt emails after successful payment

**Tech:** CSV generation library, Stripe SDK, invoice PDF generation (ReportLab or similar), email service (SendGrid)

---

### Out of Scope for MVP

**Explicitly NOT in MVP (Phase 2+):**
- ❌ **System Admin UI** (role exists, but admin screens/dashboard not built - backend access only)
- ❌ Prize draw feature (gamification, SMS reminders)
- ❌ CRM integrations (Salesforce, HubSpot direct sync)
- ❌ Address validation service
- ❌ Follow-up email automation
- ❌ Advanced analytics (heatmaps, funnels, detailed demographics)
- ❌ Event Package tier (sell to event organizers as a bundled offering)
- ❌ Multi-language support (English only for MVP)
- ❌ White-label/remove branding
- ❌ Mobile app (web app only, tablet-optimized public forms)
- ❌ Advanced team permissions (fine-grained permissions beyond Admin/User roles)
- ❌ Seat-based pricing (unlimited team members for MVP)
- ❌ API for third-party integrations

---

## Technical Architecture

### Stack
- **Frontend:** React (modern hooks-based)
- **Backend:** Python FastAPI
- **Database:** MS SQL Server (Azure SQL Database)
- **Hosting:** Azure App Service
- **Storage:** Azure Blob Storage (images)
- **Payments:** Stripe
- **Email:** SendGrid or Azure Communication Services
- **Development:** Cursor + BMAD agentic development tools

### Infrastructure
- Azure hosting (already setup)
- MS SQL Server database (already configured)
- Azure CDN for form hosting
- SSL/TLS for all public forms
- Backup and disaster recovery

### Key Data Models

**User:**
- `user_id` (PK)
- `email` (unique)
- `password_hash`
- `first_name` (collected during onboarding)
- `last_name` (collected during onboarding)
- `role_title` (optional, e.g., "Marketing Manager")
- `phone_number` (optional, Australian format)
- `company_id` (FK - nullable until onboarding complete)
- `role` (enum: system_admin, company_admin, company_user)
- `email_verified` (boolean - set true after email verification link clicked)
- `onboarding_complete` (boolean - gates access to dashboard)
- `created_at`
- `last_login`
- `is_active` (boolean)

**Company:**
- `company_id` (PK)
- `company_name`
- `abn` (Australian Business Number)
- `billing_address` (JSON: street, city, state, postcode, country)
- `company_phone` (optional)
- `industry` (optional)
- `test_threshold` (integer, default: 5 - required preview tests before publish)
- `usage_analytics_opt_out` (boolean, default: false)
- `created_by_user_id` (FK to User - first user who created company)
- `created_at`
- `updated_at`
- `is_active` (boolean)

**Event:**
- `event_id` (PK)
- `company_id` (FK)
- `created_by_user_id` (FK to User)
- `event_name`
- `event_type` (enum: trade_show, conference, expo, community_event, job_fair, product_launch, other)
- `event_date_start` (datetime)
- `event_date_end` (datetime)
- `location` (string, optional for private events)
- `description` (text, optional)
- `is_private` (boolean - personal/private event, not in public listings)
- `needs_review` (boolean - flagged for quality review if created inline)
- `reviewed_by_admin_id` (FK to User - System Admin who reviewed, nullable)
- `reviewed_at` (timestamp, nullable)
- `status` (enum: draft, active, completed, cancelled, pending_review)
- `activation_start` (datetime - calculated: event_date_start - 3 hours)
- `activation_end` (datetime - calculated: event_date_end + 3 hours)
- `created_at`
- `updated_at`

**Form:**
- `form_id` (PK)
- `event_id` (FK)
- `company_id` (FK)
- `created_by_user_id` (FK to User)
- `form_name`
- `status` (enum: draft, published, unpublished, pending_admin_review)
- `design_json` (component layout, styles, background, tab order)
- `canvas_width` (integer, default: 1200px - design canvas dimensions)
- `canvas_height` (integer, default: 1600px)
- `screen_aspect_ratio` (enum: portrait_3_4, square_1_1, landscape_16_9 - default: portrait_3_4)
- `component_defaults_json` (form-level defaults: font_family, font_size, color, label_position, etc.)
- `preview_test_count` (integer - number of preview tests completed)
- `preview_tests_required` (integer - uses company.test_threshold, can be overridden)
- `undo_history_json` (array of actions for undo/redo, cleared on publish)
- `tab_order_json` (array of component_ids in tab order sequence)
- `public_url` (unique, generated on publish)
- `created_at`
- `published_at`
- `unpublished_at`
- `updated_at`
- `updated_by_user_id` (FK to User - last editor)

**Payment:**
- `payment_id` (PK)
- `company_id` (FK)
- `form_id` (FK)
- `event_id` (FK)
- `paid_by_user_id` (FK to User)
- `amount` (9900 cents = $99, includes GST)
- `gst_amount` (900 cents = 10% GST)
- `stripe_payment_id`
- `status` (enum: pending, succeeded, failed, refunded)
- `invoice_number` (unique, generated)
- `invoice_pdf_url` (Azure Blob Storage)
- `created_at`

**Invoice:**
- `invoice_id` (PK)
- `company_id` (FK)
- `payment_id` (FK)
- `invoice_number` (unique)
- `invoice_date`
- `due_date`
- `subtotal` (9000 cents = $90 ex GST)
- `gst_amount` (900 cents)
- `total_amount` (9900 cents)
- `line_items_json` (array of: form_name, event_name, amount)
- `pdf_url` (Azure Blob Storage)
- `sent_at` (timestamp when emailed)
- `created_at`

**Submission:**
- `submission_id` (PK)
- `form_id` (FK)
- `event_id` (FK)
- `company_id` (FK)
- `data_json` (all form fields as JSON)
- `is_preview` (boolean - true for preview/test submissions, false for production)
- `test_completed_by_user_id` (FK to User - if preview test, who completed it, nullable)
- `ip_address_hash` (privacy-safe, hashed for Australian privacy compliance)
- `user_agent`
- `device_type` (string - desktop, tablet, mobile - detected from user agent)
- `screen_resolution` (string - captured for analytics, e.g., "1024x768")
- `submitted_at`

**Template:**
- `template_id` (PK)
- `name`
- `category`
- `thumbnail_url`
- `design_json` (pre-configured layout)
- `is_active` (boolean)
- `created_at`

**Invitation:**
- `invitation_id` (PK)
- `company_id` (FK)
- `invited_by_user_id` (FK to User - Company Admin who sent invite)
- `invited_email`
- `invited_first_name` (pre-filled by Admin, shown during invitation acceptance)
- `invited_last_name` (pre-filled by Admin, shown during invitation acceptance)
- `assigned_role` (enum: company_admin, company_user - set by Admin during invitation)
- `invitation_token` (unique, secure token for invitation link)
- `status` (enum: pending, accepted, cancelled, expired)
- `invited_at`
- `accepted_at` (nullable)
- `expires_at` (7 days from invited_at)

**PublishRequest:**
- `publish_request_id` (PK)
- `form_id` (FK)
- `event_id` (FK)
- `company_id` (FK)
- `requested_by_user_id` (FK to User - Company User who created form)
- `admin_user_id` (FK to User - Admin who will review, nullable)
- `status` (enum: pending, approved, declined, cancelled)
- `user_message` (optional message from user to admin)
- `admin_response` (optional message from admin to user)
- `requested_at`
- `reviewed_at` (nullable)
- `approved_at` (nullable)

**ActivityLog:**
- `activity_id` (PK)
- `company_id` (FK)
- `user_id` (FK)
- `action` (enum: created, updated, deleted, published, unpublished, invited_user, publish_requested, publish_approved, publish_declined, etc.)
- `entity_type` (enum: form, event, user, company, invitation, publish_request)
- `entity_id` (ID of the entity acted upon)
- `details_json` (additional context about the action)
- `created_at`

---

## User Flows

### 1. New Company Sign Up & Onboarding (First User - Company Creator)

**Phase 1 - Sign Up & Verification (Unauthenticated):**
1. User visits landing page
2. Clicks "Get Started" or "Sign Up"
3. Enters email and password on signup form
4. Submits form
5. System sends verification email with secure token link
6. Message displayed: "Check your email to verify your account"
7. User checks email, clicks verification link
8. Redirected to login page with "Email verified! Please log in" message

**Phase 2 - Login & Authentication:**
9. User enters email/password on login page
10. System validates credentials
11. System generates JWT token for session
12. System checks: Has user completed onboarding? → NO

**Phase 3 - Onboarding (Authenticated, Inside App):**
13. Onboarding modal/screen appears (cannot dismiss, required)
14. **Onboarding Step 1 - User Details:**
    - First Name (required)
    - Last Name (required)
    - Role/Title (optional, e.g., "Marketing Manager")
    - Phone Number (optional, Australian format +61)
    - Click "Next"
15. **Onboarding Step 2 - Company Setup:**
    - Company Name (required)
    - ABN (Australian Business Number - 11 digits, validated)
    - Billing Address (required, Australian address):
      - Street Address
      - City
      - State (dropdown: NSW, VIC, QLD, SA, WA, TAS, NT, ACT)
      - Postcode (4 digits)
    - Company Phone (optional)
    - Industry (dropdown, optional)
    - Click "Complete Setup"
16. System creates company record
17. User automatically assigned Company Admin role
18. Onboarding complete flag set (`user.onboarding_complete = true`)
19. Dashboard loads with welcome overlay/tutorial
20. Dashboard shows "Create Your First Event" prompt

### 2. Create Event & First Form (Company Admin)
1. From dashboard, clicks "Create Event"
2. Event creation modal:
   - Event Name (e.g., "Tech Summit 2026")
   - Date Range (start date, end date)
   - Location (text field)
   - Description (optional)
3. Event created, lands on Event Dashboard
4. Clicks "Create Form" for this event
5. Form builder opens in new tab/window (maximized screen space)
6. Chooses template OR uploads custom background
7. Drags components onto canvas (freeform positioning)
8. Styles and positions elements
9. Real-time preview updates
10. Auto-save (draft status)
11. Clicks "Publish"
12. Payment screen: $99 + GST breakdown shown
13. Stripe payment flow
14. Payment succeeds → Invoice emailed to Company Admin
15. Form published, receives unique public URL
16. Returns to Event Dashboard, sees published form listed
17. Shares public URL (QR code, email, print for booth)

### 3. Invite Team Member (Company Admin)

**Company Admin Flow:**
1. Company Admin navigates to "Team" tab
2. Clicks "Invite User" button
3. Invitation modal appears with form:
   - First Name (required)
   - Last Name (required)
   - Email Address (required, validated)
   - Assigned Role (dropdown: Company Admin OR Company User)
4. Clicks "Send Invitation"
5. System creates invitation record with token
6. System sends invitation email to invitee
7. Success message: "Invitation sent to [email]"
8. Invitation appears in "Pending Invitations" list

**Invitee Flow (Unauthenticated):**
9. Invitee receives email with:
   - "You've been invited to join [Company Name]"
   - "Role: [Company Admin/Company User]"
   - Secure invitation link (expires in 7 days)
10. Clicks invitation link
11. Lands on invitation acceptance page showing:
    - "Join [Company Name] as [Role]"
    - First Name (pre-filled from invitation, read-only)
    - Last Name (pre-filled from invitation, read-only)
    - Email (pre-filled, read-only)
    - Password field (set new password)
    - Password confirmation field
12. Invitee sets password and clicks "Accept Invitation"
13. Account created with user.company_id set from invitation (joined company immediately)
14. user.role set from invitation (company_admin or company_user)
15. Email marked as verified (invitation email = verification)
16. Invitation status updated to "Accepted"
17. System generates JWT token, user logged in automatically

**Invitee Flow (Authenticated, Onboarding):**
18. System checks: Has user completed onboarding? → NO
19. Onboarding modal appears (simplified for invited users)
20. **Onboarding Step - User Details Only:**
    - First Name (pre-filled from invitation, editable)
    - Last Name (pre-filled from invitation, editable)
    - Role/Title (optional, e.g., "Sales Manager")
    - Phone Number (optional, Australian format)
    - Click "Complete Setup"
21. NO Company Setup step (already joined company in step 13)
22. Onboarding complete flag set
23. System sends notification to Company Admin: "[Name] has joined your team"
24. Redirect to company dashboard
25. User sees existing company events and forms (already has access via company_id)

### 4. Create Form & Request Publish (Company User)

**Create Form (Company User):**
1. Company User logs in (already verified email, completed onboarding)
2. Dashboard shows list of company events
3. Selects event from list OR creates new event
4. Event Dashboard opens
5. Clicks "Create Form"
6. Form builder opens in new tab
7. Builds form (chooses template/background, drags components, styles)
8. Auto-save creates draft form
9. Clicks "Publish" button
10. **Permission Check:** User role = Company User (NOT Admin)

**Publish Request Flow (Company User cannot publish directly):**
11. Modal appears: "Request Admin to Publish"
    - Message: "Only Company Admins can publish forms. Would you like to notify an Admin?"
    - List of Company Admins (select recipient)
    - Optional message to Admin
    - "Send Request" button
12. System sends notification email to selected Admin(s)
13. System creates pending publish request record
14. Success message: "Admin has been notified. They'll publish your form."
15. Form status remains "draft" with flag "pending_admin_review"
16. User returns to Event Dashboard
17. Form shows "Waiting for Admin to Publish" status badge

**Admin Approves Publish (Company Admin):**
18. Company Admin receives email: "[User Name] requests to publish form [Form Name] for [Event Name]"
19. Email has link: "Review and Publish"
20. Admin clicks link, lands on form preview page
21. Admin reviews form, sees price: $99 + GST
22. Options:
    - "Publish & Pay" → Triggers Stripe payment flow
    - "Request Changes" → Sends message back to user
    - "Decline" → Notifies user, form stays draft
23. If Admin clicks "Publish & Pay":
24. Stripe payment flow (same as flow #2)
25. Payment succeeds
26. Form published, public URL generated
27. Invoice emailed to Admin
28. User who created form gets notification: "Your form has been published!"
29. Form appears as "Published" in Event Dashboard

### 5. Return Customer - New Event (Company Admin)
1. Logs in, lands on dashboard
2. Sees list of past/upcoming events
3. Clicks "Create Event" for new event
4. Fills event details
5. Option to "Duplicate form from previous event"
6. Selects form from dropdown (shows all company forms)
7. Form duplicated into new event (as draft)
8. Can edit in builder or publish immediately
9. Publishes (pays $99 per form)

### 6. View Analytics & Export (Any User)
1. User logs in
2. Dashboard shows events → forms
3. Clicks on a published form
4. Analytics view opens:
   - Real-time lead count
   - Submission timeline chart
   - List of all submissions
   - Search/filter capability
5. Clicks "Export CSV"
6. Selects format (Salesforce, Marketing Cloud, Emarsys, Generic)
7. Downloads CSV
8. Imports to their CRM

### 7. Billing & Invoice Management (Company Admin)
1. Company Admin navigates to "Billing" section
2. Sees list of all invoices (invoice number, date, amount, status)
3. Can download invoice PDF
4. Can view payment history
5. Can update company billing details (address, ABN)

---

## Success Metrics (MVP)

### Primary Metrics
- **Revenue:** $14,000/month breakeven target
- **Customers:** 70-94 paying events/month (mix of $99 standard)
- **Conversion Rate:** Draft forms → Published forms (target: 30%+)
- **Form Creation Time:** Average time to build form (target: <5 minutes)
- **Data Quality:** % of valid leads (target: >90%)

### Secondary Metrics
- **User Signups:** Total accounts created
- **Forms Created:** Total draft forms (engagement signal)
- **Forms Published:** Total paid publishes (revenue)
- **Submissions per Form:** Average leads collected per event
- **CSV Exports:** % of customers who export data (usage signal)
- **Return Customers:** % who publish multiple events

### Technical Metrics
- **Uptime:** 99.5%+ (forms must stay live during events)
- **Form Load Time:** <2 seconds on tablet
- **Payment Success Rate:** >98%
- **Data Loss:** 0 submissions lost

---

## Go-to-Market Strategy (MVP)

### Target Customer
- **Primary:** Businesses exhibiting at Sydney events
- **Profile:** B2B companies, professional services, tech startups, healthcare, education
- **Pain:** Currently pay $200 to contractor with 2-3 day turnaround OR use generic Google Forms
- **Events per Year:** 6-10 events (some customers will return)

### Market Size (Sydney Focus)
- ~10 events per weekend = 40+ events/month
- Average 10-20 exhibitors per event
- Need 2-4 customers per event to hit target
- Addressable market: 400-800 potential customers/month

### Customer Acquisition Channels
1. **Direct Outreach:** Find upcoming Sydney events, contact exhibitors 2-4 weeks before
2. **Event Discovery:** Eventbrite, venue websites, industry calendars
3. **Word-of-Mouth:** Beautiful forms create social proof at events
4. **Content:** "Event Marketing Best Practices" blog/guide (SEO)
5. **Referrals:** Happy customers refer other exhibitors

### Marketing Messages
- "Form live in 5 minutes" (vs 2-3 day contractor)
- "Beautiful branded forms, not generic templates"
- "$99 per event" (vs $200 contractor)
- "Try free, pay only when you publish"
- "Own your leads, export anytime"

### Launch Plan (Month 3)
1. **Week 1:** Soft launch, 5 beta customers (friends/network)
2. **Week 2:** Collect feedback, fix critical bugs
3. **Week 3:** Public launch, direct outreach to 20 events
4. **Week 4:** Iterate based on customer feedback

---

## Phase 2 Roadmap (Post-MVP)

### Immediate Priorities (Month 4-6)

**1. Prize Draw Feature (Premium Tier Unlock)**
- Gamified prize draw (spin wheel, countdown)
- Automated SMS reminders 30min before draw
- Winner announcement and notifications
- Unlocks $199 Premium tier
- **Revenue Impact:** 2x ARPU if 50% choose Premium

**2. CRM Integration**
- Direct sync to Salesforce, HubSpot, Marketing Cloud
- Automated lead routing
- Retention hook (customers depend on integration)
- **Revenue Impact:** Reduces churn, increases LTV

**3. Address Validation Service**
- Integration with address validation API
- Variable pricing for location-based fields
- Enables demographic mapping
- **Revenue Impact:** Additional per-submission fees

### Future Expansion (Month 7+)
- Multiple prize draws per event
- Follow-up email automation
- Advanced analytics (demographics, heatmaps, funnels)
- Event Package tier (sell to event organizers for all exhibitors)
- White-label option (enterprise)
- Designer marketplace (creatives sell form design services)

### Long-Term Vision (5+ years)
- **Event Marketing Platform:** Complete suite for event exhibitors (HubSpot for events)
- **Designer Marketplace Ecosystem:** Network effects, thousands of creatives
- **Multi-sided Platform:** Direct + Event Packages + Marketplace + White Label coexisting

---

## Development Timeline (Realistic: 22 weeks / 5.5 months)

### Phase 1: Platform Foundation (Weeks 1-8 / Months 1-2)

**Month 1 (Weeks 1-4): Core Infrastructure**
- Week 1: Database schema (all tables), Azure setup, environment config
- Week 2: Authentication system (signup, login, email verification, password reset)
- Week 3: Multi-tenant architecture, company/user relationships, RBAC middleware
- Week 4: Onboarding flows (user details + company setup, invited user flow)

**Milestone 1:** Users can sign up, verify email, complete onboarding, log in with roles

**Month 2 (Weeks 5-8): Events, Team, Billing**
- Week 5: Events management (CRUD, event types, private events, activation windows)
- Week 6: Team collaboration (invite users, expired invite handling, role management)
- Week 7: Payment integration (Stripe), company billing, GST-compliant invoicing
- Week 8: Form publishing infrastructure, public URL generation, activation logic

**Milestone 2:** Can create company, events, invite team, handle billing/invoicing

---

### Phase 2: Form Builder Core (Weeks 9-14 / Months 3-3.5)

**Weeks 9-10: Basic Builder**
- Canvas workspace with fixed dimensions (1200x1600px)
- Component library (9 field types including Address)
- Drag-and-drop from library to canvas
- Component selection and deletion
- Basic properties panel (label, required, validation)
- Auto-save draft forms

**Weeks 11-12: Templates & Backgrounds**
- Template library (5-10 pre-built templates)
- Template selection and application
- Custom background upload (Azure Blob)
- Background resize/pan mode
- Background lock after first component added
- Canvas vs Screen rectangle (80% screen within canvas)

**Weeks 13-14: Component Framework & Styling**
- Form-level default settings (fonts, colors, label position)
- Component-level overrides
- Label/Input/Validation 3-part structure
- Horizontal vs Vertical stacking options
- Tab order management
- Visual tab order display toggle

**Milestone 3:** Can build forms with templates or custom backgrounds, style consistently

---

### Phase 3: Advanced Builder Features (Weeks 15-18 / Month 4)

**Weeks 15-16: Enhanced Interactions**
- Enhanced drag UX (open/closed hand cursors, ghost preview)
- Component fencing (cannot drag outside screen)
- Return-to-library if dropped outside screen
- Collision detection (component overlap prevention)
- Snap-to-grid with visual feedback
- Keyboard shortcuts (Delete, Ctrl+D duplicate, arrow keys nudge)

**Weeks 17-18: Undo/Redo & Rendering**
- Undo/Redo system (50 action history)
- Proportional scaling rendering engine
- Preview modes (desktop, tablet, mobile views)
- Aspect ratio handling (letterbox/crop for different ratios)
- WYSIWYG accuracy validation

**Milestone 4:** Form builder feature-complete, polished UX, accurate rendering

---

### Phase 4: Preview/Testing & Analytics (Weeks 19-20 / Month 5)

**Week 19: Preview & Testing System**
- Preview mode toggle (?preview=true URL parameter)
- Preview test counter and threshold enforcement
- Preview vs Production lead flagging
- Test audit logging (who tested, when)
- Company Admin test threshold settings
- Approver testing requirements

**Week 20: Analytics & Export**
- Analytics dashboard (real-time lead counts, preview vs production split)
- Submissions timeline chart
- Leads list with search/filter
- CSV export (multiple formats: Salesforce, Marketing Cloud, Emarsys)
- Preview lead deletion (individual and bulk)
- Usage analytics instrumentation (PostHog/Plausible integration)

**Milestone 5:** Testing workflow complete, analytics functional

---

### Phase 5: Polish & Launch (Weeks 21-22 / Month 5.5)

**Week 21: Polish & Bug Fixes**
- Fix critical bugs from testing
- Performance optimization (form load times, drag performance)
- Accessibility audit (WCAG 2.1 AA for public forms)
- Cross-browser testing (Chrome, Safari, Edge, Firefox)
- Tablet device testing (iPad, Surface, Android tablets)

**Week 22: Launch Preparation**
- Landing page with value proposition
- Pricing page
- Terms of Service and Privacy Policy (Australian compliance)
- Support email setup
- Domain registration and SSL
- 5 beta customer tests
- Soft launch preparation

**Milestone 6:** MVP COMPLETE - Ready for first paying customers

---

### Post-MVP Priorities (Month 6+)

**Phase 6 (Months 6-7):** Prize Draw Feature + CRM Integration
**Phase 7 (Months 8-9):** Address Validation (GeoScape), Custom Components per Company
**Phase 8 (Month 10+):** Event Types Pricing, Event Package Tier, Designer Marketplace

---

## Constraints & Assumptions

### Constraints
- **Solo founder:** No team, all development by Anthony
- **5.5-month realistic timeline:** Extended from original 3-month goal after full scope definition
- **6-month personal runway:** Must launch before funds run out
- **Bootstrap:** No external funding, personal runway only
- **Zero marketing budget:** Must rely on product quality and word-of-mouth
- **Agentic tools:** Using Cursor + BMAD (months of experience, still learning)
- **Complexity acknowledgment:** Level 3 project with sophisticated form builder and multi-tenant architecture

### Assumptions
- Azure + SQL Server infrastructure is sufficient for multi-tenant architecture
- Advanced form builder (drag-drop, undo/redo, proportional scaling) is achievable in 10 weeks
- Proportional scaling (Option 1) provides acceptable rendering quality across tablets
- $99 pricing is attractive vs $200 contractor baseline
- Event Types differential pricing will be defined during architecture phase
- Sydney events market is accessible via public event listings
- 30% conversion (drafts → published) is realistic after 5 preview tests
- Data quality >90% is achievable with validation + preview testing
- GeoScape API integration for Address field is straightforward (standard REST API)
- Preview testing requirement (5 tests) won't cause excessive friction
- Company Admins will test forms before publishing (compliance with approval workflow)

### Risks & Mitigations
- **Risk:** 5.5-month timeline exceeds 6-month personal runway (tight margin)
  - **Mitigation:** Disciplined scope management, no feature creep, weekly progress reviews
  - **Mitigation:** If ahead of schedule, add polish; if behind, cut nice-to-have features
  
- **Risk:** Technical complexity too high (undo/redo, proportional scaling, collision detection)
  - **Mitigation:** Proof-of-concept for critical features in Weeks 9-10, pivot if needed
  - **Mitigation:** Proportional scaling chosen over percentage positioning (saves 2 weeks)
  
- **Risk:** Preview testing requirement (5 tests) creates friction, reduces conversion
  - **Mitigation:** Company Admin can adjust threshold (even set to 0 if needed)
  - **Mitigation:** Monitor conversion impact, adjust based on data
  
- **Risk:** Form rendering breaks on non-iPad tablets (proportional scaling limitations)
  - **Mitigation:** Design for iPad (dominant event tablet), acceptable degradation on others
  - **Mitigation:** Can upgrade to full percentage positioning in Phase 6 if needed
  
- **Risk:** Can't acquire customers with zero marketing budget
  - **Mitigation:** Direct outreach to Sydney events, content marketing, referrals built into product
  
- **Risk:** Customers choose Google Forms (free) over $99 product
  - **Mitigation:** Custom backgrounds + advanced builder features differentiate significantly
  - **Mitigation:** Target customers who currently pay $200 to contractors
  
- **Risk:** Overlap prevention and collision detection too slow, impacts builder performance
  - **Mitigation:** Optimize algorithms, use spatial indexing, test performance early
  - **Mitigation:** Option to disable overlap prevention if performance issue
  
- **Risk:** GeoScape API costs for Address validation unsustainable
  - **Mitigation:** Monitor usage, implement caching, consider usage limits or variable pricing
  - **Mitigation:** Address field optional, most customers won't use it initially

---

## Australian Compliance & Legal Requirements

### Privacy & Data Protection

**Australian Privacy Principles (APPs):**
- Collect only necessary personal information
- Clear privacy policy explaining data collection and use
- Secure storage of personal information
- Right for individuals to access and correct their data
- Data breach notification requirements
- IP address hashing for privacy protection

**GDPR Alignment:**
- While focused on Australian market, maintain GDPR-compatible practices
- Data export capabilities (CSV export meets data portability requirements)
- Clear consent mechanisms for data collection

### Business & Tax Compliance

**Australian Business Number (ABN):**
- Collect and validate ABN format for company accounts
- Store ABN for invoicing purposes
- Display ABN on all invoices

**Goods and Services Tax (GST):**
- Include 10% GST in all pricing
- Display GST amount separately on invoices
- GST registration required if annual turnover exceeds $75,000
- Invoice must show: ABN, GST amount, total amount, invoice date

**Tax Invoice Requirements:**
- Invoice number (unique, sequential)
- Issue date
- Supplier details (company name, ABN)
- Customer details (company name, ABN, address)
- Description of goods/services
- GST amount
- Total amount payable

### Consumer Protection

**Australian Consumer Law (ACL):**
- Clear pricing with no hidden fees ($99 all-inclusive pricing)
- Refund policy (if form doesn't publish due to platform error)
- Terms of Service clearly stated
- No misleading or deceptive conduct in marketing

### Electronic Transactions

**Electronic Transactions Act:**
- Digital signatures for agreements
- Electronic invoicing legally valid
- Email receipts acceptable
- Secure payment processing (Stripe compliance)

### Accessibility (Future Consideration)

**Disability Discrimination Act:**
- Not strictly enforced for MVP but best practice
- WCAG 2.1 AA compliance goals for public forms
- Screen reader compatibility for published forms

---

## Dependencies

### External Services
- **Stripe:** Payment processing (must be approved for Australian merchants)
- **Azure:** Hosting, database, storage (already setup)
- **Email Service:** SendGrid or Azure Communication (for receipts, notifications)
- **Domain:** Need to register domain for public forms (e.g., `forms.eventlead.com`)

### Internal
- **Brainstorming Session Doc:** Reference for all product decisions (`docs/brainstorming-session-results-2025-10-10.md`)
- **Design System:** Need basic UI components (buttons, forms, modals)
- **Template Library:** Must create 5-10 professional templates before launch

---

## Definition of Done (MVP Launch Criteria)

### Must Have (Blocking)
- [ ] User can sign up and log in
- [ ] User can create draft forms with drag-and-drop
- [ ] User can upload custom background OR choose template
- [ ] User can preview form before publishing
- [ ] User can pay $99 and publish form
- [ ] Published form has public URL and accepts submissions
- [ ] Data validation prevents bad leads (>90% quality)
- [ ] User can view analytics dashboard with real-time data
- [ ] User can export leads to CSV (Salesforce format minimum)
- [ ] Payment flow works end-to-end with Stripe
- [ ] Forms are tablet-responsive
- [ ] System handles 100 concurrent form submissions without errors
- [ ] No data loss (submissions persist reliably)

### Nice to Have (Non-blocking)
- Multiple CSV format options (Marketing Cloud, Emarsys)
- Form duplication (copy previous event's form)
- Form editing after publish (update live form)
- User profile customization
- Receipt emails for payments

### Launch Checklist
- [ ] Landing page with clear value proposition
- [ ] 5 beta customers tested and provided feedback
- [ ] All critical bugs fixed
- [ ] Terms of Service and Privacy Policy published
- [ ] Stripe account approved and live
- [ ] Domain registered and SSL configured
- [ ] Support email setup (support@eventlead.com)
- [ ] Basic documentation (FAQ, how-to guides)

---

## Appendix

### Key Documents
- **Brainstorming Session:** `docs/brainstorming-session-results-2025-10-10.md` (strategy decisions)
- **Architecture:** `docs/architecture/v2-architecture.md` (if exists)
- **Observability:** Logging and monitoring requirements (lines 101-151 in old PRD - adapt for MVP)

### Archived Decisions
- **Previous PRD v2:** Had Day-Pass, Consumption, Reseller models + SKU catalog + Enterprise features
- **Decision:** Simplified to single "Create Free, Pay to Publish" model for MVP focus
- **Rationale:** Solo founder, 3-month timeline, need simplicity to ship

---

**Last Updated:** 2025-10-11  
**Next Review:** After MVP launch (Month 3)

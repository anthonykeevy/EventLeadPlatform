# Unified Form Workspace - Feature Specification

**Epic:** 3 - Form Builder & Logic Engine (or new Epic 4)  
**Domain:** Form Management, Access Control, User Experience  
**Status:** 📋 Specification Draft  
**Priority:** High  
**Estimated Complexity:** Large (Multi-Sprint)  

---

## 📖 Executive Summary

This specification defines a **Unified Form Workspace** that consolidates all form-related functionality into a single, tabbed interface. The workspace replaces the current fragmented experience (separate modals and pages) with a cohesive, access-controlled environment where users can view, design, configure, and analyze forms based on their access level.

### Key Benefits

1. **Unified Experience**: Single entry point for all form operations
2. **Access-Aware UI**: Tabs and features dynamically adapt to user's access level
3. **Deep Linking**: Shareable URLs to specific workspace tabs
4. **View-Only Mode**: Users with VIEW access can inspect forms without edit capability
5. **Seamless Transitions**: No modal juggling; smooth tab navigation

---

## 📖 User Stories

### Primary User Story

**As a** Platform User (Company Admin, Company User, or Company Viewer),  
**I want to** access all form-related functions from a single workspace interface,  
**So that** I can efficiently manage, design, and analyze forms without navigating between multiple modals and pages.

### Supporting User Stories

**As a** User with VIEW access,  
**I want to** inspect form design and properties in read-only mode,  
**So that** I can understand the form structure without accidentally modifying it.

**As a** User with EDIT access,  
**I want to** seamlessly switch between overview, design, and settings,  
**So that** I can make comprehensive form updates in a single session.

**As a** User with MANAGE access,  
**I want to** control who can access my form from the same interface where I design it,  
**So that** I can manage both content and permissions efficiently.

**As a** Manager granting access,  
**I want** my team member to simply refresh their page to gain new access,  
**So that** access changes take effect immediately without re-navigation.

---

## 🧭 Scope Boundary

### In Scope

1. **Form Workspace Page** (`/forms/:formId/*`)
   - Tabbed interface with Overview, Design, Settings, Access, Analytics tabs
   - Access-level-aware tab visibility and functionality
   - Consistent header with form name, access badge, and navigation

2. **Access Check Integration**
   - API call on workspace load to determine access level
   - Tab-level access enforcement
   - Proper 403/404 handling for unauthorized access
   - Refresh-to-update access level

3. **View-Only Mode for Design Tab**
   - Component selection enabled (to view properties)
   - Resize/drag handles disabled
   - Toolbox (component palette) hidden
   - Properties panel inputs disabled (read-only display)
   - Save button hidden
   - Preview button functional

4. **Dashboard Integration**
   - Enhanced form cards with clickable zones
   - Zones navigate to specific workspace tabs
   - Access level badge displayed on form cards

5. **URL Structure**
   - Nested routes: `/forms/:formId/overview`, `/forms/:formId/design`, etc.
   - Deep linking support for sharing specific tabs
   - Browser back/forward navigation between tabs

6. **Tab Content Migration**
   - Overview tab: Current `FormDetailView` content
   - Design tab: Current `BuilderPage` content (form builder)
   - Settings tab: Current `EditFormModal` content + form configuration
   - Access tab: Current `FormAccessControlModal` content
   - Analytics tab: Placeholder for future analytics dashboard

### Out of Scope

1. **New Analytics Features** - Analytics tab will be placeholder; full analytics is a separate story
2. **Form Templates** - Template selection/management is a separate feature
3. **Form Versioning UI** - Version history browser (already in builder, stays there)
4. **Multi-Form Operations** - Bulk form actions remain on dashboard
5. **Real-time Collaboration** - Multi-user concurrent editing
6. **Mobile-Responsive Workspace** - Initial focus on desktop; mobile optimization later

---

## 🎯 Functional Requirements

### 1. Workspace Layout & Navigation

#### 1.1 Page Structure

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ WORKSPACE HEADER                                                                 │
│ ┌──────────────────────────────────────────────────────────────────────────────┐ │
│ │ ← Back to Dashboard    Form: {formName}              [ACCESS BADGE] [?] [⚙️] │ │
│ └──────────────────────────────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────────────────────┤
│ TAB BAR                                                                          │
│ ┌──────────────────────────────────────────────────────────────────────────────┐ │
│ │  [📋 Overview]  [🎨 Design]  [⚙️ Settings]  [🔐 Access]  [📊 Analytics]      │ │
│ │       ↑ Active tab highlighted                                               │ │
│ └──────────────────────────────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────────────────────┤
│ TAB CONTENT AREA                                                                 │
│ ┌──────────────────────────────────────────────────────────────────────────────┐ │
│ │                                                                              │ │
│ │                     Content varies by active tab                             │ │
│ │                                                                              │ │
│ └──────────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────────┘
```

#### 1.2 Header Components

| Element | Description | Behavior |
|---------|-------------|----------|
| Back Button | "← Back to Dashboard" | Navigate to dashboard, preserving company/event context |
| Form Name | Display form name | Editable inline for EDIT/MANAGE access |
| Access Badge | Show current user's access level | Tooltip explains access level |
| Help Button | "?" icon | Opens contextual help for current tab |
| Settings Menu | "⚙️" icon | Quick actions: Duplicate, Export, Delete (MANAGE only) |

#### 1.3 Tab Bar

| Tab | Icon | URL Segment | Description |
|-----|------|-------------|-------------|
| Overview | 📋 | `/overview` | Form status, activity, metrics, audit trail |
| Design | 🎨 | `/design` | Form builder (canvas, components, properties) |
| Settings | ⚙️ | `/settings` | Form configuration, metadata, workflow settings |
| Access | 🔐 | `/access` | Access control management |
| Analytics | 📊 | `/analytics` | Submission analytics and reports |

### 2. Access Control Integration

#### 2.1 Access Check Flow

```
User navigates to /forms/44/design
         │
         ▼
┌─────────────────────────────┐
│  API: GET /api/forms/44/    │
│        access/check         │
└─────────────────────────────┘
         │
         ▼
    ┌────┴────┐
    │ Access? │
    └────┬────┘
         │
    ┌────┴────────────────────────────────┐
    │                                     │
    ▼                                     ▼
 No Access                           Has Access
    │                                     │
    ▼                                     ▼
┌─────────────────┐         ┌─────────────────────────┐
│ Access Denied   │         │ Check tab permission    │
│ Page (403)      │         │ based on access level   │
│ - No form info  │         └─────────────────────────┘
│ - Contact owner │                   │
└─────────────────┘              ┌────┴────┐
                                 │Tab OK?  │
                                 └────┬────┘
                                      │
                            ┌─────────┴─────────┐
                            │                   │
                            ▼                   ▼
                       Tab Allowed         Tab Forbidden
                            │                   │
                            ▼                   ▼
                    ┌───────────────┐   ┌────────────────┐
                    │ Render tab    │   │ Redirect to    │
                    │ with access   │   │ /overview      │
                    │ mode applied  │   └────────────────┘
                    └───────────────┘
```

#### 2.2 Tab Visibility Matrix

| Tab | VIEW | SUBMIT | ANALYZE | EDIT | MANAGE |
|-----|------|--------|---------|------|--------|
| Overview | ✅ Read-only | ✅ Read-only | ✅ + Metrics | ✅ Read-only | ✅ Full |
| Design | ✅ View-only | ✅ View-only | ✅ View-only | ✅ Full edit | ✅ Full edit |
| Settings | ❌ Hidden | ❌ Hidden | ❌ Hidden | ✅ Editable | ✅ Full |
| Access | ❌ Hidden | ❌ Hidden | ❌ Hidden | ❌ Hidden | ✅ Full |
| Analytics | ❌ Hidden | ❌ Hidden | ✅ Full | ❌ Hidden | ✅ Full |

#### 2.3 View-Only Mode (Design Tab)

When user has VIEW, SUBMIT, or ANALYZE access:

| Feature | Behavior |
|---------|----------|
| Toolbox (Component Palette) | Hidden |
| Canvas | Visible, non-interactive for drag/resize |
| Component Selection | **Enabled** - click to view properties |
| Resize Handles | Hidden |
| Drag Handles | Disabled |
| Properties Panel | Visible, all inputs **disabled** |
| Save Button | Hidden |
| Preview Button | **Visible and functional** |
| View Mode Banner | Displayed: "🔒 View Only - You have {level} access" |

#### 2.4 Access Refresh Behavior

- Access level is checked on:
  - Initial workspace load
  - Tab navigation (via route change)
  - Manual page refresh
- If access is upgraded (e.g., VIEW → EDIT):
  - User refreshes page
  - New access level is fetched
  - UI updates to reflect new permissions (tabs appear, edit mode enabled)
- LocalStorage is NOT used for access caching (always fetch from API)

### 3. Dashboard Form Card Enhancement

#### 3.1 Clickable Zones

```
┌──────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│  ┌─────────────────┐  ┌────────────────────────────────────────────────┐ │
│  │                 │  │ ZONE A: Form Title & Description               │ │
│  │  ZONE B:        │  │ Click → /forms/{id}/overview                   │ │
│  │  Thumbnail      │  ├────────────────────────────────────────────────┤ │
│  │  Click →        │  │ ZONE C: Status       │ ZONE D: Analytics       │ │
│  │  /forms/{id}/   │  │ ✅ Published         │ 📊 1,234 submissions    │ │
│  │  design         │  │ Click → /overview    │ Click → /analytics      │ │
│  │                 │  ├────────────────────────────────────────────────┤ │
│  │                 │  │ ZONE E: Access Summary               [MANAGE]  │ │
│  │                 │  │ 🔐 3 users have access                         │ │
│  │                 │  │ Click → /forms/{id}/access                     │ │
│  └─────────────────┘  └────────────────────────────────────────────────┘ │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

#### 3.2 Zone Definitions

| Zone | Content | Click Action | Visibility by Access Level |
|------|---------|--------------|---------------------------|
| A - Title/Desc | Form name, description | → `/forms/{id}/overview` | All |
| B - Thumbnail | Form preview image | → `/forms/{id}/design` | All |
| C - Status | Form status, approval status | → `/forms/{id}/overview` | All |
| D - Analytics | Submission count, last activity | → `/forms/{id}/analytics` | ANALYZE, MANAGE |
| E - Access | User/company count with access | → `/forms/{id}/access` | MANAGE only |
| Badge | Access level indicator | Tooltip | All |

#### 3.3 Access-Based Card Variants

**VIEW Access Card:**
```
┌─────────────────────────────────────────────────────────────────┐
│ [Thumbnail] │ Form Name                              [VIEW]    │
│             │ Description...                                   │
│             ├─────────────────────────────────────────────────┤
│             │ ✅ Published  ✅ Approved                         │
└─────────────────────────────────────────────────────────────────┘
```

**MANAGE Access Card:**
```
┌─────────────────────────────────────────────────────────────────┐
│ [Thumbnail] │ Form Name                            [MANAGE]    │
│             │ Description...                                   │
│             ├───────────────────────┬─────────────────────────┤
│             │ ✅ Published          │ 📊 1,234 submissions    │
│             │ ✅ Approved           │ 📈 Last: 2 hours ago    │
│             ├───────────────────────┴─────────────────────────┤
│             │ 🔐 3 users, 2 companies              [Manage →] │
└─────────────────────────────────────────────────────────────────┘
```

### 4. URL Routing Structure

#### 4.1 Route Definitions

```typescript
const formWorkspaceRoutes = [
  // Base route redirects to overview
  {
    path: '/forms/:formId',
    element: <Navigate to="overview" replace />
  },
  
  // Tab routes
  {
    path: '/forms/:formId/overview',
    element: <FormWorkspace defaultTab="overview" />
  },
  {
    path: '/forms/:formId/design',
    element: <FormWorkspace defaultTab="design" />
  },
  {
    path: '/forms/:formId/settings',
    element: <FormWorkspace defaultTab="settings" />
  },
  {
    path: '/forms/:formId/access',
    element: <FormWorkspace defaultTab="access" />
  },
  {
    path: '/forms/:formId/analytics',
    element: <FormWorkspace defaultTab="analytics" />
  },
  
  // Legacy route redirect (backwards compatibility)
  {
    path: '/forms/:formId/builder',
    element: <Navigate to="../design" replace />
  }
];
```

#### 4.2 Navigation Behavior

| Action | Result |
|--------|--------|
| Click tab | Route changes to `/forms/{id}/{tab}` |
| Browser back | Returns to previous tab (or dashboard) |
| Browser forward | Goes to next tab in history |
| Direct URL access | Opens specific tab after access check |
| Refresh | Re-checks access, reloads current tab |

### 5. Tab Content Specifications

#### 5.1 Overview Tab

**Source:** Migrate from `FormDetailView.tsx`

**Sections:**
1. Form Identity
   - Form name (editable for EDIT/MANAGE)
   - Description (editable for EDIT/MANAGE)
   - Created by / Created date
   - Last updated / Updated by

2. Status & Workflow
   - Form status badge
   - Approval status badge
   - Publish/Submit for Approval actions (access-dependent)

3. Activity Metrics
   - Total submissions
   - Demo leads collected
   - Production leads collected
   - Last submission date
   - Last activity date

4. Deployment Info
   - Deployment cost
   - Thumbnail URL
   - Preview URL
   - Public access toggle

5. Audit Trail (collapsed by default)
   - Creation details
   - Last update details
   - "View Full Audit Report" button (MANAGE only)

#### 5.2 Design Tab

**Source:** Migrate from `BuilderPage.tsx`

**Layout:**
```
┌──────────────────────────────────────────────────────────────────────────┐
│ TOOLBAR                                                                  │
│ [Undo] [Redo] [Device: Desktop ▼] [Grid: On] [Preview] [Save Draft]     │
├────────────┬────────────────────────────────────────────┬────────────────┤
│  TOOLBOX   │               CANVAS                       │  PROPERTIES    │
│            │                                            │                │
│ [Search]   │  ┌────────────────────────────────────┐   │  Component:    │
│            │  │                                    │   │  [First Name]  │
│ [Fields]   │  │     Form Canvas                    │   │                │
│ • Text     │  │     (Absolute positioning)         │   │  ┌──────────┐  │
│ • Email    │  │                                    │   │  │ General  │  │
│ • Phone    │  │                                    │   │  ├──────────┤  │
│ ...        │  │                                    │   │  │ Styling  │  │
│            │  │                                    │   │  ├──────────┤  │
│ [Layout]   │  └────────────────────────────────────┘   │  │ Logic    │  │
│ • Divider  │                                            │  └──────────┘  │
│            │                                            │                │
└────────────┴────────────────────────────────────────────┴────────────────┘
```

**View-Only Mode Modifications:**
- Toolbox: Hidden (entire left sidebar)
- Canvas: Selection allowed, resize/drag disabled
- Properties: Visible but all inputs disabled
- Toolbar: Only Preview visible; Undo/Redo/Save hidden

#### 5.3 Settings Tab

**Source:** Migrate and expand from `EditFormModal.tsx`

**Sections:**
1. Basic Information
   - Form name*
   - Form description
   - Event association

2. Status & Workflow
   - Form status dropdown
   - Approval status (Admin only)
   - Deployment cost (Admin only)

3. Publishing Options
   - Public access toggle
   - Preview URL generation
   - Thumbnail URL

4. Validation & Behavior (New)
   - Client-side validation settings
   - Submission behavior
   - Confirmation message

5. Advanced (collapsed)
   - Export name configuration
   - Schema version info

#### 5.4 Access Tab

**Source:** Migrate from `FormAccessControlModal.tsx`

**Layout:**
```
┌──────────────────────────────────────────────────────────────────────────┐
│ ACCESS CONTROL                                                           │
├──────────────────────────────────────────────────────────────────────────┤
│ ┌──────────────────────────────────────────────────────────────────────┐ │
│ │ GRANT ACCESS                                            [+ Grant]   │ │
│ │ ┌─────────────────┐  ┌─────────────────┐  ┌───────────────────────┐ │ │
│ │ │ Search User/Co  │  │ Access Level ▼  │  │ Relationship Type ▼  │ │ │
│ │ └─────────────────┘  └─────────────────┘  └───────────────────────┘ │ │
│ └──────────────────────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────────────┤
│ CURRENT ACCESS LIST                                                      │
│ ┌──────────────────────────────────────────────────────────────────────┐ │
│ │ 👤 John Smith (john@company.com)                                     │ │
│ │    Access: EDIT  │  Granted by: Admin  │  Date: Jan 10, 2026  [🗑️] │ │
│ ├──────────────────────────────────────────────────────────────────────┤ │
│ │ 🏢 Partner Agency Ltd                                                │ │
│ │    Access: VIEW  │  Relationship: Partner  │  Date: Jan 5, 2026 [🗑️]│ │
│ └──────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────┘
```

#### 5.5 Analytics Tab (Placeholder)

**Initial Implementation:**
- Display placeholder message: "Analytics coming soon"
- Show basic metrics (already in Overview)
- Link to export submissions

**Future Scope (separate story):**
- Submission trends chart
- Completion rate analytics
- Field-level analytics
- Export options

---

## ✅ Acceptance Criteria

### Phase 1: Core Workspace Structure

- [ ] **AC-1.1:** Form Workspace page exists at `/forms/:formId/*` with tab navigation
- [ ] **AC-1.2:** Tab bar displays all five tabs with appropriate icons
- [ ] **AC-1.3:** Clicking tab changes route and renders corresponding content
- [ ] **AC-1.4:** Browser back/forward navigates between tabs correctly
- [ ] **AC-1.5:** Workspace header displays form name and back button

### Phase 2: Access Control Integration

- [ ] **AC-2.1:** Access check API called on workspace load
- [ ] **AC-2.2:** 403/404 errors display Access Denied page with no form information
- [ ] **AC-2.3:** Tabs are hidden/shown based on access level per matrix
- [ ] **AC-2.4:** Accessing restricted tab via URL redirects to Overview
- [ ] **AC-2.5:** Access badge displays current user's access level
- [ ] **AC-2.6:** Page refresh re-checks access and updates UI accordingly

### Phase 3: View-Only Mode (Design Tab)

- [ ] **AC-3.1:** View-only banner displays for VIEW/SUBMIT/ANALYZE access
- [ ] **AC-3.2:** Toolbox is hidden for view-only users
- [ ] **AC-3.3:** Component selection works in view-only mode
- [ ] **AC-3.4:** Resize and drag handles are disabled
- [ ] **AC-3.5:** Properties panel displays values but inputs are disabled
- [ ] **AC-3.6:** Save button is hidden; Preview button is visible and functional

### Phase 4: Dashboard Integration

- [ ] **AC-4.1:** Form cards display clickable zones as specified
- [ ] **AC-4.2:** Clicking thumbnail navigates to Design tab
- [ ] **AC-4.3:** Clicking status area navigates to Overview tab
- [ ] **AC-4.4:** Analytics zone visible only for ANALYZE/MANAGE access
- [ ] **AC-4.5:** Access zone visible only for MANAGE access
- [ ] **AC-4.6:** Access level badge displays on all form cards

### Phase 5: Tab Content Migration

- [ ] **AC-5.1:** Overview tab contains all FormDetailView functionality
- [ ] **AC-5.2:** Design tab contains full BuilderPage functionality
- [ ] **AC-5.3:** Settings tab contains EditFormModal functionality plus form config
- [ ] **AC-5.4:** Access tab contains FormAccessControlModal functionality
- [ ] **AC-5.5:** Analytics tab displays placeholder with basic metrics

### Phase 6: Security & Stability

- [ ] **AC-6.1:** Unauthorized form access returns 403 with no form data leaked
- [ ] **AC-6.2:** Non-existent form returns 404 with generic message
- [ ] **AC-6.3:** All edit operations verify access before saving
- [ ] **AC-6.4:** View-only mode cannot submit any edit operations

---

## 🛠️ Technical Notes

### Component Architecture

```
src/features/forms/
├── components/
│   ├── workspace/
│   │   ├── FormWorkspace.tsx         # Main workspace container
│   │   ├── WorkspaceHeader.tsx       # Header with form name, access badge
│   │   ├── WorkspaceTabBar.tsx       # Tab navigation
│   │   ├── AccessDeniedPage.tsx      # 403/404 display
│   │   └── tabs/
│   │       ├── OverviewTab.tsx       # Overview content
│   │       ├── DesignTab.tsx         # Builder wrapper
│   │       ├── SettingsTab.tsx       # Settings form
│   │       ├── AccessTab.tsx         # Access control
│   │       └── AnalyticsTab.tsx      # Analytics (placeholder)
│   └── FormCard/
│       ├── FormCard.tsx              # Enhanced card with zones
│       ├── FormCardZone.tsx          # Individual clickable zone
│       └── AccessBadge.tsx           # Access level badge
├── hooks/
│   ├── useFormAccess.ts              # Access check hook
│   ├── useWorkspaceNavigation.ts     # Tab navigation hook
│   └── useFormData.ts                # Form data fetching
├── pages/
│   └── FormWorkspacePage.tsx         # Route component
└── types/
    └── workspace.types.ts            # TypeScript types
```

### State Management

```typescript
// Workspace state (Zustand store or React Context)
interface WorkspaceState {
  formId: string;
  formData: FormData | null;
  accessLevel: AccessLevel | null;
  activeTab: WorkspaceTab;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  loadForm: (formId: string) => Promise<void>;
  checkAccess: (formId: string) => Promise<AccessLevel>;
  setActiveTab: (tab: WorkspaceTab) => void;
  refreshAccess: () => Promise<void>;
}

type AccessLevel = 'VIEW' | 'SUBMIT' | 'ANALYZE' | 'EDIT' | 'MANAGE';
type WorkspaceTab = 'overview' | 'design' | 'settings' | 'access' | 'analytics';
```

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/forms/{id}/access/check` | GET | Check current user's access level |
| `/api/forms/{id}` | GET | Get form metadata and data |
| `/api/forms/{id}/definition` | GET | Get form definition (for builder) |
| `/api/forms/{id}` | PATCH | Update form metadata |
| `/api/forms/{id}/access` | GET | List access control entries |
| `/api/forms/{id}/access` | POST | Grant access |
| `/api/forms/{id}/access/{id}` | DELETE | Revoke access |

### Migration Strategy

1. **Phase 1:** Create workspace shell with routing; tabs render placeholders
2. **Phase 2:** Add access checking; implement tab visibility matrix
3. **Phase 3:** Migrate Overview tab from FormDetailView
4. **Phase 4:** Integrate existing Builder into Design tab with view-only mode
5. **Phase 5:** Migrate Settings tab from EditFormModal
6. **Phase 6:** Migrate Access tab from FormAccessControlModal
7. **Phase 7:** Update dashboard form cards with clickable zones
8. **Phase 8:** Remove legacy modals and routes; update all navigation

---

## 📋 Dependencies

### Existing Components (to be migrated/wrapped)

- `FormDetailView.tsx` → Overview Tab
- `BuilderPage.tsx` → Design Tab
- `EditFormModal.tsx` → Settings Tab
- `FormAccessControlModal.tsx` → Access Tab

### APIs (existing)

- `checkFormAccess()` - Form access check
- `getForm()` - Form metadata
- `updateForm()` - Form updates
- `getFormAccessList()` - Access entries
- `grantFormAccess()` - Grant access
- `revokeFormAccess()` - Revoke access

### Access Control Matrix

- `docs/ACCESS-CONTROL-MATRIX.md` - Reference for access levels

---

## 📚 Related Documentation

- `docs/ACCESS-CONTROL-MATRIX.md` - Access control rules
- `docs/FORM-ACCESS-RELATIONSHIP-TYPES.md` - Relationship types
- `docs/COMPONENT-FRAMEWORK-REFERENCE.md` - Component architecture
- `docs/stories/story-3.8.md` - Public Form Renderer

---

## 📋 Implementation Phases

### Phase 1: Workspace Shell (Sprint 1)
**Effort:** Medium

- Create FormWorkspace component structure
- Implement routing with tab navigation
- Add basic access check on load
- Display placeholder content in each tab

### Phase 2: Access Control (Sprint 1)
**Effort:** Medium

- Implement tab visibility matrix
- Add Access Denied page
- Add access badge to header
- Handle refresh-to-update-access

### Phase 3: Design Tab with View-Only (Sprint 1-2)
**Effort:** Large

- Integrate existing builder into Design tab
- Implement view-only mode modifications
- Add view-only banner
- Hide toolbox for view-only users

### Phase 4: Overview Tab (Sprint 2)
**Effort:** Small

- Migrate FormDetailView content
- Update styling for tab context
- Remove modal wrapper

### Phase 5: Settings Tab (Sprint 2)
**Effort:** Medium

- Migrate EditFormModal content
- Add form configuration options
- Remove modal wrapper

### Phase 6: Access Tab (Sprint 2)
**Effort:** Small

- Migrate FormAccessControlModal content
- Update styling for tab context
- Remove modal wrapper

### Phase 7: Dashboard Integration (Sprint 3)
**Effort:** Medium

- Redesign form cards with clickable zones
- Add access-based zone visibility
- Update navigation to workspace routes

### Phase 8: Cleanup & Polish (Sprint 3)
**Effort:** Small

- Remove legacy modals
- Update all navigation paths
- Add legacy route redirects
- Final testing

---

## 🧪 UAT Test Scenarios

### Scenario 1: Access Level Display
1. Login as Company User (VIEW access to form)
2. Navigate to form via dashboard
3. Verify access badge shows "VIEW"
4. Verify only Overview and Design tabs visible
5. Verify view-only banner in Design tab

### Scenario 2: Tab Navigation
1. Login with MANAGE access
2. Open form workspace
3. Navigate through all tabs
4. Use browser back/forward
5. Verify correct tab renders

### Scenario 3: Access Upgrade
1. Login as user with VIEW access
2. Open form Design tab (view-only mode)
3. Have admin grant EDIT access
4. Refresh page
5. Verify Design tab is now editable

### Scenario 4: Unauthorized Access
1. Attempt to access `/forms/999/design` (no access)
2. Verify Access Denied page
3. Verify no form information displayed
4. Verify "Contact owner" message shown

### Scenario 5: Dashboard Clickable Zones
1. Login with MANAGE access
2. Click form thumbnail → verify Design tab opens
3. Click status area → verify Overview tab opens
4. Click access summary → verify Access tab opens

---

## ✅ Completion Criteria

- [ ] All Acceptance Criteria are completed
- [ ] All UAT Test Scenarios pass
- [ ] Legacy modals removed or deprecated
- [ ] All routes properly redirected
- [ ] No console errors or TypeScript warnings
- [ ] Access control matrix updated if needed
- [ ] Documentation updated

---

## 📝 Notes & Decisions

### Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| Jan 2026 | Use nested routes (Option B) | Deep linking, browser navigation, access control per tab |
| Jan 2026 | Keep action icons on form cards | Users expect quick actions; zones are enhancement |
| Jan 2026 | Include form configuration in Settings | Centralize all form settings in one place |
| Jan 2026 | Allow component selection in view-only | Users need to inspect properties |

### Open Questions

1. Should Analytics tab have a minimum viable implementation or remain placeholder?
2. Should we add a "Request Access" button for VIEW users in restricted tabs?
3. Should form name be editable inline in the header or only in Settings?

---

## ✅ Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jan 2026 | AI Assistant | Initial specification |

# Story 5.2: UX Expert Consultation — Company Form Defaults

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Consultants:** Sally (UX Expert) + John (PM)  
**Created:** 2026-02-13  
**Status:** Draft for Review  

---

## Executive Summary

This document captures the UX design resulting from PM review of Story 5.2, refined in consultation with the UX Expert. It defines the Company Defaults page, inheritance model, entry points, builder integration, and audit trail UX.

---

## 1. Inheritance Model (Refined)

**Model:** Global Defaults → Company Defaults → Form Overrides → Component Overrides

| Tier | Scope | Managed Where | Purpose |
|------|-------|---------------|---------|
| **Global Defaults** | Platform-wide | System config / Admin (future) | Baseline for all companies |
| **Company Defaults** | Per company | Company Settings → Form Branding Defaults | Set once for all forms in the company |
| **Form Overrides** | Per form | Builder → Global Properties Panel | Override company defaults for a specific form |
| **Component Overrides** | Per component | Builder → Component Properties | Override for individual fields/widgets |

**Resolution order:** When rendering or building, the resolver applies (lowest specificity wins for overrides):  
`Global → Company (overrides Global) → Form (overrides Company) → Component (overrides Form)`.

---

## 2. Entry Point: Company Settings

- **Location:** Dashboard → Company container (company card/header) → **Cog icon** opens Company Settings.
- **Company Settings** is a dedicated area (modal, side panel, or page) containing:
  - General company settings (existing)
  - **Form Branding Defaults** — new section/page for Story 5.2

**Flow:** User clicks cog → Company Settings opens → "Form Branding Defaults" (or "Form Defaults") link/section → navigates to the Company Defaults management page.

---

## 3. Company Defaults Page — Content and Layout

The Company Defaults page must mirror the builder experience so admins configure exactly what forms will inherit. It includes:

### 3.1 Global Properties Controls (Exact Reuse)

Place the **exact same controls** as the Builder’s **Global Properties Panel** on this page:

| Control Category | Example Properties | Notes |
|------------------|-------------------|-------|
| **Theme / Colors** | Primary color, background color, accent | Color pickers |
| **Typography** | Font family, base font size, heading/body font | Font selectors, number inputs |
| **Spacing** | Padding, margins, component spacing | Number inputs, units |
| **Background** | Background asset (from Story 5.1) | Asset picker (upload/select) |
| **Other global styles** | Border radius, shadows (if in scope) | Per current builder schema |

**Implementation note:** Reuse the same React components or a shared design-system layer as the Global Properties Panel to ensure parity and consistency.

### 3.2 Toolbox Components — Visual Guide

Place the **exact components from the Toolbox Panel** on the page as a **read-only visual guide** (not draggable or interactive):

- **Purpose:** Show admins what each component type looks like with the current company defaults applied.
- **Behavior:** Live preview of Text, Number, Select, Email, Phone, etc., styled with the company defaults.
- **Layout:** Grid or list of component thumbnails/previews, updated in real time as defaults change.

**Rationale:** Admins can see “this is how my forms will look” without opening the builder.

---

## 4. Builder Integration

### 4.1 Global Properties Panel — "Save to Company Defaults"

- **Control:** A button in the Global Properties Panel: **"Save to Company Defaults"** (or "Promote to Company Defaults").
- **Behavior:**
  - When clicked: Take the **current form’s form-level overrides** (i.e., what is in the Global Properties Panel for this form) and save them as the **company defaults**.
  - Confirmation: "Save current form style as company default? Existing company defaults will be replaced. All forms without overrides will inherit these settings."
  - Success: Toast + optional link to "View in Company Settings".
- **Visibility:** Only for users with Company Admin (or equivalent) permission.
- **Edge case:** If form has no overrides (fully inherited), the button could either:
  - Be disabled with tooltip: "No form overrides to save. Change properties above first."
  - Or save the current *resolved* values (company + global) as new company defaults.

### 4.2 Inherited vs Overridden (Existing Story 5.2 Scope)

- Show inherited values (read-only) with an "Override" action.
- Link: "Edit company defaults" → opens Company Settings → Form Branding Defaults (or deep link to Company Defaults page).

---

## 5. Audit Trail UX

- **Location:** Company Settings → Form Branding Defaults → **"Change history"** or **"Audit trail"** tab/section.
- **Content:** List of changes with:
  - Timestamp (UTC, display in user’s timezone)
  - User (who made the change)
  - Version or change summary (e.g., "Primary color updated")
  - Optional: "View version" to see full snapshot at that point in time.
- **Access:** Company Admin only.

---

## 6. User Journeys

### Journey A: Admin sets company defaults (first time)

1. Admin opens Dashboard → clicks cog on company → Company Settings.
2. Selects "Form Branding Defaults".
3. Sees Company Defaults page: Global Properties controls + Toolbox visual guide.
4. Configures colors, fonts, spacing, background.
5. Sees live preview of components.
6. Clicks "Save". Version created; audit entry recorded.

### Journey B: Builder promotes form overrides to company defaults

1. Admin opens Builder for a form.
2. Customizes form styles in Global Properties Panel (override company defaults).
3. Clicks "Save to Company Defaults".
4. Confirms. Company defaults updated; audit trail updated.
5. All other forms without overrides now inherit the new company defaults.

### Journey C: Admin reviews change history

1. Admin opens Company Settings → Form Branding Defaults.
2. Clicks "Change history" / "Audit trail".
3. Sees list of changes with timestamp, user, summary.
4. Optionally views a past version snapshot.

---

## 7. Out of Scope (This Story)

- **Global Defaults management UI:** Global Defaults are system/platform level. Story 5.2 focuses on Company Defaults. Global Defaults may be config-only or managed in a future admin surface.
- **APIs for defaults:** Per PM, add to backlog: APIs for Form Builder to fetch Company and Global Defaults from backend instead of hardcoded frontend values. Not in Story 5.2 scope.

---

## 8. Open Questions (To Resolve in Implementation)

1. **Global Defaults source:** Where do Global Defaults live today? Config? Seed data? Need alignment with Data Model.
2. **Component preview granularity:** Should the Toolbox guide show all component types or a subset?
3. **"Save to Company Defaults" when no overrides:** Preferred behavior (disabled vs save resolved values)?

---

*UX Expert Consultation — prepared with PM input*  
*Last Updated: 2026-02-13*

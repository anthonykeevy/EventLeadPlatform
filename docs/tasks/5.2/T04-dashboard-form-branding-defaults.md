# Task T04: Dashboard — Form Branding Defaults Page

**Story:** 5.2 - Company Form Defaults (Brand System)  
**Task ID:** T04  
**Status:** ✅ Done
**Dependencies:** T02  
**Estimated Time:** 2–3 hours  

---

## 📋 Task Overview

**Objective:** Add Form Branding Defaults page to Company Settings. Entry: Dashboard → Company container (cog) → Company Settings → "Form Branding Defaults". Page contains Global Properties controls + Toolbox components as visual guide (live preview). Includes audit trail (version history).

---

## ✅ Scope (In)

- [x] New route/page: Company Settings → Form Branding Defaults
- [x] Controls matching Global Properties Panel (theme, globalStyles, canvasSettings)
- [x] Toolbox components as visual guide (live preview)
- [x] Load defaults via GET `/api/companies/{id}/form-defaults`
- [x] Save via PUT `/api/companies/{id}/form-defaults`
- [x] Audit trail: version history viewable (GET history endpoint)
- [x] Access: Company Admin only

---

## 🚫 Scope (Out)

- ❌ Builder changes (T05)
- ❌ Global Defaults screen (Epic 5 backlog)

---

## ✅ Acceptance Criteria

### AC1: Page exists and is reachable
- Entry path: Dashboard → Company container → Company Settings → Form Branding Defaults

### AC2: Controls match Global Properties Panel
- Theme (primaryColor, backgroundColor, fontFamily)
- GlobalStyles (typography, spacing, label/input defaults)
- Canvas settings

### AC3: Toolbox preview visible
- Live preview of toolbox components using current defaults

### AC4: Save persists to company defaults
- PUT succeeds; version history updated

### AC5: Audit trail viewable
- Version history with who, when, what

---

## 📚 References

- `docs/stories/STORY-5.2-UX-EXPERT-CONSULTATION.md`
- `docs/COMPONENT-FRAMEWORK-REFERENCE.md`

---

## 🌿 Git

- Branch: `task/5.2/T04-dashboard-form-branding-defaults`
- PR into: `story/epic5-5.2-company-form-defaults`

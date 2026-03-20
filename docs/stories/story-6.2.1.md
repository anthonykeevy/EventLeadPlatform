# Story 6.2.1 — Component Library Expansion

**Epic:** 6 — AI Generation & Monetization Engine  
**Story ID:** 6.2.1  
**Title:** Component Library Expansion  
**Status:** In Progress  
**Branch:** `story/epic6-6.2.1-component-library-expansion`  
**PR:** #54  
**Depends On:** Story 6.2 (✅ Complete)  
**Blocks:** Story 6.3 (AI Context Uplift & Benchmark Baseline)  
**Created:** 2026-03-20  
**PM Decisions Source:** User prompt + STORY-6.2-CLOSEOUT-REPORT.md §2

---

## 1) Goal

Expand the form builder component library by adding two new component types (`url`, `rating`) and promoting one existing-but-unregistered type (`paragraph`) to full first-class status. Every new/promoted component must be fully integrated across all layers: types, registry, structure defaults, drag preview, properties panel, backend enum, and validator acceptance. Update the COMPONENT-FRAMEWORK-GUIDE.md with a complete component inventory covering ALL registered components.

---

## 2) In Scope

### 2.1 New Components (2)

| Component | Purpose | Key Props |
|-----------|---------|-----------|
| `url` | URL/website input | Built-in URL validation (pattern, protocol prefix) |
| `rating` | Star/number/emoji rating scale | `ratingMax` (5 or 10), `ratingStyle` ("stars", "numbers", "emoji") |

### 2.2 Promoted Component (1)

| Component | Current State | Promotion Work |
|-----------|--------------|----------------|
| `paragraph` | In `ComponentType` union + backend enum, but NO registry entry, NO toolbox visibility, NO Properties Panel support | Full registry entry, structure defaults, preview, properties panel controls |

### 2.3 Per-Component Implementation Checklist

For EVERY new/promoted component, ALL of the following must be implemented:

- [ ] `ComponentType` union in `builder.types.ts`
- [ ] Component-specific props in `ComponentProps` interface (if any)
- [ ] `ComponentRegistry` entry with structure, preview component, runtime component
- [ ] `structureDefaults.ts` type check (add to correct category)
- [ ] `ComponentPreview.tsx` drag preview case
- [ ] Properties Panel controls in `PropertiesPanel.tsx` (type-specific section if needed)
- [ ] Backend `ComponentType` enum in `form_definition.py`
- [ ] Validator acceptance (`form-validate` endpoint must accept the new types)

### 2.4 Documentation

- Update `docs/COMPONENT-FRAMEWORK-GUIDE.md` with a **complete component inventory** section covering ALL registered components (existing + new) with their type, purpose, key props, and default behaviour.
- Document the `date` component's `dateType` prop (`"date"`, `"time"`, `"datetime"`) in the inventory — this is already implemented but undocumented.
- Document that background images are handled at the page level (`FormPage.background`), NOT as components.
- Update `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md` to include the 3 new component types in the Component Catalog section.

### 2.5 Frontend UAT

Visual verification that each new/promoted component renders correctly on all 3 surfaces:
- **Toolbox**: appears with correct icon, label, and category
- **Canvas**: drag-drops onto canvas with correct structure and preview
- **Runtime**: renders correctly in public form preview

---

## 3) Out of Scope

| Item | Reason |
|------|--------|
| Separate "time" component | Date already supports `dateType: "time"` — document, don't duplicate |
| Background image component | Handled at page level (`FormPage.background`), not component level |
| File upload component | Moved to Story 6.2.2 — requires full backend infrastructure (public upload endpoint, SubmissionAttachment model, secure download) |
| Payment component | Story 6.9 scope (Stripe Connect) |
| AI context pack v2 restructuring | Story 6.3 scope |
| Benchmark re-runs | Story 6.3 scope (depends on this story's expanded component set) |
| Rating component persistence/submission | Only the builder/renderer UI is in scope; backend data handling is future work |

---

## 4) Acceptance Criteria

### AC-1: URL Component
- **Given** a user opens the form builder toolbox
- **When** they drag a "URL" component onto the canvas
- **Then** it appears with label, URL input placeholder, and validation area
- **And** the Properties Panel shows URL-specific validation (pattern, required)
- **And** the component renders identically on canvas and runtime
- **And** `POST /api/form-validate` accepts definitions containing `type: "url"`

### AC-2: Rating Component
- **Given** a user opens the form builder toolbox
- **When** they drag a "Rating" component onto the canvas
- **Then** it appears with label, star/number rating display, and validation area
- **And** the Properties Panel shows rating-specific controls (max rating, style: stars/numbers/emoji)
- **And** the component renders identically on canvas and runtime
- **And** `POST /api/form-validate` accepts definitions containing `type: "rating"`

### AC-3: Paragraph Component (Promotion)
- **Given** a user opens the form builder toolbox
- **When** they look in the "Display" category
- **Then** "Paragraph" is visible alongside Header and Divider
- **And** they can drag it onto the canvas and see rendered paragraph text
- **And** the Properties Panel shows text content controls
- **And** the component renders identically on canvas and runtime
- **And** `POST /api/form-validate` already accepts `type: "paragraph"` (backend enum exists)

### AC-4: Component Inventory Documentation
- **Given** the COMPONENT-FRAMEWORK-GUIDE.md is opened
- **Then** it contains a "Component Inventory" section listing ALL registered components
- **And** each entry includes: type, category, purpose, key props, default behaviour
- **And** the `date` component entry documents `dateType` options (date, time, datetime)
- **And** a note clarifies that background images are page-level, not components

### AC-5: AI Context Pack Update
- **Given** the STORY-6.2-AI-CONTEXT-PACK.md is opened
- **Then** the Component Catalog section includes `url`, `rating`, and `paragraph`
- **And** `file-upload` is listed as "planned (Story 6.2.2)" so the AI knows it exists but is not yet available

### AC-6: Green CI/CD Gate
- **Given** all implementation is complete
- **Then** `npm run lint` produces 0 errors and 0 warnings
- **And** `npm run test:unit -- --watch=false` passes all existing tests (baseline: 237)
- **And** `python -m pytest --tb=short` passes all existing tests (baseline: 512+)
- **And** no regressions are introduced in existing component behaviour

---

## 5) Technical Notes

### Component Registry Pattern
Each registered component needs a `ComponentDefinition` object with:
- `type`, `label`, `icon`, `category` (layout | input | display)
- `defaultProps` with sensible defaults
- `structure` (ComponentStructure with objects, layout, layoutGroups)
- `previewComponent` via `makeToolboxPreview()`
- `runtimeComponent` using `UniversalFieldShell` + `getRenderersForComponent()`

### Structure Defaults Pattern
Components are categorized in `structureDefaults.ts`:
- Input fields: label + input + validation, `defaultLayout: 'vertical'`
- Display types: single content object with `customType`
- Special types (terms, submit-button) have unique structures

### Properties Panel Pattern
Type-specific sections are conditionally rendered based on `selectedComponent.type`. Shared sections (General, Validation, Appearance) apply broadly with exclusion lists.

### Backend Validation
The `form_definition.py` `ComponentType` enum must include new types. The validator endpoint uses this enum to accept/reject component types in submitted definitions.

### New Component Props

```typescript
// URL-SPECIFIC
urlPrefix?: string;      // e.g., "https://"
urlPattern?: string;     // custom regex for validation

// RATING-SPECIFIC
ratingMax?: number;           // 5 (stars) or 10 (NPS)
ratingStyle?: 'stars' | 'numbers' | 'emoji';
ratingLabels?: { low?: string; high?: string };  // e.g., "Not likely" / "Very likely"
```

---

## 6) Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| New component types break existing validator tests | Medium | Medium | Run full backend test suite before and after enum changes |
| Rating component star rendering WYSIWYG parity | Low | Low | Use simple CSS/SVG stars that render identically on canvas and runtime |
| Paragraph promotion reveals hidden dependencies | Low | Medium | Paragraph is already in ComponentType union and backend enum — promotion is additive |
| Properties Panel becomes too large | Low | Low | Follow existing pattern of type-specific sections; no new architectural patterns needed |

---

## 7) Dependencies

| Dependency | Status | Notes |
|-----------|--------|-------|
| Story 6.2 (AI Form Builder POC) | ✅ Complete | Merged PR #53 |
| Component Framework (Epic 5) | ✅ Complete | All framework files stable |
| Backend validator (Story 6.1) | ✅ Complete | Merged PR #52 |

---

*Story 6.2.1 — Component Library Expansion*  
*Created: 2026-03-20 by SM Agent*

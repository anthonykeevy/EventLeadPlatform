# Story 6.2.1 — Single-Session Dev Prompt

**Story:** 6.2.1 — Component Library Expansion  
**Agent:** `@bmad-agent-bmm-dev`  
**Worktree:** `C:\wt\elp\story-epic6-6.2.1-component-library-expansion`  
**Branch:** `story/epic6-6.2.1-component-library-expansion`  
**PR:** #54

---

## Execution Contract

You are the Dev agent for Story 6.2.1. Implement the full story scope in one execution loop. You MUST follow every step below in order. Do NOT skip steps, do NOT weaken quality gates, do NOT claim completion until Green CI/CD evidence is provided.

---

## Step 0: Preflight

Run the preflight script to verify worktree and branch state:

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.2.1-component-library-expansion" `
  -ExpectedBranch "story/epic6-6.2.1-component-library-expansion" `
  -ReportFile "docs/stories/STORY-6.2.1-PREFLIGHT.md"
```

If preflight fails, resolve before proceeding.

---

## Step 1: Read Story Context

Read these files before writing any code:
1. `docs/stories/story-6.2.1.md` — scope, ACs, risks
2. `docs/stories/story-context-6.2.1.xml` — implementation context with file targets, patterns, constraints
3. `docs/COMPONENT-FRAMEWORK-GUIDE.md` — component framework guide
4. `docs/COMPONENT-FRAMEWORK-REFERENCE.md` — detailed framework reference (skim key sections)

---

## Step 2: Backend Enum Expansion

**File:** `backend/schemas/form_definition.py`

Add 2 new values to the `ComponentType` enum:
```python
URL = "url"
RATING = "rating"
```

Note: FILE_UPLOAD is deferred to Story 6.2.2.

PARAGRAPH already exists — no change needed.

**Verify:** Run `python -m pytest tests/ -k "form_definition or form_validate" --tb=short` to check for immediate breakage.

---

## Step 3: Frontend Types Expansion

**File:** `frontend/src/features/builder/types/builder.types.ts`

### 3.1 ComponentType Union
Add to the union (paragraph already exists):
```typescript
| 'url' | 'rating'
```

Note: 'file-upload' is deferred to Story 6.2.2.

### 3.2 ComponentProps Interface
Add new prop sections:

```typescript
// URL-SPECIFIC
urlPrefix?: string;
urlPattern?: string;

// RATING-SPECIFIC
ratingMax?: number;
ratingStyle?: 'stars' | 'numbers' | 'emoji';
ratingLabels?: { low?: string; high?: string };
```

---

## Step 4: Structure Defaults

**File:** `frontend/src/features/builder/utils/structureDefaults.ts`

1. Add `'url'`, `'rating'` to the input field type check (the array/condition that includes text, email, phone, etc.)
2. Add `'paragraph'` to the display type check (alongside header, divider)

---

## Step 5: Component Registry — All 3 Components

**File:** `frontend/src/features/builder/registry/ComponentRegistry.tsx`

Add 3 ComponentDefinition entries. Follow these patterns:

### 5.1 Paragraph (promote — follow header pattern)
- category: `'display'`
- structure: single content object with `customType: 'paragraph'`
- icon: DocumentTextIcon or Bars3BottomLeftIcon
- label: `'Paragraph'`
- defaultProps: `{ text: 'Paragraph text goes here.' }`

### 5.2 URL (follow email pattern)
- category: `'input'`
- structure: label + input + validation (vertical layout)
- icon: LinkIcon or GlobeAltIcon
- label: `'Website URL'`
- defaultProps: `{ label: 'Website URL', placeholder: 'https://example.com', required: false }`

### 5.3 Rating (input category, custom input renderer)
- category: `'input'`
- structure: label + input + validation (vertical layout)
- icon: StarIcon
- label: `'Rating'`
- defaultProps: `{ label: 'Rating', required: false, ratingMax: 5, ratingStyle: 'stars' }`
- Input renderer: render star icons (filled/unfilled) or number buttons based on ratingStyle

**Critical:** Each entry needs `previewComponent` via `makeToolboxPreview()` and `runtimeComponent` using `UniversalFieldShell` + `getRenderersForComponent()`.

---

## Step 6: Component Preview

**File:** `frontend/src/features/builder/components/ComponentPreview.tsx`

Add cases in `renderInputPlaceholder` for:
- `'url'` — URL input placeholder with link icon
- `'rating'` — Star outline placeholder

Verify the existing `'paragraph'` case works correctly.

---

## Step 7: Properties Panel

**File:** `frontend/src/features/builder/components/PropertiesPanel.tsx`

### 7.1 Type-Specific Sections
Add rendering cases in the type-specific section block:
- `'url'` → UrlPropertiesSection (urlPrefix, urlPattern controls)
- `'rating'` → RatingPropertiesSection (ratingMax, ratingStyle, ratingLabels)

You may create these as inline sections or separate components depending on complexity.

### 7.2 Exclusion Lists
Verify paragraph is correctly handled:
- **ValidationSection excluded for:** submit-button, divider, header, paragraph (already in list)
- **GeneralSection excluded for:** submit-button, divider (paragraph should NOT be excluded)
- **AppearanceSection excluded for:** divider only (paragraph should NOT be excluded)

---

## Step 8: Object Renderers (if needed)

**File:** `frontend/src/features/builder/utils/objectRenderers.tsx`

If the registry's `getRenderersForComponent()` pattern requires explicit renderer cases for new types, add them. The input object renderer needs cases for:
- `url`: text input with link/globe icon prefix
- `rating`: row of star SVGs or number buttons

Check how existing types (email, phone, date) handle their input rendering and follow the same pattern.

---

## Step 9: Documentation Updates

### 9.1 Component Framework Guide
**File:** `docs/COMPONENT-FRAMEWORK-GUIDE.md`

Add a **"Component Inventory"** section after the "Key Files" section. Include ALL registered components (existing + new) in a table with columns:

| Type | Category | Purpose | Key Props | Default Behaviour |
|------|----------|---------|-----------|-------------------|

Components to list (18 total):
- INPUT: text, first-name, number, email, phone, url, textarea, dropdown, date, checkbox, radio, address, rating
- ACTION/LEGAL: terms, submit-button
- DISPLAY: header, paragraph, divider

Special entries:
- **date**: document `dateType` prop accepting `"date"` | `"time"` | `"datetime"` (already implemented)
- **paragraph**: note promoted from unregistered in Story 6.2.1

Add a note: "Background images are handled at the page level (`FormPage.background`), not as components."

### 9.2 AI Context Pack
**File:** `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md`

Add to the "Component Catalog (MVP Set)" section:
- `url`
- `rating`
- `paragraph`
- Note `file-upload` as "planned (Story 6.2.2)" so the AI is aware but won't generate it
- `terms` (was already supported but missing from the list)
- `first-name` (was already supported but missing from the list)

Add brief prop notes for the new types.

---

## Step 10: Green CI/CD Gate (MANDATORY)

Run the green gate script:

```powershell
.\scripts\workflow\run-green-gate.ps1 `
  -StoryId "6.2.1" `
  -BackendGateCommand "python -m pytest --tb=short" `
  -EvidenceFile "docs/stories/STORY-6.2.1-GATE-EVIDENCE.md"
```

**Or run manually in sequence:**

```powershell
# Frontend lint (from frontend/ directory)
npm run lint

# Frontend unit tests (from frontend/ directory)
npm run test:unit -- --watch=false

# Backend full suite (from backend/ directory — requires MSSQL running)
python -m pytest --tb=short
```

### Anti-Hallucination Protocol
- You MUST read the **exact output** of each test run.
- If the test process times out, hangs, or output is truncated before showing the final `=== X passed, Y failed ===` summary, treat the test as **FAILED**.
- You are NOT allowed to end your turn until all tests demonstrably pass and 0 linting errors/warnings remain.
- If tests fail, fix them and re-run until green.

### Expected Baselines
| Check | Baseline | Must |
|-------|----------|------|
| Frontend lint | 0 errors, 0 warnings | No regressions |
| Frontend tests | 237 passed | All pass, no decrease |
| Backend tests | 512+ passed | All pass, no decrease |

---

## Step 11: Evidence & Commit

### 11.1 Generate Evidence
```powershell
.\scripts\workflow\generate-story-evidence.ps1 `
  -StoryId "6.2.1" `
  -GateEvidenceFile "docs/stories/STORY-6.2.1-GATE-EVIDENCE.md" `
  -UatResultsFile "docs/stories/STORY-6.2.1-UAT-RESULTS.md"
```

### 11.2 Final Commit
Only commit when Green CI/CD is demonstrably passing:

```powershell
git add -A
git commit -m "feat(epic6): Story 6.2.1 — Component Library Expansion

- Add url, rating components (full stack integration)
- Promote paragraph to first-class registered component
- Update COMPONENT-FRAMEWORK-GUIDE.md with complete component inventory
- Update AI Context Pack with expanded component catalog
- All green gates passing (frontend lint, unit tests, backend tests)"

git push origin story/epic6-6.2.1-component-library-expansion
```

---

## Constraints (MUST follow)

1. **WYSIWYG parity**: Canvas and Runtime must render identically for all new components
2. **No separate time component**: Date already supports `dateType: "time"` — document only
3. **No background component**: Background images are page-level (`FormPage.background`)
4. **Rating UI shell only**: rating is a UI shell — no backend persistence
5. **No ad-hoc margins/padding**: Use layout engine, not inline hacks
6. **Surface-gate builder visuals**: TextLengthIndicator, resize handles only on canvas
7. **Check capabilities before showing UI**: Don't show controls for unsupported features
8. **Paragraph is additive**: Type already exists in union + backend enum — only add registry entry + properties

---

## Out of Scope (do NOT implement)

- File upload component (entire component deferred to Story 6.2.2 for full backend infrastructure)
- Rating submission/persistence backend
- AI context pack v2 restructuring (Story 6.3)
- Benchmark re-runs (Story 6.3)
- Payment component (Story 6.9)
- Separate time component (date already handles it)
- Background image component (page-level feature)

---

*Story 6.2.1 Single-Session Dev Prompt*  
*Created: 2026-03-20 by SM Agent*

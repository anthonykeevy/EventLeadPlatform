# Story 6.2.1 — UAT Test Guide

**Story:** 6.2.1 — Component Library Expansion  
**Tester:** Human (manual UAT)  
**Prerequisites:** Dev agent has completed implementation and Green CI/CD gate is passing  
**Environment:** Local dev server (`npm run dev` for frontend, backend running)

---

## UAT progress log (Form 340, 2026-03-30)

UAT follow-up run: tests **1.2–1.4**, **2.1–2.6**, **3.1–3.5**, **4.1–4.3**, **5.1–5.2**, **6.1–6.2** recorded **PASS** on **2026-03-30**.

| Test | Status | Notes |
|------|--------|--------|
| **1.1** Toolbox — URL visible | **PASS** | Website URL in Input category |
| **1.2** Canvas — URL presentation | **PASS** | Re-test after URL/layout fixes: prefix + `example.com` placeholder, no double scheme. |
| **1.3** Properties — URL / General | **PASS** | Label/placeholder/required/URL sections behave |
| **1.3b** Identity **Layout** vs canvas | **PASS** | Horizontal/vertical on URL confirmed after `objectLayout` wiring. |
| **1.3c** Global **Default Object Layout** vs existing canvas | **PASS** | Behaviour matches product rule: existing instances not reshuffled by live global. |
| **1.4** Runtime parity | **PASS** | URL matches canvas; no builder chrome. |
| **1.5** Backend validation | *Covered by automation* | `test_story_621_url_rating_paragraph_types_accepted` |

**Reference doc vs raised issues:** `COMPONENT-FRAMEWORK-REFERENCE.md` states that `defaultObjectLayout` is **applied** when there is no `props.objectLayout` override (inheritance from form global). Your expectation is **stricter**: global default must **not** reshuffle already-placed components; only **toolbox + new drops** follow the live global. The implementation now follows **your** rule; the reference file was **not** edited — if you want the doc updated to match, say so.

---

## Pre-UAT Checklist

Before starting manual UAT, verify the Dev agent's evidence package:

- [ ] `npm run lint` — 0 errors, 0 warnings
- [ ] `npm run test:unit -- --watch=false` — all tests pass (baseline: 237+)
- [ ] `python -m pytest --tb=short` — all tests pass (baseline: 512+)
- [ ] Dev agent evidence is complete (not truncated, shows final summary)

---

## Test 1: URL Component — Toolbox to Canvas to Runtime

### 1.1 Toolbox Visibility
1. Open the Form Builder
2. Look in the toolbox panel (left sidebar)
3. **Verify:** "Website URL" (or "URL") component appears in the Input category
4. **Verify:** It has a recognizable icon (link or globe icon)

### 1.2 Canvas Drag & Drop
1. Drag the URL component from the toolbox onto the canvas
2. **Verify:** Component appears with:
   - Label text (e.g., "Website URL")
   - When `urlPrefix` is set (e.g. `https://`): prefix shown **once** beside the field; inner placeholder is **`example.com`** only (not a second full URL)
   - Validation area below

### 1.3 Properties Panel
1. Click the URL component on the canvas to select it
2. **Verify:** Properties Panel opens on the right
3. **Verify:** General section shows label, placeholder, required toggle
4. **Verify:** URL-specific controls appear (if any — urlPrefix, pattern)
5. Change the label to "LinkedIn Profile"
6. **Verify:** Canvas updates to show "LinkedIn Profile"

### 1.4 Runtime Parity
1. Open the form in Runtime/Preview mode
2. **Verify:** URL component renders identically to the canvas version
3. **Verify:** No builder-only chrome (resize handles, SmartBorder) appears

### 1.5 Backend Validation
1. Save the form definition containing the URL component
2. **Verify:** No validation errors from the backend
3. **Verify:** `POST /api/form-validate` accepts `type: "url"` without error

| Step | Expected | Pass/Fail |
|------|----------|-----------|
| 1.1 Toolbox | URL visible in Input category | **PASS** (2026-03-30) |
| 1.2 Canvas | Renders with label, input (prefix + `example.com` placeholder), validation — no double scheme | **PASS** (2026-03-30) |
| 1.3 Properties | Controls work, canvas updates live; Identity **Layout** changes `objectLayout` on canvas | **PASS** (2026-03-30) |
| 1.4 Runtime | Identical to canvas, no builder chrome | **PASS** (2026-03-30) |
| 1.5 Validation | Backend accepts url type | **PASS** (automated test) |

---

## Test 2: Rating Component — Toolbox to Canvas to Runtime

### 2.1 Toolbox Visibility
1. Look in the toolbox panel
2. **Verify:** "Rating" component appears in the Input category
3. **Verify:** It has a star icon

### 2.2 Canvas Drag & Drop
1. Drag the Rating component onto the canvas
2. **Verify:** Component appears with:
   - Label text (e.g., "Rating")
   - Star/number rating display (default: 5 stars)
   - Validation area below

### 2.3 Properties Panel — Stars Mode
1. Click the Rating component to select it
2. **Verify:** Properties Panel shows:
   - General section (label, required)
   - Rating-specific controls:
     - Max rating (5 or 10)
     - Style selector (stars, numbers, emoji)
     - Labels (low/high text, e.g., "Not likely" / "Very likely")
3. **Verify:** Default is 5 stars

### 2.4 Properties Panel — Numbers Mode (NPS)
1. Change ratingStyle to "numbers"
2. Change ratingMax to 10
3. Set low label to "Not likely", high label to "Very likely"
4. **Verify:** Canvas updates to show 0-10 number scale with labels

### 2.5 Runtime Parity
1. Open Runtime/Preview mode
2. **Verify:** Rating renders identically to canvas in both star and number modes
3. Test with star mode (5 stars) and number mode (0-10 NPS)

### 2.6 Backend Validation
1. Save the form definition containing the Rating component
2. **Verify:** `POST /api/form-validate` accepts `type: "rating"` without error

| Step | Expected | Pass/Fail |
|------|----------|-----------|
| 2.1 Toolbox | Rating visible in Input category | **PASS** (2026-03-30) |
| 2.2 Canvas | Renders with label, stars, validation | **PASS** (2026-03-30) |
| 2.3 Properties (stars) | Star-specific controls, default 5 stars | **PASS** (2026-03-30) |
| 2.4 Properties (NPS) | Numbers mode, 0-10, labels work | **PASS** (2026-03-30) |
| 2.5 Runtime | Identical to canvas for both modes | **PASS** (2026-03-30) |
| 2.6 Validation | Backend accepts rating type | **PASS** (2026-03-30) |

---

## Test 3: Paragraph Component (Promotion) — Toolbox to Canvas to Runtime

### 3.1 Toolbox Visibility
1. Look in the toolbox panel
2. **Verify:** "Paragraph" component appears in the **Display** category
3. **Verify:** It appears alongside Header and Divider
4. **Verify:** It has a text/document icon

### 3.2 Canvas Drag & Drop
1. Drag the Paragraph component onto the canvas
2. **Verify:** Component appears with rendered paragraph text
3. **Verify:** Default text is visible (e.g., "Paragraph text" or similar placeholder)

### 3.3 Properties Panel
1. Click the Paragraph component to select it
2. **Verify:** Properties Panel shows:
   - General section with text content controls
   - Appearance section
   - NO Validation section (paragraph is display-only)
3. Change the text content
4. **Verify:** Canvas updates to show the new text

### 3.4 Runtime Parity
1. Open Runtime/Preview mode
2. **Verify:** Paragraph renders identically to canvas
3. **Verify:** Text content is displayed as expected

### 3.5 Backend Validation
1. Save the form definition containing the Paragraph component
2. **Verify:** Backend accepts `type: "paragraph"` (it already exists in the enum)

| Step | Expected | Pass/Fail |
|------|----------|-----------|
| 3.1 Toolbox | Paragraph visible in Display category | **PASS** (2026-03-30) |
| 3.2 Canvas | Renders with paragraph text | **PASS** (2026-03-30) |
| 3.3 Properties | Text controls work, no validation section | **PASS** (2026-03-30) |
| 3.4 Runtime | Identical to canvas | **PASS** (2026-03-30) |
| 3.5 Validation | Backend accepts paragraph type | **PASS** (2026-03-30) |

---

## Test 4: Mixed Form — All New Components Together

### 4.1 Build a Test Form
1. Create a new form
2. Add the following components in order:
   - Header ("Job Application")
   - Text ("Full Name")
   - Email ("Email Address")
   - URL ("LinkedIn Profile")
   - Paragraph ("Tell us about yourself")
   - Rating ("How interested are you?")
   - Submit Button
3. **Verify:** All components render correctly on canvas
4. **Verify:** No overlapping, proper spacing between components

### 4.2 Runtime Preview
1. Open the form in Runtime/Preview mode
2. **Verify:** All components render correctly
3. **Verify:** Component order matches canvas
4. **Verify:** WYSIWYG parity — runtime looks identical to canvas

### 4.3 Validate
1. Save the form
2. **Verify:** `POST /api/form-validate` accepts the mixed form without errors

| Step | Expected | Pass/Fail |
|------|----------|-----------|
| 4.1 Build | All components render on canvas | **PASS** (2026-03-30) |
| 4.2 Runtime | WYSIWYG parity, correct order | **PASS** (2026-03-30) |
| 4.3 Validate | Backend accepts all types | **PASS** (2026-03-30) |

---

## Test 5: Existing Components — Regression Check

### 5.1 Core Components Still Work
1. Create a form with existing components only: text, email, phone, number, date, dropdown, checkbox, radio, textarea, address, terms, submit-button, header, divider
2. **Verify:** All existing components still work as expected
3. **Verify:** No visual regressions (compare to known-good state)

### 5.2 Date Component Time Mode
1. Add a Date component to the canvas
2. In Properties Panel, change dateType to "time"
3. **Verify:** Component changes to show a time picker (not date picker)
4. Change dateType to "datetime"
5. **Verify:** Component shows date+time picker

| Step | Expected | Pass/Fail |
|------|----------|-----------|
| 5.1 Regression | All existing components work | **PASS** (2026-03-30) |
| 5.2 Date modes | time and datetime modes render correctly | **PASS** (2026-03-30) |

---

## Test 6: Documentation Verification

### 6.1 Component Inventory
1. Open `docs/COMPONENT-FRAMEWORK-GUIDE.md`
2. **Verify:** Contains a "Component Inventory" section
3. **Verify:** Lists ALL registered components with type, category, purpose, key props
4. **Verify:** Date component entry documents dateType options (date, time, datetime)
5. **Verify:** Note about background images being page-level exists

### 6.2 AI Context Pack
1. Open `docs/stories/STORY-6.2-AI-CONTEXT-PACK.md`
2. **Verify:** Component Catalog includes url, rating, paragraph
3. **Verify:** file-upload is noted as "planned (Story 6.2.2)"

| Step | Expected | Pass/Fail |
|------|----------|-----------|
| 6.1 Guide | Complete inventory with all components | **PASS** (2026-03-30) |
| 6.2 Context Pack | New types listed in catalog | **PASS** (2026-03-30) |

---

## UAT Result Summary

| Test | Description | Result |
|------|------------|--------|
| Test 1 | URL Component (5 steps) | **PASS** — 1.1–1.5 (1.5 automated) |
| Test 2 | Rating Component (6 steps) | **PASS** |
| Test 3 | Paragraph Component (5 steps) | **PASS** |
| Test 4 | Mixed Form (3 steps) | **PASS** |
| Test 5 | Regression Check (2 steps) | **PASS** |
| Test 6 | Documentation (2 steps) | **PASS** |

**Overall UAT Result:** **PASS** (manual steps 1.2–1.4, 2.1–2.6, 3.1–3.5, 4.1–4.3, 5.1–5.2, 6.1–6.2)  
**Tested By:** Human (manual UAT)  
**Date:** 2026-03-30  
**Notes:** Follow-up run after URL/layout/Rating marks UX fixes; all listed steps passed.

---

*Story 6.2.1 UAT Test Guide*  
*Created: 2026-03-20 by SM Agent*

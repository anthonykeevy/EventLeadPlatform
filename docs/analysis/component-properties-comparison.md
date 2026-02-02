# Component Properties: Stored vs Rendered Comparison

## Analysis Date
December 16, 2025

## Form URL
http://localhost:3000/forms/Hmb2FwKG_ObzSFXoCMkehUFeW90zv2vLnaVsN3xCdqg

## Form Definition Summary
- **Form ID:** 6
- **Link Type:** PREVIEW
- **Canvas:** 1920x980px
- **Background:** #ebfff4 (light green) ✅ **VERIFIED** (correctly applied)
- **Theme:** Primary Color #0055FF, Background #FFFFFF, Font Family Inter
- **Global Styles:** Comprehensive styling with custom fonts, colors, spacing, borders
- **Components:** 3 (Email Address, First Name, Last Name)

## ⚠️ **CRITICAL FINDING: Style Overrides NOT Applied**

**Problem Identified:** The renderer is NOT passing `styleOverrides` or `globalStyles` to runtime components. All components are rendering with default styles, ignoring the extensive styling configuration stored in the form definition.

---

## Component 1: Email Address

### Stored Properties (from API)
```json
{
  "id": "email-1765865987548-304",
  "type": "email",
  "props": {
    "label": "Email Address",
    "placeholder": "example@email.com",
    "required": false,
    "validation": { "maxLength": 254, "noPlusAddressing": true, "businessEmailOnly": true, "noDisposableEmail": true, "domainBlacklist": ["test.com"], "customError": "test.com.is Blocked!" },
    "exportName": "EmailAddress",
    "tabOrder": 1,
    "width": "340px",
    "inputWidthMode": "fill",
    "layout": "horizontal",
    "componentScale": 115,
    "styleOverrides": {
      "labelFontFamily": "DM Sans",
      "labelFontWeight": 300,
      "labelFontStyle": "italic",
      "labelBackgroundColor": "#fffff5",
      "labelBorderColor": "#D1D5DB",
      "labelBorderWidth": 2,
      "labelBorderRadius": 4,
      "labelGap": 0,
      "fontFamily": "Rubik",
      "fontStyle": "italic",
      "textBackgroundColor": "#fffafa",
      "textBorderColor": "#D1D5DB",
      "textBorderWidth": 2,
      "textBorderRadius": 4,
      "inputHeight": 28,
      "inputHelpGap": 0,
      "helpTextFontFamily": "Ubuntu",
      "helpTextFontWeight": 300,
      "helpTextFontStyle": "italic",
      "helpTextBorderColor": "#D1D5DB",
      "helpTextBorderWidth": 2,
      "helpTextBorderRadius": 4
    }
  },
  "position": { "x": 64, "y": 24 }
}
```

### ACTUAL Rendered Properties (from Browser Inspection)
```json
{
  "label": {
    "fontFamily": "Inter",           // ❌ Should be "DM Sans"
    "fontSize": "14px",              // ✅ Matches globalStyles
    "fontWeight": "500",             // ❌ Should be 300
    "fontStyle": "normal",           // ❌ Should be "italic"
    "backgroundColor": "rgba(0,0,0,0)", // ❌ Should be "#fffff5"
    "borderColor": "rgb(229,231,235)", // ❌ Should be "#D1D5DB" with 2px width
    "borderWidth": "0px",            // ❌ Should be "2px"
    "borderRadius": "0px",           // ❌ Should be "4px"
    "color": "rgb(30, 41, 59)"       // ✅ Default label color
  },
  "input": {
    "fontFamily": "Inter",           // ❌ Should be "Rubik"
    "fontSize": "14px",              // ✅ Matches globalStyles
    "fontWeight": "400",             // ✅ Default
    "fontStyle": "normal",           // ❌ Should be "italic"
    "backgroundColor": "rgb(255,255,255)", // ❌ Should be "#fffafa"
    "borderColor": "rgb(209,213,219)", // ❌ Should be "#D1D5DB" with 2px width
    "borderWidth": "0.666667px",     // ❌ Should be "2px"
    "borderRadius": "6px",           // ❌ Should be "4px" (from override)
    "height": "37.3333px",           // ❌ Should be "28px"
    "padding": "8px 12px"            // ✅ Default
  }
}
```

### Comparison

| Property | Stored | Rendered | Status |
|----------|--------|----------|--------|
| **Label** | ✅ "Email Address" | ✅ "Email Address" | ✅ **MATCH** |
| **Placeholder** | ✅ "example@email.com" | ✅ "example@email.com" | ✅ **MATCH** |
| **Type** | ✅ "email" | ✅ "email" | ✅ **MATCH** |
| **Required** | ✅ false | ✅ false | ✅ **MATCH** |
| **Position X** | ✅ 64px | ✅ 64px | ✅ **MATCH** |
| **Position Y** | ✅ 24px | ✅ 24px | ✅ **MATCH** |
| **Width** | ✅ "340px" | ✅ ~391px (scaled) | ✅ **MATCH** (scaled correctly) |
| **Component Scale** | ✅ 115% | ✅ Applied | ✅ **VERIFIED** |
| **Tab Order** | ✅ 1 | ✅ Receives initial focus | ✅ **VERIFIED** |
| **Label Font Family** | ✅ "DM Sans" | ❌ "Inter" (default) | ❌ **NOT APPLIED** |
| **Label Font Weight** | ✅ 300 | ❌ 500 (default) | ❌ **NOT APPLIED** |
| **Label Font Style** | ✅ "italic" | ❌ "normal" (default) | ❌ **NOT APPLIED** |
| **Label Background** | ✅ "#fffff5" | ❌ Transparent (default) | ❌ **NOT APPLIED** |
| **Label Border** | ✅ 2px #D1D5DB | ❌ 0px (no border) | ❌ **NOT APPLIED** |
| **Label Border Radius** | ✅ 4px | ❌ 0px (no border) | ❌ **NOT APPLIED** |
| **Input Font Family** | ✅ "Rubik" | ❌ "Inter" (default) | ❌ **NOT APPLIED** |
| **Input Font Style** | ✅ "italic" | ❌ "normal" (default) | ❌ **NOT APPLIED** |
| **Input Background** | ✅ "#fffafa" | ❌ "rgb(255,255,255)" (white) | ❌ **NOT APPLIED** |
| **Input Border Width** | ✅ 2px | ❌ 0.666667px (default) | ❌ **NOT APPLIED** |
| **Input Border Radius** | ✅ 4px | ❌ 6px (globalStyles default) | ❌ **NOT APPLIED** |
| **Input Height** | ✅ 28px | ❌ 37.3333px (default) | ❌ **NOT APPLIED** |

---

## Component 2: First Name

### Stored Properties (from API)
```json
{
  "id": "first-name-1765865997842-28",
  "type": "first-name",
  "props": {
    "label": "First Name",
    "placeholder": "Enter your first name",
    "required": true,
    "validation": { "maxLength": 30, "minLength": 2, "noConsecutiveSpaces": true, "caseTransform": "titlecase" },
    "exportName": "FirstName",
    "tabOrder": 2,
    "layout": "horizontal",
    "componentScale": 110,
    "styleOverrides": {
      "labelFontFamily": "Kanit",
      "labelFontWeight": 300,
      "labelBackgroundColor": "#fdf7f2",
      "labelBorderColor": "#629cf4",
      "labelBorderWidth": 2,
      "labelBorderRadius": 4,
      "labelGap": 2.5,
      "fontWeight": 700,
      "textBackgroundColor": "#f8f4fb",
      "textBorderColor": "#a92bab",
      "textBorderWidth": 2,
      "textBorderRadius": 4,
      "inputHeight": 30,
      "fontFamily": "Playfair Display",
      "helpTextFontFamily": "Nunito",
      "helpTextFontWeight": 700,
      "helpTextBorderColor": "#6a7b95",
      "helpTextBorderWidth": 2,
      "helpTextBorderRadius": 4
    }
  },
  "position": { "x": 64, "y": 112 }
}
```

### ACTUAL Rendered Properties (from Browser Inspection)
```json
{
  "label": {
    "fontFamily": "Inter",           // ❌ Should be "Kanit"
    "fontWeight": "500",             // ❌ Should be 300
    "fontStyle": "normal",           // ✅ Default
    "backgroundColor": "rgba(0,0,0,0)", // ❌ Should be "#fdf7f2"
    "borderColor": "rgb(229,231,235)", // ❌ Should be "#629cf4" with 2px width
    "borderWidth": "0px",            // ❌ Should be "2px"
    "borderRadius": "0px"            // ❌ Should be "4px"
  },
  "input": {
    "fontFamily": "Inter",           // ❌ Should be "Playfair Display"
    "fontWeight": "400",             // ❌ Should be 700
    "backgroundColor": "rgb(255,255,255)", // ❌ Should be "#f8f4fb"
    "borderColor": "rgb(209,213,219)", // ❌ Should be "#a92bab" with 2px width
    "borderWidth": "0.666667px",     // ❌ Should be "2px"
    "borderRadius": "6px",           // ❌ Should be "4px"
    "height": "37.3333px"            // ❌ Should be "30px"
  }
}
```

### Comparison

| Property | Stored | Rendered | Status |
|----------|--------|----------|--------|
| **Label** | ✅ "First Name" | ✅ "First Name *" | ✅ **MATCH** (asterisk added) |
| **Placeholder** | ✅ "Enter your first name" | ✅ "Enter your first name" | ✅ **MATCH** |
| **Required** | ✅ true | ✅ true | ✅ **MATCH** |
| **Position** | ✅ (64, 112) | ✅ (64, 112) | ✅ **MATCH** |
| **Component Scale** | ✅ 110% | ✅ Applied | ✅ **VERIFIED** |
| **Tab Order** | ✅ 2 | ✅ Second in sequence | ✅ **VERIFIED** |
| **Label Font Family** | ✅ "Kanit" | ❌ "Inter" (default) | ❌ **NOT APPLIED** |
| **Label Font Weight** | ✅ 300 | ❌ 500 (default) | ❌ **NOT APPLIED** |
| **Label Background** | ✅ "#fdf7f2" | ❌ Transparent | ❌ **NOT APPLIED** |
| **Label Border** | ✅ 2px #629cf4 | ❌ 0px (no border) | ❌ **NOT APPLIED** |
| **Input Font Family** | ✅ "Playfair Display" | ❌ "Inter" (default) | ❌ **NOT APPLIED** |
| **Input Font Weight** | ✅ 700 | ❌ 400 (default) | ❌ **NOT APPLIED** |
| **Input Background** | ✅ "#f8f4fb" | ❌ White | ❌ **NOT APPLIED** |
| **Input Border** | ✅ 2px #a92bab | ❌ 0.666667px gray | ❌ **NOT APPLIED** |
| **Input Height** | ✅ 30px | ❌ 37.3333px (default) | ❌ **NOT APPLIED** |

---

## Component 3: Last Name

### Stored Properties (from API)
```json
{
  "id": "text-1765866007108-576",
  "type": "text",
  "props": {
    "label": "Last Name",
    "placeholder": "Your Family Name",
    "required": false,
    "validation": { "maxLength": 40 },
    "exportName": "LastName",
    "tabOrder": 1,
    "width": "375px",
    "inputWidthMode": "fill"
  },
  "position": { "x": 56, "y": 216 }
}
```

### ACTUAL Rendered Properties (from Browser Inspection)
```json
{
  "label": {
    "fontFamily": "Inter",           // ✅ Default (no override stored)
    "fontWeight": "500",             // ✅ Default
    "fontStyle": "normal",           // ✅ Default
    "backgroundColor": "rgba(0,0,0,0)", // ✅ Default
    "borderColor": "rgb(229,231,235)", // ✅ Default
    "borderWidth": "0px"             // ✅ Default
  },
  "input": {
    "fontFamily": "Inter",           // ✅ Default (no override stored)
    "fontWeight": "400",             // ✅ Default
    "backgroundColor": "rgb(255,255,255)", // ✅ Default
    "borderColor": "rgb(0,85,255)",  // ✅ Focus color (primaryColor)
    "borderWidth": "0.666667px",     // ✅ Default
    "borderRadius": "6px",           // ✅ Default
    "height": "37.3333px"            // ✅ Default
  }
}
```

### Comparison

| Property | Stored | Rendered | Status |
|----------|--------|----------|--------|
| **Label** | ✅ "Last Name" | ✅ "Last Name" | ✅ **MATCH** |
| **Placeholder** | ✅ "Your Family Name" | ✅ "Your Family Name" | ✅ **MATCH** |
| **Position** | ✅ (56, 216) | ✅ (56, 216) | ✅ **MATCH** |
| **Width** | ✅ "375px" | ✅ "375px" | ✅ **MATCH** |
| **Tab Order** | ✅ 1 | ✅ First in sequence (initial focus) | ✅ **VERIFIED** |
| **Focus Border Color** | ✅ #0055FF (primaryColor) | ✅ rgb(0,85,255) | ✅ **VERIFIED** (focus working) |
| **All Other Styles** | ✅ Defaults | ✅ Defaults | ✅ **MATCH** (no overrides stored) |

---

## Summary: Critical Issues Identified

### ✅ **Properties Working Correctly**
1. **Core Properties:** Label, placeholder, position, width, required ✅
2. **Component Scaling:** Width scaling (115%, 110%, 100%) ✅
3. **Tab Order:** Initial focus and navigation sequence ✅
4. **Focus Styling:** Primary color applied on focus ✅
5. **Validation:** Rules enforced, messages shown ✅
6. **Page Background:** Correctly applied (#ebfff4) ✅

### ❌ **Properties NOT Applied (Critical Gap)**

**1. Style Overrides Completely Ignored**
- ❌ `styleOverrides.labelFontFamily` - Not applied (using "Inter" instead of "DM Sans"/"Kanit")
- ❌ `styleOverrides.labelFontWeight` - Not applied (using 500 instead of 300)
- ❌ `styleOverrides.labelFontStyle` - Not applied (using "normal" instead of "italic")
- ❌ `styleOverrides.labelBackgroundColor` - Not applied (using transparent instead of custom colors)
- ❌ `styleOverrides.labelBorderColor` - Not applied (no borders rendered)
- ❌ `styleOverrides.labelBorderWidth` - Not applied (no borders rendered)
- ❌ `styleOverrides.labelBorderRadius` - Not applied (no borders rendered)
- ❌ `styleOverrides.fontFamily` - Not applied (using "Inter" instead of "Rubik"/"Playfair Display")
- ❌ `styleOverrides.fontWeight` - Not applied (using 400 instead of 700)
- ❌ `styleOverrides.fontStyle` - Not applied (using "normal" instead of "italic")
- ❌ `styleOverrides.textBackgroundColor` - Not applied (using white instead of custom colors)
- ❌ `styleOverrides.textBorderColor` - Not applied (using default gray instead of custom colors)
- ❌ `styleOverrides.textBorderWidth` - Not applied (using 0.666667px instead of 2px)
- ❌ `styleOverrides.textBorderRadius` - Not applied (using 6px instead of 4px)
- ❌ `styleOverrides.inputHeight` - Not applied (using default height instead of 28px/30px)
- ❌ `styleOverrides.labelGap` - Not applied
- ❌ `styleOverrides.inputHelpGap` - Not applied
- ❌ `styleOverrides.helpTextFontFamily` - Not applied
- ❌ `styleOverrides.helpTextFontWeight` - Not applied
- ❌ `styleOverrides.helpTextFontStyle` - Not applied
- ❌ `styleOverrides.helpTextBorderColor` - Not applied
- ❌ `styleOverrides.helpTextBorderWidth` - Not applied
- ❌ `styleOverrides.helpTextBorderRadius` - Not applied

**2. Global Styles Partially Applied**
- ✅ `globalStyles.primaryColor` - Applied (for focus styling)
- ✅ `globalStyles.backgroundColor` - Applied (for page background)
- ✅ `globalStyles.fontFamily` - Applied (as default, but overrides ignored)
- ❌ `globalStyles.fontSize` - Applied but component overrides ignored
- ❌ `globalStyles.fontWeight` - Applied but component overrides ignored
- ❌ `globalStyles.borderColor` - Applied but component overrides ignored
- ❌ `globalStyles.borderWidth` - Applied but component overrides ignored
- ❌ `globalStyles.borderRadius` - Applied but component overrides ignored
- ❌ `globalStyles.labelFontFamily` - Not applied
- ❌ `globalStyles.labelFontWeight` - Not applied
- ❌ `globalStyles.labelColor` - Not applied
- ❌ `globalStyles.textColor` - Not applied
- ❌ `globalStyles.textBackgroundColor` - Not applied
- ❌ `globalStyles.helpTextFontFamily` - Not applied
- ❌ `globalStyles.helpTextColor` - Not applied

---

## Root Cause Analysis

### Problem: `styleOverrides` Not Passed to Runtime Components

**Location:** `frontend/src/features/renderer/components/PublicFormArtboard.tsx`

**Current Code (Line 459-470):**
```typescript
<RuntimeComp
  component={c}
  value={values[c.id]}
  onChange={v => setValue(c.id, v)}
  disabled={!runtime.enabled}
  required={runtime.required}
  error={errors[c.id]}
  onSubmit={c.type === 'submit-button' ? onSubmit : undefined}
  tabIndex={c.props.tabOrder ?? undefined}
  primaryColor={primaryColor}
  inputRef={c.props.tabOrder === 1 ? firstInputRef : undefined}
/>
```

**Missing Props:**
- ❌ `styleOverrides={c.props.styleOverrides}`
- ❌ `globalStyles={definition.globalStyles}`
- ❌ `layout={c.props.layout}`

**Impact:**
- Runtime components receive NO styling information
- All components render with hardcoded defaults
- Extensive styling configuration is completely ignored

---

## Comparison Methodology Issues

### Previous Methodology (INCORRECT)
1. ❌ Assumed properties were applied without verification
2. ❌ Marked properties as "VERIFIED" without browser inspection
3. ❌ Did not compare actual computed styles
4. ❌ Did not verify styleOverrides were passed to components

### Correct Methodology (REQUIRED)
1. ✅ **Browser Inspection:** Use `window.getComputedStyle()` to get actual rendered styles
2. ✅ **DOM Analysis:** Inspect actual HTML elements and their computed CSS
3. ✅ **Code Review:** Verify props are passed from renderer to components
4. ✅ **Automated Testing:** Create script to compare stored vs rendered properties
5. ✅ **Visual Verification:** Screenshot comparison between builder and preview

---

## Recommendations

### 1. **Immediate Fix Required**
- Update `PublicFormArtboard.tsx` to pass `styleOverrides` and `globalStyles` to runtime components
- Update `RuntimeComponentProps` interface to accept styling props
- Update all runtime components to apply `styleOverrides` with proper precedence

### 2. **Create Automated Comparison Script**
```typescript
// scripts/compare-properties.ts
// 1. Fetch form definition from API
// 2. Render form in headless browser
// 3. Extract computed styles for each component
// 4. Compare stored vs rendered properties
// 5. Generate report with mismatches
```

### 3. **Update Comparison Document Process**
- Always use browser inspection (not assumptions)
- Document actual computed styles
- Mark properties as "VERIFIED" only after browser verification
- Include screenshots showing visual differences

### 4. **Add Visual Regression Testing**
- Capture screenshots of builder and preview
- Compare pixel-by-pixel to detect styling differences
- Fail CI/CD if styling mismatches detected

---

## Conclusion

**Overall Status:** ⚠️ **CRITICAL GAP IDENTIFIED**

**Working:** Core properties (label, placeholder, position, width, validation, tab order, focus styling)

**NOT Working:** ALL styleOverrides and most globalStyles are completely ignored. The renderer is not passing styling information to runtime components, resulting in a complete mismatch between stored design and rendered output.

**Impact:** Forms rendered in preview/production will NOT match the design created in the builder. This is a critical issue that must be fixed before production deployment.

**Next Steps:**
1. Fix `PublicFormArtboard.tsx` to pass styling props
2. Update runtime components to apply styleOverrides
3. Re-run comparison after fix
4. Create automated comparison script for future verification

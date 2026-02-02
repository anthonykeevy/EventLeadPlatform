# Story 3.8–3.9 UAT Test Guide — Public Form Renderer + Builder Persistence

**Status:** 📋 TBD (Run during Stories 3.8–3.9 validation)

**Stories:**
- `docs/stories/story-3.8.md`
- `docs/stories/story-3.9.md`

**Context:**
- `docs/stories/story-context-3.8.xml`
- `docs/stories/story-context-3.9.xml`

---

## 🛠️ Pre-requisites

Before starting the tests, ensure the following:

1. **Application is running:** Frontend dev server is active.
2. **Backend is running:** API is reachable (needed to save/load FormVersion and resolve public tokens).
3. **Authentication available:** You can log into the app as a user with **MANAGE** access to at least one form.
4. **At least one Form exists** in the system that you can open in the Builder (`/forms/:formId/builder`).
5. **DevTools available:** You can open browser DevTools to verify network requests, DOM element dimensions, and console errors.
6. **(Optional) Frontend diagnostic logging to DB (for Builder)**:
   - If you want drag/resize/collision decisions written to the database, enable the Vite env flags described in `docs/AGENT-LOGGING-GUIDE.md`.
   - Note: `npm run dev` runs Vite in `development` mode, so it loads `.env`, `.env.local`, `.env.development`, `.env.development.local` (it does not load `dev.env`).

---

## 📋 Comprehensive Component & Capability Checklist

This section provides complete checklists for all components, properties, validation rules, and logic rules available in the form builder. Use these checklists to ensure comprehensive coverage during UAT.

### Component Inventory (15 Total Components)

#### Input Field Components (11)
- [ ] `first-name` - First Name field (POC component)
- [ ] `text` - Text input (single line)
- [ ] `number` - Number input
- [ ] `email` - Email address input
- [ ] `phone` - Phone number input
- [ ] `textarea` - Multi-line text area
- [ ] `select` - Dropdown/select menu
- [ ] `radio` - Radio button group
- [ ] `checkbox` - Checkbox (single or group)
- [ ] `date` - Date picker
- [ ] `address` - Address input (with autocomplete placeholder)

#### Action/Legal Components (2)
- [ ] `terms` - Terms & Conditions checkbox
- [ ] `submit-button` - Form submission button

#### Display Components (3)
- [ ] `header` - Header text
- [ ] `paragraph` - Paragraph text
- [ ] `divider` - Visual separator/divider

---

### Component Properties Checklist

For each component, verify these properties can be set and persist correctly:

#### General Properties (All Components)
- [ ] `label` - Field label text (Unicode supported)
- [ ] `required` - Required field toggle
- [ ] `placeholder` - Placeholder text (Unicode supported)
- [ ] `helpText` - Help text below field (Unicode supported)
- [ ] `layout` - Layout orientation (`vertical` | `horizontal`)
- [ ] `labelAlign` - Label text alignment (`left` | `center` | `right`)
- [ ] `textAlign` - Input text alignment (`left` | `center` | `right`)
- [ ] `validation` - Validation rules object (see Validation Rules Checklist)
- [ ] `validationMessage` - Custom validation message
- [ ] `styleOverrides` - Component-specific style overrides (see Style Overrides Checklist)
- [ ] `exportName` - Export field name for data integration (camelCase)
- [ ] `tabOrder` - Tab order for keyboard navigation (1-based)
- [ ] `width` - Component width (e.g., "100%", "300px", "auto")
- [ ] `componentScale` - Proportional scale factor (50-200%, default 100)
- [ ] `inputWidthMode` - Input width mode (`fill` | `fixed` | `auto`)
- [ ] `inputWidth` - Explicit input width in pixels (when `inputWidthMode = 'fixed'`)
- [ ] `inputWidthOverride` - Input-object-only width override (settable via the Canvas input-only width handle for supported components)
- [ ] `labelWidthOverride` / `helpWidthOverride` - Object-specific width overrides (used by horizontal/mixed layouts)
- [ ] `labelWrap` - Allow label text to wrap (default: true)
- [ ] `labelGapOverride` - Override gap between label and input (pixels)
- [ ] `inputHelpGapOverride` - Override gap between input and help text (pixels)

#### Select/Dropdown-Specific Properties
- [ ] `options` - Array of option objects with `label`, `value`, `disabled`, `group`
- [ ] `allowOther` - Allow "Other" option with free text
- [ ] `otherPlaceholder` - Placeholder for "Other" input
- [ ] `defaultValue` - Default selected value
- [ ] `allowEmpty` - Allow empty selection (show placeholder)
- [ ] `emptyPlaceholder` - Placeholder text for empty selection
- [ ] `searchable` - Enable search/filter in dropdown

#### Checkbox/Radio-Specific Properties
- [ ] `options` - Array of option objects (for groups)
- [ ] `defaultChecked` - Default checked values (array, for checkbox groups)
- [ ] `minSelections` - Minimum number of selections required (checkbox)
- [ ] `maxSelections` - Maximum number of selections allowed (checkbox)
- [ ] `exportMode` - Export mode (`single-value` | `multi-column`)
- [ ] `exportSeparator` - Custom separator for combined export mode
- [ ] `optionsDirection` - Layout direction (`horizontal` | `vertical`)

#### Textarea-Specific Properties
- [ ] `height` - Height in pixels (rows)
- [ ] `resizeMode` - Resize behavior (`none` | `vertical` | `horizontal` | `both` | `auto-grow`)
- [ ] `showCharacterCount` - Show character count

#### Date-Specific Properties
- [ ] `dateType` - Type of date/time input (`date` | `datetime` | `time`)
- [ ] `pickerStyle` - Date picker UI style (`calendar` | `dropdown` | `native`)
- [ ] `dateFormat` - Display format (e.g., "DD/MM/YYYY")
- [ ] `dateParts` - Which date parts to include (year, month, day, hour, minute)
- [ ] `dateRangeLabels` - Labels for date range fields (start, end)

#### Terms & Conditions-Specific Properties
- [ ] `termsUrl` - URL to terms document
- [ ] `termsContent` - Terms document content (for modal display)
- [ ] `termsLinkText` - Link text (e.g., "Terms of Service")

#### Submit Button-Specific Properties
- [ ] `buttonText` - Button text
- [ ] `buttonAction` - Button behavior (`submit` | `submit-and-reset` | `next-page`)
- [ ] `buttonWidth` - Button width (`auto` | `full`)
- [ ] `buttonAlign` - Button alignment (`left` | `center` | `right`)
- [ ] `showLoadingState` - Show loading indicator on submit
- [ ] `disableUntilValid` - Disable until form is valid

#### Address-Specific Properties (Placeholder)
- [ ] `enableAutocomplete` - Enable Google Places autocomplete
- [ ] `decomposeAddress` - Export decomposed address fields
- [ ] `addressExportMapping` - Address subfield mappings for export

#### Style Overrides Checklist
- [ ] Input text typography: `fontFamily`, `fontSize`, `fontWeight`, `fontStyle`, `textColor`, `textBackgroundColor`, `textBorderColor`, `textBorderWidth`, `textBorderRadius`
- [ ] Label typography: `labelFontFamily`, `labelFontSize`, `labelFontWeight`, `labelFontStyle`, `labelColor`, `labelBackgroundColor`, `labelBorderColor`, `labelBorderWidth`, `labelBorderRadius`
- [ ] Help text typography: `helpTextFontFamily`, `helpTextFontSize`, `helpTextFontWeight`, `helpTextFontStyle`, `helpTextColor`, `helpTextBackgroundColor`, `helpTextBorderColor`, `helpTextBorderWidth`, `helpTextBorderRadius`
- [ ] Borders & spacing: `borderRadius`, `borderWidth`, `inputHeight`, `labelGap`, `inputHelpGap`
- [ ] Legacy colors: `placeholderColor`, `backgroundColor`, `borderColor`

---

### Validation Rules Checklist

#### General Rules (All Components)
- [ ] `required` - Field is required
- [ ] `customError` - Custom error message (Unicode string)

#### Text Rules (text, textarea, first-name)
- [ ] `minLength` - Minimum character length (Unicode graphemes)
- [ ] `maxLength` - Maximum character length (Unicode graphemes)
- [ ] `pattern` - Regex pattern (use /u flag for Unicode support)
- [ ] `alpha` - Alpha only (letters)
- [ ] `alphanumeric` - Alphanumeric (letters and digits)
- [ ] `noHtmlScript` - Block HTML tags and script content (XSS prevention)
- [ ] `trimWhitespace` - Automatically trim leading/trailing whitespace
- [ ] `noConsecutiveSpaces` - Prevent multiple consecutive spaces
- [ ] `caseTransform` - Auto-transform text case (`uppercase` | `lowercase` | `titlecase`)
- [ ] `blockedCharacters` - Characters that are not allowed
- [ ] `mustMatchField` - Field ID that this value must match (confirmation fields)

#### Number Rules
- [ ] `numeric` - Numeric only (digits)
- [ ] `minValue` - Minimum numeric value
- [ ] `maxValue` - Maximum numeric value
- [ ] `integerOnly` - No decimal values allowed
- [ ] `decimalPrecision` - Maximum number of decimal places
- [ ] `stepIncrement` - Value must be a multiple of this number
- [ ] `positiveOnly` - Must be greater than zero
- [ ] `nonNegative` - Zero or positive only (no negatives)
- [ ] `nonZero` - Cannot be exactly zero
- [ ] `oddOnly` - Only odd numbers allowed
- [ ] `evenOnly` - Only even numbers allowed
- [ ] `allowedValues` - Only these specific numbers are valid

#### Email Rules
- [ ] `email` - Email format validation
- [ ] `businessEmailOnly` - Block free email providers (gmail, yahoo, hotmail, etc.)
- [ ] `domainWhitelist` - Only accept emails from these domains
- [ ] `domainBlacklist` - Reject emails from these domains
- [ ] `noDisposableEmail` - Block known disposable/temporary email providers
- [ ] `noPlusAddressing` - Block email+tag@domain format

#### Phone Rules
- [ ] `phone` - Phone number validation
- [ ] `countryCodeRequired` - Must include country code (+XX)
- [ ] `allowedCountries` - Only accept phone numbers from these countries (ISO codes)
- [ ] `mobileOnly` - Only accept mobile numbers (reject landlines)

#### URL Rules
- [ ] `url` - URL format validation

#### Date Rules
- [ ] `minDate` - Earliest allowed date (YYYY-MM-DD or "today")
- [ ] `maxDate` - Latest allowed date (YYYY-MM-DD or "today")
- [ ] `futureOnly` - Date must be in the future
- [ ] `pastOnly` - Date must be in the past
- [ ] `minimumAge` - User must be at least N years old
- [ ] `maximumAge` - User cannot be older than N years
- [ ] `weekdaysOnly` - Only weekdays allowed (no Saturday/Sunday)
- [ ] `isDateRange` - Enable date range selection (start + end dates)
- [ ] `maxDateRangeSpan` - Maximum days between start and end date
- [ ] `minDateRangeSpan` - Minimum days between start and end date

---

### Logic Rules Checklist

#### Logic Operators
- [ ] `equals` - Source value equals specified value
- [ ] `notEquals` - Source value does not equal specified value
- [ ] `contains` - Source value contains specified substring
- [ ] `isEmpty` - Source value is empty (null, undefined, empty string, empty array)

#### Logic Actions
- [ ] `show` - Show target component (make visible)
- [ ] `hide` - Hide target component (make invisible)
- [ ] `require` - Make target component required
- [ ] `unrequire` - Make target component not required
- [ ] `enable` - Enable target component (allow input)
- [ ] `disable` - Disable target component (block input)

#### Logic Rule Properties
- [ ] `id` - Unique rule identifier
- [ ] `enabled` - Rule is enabled/active
- [ ] `name` - Optional user-friendly name for rule management
- [ ] `when.sourceComponentId` - Source component ID
- [ ] `when.operator` - Logic operator
- [ ] `when.value` - Value for equals/notEquals/contains (omitted for isEmpty)
- [ ] `then.targetComponentId` - Target component ID
- [ ] `then.action` - Logic action to apply

---

### Recommended UAT Test Form Templates

Create/ensure at least **two** forms (or two versions of the same form) using the **Builder UI**, then **Save Draft** (Story 3.9).

#### Template A — Canvas Fidelity Form (Layout Verification)

**Use Case:** A marketing team needs a simple contact form to verify that component positions, canvas dimensions, and layout fidelity are preserved exactly between the form builder and public preview. This form tests absolute positioning and canvas settings.

**Template A — Current execution status (carry forward)**

| Step | Status | Notes |
|------|--------|------|
| 1 | ✅ Pass | Background color persists in API (see Step 1 note). |
| 2 | ✅ Pass | — |
| 3 | ✅ Pass | — |
| 4 | ✅ Pass | Email `validation.maxLength` is editable and applies correctly. |
| 5 | ✅ Pass | Component is named **Dropdown** in UI (not “Select”). |
| 6 | ✅ Pass | Divider properties panel exists; color/thickness/length configurable. |
| 7 | ✅ Pass | Submit button settings include loading state + icon; tabOrder available; preview matches canvas sizing. |
| 8 | ✅ Pass | — |
| 9 | ✅ Pass | — |
| 10 | ✅ Pass | Submit button width matches; background color persists. |

**⚠️ Current Platform Limitations (as of Form 38 build):**
- **Canvas Size:** Canvas width/height configuration is not available in UI (future story). Canvas dimensions can be verified via API/DB inspection.
- **Paragraph Component:** Does not exist. Use **Long Text** (textarea) component instead as a substitute.
- **Color Format:** Color picker accepts hex format (#RRGGBB). If you see RGB-only input, hex codes work in the hex input field.
- ~~**Email maxLength:** Not available in properties panel (will be fixed). Skip this validation for now.~~ ✅ **Fixed:** Email `validation.maxLength` is now editable (see Step 4).
- ~~**Divider Properties:** Divider has no properties panel (will be fixed). Divider renders correctly in preview but cannot be styled in builder yet.~~ ✅ **Fixed:** Divider has a properties panel (color/thickness/length), and supports per-divider length override.
- ~~**Submit Button tabOrder:** Not available (will be fixed).~~ ✅ **Available:** Submit Button `tabOrder` is editable (see Step 7).
- **Component Positioning:** Drag-and-drop may result in ±4px variance from exact coordinates. This is acceptable.

**Step-by-Step Build Instructions:**

**Step 1: Configure Canvas Background**
- Open form builder for new form
- In the **Background** tab, set the page background color to `#F9FAFB` (light gray) - **Available**
- **Persistence check (required):** Ensure the public preview API response includes one of:
  - `definition.pages[0].background.value === "#F9FAFB"` (preferred, page-level background), and/or
  - `definition.canvasSettings.backgroundColor === "#F9FAFB"` (compat field)
- ⚠️ **Skip:** `canvasSettings.width` and `canvasSettings.height` are not available in UI (future story)
- **Note:** Canvas dimensions will be verified via API/DB inspection after save

**Step 2: Add Long Text Component (Paragraph Substitute)**
- Drag **Long Text** (textarea) component to canvas at position (80, 60)
- **Note:** Paragraph component doesn't exist, using Long Text as substitute
- Set `label`: "Contact Us"
- Set `styleOverrides.helpTextFontSize`: 18
- Set `styleOverrides.helpTextFontWeight`: 600
- Set `styleOverrides.helpTextColor`: "#111827" (or `rgb(17, 24, 39)` if RGB input is shown)
- **Note:** Position may vary by ±4px due to drag-and-drop limitations (acceptable)

**Step 3: Add Text Input Field (Left Side)**
- Drag **Text** component to canvas at position (120, 180)
- Set `label`: "Full Name"
- Set `required`: true
- Set `placeholder`: "Enter your full name"
- Set `tabOrder`: 1
- Set `layout`: "vertical"
- Set `validation.maxLength`: 100
- Set `styleOverrides.labelFontSize`: 14
- Set `styleOverrides.labelFontWeight`: 500
- Set `styleOverrides.labelColor`: "#374151"
- Set `styleOverrides.textBorderColor`: "#D1D5DB"
- Set `styleOverrides.textBorderWidth`: 1
- Set `styleOverrides.textBorderRadius`: 4
- Set `exportName`: "fullName"
- Verify component is positioned at (120, 180)

**Step 4: Add Email Input Field (Right Side)**
- Drag **Email** component to canvas at position (520, 180)
- Set `label`: "Email Address"
- Set `required`: true
- Set `placeholder`: "your.email@company.com"
- Set `tabOrder`: 2
- Set `layout`: "vertical"
- Set `validation.email`: true
- Set `validation.maxLength`: 254
- Set `styleOverrides.labelFontSize`: 14
- Set `styleOverrides.labelFontWeight`: 500
- Set `styleOverrides.labelColor`: "#374151" (or `rgb(55, 65, 81)`)
- Set `styleOverrides.textBorderColor`: "#D1D5DB" (or `rgb(209, 213, 219)`)
- Set `styleOverrides.textBorderWidth`: 1
- Set `styleOverrides.textBorderRadius`: 4
- Set `exportName`: "emailAddress"
- **Note:** Position may vary by ±4px (acceptable)

**Step 5: Add Dropdown (Select)**
- Drag **Dropdown** component to canvas at position (120, 320)
- Set `label`: "Subject"
- Set `required`: true
- Set `placeholder`: "Select a subject"
- Set `tabOrder`: 3
- Set `layout`: "vertical"
- Set `options`: [
    { label: "General Inquiry", value: "general" },
    { label: "Support Request", value: "support" },
    { label: "Sales Inquiry", value: "sales" },
    { label: "Other", value: "other" }
  ]
- Set `styleOverrides.labelFontSize`: 14
- Set `styleOverrides.labelFontWeight`: 500
- Set `styleOverrides.labelColor`: "#374151"
- Set `exportName`: "subject"
- Verify component is positioned at (120, 320) - **below Full Name**

**Step 6: Add Divider**
- Drag **Divider** component to canvas at position (120, 460)
- Use the Divider properties panel to set:
  - Divider color
  - Divider thickness (px)
  - Divider length (global default or per-divider override)
- **Note:** Divider will render correctly in preview but may look like text component in builder
- **Note:** Position may vary by ±4px (acceptable)

**Step 7: Add Submit Button**
- Drag **Submit Button** component to canvas at position (120, 520)
- Set `buttonText`: "Send Message"
- Set `buttonAction`: "submit"
- Set `buttonWidth`: "auto"
- Set `buttonAlign`: "left"
- Set `showLoadingState`: true
- Set `showIcon`: true
- Set `disableUntilValid`: true
- Set `tabOrder`: 4
- **Note:** Submit button will render correctly in preview but may look like text component in builder
- **Note:** Position may vary by ±4px (acceptable)

**Step 8: Verify Component Positions**
- In Builder, verify all components are approximately at their specified positions (allow ±4px variance):
  - Long Text (Paragraph substitute): ~(80, 60)
  - Full Name (Text): ~(120, 180)
  - Email Address: ~(520, 180) - **same Y as Full Name, different X**
  - Subject (Select): ~(120, 320)
  - Divider: ~(120, 460)
  - Submit Button: ~(120, 520)
- Verify components are **not** in a simple vertical stack (Email is offset to the right)
- ⚠️ **Skip:** Canvas dimensions verification (not available in UI, verify via API/DB)

**Step 9: Save Draft**
- Click **Save Draft** button
- Verify success message appears
- ⚠️ **Note:** Canvas dimensions will be verified via API/DB inspection (not available in UI)
- Note the form ID for later testing (e.g., Form 38)

**Step 10: Verify in Preview**
- Click **Preview** button
- Verify all components render correctly:
  - Long Text displays as text (not textarea input)
  - Divider displays as horizontal line (not text component)
  - Submit button displays as styled button (not text component)
- Verify Submit Button width matches the canvas (no unexpected full-width expansion unless `buttonWidth: "full"` is set)
- Verify background color matches (#F9FAFB)
- Verify Email Address is positioned to the right of Full Name (same Y coordinate)
- Verify component positioning is preserved from builder
- ⚠️ **Note:** Exact pixel positions may vary by ±4px (acceptable)

#### Template B — Logic-Enabled Form (Runtime Rules Testing)

**Use Case:** A product team needs a simple form to test all logic rule actions (show/hide, enable/disable, require/unrequire) work correctly. This form uses a single source field to trigger multiple target fields, testing each action type systematically.

**Template B — Current execution status (carry forward)**

| Step | Status | Notes |
|------|--------|------|
| 1 | ✅ Pass | Canvas size not configurable in UI; background color set successfully. |
| 2 | ⏭️ Skip | Header component removed from test run. |
| 3 | ⏭️ Skip | Paragraph component removed from test run. |
| 4 | ✅ Pass | Added Dropdown and configured all settings. |
| 5 | ⚠️ Pass (issue) | Properties set successfully, but component was positioned overlapping another component (done via keyboard). |
| 6 | ⚠️ Pass (issue) | Step passed, but component overlapped another component (keyboard positioning). |
| 7 | ⚠️ Pass (issue) | Step passed, but component overlapped another component (keyboard positioning). |
| 8 | ✅ Pass | — |
| 9 | ✅ Pass | Added rules successfully. |
| 10 | ✅ Pass | — |
| 11 | ✅ Pass | — |
| 12 | ✅ Pass | — |

**Step-by-Step Build Instructions:**

**Step 1: Configure Canvas Background**
- Open form builder for new form
- In the **Background** tab, set the page background color (e.g., `#FFFFFF`)
- ⚠️ **Skip:** `canvasSettings.width/height` are not configurable in UI yet

**Step 2: (Optional) Add Header Component**
- Drag **Header** component to canvas at position (100, 50)
- Set `label`: "Logic Rules Test Form"
- Set `styleOverrides.labelFontSize`: 24
- Set `styleOverrides.labelFontWeight`: 700
- Set `styleOverrides.labelColor`: "#111827"

**Step 3: (Optional) Add Paragraph Component**
- Drag **Paragraph** component to canvas at position (100, 100)
- Set `label`: "Select 'Yes' or 'No' below to test logic rules. Each target field will respond differently."
- Set `styleOverrides.helpTextFontSize`: 14
- Set `styleOverrides.helpTextColor`: "#6B7280"

**Step 4: Add Field A - Source Field (Dropdown)**
- Drag **Dropdown** component to canvas at position (100, 180)
- Set `label`: "Do you want to proceed?"
- Set `required`: true
- Set `placeholder`: "Select Yes or No"
- Set `tabOrder`: 1
- Set `layout`: "vertical"
- Set `options`: [
    { label: "Yes", value: "Y" },
    { label: "No", value: "N" }
  ]
- Set `styleOverrides.labelFontSize`: 16
- Set `styleOverrides.labelFontWeight`: 600
- Set `styleOverrides.labelColor`: "#374151"
- Set `exportName`: "proceed"
- **Note:** This is the source field that will trigger all logic rules

**Step 5: Add Field B - Target for Visibility (Text)**
- Drag **Text** component to canvas at position (100, 280)
- Set `label`: "Field B - Visibility Test"
- Set `required`: false
- Set `placeholder`: "This field will show/hide"
- Set `tabOrder`: 2
- Set `layout`: "vertical"
- Set `validation.maxLength`: 100
- Set `styleOverrides.labelFontSize`: 14
- Set `styleOverrides.labelColor`: "#374151"
- Set `exportName`: "fieldB"
- **Note:** This field will be hidden initially, shown when Field A = "Y"

**Step 6: Add Field C - Target for Enable/Disable (Text)**
- Drag **Text** component to canvas at position (100, 380)
- Set `label`: "Field C - Enable/Disable Test"
- Set `required`: false
- Set `placeholder`: "This field will enable/disable"
- Set `tabOrder`: 3
- Set `layout`: "vertical"
- Set `validation.maxLength`: 100
- Set `styleOverrides.labelFontSize`: 14
- Set `styleOverrides.labelColor`: "#374151"
- Set `exportName`: "fieldC"
- **Note:** This field will be disabled initially, enabled when Field A = "Y"

**Step 7: Add Field D - Target for Require/Unrequire (Email)**
- Drag **Email** component to canvas at position (100, 480)
- Set `label`: "Field D - Require/Unrequire Test"
- Set `required`: false (will be set via logic)
- Set `placeholder`: "This field will require/unrequire"
- Set `tabOrder`: 4
- Set `layout`: "vertical"
- Set `validation.email`: true
- Set `validation.maxLength`: 254
- Set `styleOverrides.labelFontSize`: 14
- Set `styleOverrides.labelColor`: "#374151"
- Set `exportName`: "fieldD"
- **Note:** This field will be not required initially, required when Field A = "Y"

**Step 8: Add Submit Button**
- Drag **Submit Button** component to canvas at position (100, 580)
- Set `buttonText`: "Submit"
- Set `buttonAction`: "submit"
- Set `buttonWidth`: "auto"
- Set `buttonAlign`: "left"
- Set `showLoadingState`: true
- Set `disableUntilValid`: true
- Set `tabOrder`: 5

**Step 9: Configure Logic Rules**

**Rule 1: Show Field B when Field A = "Y"**
- Create logic rule:
  - `name`: "Show Field B when Yes"
  - `enabled`: true
  - `when.sourceComponentId`: [Field A (Select) component ID]
  - `when.operator`: "equals"
  - `when.value`: "Y"
  - `then.targetComponentId`: [Field B (Text) component ID]
  - `then.action`: "show"

**Rule 2: Hide Field B when Field A = "N"**
- Create logic rule:
  - `name`: "Hide Field B when No"
  - `enabled`: true
  - `when.sourceComponentId`: [Field A (Select) component ID]
  - `when.operator`: "equals"
  - `when.value`: "N"
  - `then.targetComponentId`: [Field B (Text) component ID]
  - `then.action`: "hide"

**Rule 3: Enable Field C when Field A = "Y"**
- Create logic rule:
  - `name`: "Enable Field C when Yes"
  - `enabled`: true
  - `when.sourceComponentId`: [Field A (Select) component ID]
  - `when.operator`: "equals"
  - `when.value`: "Y"
  - `then.targetComponentId`: [Field C (Text) component ID]
  - `then.action`: "enable"

**Rule 4: Disable Field C when Field A = "N"**
- Create logic rule:
  - `name`: "Disable Field C when No"
  - `enabled`: true
  - `when.sourceComponentId`: [Field A (Select) component ID]
  - `when.operator`: "equals"
  - `when.value`: "N"
  - `then.targetComponentId`: [Field C (Text) component ID]
  - `then.action`: "disable"

**Rule 5: Require Field D when Field A = "Y"**
- Create logic rule:
  - `name`: "Require Field D when Yes"
  - `enabled`: true
  - `when.sourceComponentId`: [Field A (Select) component ID]
  - `when.operator`: "equals"
  - `when.value`: "Y"
  - `then.targetComponentId`: [Field D (Email) component ID]
  - `then.action`: "require"

**Rule 6: Unrequire Field D when Field A = "N"**
- Create logic rule:
  - `name`: "Unrequire Field D when No"
  - `enabled`: true
  - `when.sourceComponentId`: [Field A (Select) component ID]
  - `when.operator`: "equals"
  - `when.value`: "N"
  - `then.targetComponentId`: [Field D (Email) component ID]
  - `then.action`: "unrequire"

**Step 10: Verify Initial State**
- In Builder, verify initial state:
  - Field B (Visibility Test) is **hidden** (not visible)
  - Field C (Enable/Disable Test) is **disabled** (grayed out, cannot type)
  - Field D (Require/Unrequire Test) is **not required** (no red asterisk)
- Verify all 6 logic rules are configured and enabled

**Step 11: Save Draft**
- Click **Save Draft** button
- Verify success message appears
- Verify logic rules are persisted (check `logic.rules` in saved definition)
- Note the form ID for later testing

**Step 12: Verify in Preview**
- Click **Preview** button
- Verify initial state matches builder:
  - Field B is hidden
  - Field C is disabled
  - Field D is not required
- Test logic rules:
  - Select "Yes" in Field A → Field B appears, Field C enables, Field D becomes required
  - Select "No" in Field A → Field B hides, Field C disables, Field D becomes not required
- Verify all actions execute immediately (no delay)
Use the same structure as Story 3.7’s UAT template:
- Field A (Source): Select/Radio with values `Y` and `N` (values matter)
- Field B (Target for visibility)
- Field C (Target for enabled)
- Field D (Target for required)
- Ensure rules are persisted into `logic.rules` and the form is saved.

#### Template C — Event Registration Form (Comprehensive Component & Validation)

**Use Case:** A conference organizer needs an event registration form that captures attendee information with strict validation rules. The form must validate business emails only, require country codes for phone numbers, limit attendee counts, and conditionally show fields based on selections.

**Latest Test Run Notes (Tony – Jan 6, 2026)**
- **Step 1**: Skipped (Header component does not exist)
- **Step 2**: Skipped (Paragraph component does not exist)
- **Step 3**: Passed
- **Step 4**: Passed
- **Step 5**: Passed
- **Step 6**: Passed
- **Step 7**: Passed (properties editable), but **expected UX gap**:
  - When `allowOther: true`, expected an **inline “Other” text input** beside the dropdown.
  - Canvas should show the extra input when `allowOther` is enabled (so users can size/position correctly).
  - Preview/Production should show the extra input **only when “Other” is selected**.
  - The “Other” text input needs its **own text validation rules** (different to dropdown rules).
- **Step 8**: Passed
- **Step 9**: Passed, but could not find how to set the **numeric flag** to true in Properties Panel
- **Step 10**: Passed
- **Step 11**: Confusing default Object Layout (Input appeared left of Label; expected Label then Input)
- **Step 12**: Height/resize UX unclear; textarea “lines required” + green fit indicator **not working anymore**
- **Step 13**: Passed (no textarea indicator issue on this one)
- **Step 14**: Issue: setting `weekdaysOnly` deselects `futureOnly` (should allow both)
- **Step 15**: Passed
- **Step 16**: Passed
- **Step 17**:
  - Rule 1: Passed
  - Rule 2: Missing operators (`contains`, `<`, `>`) — operator set should depend on source field type (e.g., number vs text)
  - Rule 3: Added
- **Step 18**: Passed
- **Step 19**: Validation Message UX unclear (expected custom regex validation message semantics). Needs review for canvas + preview.

**Step-by-Step Build Instructions:**

**Step 1: Add Header Component**
- Drag **Header** component to canvas at position (100, 50)
- Set `label`: "Event Registration"
- Set `styleOverrides.labelFontSize`: 24
- Set `styleOverrides.labelFontWeight`: 700
- Set `styleOverrides.labelColor`: "#1F2937"

**Step 2: Add Paragraph Component**
- Drag **Paragraph** component to canvas at position (100, 100)
- Set `label`: "Please complete all required fields. Business email addresses only."
- Set `styleOverrides.helpTextFontSize`: 14
- Set `styleOverrides.helpTextColor`: "#6B7280"

**Step 3: Add First Name Field**
- Drag **First Name** component to canvas at position (100, 180)
- Set `label`: "First Name"
- Set `required`: true
- Set `placeholder`: "Enter your first name"
- Set `tabOrder`: 1
- Set `layout`: "horizontal"
- Set `validation.maxLength`: 30
- Set `validation.alpha`: true
- Set `validationMessage`: "First name must be letters only, maximum 30 characters"
- Set `styleOverrides.labelFontFamily`: "Inter" (or any custom font)
- Set `styleOverrides.labelFontSize`: 14
- Set `styleOverrides.labelFontWeight`: 600
- Set `styleOverrides.labelColor`: "#374151"
- Set `styleOverrides.textBorderColor`: "#D1D5DB"
- Set `styleOverrides.textBorderWidth`: 1
- Set `styleOverrides.textBorderRadius`: 4
- Set `exportName`: "firstName"

**Step 4: Add Last Name Field**
- Drag **Text** component to canvas at position (100, 250)
- Set `label`: "Last Name"
- Set `required`: true
- Set `placeholder`: "Enter your last name"
- Set `tabOrder`: 2
- Set `layout`: "horizontal"
- Set `validation.maxLength`: 30
- Set `validation.alpha`: true
- Set `validationMessage`: "Last name must be letters only, maximum 30 characters"
- Set `exportName`: "lastName"

**Step 5: Add Email Address Field**
- Drag **Email** component to canvas at position (100, 320)
- Set `label`: "Business Email Address"
- Set `required`: true
- Set `placeholder`: "name@company.com"
- Set `tabOrder`: 3
- Set `layout`: "vertical"
- Set `validation.maxLength`: 254
- Set `validation.businessEmailOnly`: true
- Set `validation.domainBlacklist`: ["test.com", "example.com"]
- Set `validation.noDisposableEmail`: true
- Set `validation.noPlusAddressing`: true
- Set `validationMessage`: "Please use a business email address. Free email providers and test.com are not allowed."
- Set `exportName`: "emailAddress"

**Step 6: Add Phone Number Field**
- Drag **Phone** component to canvas at position (100, 400)
- Set `label`: "Phone Number"
- Set `required`: true
- Set `placeholder`: "+61 400 000 000"
- Set `tabOrder`: 4
- Set `layout`: "vertical"
- Set `validation.maxLength`: 20
- Set `validation.countryCodeRequired`: true
- Set `validation.phone`: true
- Set `validationMessage`: "Phone number must include country code (e.g., +61)"
- Set `exportName`: "phoneNumber"

**Step 7: Add Event Type Select**
- Drag **Select** component to canvas at position (100, 480)
- Set `label`: "Event Type"
- Set `required`: true
- Set `placeholder`: "Select event type"
- Set `tabOrder`: 5
- Set `layout`: "vertical"
- Set `allowOther`: true
- Set `otherPlaceholder`: "Please specify other event type"
- Set `options`: [
    { label: "Conference", value: "conference" },
    { label: "Workshop", value: "workshop" },
    { label: "Webinar", value: "webinar" },
    { label: "Other", value: "other" }
  ]
- Set `exportName`: "eventType"

**Step 8: Add Other Event Type Field (for logic)**
- Drag **Text** component to canvas at position (100, 560)
- Set `label`: "Other Event Type"
- Set `required`: false
- Set `placeholder`: "Specify event type"
- Set `tabOrder`: 6
- Set `layout`: "vertical"
- Set `validation.maxLength`: 100
- Set `exportName`: "otherEventType"
- **Note:** This field will be hidden initially, shown via logic rule

**Step 9: Add Number of Attendees Field**
- Drag **Number** component to canvas at position (100, 640)
- Set `label`: "Number of Attendees"
- Set `required`: true
- Set `placeholder`: "1"
- Set `tabOrder`: 7
- Set `layout`: "vertical"
- Set `validation.minValue`: 1
- Set `validation.maxValue`: 50
- Set `validation.integerOnly`: true
- Set `validation.positiveOnly`: true
- Set `validation.numeric`: true
- Set `validationMessage`: "Please enter a number between 1 and 50"
- Set `exportName`: "numberOfAttendees"

**Step 10: Add Company Name Field (for logic)**
- Drag **Text** component to canvas at position (100, 720)
- Set `label`: "Company Name"
- Set `required`: false
- Set `placeholder`: "Enter company name"
- Set `tabOrder`: 8
- Set `layout`: "vertical"
- Set `validation.maxLength`: 100
- Set `exportName`: "companyName"
- **Note:** This field will become required via logic rule when attendees > 10

**Step 11: Add Dietary Requirements Checkbox**
- Drag **Checkbox** component to canvas at position (100, 800)
- Set `label`: "Dietary Requirements"
- Set `required`: false
- Set `tabOrder`: 9
- Set `options`: [
    { label: "Vegetarian", value: "vegetarian" },
    { label: "Vegan", value: "vegan" },
    { label: "Gluten-Free", value: "gluten-free" },
    { label: "Halal", value: "halal" },
    { label: "Kosher", value: "kosher" },
    { label: "None", value: "none" }
  ]
- Set `minSelections`: 0
- Set `maxSelections`: 6
- Set `optionsDirection`: "horizontal"
- Set `exportName`: "dietaryRequirements"

**Step 12: Add Allergy Information Textarea (for logic)**
- Drag **Textarea** component to canvas at position (100, 900)
- Set `label`: "Allergy Information"
- Set `required`: false
- Set `placeholder`: "Please list any allergies or dietary restrictions"
- Set `tabOrder`: 10
- Set `layout`: "vertical"
- Set `validation.maxLength`: 500
- Set `height`: 4
- Set `resizeMode`: "vertical"
- Set `exportName`: "allergyInformation"
- **Note:** This field will be enabled via logic rule when dietary requirements include Vegetarian or Vegan

**Step 13: Add Special Requests Textarea**
- Drag **Textarea** component to canvas at position (100, 1020)
- Set `label`: "Special Requests"
- Set `required`: false
- Set `placeholder`: "Any special accommodation requests?"
- Set `tabOrder`: 11
- Set `layout`: "vertical"
- Set `validation.maxLength`: 500
- Set `showCharacterCount`: true
- Set `height`: 4
- Set `resizeMode`: "vertical"
- Set `exportName`: "specialRequests"

**Step 14: Add Event Date Field**
- Drag **Date** component to canvas at position (100, 1140)
- Set `label`: "Preferred Event Date"
- Set `required`: true
- Set `tabOrder`: 12
- Set `layout`: "vertical"
- Set `validation.futureOnly`: true
- Set `validation.weekdaysOnly`: true
- Set `validationMessage`: "Please select a weekday in the future"
- Set `exportName`: "preferredEventDate"

**Step 15: Add Terms & Conditions**
- Drag **Terms & Conditions** component to canvas at position (100, 1220)
- Set `label`: "I agree to the"
- Set `required`: true
- Set `termsLinkText`: "Event Terms and Conditions"
- Set `termsUrl`: "" (or provide URL if available)
- Set `tabOrder`: 13
- Set `exportName`: "termsAccepted"

**Step 16: Add Submit Button**
- Drag **Submit Button** component to canvas at position (100, 1300)
- Set `buttonText`: "Register for Event"
- Set `buttonAction`: "submit"
- Set `buttonWidth`: "auto"
- Set `buttonAlign`: "left"
- Set `showLoadingState`: true
- Set `disableUntilValid`: true
- Set `tabOrder`: 14

**Step 17: Configure Logic Rules**

**Rule 1: Show Other Event Type when Event Type = "Other"**
- Create logic rule:
  - `when.sourceComponentId`: [Event Type select component ID]
  - `when.operator`: "equals"
  - `when.value`: "other"
  - `then.targetComponentId`: [Other Event Type text component ID]
  - `then.action`: "show"
- Create second rule:
  - `when.sourceComponentId`: [Event Type select component ID]
  - `when.operator`: "notEquals"
  - `when.value`: "other"
  - `then.targetComponentId`: [Other Event Type text component ID]
  - `then.action`: "hide"

**Rule 2: Require Company Name when Number of Attendees > 10**
- **Note:** This requires a numeric comparison rule. Use:
  - `when.sourceComponentId`: [Number of Attendees component ID]
  - `when.operator`: "greaterThan"
  - `when.value`: "10"
  - `then.targetComponentId`: [Company Name component ID]
  - `then.action`: "require"
- Create second rule for values ≤ 10:
  - `when.sourceComponentId`: [Number of Attendees component ID]
  - `when.operator`: "lessThanOrEqual"
  - `when.value`: "10"
  - `then.targetComponentId`: [Company Name component ID]
  - `then.action`: "unrequire"

> **✅ UAT Note (2026-01-12):** Test 2 PASSED after numeric comparison operators (`greaterThan`, `lessThan`, etc.) were added to the backend schema. Rule creation and persistence now works correctly.

**Rule 3: Enable Allergy Information when Dietary Requirements contains "Vegetarian" or "Vegan"**
- **Note:** Checkbox values are arrays. Test with:
  - `when.sourceComponentId`: [Dietary Requirements checkbox component ID]
  - `when.operator`: "contains"
  - `when.value`: "vegetarian"
  - `then.targetComponentId`: [Allergy Information textarea component ID]
  - `then.action`: "enable"
- Create second rule for "vegan":
  - `when.sourceComponentId`: [Dietary Requirements checkbox component ID]
  - `when.operator`: "contains"
  - `when.value`: "vegan"
  - `then.targetComponentId`: [Allergy Information textarea component ID]
  - `then.action`: "enable"

> **⚠️ UAT Note (2026-01-12):** Rule creation passed, but **testing blocked** because there is no way to preset a component's initial state (e.g., start with disabled=true). To test the `enable` action, the target component must start in a disabled state so the logic can enable it when the condition is met. **ACTION REQUIRED:** Add support for setting initial component state (disabled, hidden, etc.) in a future Story.

**Step 18: Save Draft**
- Click **Save Draft** button
- Verify success message appears
- Note the form ID for later testing

**Step 19: Verify in Preview**
- Click **Preview** button
- Verify all components render correctly
- Verify all validation rules work
- Verify all logic rules execute correctly

#### Template D — Customer Satisfaction Survey (Complete Logic & Styling Showcase)

**Use Case:** A company needs a customer satisfaction survey that adapts dynamically based on customer responses. Corporate clients must provide company names, dissatisfied customers must explain why, and contact preferences determine which contact fields are required. The form showcases comprehensive styling capabilities.

**Step-by-Step Build Instructions:**

**Step 1: Add Header Component**
- Drag **Header** component to canvas at position (100, 50)
- Set `label`: "Customer Satisfaction Survey"
- Set `styleOverrides.labelFontSize`: 28
- Set `styleOverrides.labelFontWeight`: 700
- Set `styleOverrides.labelColor`: "#111827"
- Set `styleOverrides.labelFontFamily`: "Inter" (or custom font)

> **⚠️ UAT Note (2026-01-12):** SKIPPED - Header component not yet available in the component toolbox.

**Step 2: Add Paragraph Component**
- Drag **Paragraph** component to canvas at position (100, 100)
- Set `label`: "Your feedback helps us improve. Please take a few minutes to complete this survey."
- Set `styleOverrides.helpTextFontSize`: 16
- Set `styleOverrides.helpTextColor`: "#4B5563"
- Set `styleOverrides.helpTextFontWeight`: 400

> **⚠️ UAT Note (2026-01-12):** SKIPPED - Paragraph component not yet available in the component toolbox.

**Step 3: Add Customer Type Radio**
- Drag **Radio** component to canvas at position (100, 180)
- Set `label`: "Customer Type"
- Set `required`: true
- Set `tabOrder`: 1
- Set `layout`: "vertical"
- Set `options`: [
    { label: "New Customer", value: "new" },
    { label: "Returning Customer", value: "returning" },
    { label: "Corporate Client", value: "corporate" }
  ]
- Set `optionsDirection`: "vertical"
- Set `styleOverrides.labelFontSize`: 16
- Set `styleOverrides.labelFontWeight`: 600
- Set `exportName`: "customerType"

> **✅ UAT Note (2026-01-12):** PASSED

**Step 4: Add Company Name Field**
- Drag **Text** component to canvas at position (100, 320)
- Set `label`: "Company Name"
- Set `required`: false (will be set via logic)
- Set `placeholder`: "Enter your company name"
- Set `tabOrder`: 2
- Set `layout`: "horizontal"
- Set `validation.minLength`: 2
- Set `validation.maxLength`: 100
- Set `validation.alpha`: false (allow spaces and special chars for company names)
- Set `validationMessage`: "Company name must be between 2 and 100 characters"
- Set `styleOverrides.labelFontFamily`: "Roboto"
- Set `styleOverrides.labelFontSize`: 14
- Set `styleOverrides.textBorderColor`: "#9CA3AF"
- Set `styleOverrides.textBorderWidth`: 2
- Set `styleOverrides.textBorderRadius`: 6
- Set `exportName`: "companyName"
- **Note:** This field will be hidden initially, shown and required via logic

> **✅ UAT Note (2026-01-12):** PASSED

**Step 5: Add Satisfaction Rating Select**
- Drag **Select** component to canvas at position (100, 400)
- Set `label`: "Overall Satisfaction Rating"
- Set `required`: true
- Set `placeholder`: "Select your satisfaction level"
- Set `tabOrder`: 3
- Set `layout`: "vertical"
- Set `options`: [
    { label: "Very Satisfied", value: "very-satisfied" },
    { label: "Satisfied", value: "satisfied" },
    { label: "Neutral", value: "neutral" },
    { label: "Dissatisfied", value: "dissatisfied" },
    { label: "Very Dissatisfied", value: "very-dissatisfied" }
  ]
- Set `styleOverrides.labelFontSize`: 15
- Set `styleOverrides.labelFontWeight`: 600
- Set `exportName`: "satisfactionRating"

> **✅ UAT Note (2026-01-12):** PASSED

**Step 6: Add Reason for Rating Textarea**
- Drag **Textarea** component to canvas at position (100, 480)
- Set `label`: "Reason for Your Rating"
- Set `required`: false (will be set via logic)
- Set `placeholder`: "Please explain your rating..."
- Set `tabOrder`: 4
- Set `layout`: "vertical"
- Set `validation.minLength`: 10
- Set `validation.maxLength`: 1000
- Set `validationMessage`: "Please provide at least 10 characters explaining your rating"
- Set `showCharacterCount`: true
- Set `height`: 5
- Set `resizeMode`: "vertical"
- Set `styleOverrides.helpTextFontSize`: 12
- Set `styleOverrides.helpTextColor`: "#6B7280"
- Set `exportName`: "reasonForRating"
- **Note:** This field will be required via logic when rating is Dissatisfied or Very Dissatisfied

> **⚠️ UAT Note (2026-01-12):** PARTIAL PASS - Textarea component added successfully. However, the following properties are **not visible in the Properties Panel UI**:
> - `showCharacterCount` - No toggle/checkbox found to enable character count display
> - `height` - Unclear which property controls textarea height (rows vs pixels)
> - `resizeMode` - No option found to set resize behavior (vertical/horizontal/auto-grow)
> **ACTION REQUIRED:** Add these properties to the Textarea PropertiesPanel section or document where they are located.

**Step 7: Add Would Recommend Radio**
- Drag **Radio** component to canvas at position (100, 620)
- Set `label`: "Would you recommend us to others?"
- Set `required`: true
- Set `tabOrder`: 5
- Set `layout`: "vertical"
- Set `options`: [
    { label: "Yes", value: "yes" },
    { label: "No", value: "no" },
    { label: "Maybe", value: "maybe" }
  ]
- Set `optionsDirection`: "horizontal"
- Set `styleOverrides.labelFontSize`: 15
- Set `exportName`: "wouldRecommend"

> **✅ UAT Note (2026-01-12):** PASSED

**Step 8: Add Referral Name Field**

> **⚠️ UAT Note (2026-01-12):** FAILED - When setting `optionsDirection: horizontal` on Radio/Checkbox components, the options did not display in a single row as expected. Options still appear vertically. **ACTION REQUIRED:** Investigate and fix the `optionsDirection` property for Radio and Checkbox components.
- Drag **Text** component to canvas at position (100, 700)
- Set `label`: "Referral Name"
- Set `required`: false
- Set `placeholder`: "Who would you like to refer?"
- Set `tabOrder`: 6
- Set `layout`: "horizontal"
- Set `validation.maxLength`: 100
- Set `validation.alpha`: true
- Set `styleOverrides.labelFontSize`: 14
- Set `exportName`: "referralName"
- **Note:** This field will be hidden initially, shown via logic when Would Recommend = "Yes"

**Step 9: Add Contact Preference Checkbox**
- Drag **Checkbox** component to canvas at position (100, 780)
- Set `label`: "How would you like us to contact you?"
- Set `required`: false
- Set `tabOrder`: 7
- Set `layout`: "vertical"
- Set `options`: [
    { label: "Email", value: "email" },
    { label: "Phone", value: "phone" },
    { label: "SMS", value: "sms" },
    { label: "Mail", value: "mail" },
    { label: "None", value: "none" }
  ]
- Set `minSelections`: 0
- Set `maxSelections`: 4
- Set `optionsDirection`: "horizontal"
- Set `styleOverrides.labelFontSize`: 15
- Set `exportName`: "contactPreference"

> **✅ UAT Note (2026-01-12):** PASSED

**Step 10: Add Preferred Contact Email Field**
- Drag **Email** component to canvas at position (100, 860)
- Set `label`: "Preferred Contact Email"
- Set `required`: false (will be set via logic)
- Set `placeholder`: "your.email@company.com"
- Set `tabOrder`: 8
- Set `layout`: "horizontal"
- Set `validation.email`: true
- Set `validation.maxLength`: 254
- Set `validationMessage`: "Please enter a valid email address"
- Set `styleOverrides.labelFontSize`: 14
- Set `styleOverrides.textBorderColor`: "#3B82F6"
- Set `styleOverrides.textBorderWidth`: 1
- Set `exportName`: "preferredContactEmail"
- **Note:** This field will be required via logic when Contact Preference contains "Email"

> **✅ UAT Note (2026-01-12):** PASSED

**Step 11: Add Preferred Contact Phone Field**
- Drag **Phone** component to canvas at position (100, 940)
- Set `label`: "Preferred Contact Phone"
- Set `required`: false (will be set via logic)
- Set `placeholder`: "+61 400 000 000"
- Set `tabOrder`: 9
- Set `layout`: "horizontal"
- Set `validation.phone`: true
- Set `validation.maxLength`: 20
- Set `validation.countryCodeRequired`: true
- Set `validationMessage`: "Please include country code (e.g., +61)"
- Set `styleOverrides.labelFontSize`: 14
- Set `exportName`: "preferredContactPhone"
- **Note:** This field will be required via logic when Contact Preference contains "Phone" or "SMS"

> **✅ UAT Note (2026-01-12):** PASSED

**Step 12: Add Additional Comments Textarea**
- Drag **Textarea** component to canvas at position (100, 1020)
- Set `label`: "Additional Comments"
- Set `required`: false
- Set `placeholder`: "Any other feedback or suggestions?"
- Set `tabOrder`: 10
- Set `layout`: "vertical"
- Set `validation.maxLength`: 2000
- Set `height`: 6
- Set `resizeMode`: "auto-grow"
- Set `showCharacterCount`: true
- Set `styleOverrides.helpTextFontSize`: 12
- Set `exportName`: "additionalComments"

> **⚠️ UAT Note (2026-01-12):** PARTIAL PASS - Textarea component added successfully. However, the following properties are **not visible in the Properties Panel UI**:
> - `height` - No option to set the textarea height (should be 6 rows)
> - `resizeMode` - No option to set auto-grow behavior
> - `showCharacterCount` - No toggle to enable character count display
> **ACTION REQUIRED:** These are the same missing properties noted in Step 6. Add Textarea-specific properties to the PropertiesPanel.

**Step 13: Add Divider**
- Drag **Divider** component to canvas at position (100, 1160)
- Set styling via style overrides:
  - `styleOverrides.textBorderColor`: "#E5E7EB"
  - `styleOverrides.textBorderWidth`: 1

**Step 14: Add Terms & Conditions**
- Drag **Terms & Conditions** component to canvas at position (100, 1200)
- Set `label`: "I agree to the"
- Set `required`: true
- Set `termsLinkText`: "Privacy Policy and Terms of Service"
- Set `termsUrl`: "" (or provide URL)
- Set `tabOrder`: 11
- Set `styleOverrides.labelFontSize`: 14
- Set `exportName`: "termsAccepted"

**Step 15: Add Submit Button**
- Drag **Submit Button** component to canvas at position (100, 1280)
- Set `buttonText`: "Submit Survey"
- Set `buttonAction`: "submit"
- Set `buttonWidth`: "full"
- Set `buttonAlign`: "center"
- Set `showLoadingState`: true
- Set `disableUntilValid`: true
- Set `tabOrder`: 12
- Set `styleOverrides` (if button styling supported):
  - Custom background color, font, etc.

**Step 16: Configure Logic Rules (10 Rules Total)**

**Rule 1: Require Company Name when Customer Type = "Corporate Client"**
- Create logic rule:
  - `name`: "Require Company Name for Corporate Clients"
  - `when.sourceComponentId`: [Customer Type radio component ID]
  - `when.operator`: "equals"
  - `when.value`: "corporate"
  - `then.targetComponentId`: [Company Name text component ID]
  - `then.action`: "require"
- Set `enabled`: true

**Rule 2: Show Company Name when Customer Type = "Corporate Client"**
- Create logic rule:
  - `name`: "Show Company Name for Corporate Clients"
  - `when.sourceComponentId`: [Customer Type radio component ID]
  - `when.operator`: "equals"
  - `when.value`: "corporate"
  - `then.targetComponentId`: [Company Name text component ID]
  - `then.action`: "show"
- Set `enabled`: true

**Rule 3: Hide Company Name when Customer Type ≠ "Corporate Client"**
- Create logic rule:
  - `name`: "Hide Company Name for Non-Corporate Customers"
  - `when.sourceComponentId`: [Customer Type radio component ID]
  - `when.operator`: "notEquals"
  - `when.value`: "corporate"
  - `then.targetComponentId`: [Company Name text component ID]
  - `then.action`: "hide"
- Set `enabled`: true

**Rule 4: Require Reason for Rating when Satisfaction Rating = "Dissatisfied"**
- Create logic rule:
  - `name`: "Require Reason for Dissatisfied Rating"
  - `when.sourceComponentId`: [Satisfaction Rating select component ID]
  - `when.operator`: "equals"
  - `when.value`: "dissatisfied"
  - `then.targetComponentId`: [Reason for Rating textarea component ID]
  - `then.action`: "require"
- Set `enabled`: true

**Rule 5: Require Reason for Rating when Satisfaction Rating = "Very Dissatisfied"**
- Create logic rule:
  - `name`: "Require Reason for Very Dissatisfied Rating"
  - `when.sourceComponentId`: [Satisfaction Rating select component ID]
  - `when.operator`: "equals"
  - `when.value`: "very-dissatisfied"
  - `then.targetComponentId`: [Reason for Rating textarea component ID]
  - `then.action`: "require"
- Set `enabled`: true

**Rule 6: Hide Reason for Rating when Satisfaction Rating = "Very Satisfied" or "Satisfied"**
- Create logic rule:
  - `name`: "Hide Reason for Satisfied Ratings"
  - `when.sourceComponentId`: [Satisfaction Rating select component ID]
  - `when.operator`: "equals"
  - `when.value`: "very-satisfied"
  - `then.targetComponentId`: [Reason for Rating textarea component ID]
  - `then.action`: "hide"
- Set `enabled`: true
- Create similar rule for "satisfied" value

**Rule 7: Show Referral Name when Would Recommend = "Yes"**
- Create logic rule:
  - `name`: "Show Referral Name for Yes Recommendation"
  - `when.sourceComponentId`: [Would Recommend radio component ID]
  - `when.operator`: "equals"
  - `when.value`: "yes"
  - `then.targetComponentId`: [Referral Name text component ID]
  - `then.action`: "show"
- Set `enabled`: true

**Rule 8: Hide Referral Name when Would Recommend ≠ "Yes"**
- Create logic rule:
  - `name`: "Hide Referral Name for No/Maybe Recommendation"
  - `when.sourceComponentId`: [Would Recommend radio component ID]
  - `when.operator`: "notEquals"
  - `when.value`: "yes"
  - `then.targetComponentId`: [Referral Name text component ID]
  - `then.action`: "hide"
- Set `enabled`: true

**Rule 9: Require Preferred Contact Email when Contact Preference contains "Email"**
- Create logic rule:
  - `name`: "Require Email when Email Selected"
  - `when.sourceComponentId`: [Contact Preference checkbox component ID]
  - `when.operator`: "contains"
  - `when.value`: "email"
  - `then.targetComponentId`: [Preferred Contact Email component ID]
  - `then.action`: "require"
- Set `enabled`: true

**Rule 10: Unrequire Preferred Contact Email when Contact Preference does not contain "Email"**
- Create logic rule:
  - `name`: "Unrequire Email when Email Not Selected"
  - `when.sourceComponentId`: [Contact Preference checkbox component ID]
  - `when.operator`: "notEquals" (or test with different approach)
  - `when.value`: "email"
  - `then.targetComponentId`: [Preferred Contact Email component ID]
  - `then.action`: "unrequire"
- Set `enabled`: true
- **Note:** May need to test this with `isEmpty` operator or multiple rules

**Rule 11: Require Preferred Contact Phone when Contact Preference contains "Phone"**
- Create logic rule:
  - `name`: "Require Phone when Phone Selected"
  - `when.sourceComponentId`: [Contact Preference checkbox component ID]
  - `when.operator`: "contains"
  - `when.value`: "phone"
  - `then.targetComponentId`: [Preferred Contact Phone component ID]
  - `then.action`: "require"
- Set `enabled`: true

**Rule 12: Require Preferred Contact Phone when Contact Preference contains "SMS"**
- Create logic rule:
  - `name`: "Require Phone when SMS Selected"
  - `when.sourceComponentId`: [Contact Preference checkbox component ID]
  - `when.operator`: "contains"
  - `when.value`: "sms"
  - `then.targetComponentId`: [Preferred Contact Phone component ID]
  - `then.action`: "require"
- Set `enabled`: true

**Step 17: Apply Comprehensive Styling**

**For components with `layout: "horizontal"`:**
- Company Name, Referral Name, Preferred Contact Email, Preferred Contact Phone
- Verify labels align correctly with inputs
- Verify validation messages align under inputs (not labels)

**For components with `layout: "vertical"`:**
- All other components
- Verify labels appear above inputs
- Verify proper spacing between label and input

**Apply different style overrides to test:**
- **Header:** Large font (28px), bold (700), dark color (#111827)
- **Paragraph:** Medium font (16px), gray color (#4B5563)
- **Company Name:** Custom font (Roboto), thicker border (2px), rounded corners (6px)
- **Preferred Contact Email:** Blue border (#3B82F6)
- **Reason for Rating:** Smaller help text (12px), gray color
- **Additional Comments:** Auto-grow textarea, character count

**Test `componentScale` on different components:**
- Set one component to `componentScale: 75` (smaller)
- Set another to `componentScale: 125` (larger)
- Set another to `componentScale: 150` (largest)
- Verify scaling affects fonts, heights, padding, borders proportionally

**Test `inputWidthMode`:**
- Set one component to `inputWidthMode: "fill"` (default)
- Set another to `inputWidthMode: "fixed"` with `inputWidth: 300`
- Set another to `inputWidthMode: "auto"` with `validation.maxLength: 20`
- Verify widths render correctly

**Step 18: Save Draft**
- Click **Save Draft** button
- Verify success message appears
- Note the form ID for later testing

**Step 19: Verify in Preview**
- Click **Preview** button
- Test all logic rules by changing source values
- Verify styling matches builder exactly
- Verify all validation rules work
- Verify narrow-viewport behavior does **not** reflow authored layout (the artboard may scroll/scale, but component layouts/positions remain authored)

### How to confirm the renderer is using stored `DefinitionJSON` (frontend-only)

Use **at least one** method:

- **Method A (Preferred): Network response**
  - Open DevTools → Network.
  - Load the public renderer page (`/forms/:token`).
  - Identify the API request that returns the definition payload (e.g., `GET /api/public/forms/{token}`).
  - Confirm the response contains:
    - `pages` and/or device-specific page arrays
    - `canvasSettings` (for Template A)
    - `logic.rules` (for Template B)

- **Method B: Save change, then reload**
  - Make a small visible change in the Builder (e.g., label text).
  - Click **Save Draft**.
  - Open a **new** Preview link and confirm the change appears in `/forms/:token`.

---

## 🧪 Test Scenarios

### Scenario 1: Builder loads from DB (no mock template)

**Goal:** Opening `/forms/:formId/builder` loads the latest stored definition from the backend (not the same 3-field mock template for every form).

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open an existing form in the Builder (`/forms/:formId/builder`). | The canvas loads with the form’s saved components (not always the same default 3 fields). |
| 2 | Refresh the page (hard refresh). | The same authored layout/components reload. |
| 3 | Open the builder for a *different* formId you can manage. | It loads *that form’s* saved definition (not a shared default). |

---

### Scenario 2: Save Draft persists `DefinitionJSON` to FormVersion

**Goal:** Saving writes the current form definition to the backend and survives reload/new session.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | In Builder, change a visible label (e.g., Paragraph text or a field label). | UI updates immediately. |
| 2 | Click **Save** (Save Draft). | A success confirmation is shown (exact text may vary). |
| 3 | Refresh the Builder page. | The changed label persists after reload. |
| 4 | (Optional) Open a private/incognito window and load the same builder page. | The changed label still loads (proves DB, not localStorage-only). |

---

### Scenario 3: Preview token opens `/forms/:token` and reflects stored definition

**Goal:** Preview uses the same public renderer route as production and renders from stored definition.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | In Builder, click **Preview**. | A new tab opens at `/forms/:token`. |
| 2 | In DevTools Network (renderer tab), find the `GET /api/public/forms/{token}` request. | Response includes `definition` containing the label changes you saved. |
| 3 | Make another visible change in Builder and click **Save** again. | Save succeeds. |
| 4 | Click **Preview** again (new token). | New preview reflects the latest saved changes. |

---

### Scenario 4: Permission/access + validation errors are safe and user-visible

**Goal:** When the user cannot save (or backend rejects), the UI remains stable and shows a clear message.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Log in as a user without MANAGE/EDIT access to the form (or simulate by using a form you can only VIEW). | You can still open the Builder route (if allowed) but actions are restricted. |
| 2 | Attempt to click **Save**. | A clear error is shown (no crash). |
| 3 | Attempt to click **Preview**. | Either a clear access error is shown or the app prevents the action; no crash/white screen. |

---

### Scenario 5: Render from stored DefinitionJSON (Happy Path)

**Goal:** Renderer loads and renders the form from stored `FormVersion.DefinitionJSON` without relying on builder-only state.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open a Preview link (`/forms/:token`) for a saved form (Template A or B). | A loading state appears briefly, then the form renders. |
| 2 | Verify in DevTools Network that the definition is fetched from the backend. | A request returns the definition payload containing `DefinitionJSON` content (or equivalent). |
| 3 | Confirm at least 3 component types render (e.g., paragraph + text + select). | Components render with correct labels/placeholder text and are interactive where applicable. |
| 4 | Confirm no white-screen crash. | No unhandled exception; page remains usable. |

---

### Scenario 6: Canvas/Profile Fidelity — Artboard dimensions match `canvasSettings`

**Goal:** Renderer respects authored canvas/profile dimensions exactly.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open renderer for **Template A** via Preview link. | Form renders inside a visible artboard/container. |
| 2 | Inspect the artboard/container element in DevTools (Elements). | The artboard/container has a fixed width/height matching `definition.canvasSettings.width/height` (or the equivalent stored canvas dimensions). |
| 3 | Verify component placement visually. | Components appear at the authored absolute positions within the artboard (no reflow into a single-column layout). |

---

### Scenario 7: No responsive reflow when viewport changes (layout must remain authored)

**Goal:** Changing viewport size does not cause the renderer to “auto reflow” into a different layout/profile.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | With **Template A** open, note two components’ relative placement (e.g., Text left, Email right on same row). | You have a clear reference layout. |
| 2 | Resize browser window narrower than the artboard width (or use DevTools device emulation for a smaller viewport). | The artboard may scale-to-fit or introduce scrolling, but components keep their authored positions relative to the artboard. |
| 3 | Resize back to wide viewport. | The authored layout remains the same; no reflow artifacts or “different profile” layout appears. |

---

### Scenario 8: Unknown component type fallback (Do not crash)

**Goal:** Unknown component `type` renders a fallback UI and the renderer does not crash.

**Setup (one-time):** Create a saved version whose DefinitionJSON includes a component with an unknown `type` (not in the Component Registry).

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open renderer for the “unknown component” version. | Page loads; no crash/white screen. |
| 2 | Locate the unknown component region on the artboard. | A fallback UI is shown (e.g., “Unsupported component type: <type>”). |
| 3 | Interact with other known components. | Known components remain fully usable. |
| 4 | Check DevTools Console. | No uncaught exceptions. Non-blocking warnings are acceptable. |

---

### Scenario 9: Malformed component config fallback (Do not crash)

**Goal:** Malformed/missing props for a known component type does not crash the renderer.

**Setup (one-time):** Create a saved version where a known component has malformed config (examples: `options` is not an array for a select; missing `props` entirely; invalid value types).

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open renderer for the “malformed config” version. | Page loads; no crash/white screen. |
| 2 | Locate the affected component. | It renders with safe defaults or a fallback block; layout remains stable (no collapsing the whole page). |
| 3 | Interact with unaffected components. | Other components remain usable. |
| 4 | Check DevTools Console. | No uncaught exceptions. Non-blocking warnings are acceptable. |

---

### Scenario 10: Runtime logic — visibility (show/hide) + tab order

**Goal:** Story 3.7 runtime rule outputs apply in renderer: hidden components are not rendered and removed from tab order.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open renderer for **Template B** (logic-enabled). | Form loads. |
| 2 | Set Field A to `Y` (or the value that triggers a hide/show rule). | Target visibility changes immediately and deterministically. |
| 3 | Press `Tab` repeatedly to navigate through fields. | Hidden fields never receive focus (removed from tab order). |
| 4 | Toggle Field A to `N` and repeat. | Visibility updates correctly; no flicker/crash. |

---

### Scenario 11: Runtime logic — enable/disable

**Goal:** Disabled components render disabled and do not accept input.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | In renderer (Template B), set Field A to the value that disables a target field. | Target field appears disabled (visual cue). |
| 2 | Attempt to type/select into the disabled target field. | Input is blocked; value does not change. |
| 3 | Change Field A to the value that enables the target field. | Field becomes enabled and accepts input again. |

---

### Scenario 12: Runtime logic — require/unrequire + validation message area

**Goal:** Required state changes at runtime and validation errors appear in the reserved validation message area.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | In renderer (Template B), set Field A so Field D becomes required via rule. | Field D shows required indicator. |
| 2 | Leave Field D empty and attempt to submit/validate (per renderer UX). | Field D shows a required error message in its validation message area. |
| 3 | Toggle Field A so Field D becomes unrequired. | Required indicator disappears; required error no longer blocks when Field D is empty. |

---

### Scenario 13: Broken/missing rule references (Do not crash)

**Goal:** Rules referencing missing component ids are ignored safely; renderer remains usable.

**Setup (one-time):** Save a version where at least one rule references a missing sourceComponentId or targetComponentId.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open renderer for the “broken rule references” version. | Page loads; no crash/white screen. |
| 2 | Observe any warning surface. | A non-blocking warning indicates some rules could not be applied (exact UI may vary). |
| 3 | Interact with unaffected components. | Form remains usable; broken rules do not apply. |
| 4 | Check DevTools Console. | No uncaught exceptions. |

---

### Scenario 14: Unknown component + runtime logic combined

**Goal:** Unknown component fallback does not interfere with runtime rules on known components.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open a version containing (a) unknown component type and (b) valid rules affecting known components. | Renderer loads without crashing. |
| 2 | Trigger runtime rules by changing source values. | Rules apply correctly to known components (show/hide, enable/disable, require/unrequire). |
| 3 | Locate the unknown component. | Fallback UI renders and remains non-blocking. |

---

### Scenario 15: Submit UX (client-side only) — validate + no submission transport

**Goal:** Submit performs client-side validation and does not send submission requests (submission/outbox is deferred to Story 3.10).

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open renderer for a form containing required fields and (if present) a submit button. | Form loads. |
| 2 | Open DevTools → Network and clear prior requests. | Network view is clean. |
| 3 | Leave at least one visible required field empty and click Submit. | Validation errors appear; submit does not proceed silently. |
| 4 | Fill required fields and click Submit again. | A clear UI confirmation indicates submission transport/outbox is deferred to Story 3.10 (exact text may vary). |
| 5 | Inspect DevTools Network after clicking Submit. | No submission POST/transport request is made (no outbox/network pipeline yet). |

---

### Scenario 16: Deterministic ordering / conflict resolution (last applicable wins)

**Goal:** When multiple enabled rules affect the same target property, the renderer resolves deterministically based on persisted rule order.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Use a saved form where two enabled rules can both be true and target the same component + property with opposing actions (e.g., `show` and `hide` on Field B). | Form and rules exist in stored DefinitionJSON. |
| 2 | In renderer, set inputs so both conflicting rules are true simultaneously. | Renderer remains stable; no crash/flicker loop. |
| 3 | Observe the final state for the targeted property. | Outcome matches the **last applicable rule** in persisted order. |
| 4 | Swap rule order in Builder, Save Draft, open a new Preview link, and repeat Step 2. | Outcome flips accordingly, proving ordering determinism from stored DefinitionJSON. |

---

### Scenario 17: Build & Test Template C — Event Registration Form

**Goal:** Build Template C following the step-by-step instructions, then verify all component types render correctly with their specific properties.

**Part A: Build Template C Form**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Create new form in Builder. | New form opens with empty canvas. |
| 2 | Follow **Template C Step-by-Step Build Instructions** (above). | Complete all 19 steps to build the form. |
| 3 | After Step 18, click **Save Draft**. | Form saves successfully, success message appears. |
| 4 | Verify form ID is displayed. | Note form ID for testing. |

**Part B: Test Component Rendering in Preview**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 5 | Click **Preview** button. | Preview opens in new tab at `/forms/:token`. |
| 6 | Verify Header component renders. | "Event Registration" displays with 24px font, bold, dark color. |
| 7 | Verify Paragraph component renders. | Help text displays with 14px font, gray color. |
| 8 | Verify First Name field renders with horizontal layout. | Label appears to left of input, validation message aligns under input (not label). |
| 9 | Verify Last Name field renders with horizontal layout. | Label appears to left of input. |
| 10 | Verify Email field renders with vertical layout. | Label appears above input. |
| 11 | Verify Phone field renders. | Field displays with placeholder showing country code format. |
| 12 | Verify Select dropdown renders. | Dropdown shows all options including "Other". |
| 13 | Verify Number field renders. | Field accepts numeric input only. |
| 14 | Verify Checkbox group renders. | All 6 options display horizontally. |
| 15 | Verify Textarea (Special Requests) renders. | Textarea displays with character count visible. |
| 16 | Verify Date picker renders. | Date picker opens, shows calendar interface. |
| 17 | Verify Terms & Conditions renders. | Checkbox with terms link displays. |
| 18 | Verify Submit button renders. | Button displays "Register for Event" text. |
| 19 | Count total components rendered. | All 16 components (including logic-triggered fields) render correctly. |

---

### Scenario 18: Build Template C & Test All Validation Rules

**Goal:** Build Template C following instructions, then systematically test every validation rule configured.

**Part A: Build Template C (if not already built in Scenario 17)**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | If Template C not yet built, follow **Template C Step-by-Step Build Instructions**. | Form is built with all validation rules configured. |
| 2 | Click **Save Draft**. | Form saves successfully. |
| 3 | Click **Preview**. | Preview opens. |

**Part B: Test Text Validation Rules**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 4 | Click in **First Name** field. | Field receives focus, shows focus border color. |
| 5 | Type 31 characters into First Name. | After 30th character, validation message appears: "First name must be letters only, maximum 30 characters" OR "We only allow a max of 30 Characters". |
| 6 | Type numbers into First Name (e.g., "John123"). | Error appears: "Please enter letters only" (or custom message). |
| 7 | Type special characters into First Name (e.g., "John@"). | Error appears for invalid characters. |
| 8 | Clear First Name and type only letters (e.g., "John"). | No error appears, field is valid. |
| 9 | Repeat Steps 4-8 for **Last Name** field. | Same validation behavior applies. |

**Part C: Test Email Validation Rules**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 10 | Click in **Email Address** field. | Field receives focus. |
| 11 | Type "test@gmail.com" and click Validate or Submit. | Error appears: "Please use a business email address. Free email providers and test.com are not allowed." |
| 12 | Type "user@yahoo.com" and click Validate. | Error appears (business email only validation). |
| 13 | Type "user@test.com" and click Validate. | Error appears (domain blacklist validation). |
| 14 | Type "user+tag@company.com" and click Validate. | Error appears (no plus addressing validation). |
| 15 | Type "user@company.com" and click Validate. | No error appears, field is valid. |
| 16 | Type 255 characters into Email field. | Error appears when exceeding 254 characters (maxLength). |

**Part D: Test Phone Validation Rules**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 17 | Click in **Phone Number** field. | Field receives focus. |
| 18 | Type "0400000000" (without country code) and click Validate. | Error appears: "Phone number must include country code (e.g., +61)". |
| 19 | Type "+61400000000" and click Validate. | No error appears, field is valid. |
| 20 | Type 21 characters into Phone field. | Error appears when exceeding 20 characters (maxLength). |

**Part E: Test Number Validation Rules**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 21 | Click in **Number of Attendees** field. | Field receives focus. |
| 22 | Type "0" and click Validate. | Error appears: "Please enter a value of at least 1" (minValue). |
| 23 | Type "-5" and click Validate. | Error appears (positiveOnly validation). |
| 24 | Type "51" and click Validate. | Error appears: "Please enter a value no greater than 50" (maxValue). |
| 25 | Type "25.5" and click Validate. | Error appears or value is rounded (integerOnly validation). |
| 26 | Type "25" and click Validate. | No error appears, field is valid. |

**Part F: Test Textarea Validation Rules**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 27 | Click in **Special Requests** textarea. | Field receives focus, character count shows "0 / 500". |
| 28 | Type 501 characters into textarea. | After 500th character, error appears: "We only allow a max of 500 Characters". |
| 29 | Verify character count updates as you type. | Character count increments: "100 / 500", "200 / 500", etc. |

**Part G: Test Date Validation Rules**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 30 | Click in **Event Date** field. | Date picker opens. |
| 31 | Try to select yesterday's date. | Date is disabled or shows error (futureOnly validation). |
| 32 | Try to select a Saturday. | Saturday is disabled (weekdaysOnly validation). |
| 33 | Try to select a Sunday. | Sunday is disabled (weekdaysOnly validation). |
| 34 | Select a future weekday (e.g., next Tuesday). | Date is selected, no error appears. |

**Part H: Test Required Field Validation**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 35 | Leave **First Name** empty and click **Validate** button (or Submit). | Error appears: "This field is required." |
| 36 | Fill First Name, leave **Last Name** empty, click Validate. | Error appears on Last Name. |
| 37 | Fill all required fields except **Email**, click Validate. | Error appears on Email. |
| 38 | Fill all required fields, click Validate. | No errors appear, form is valid. |

**Part I: Test Custom Error Messages**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 39 | Verify First Name shows custom message when maxLength exceeded. | Custom message displays instead of default. |
| 40 | Verify Email shows custom message for business email validation. | Custom message displays. |
| 41 | Verify Date shows custom message for invalid date selection. | Custom message displays. |

---

### Scenario 19: Build Template D & Test Complete Logic Rules Coverage

**Goal:** Build Template D following step-by-step instructions, then systematically test all logic operators and actions.

**Part A: Build Template D Form**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Create new form in Builder. | New form opens with empty canvas. |
| 2 | Follow **Template D Step-by-Step Build Instructions** (above). | Complete all 19 steps to build the form with all 12 logic rules. |
| 3 | After Step 18, click **Save Draft**. | Form saves successfully, success message appears. |
| 4 | Verify all 12 logic rules are configured. | Logic rules panel shows all rules enabled. |
| 5 | Click **Preview**. | Preview opens in new tab. |

**Part B: Test `equals` Operator**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 6 | In preview, select **Customer Type** = "Corporate Client". | Company Name field immediately becomes visible and required (red asterisk appears). |
| 7 | Verify Company Name field is visible. | Field appears below Customer Type. |
| 8 | Try to submit form without filling Company Name. | Error appears: "This field is required." |
| 9 | Fill Company Name with "Acme Corp". | Field accepts input, no error. |

**Part C: Test `notEquals` Operator**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 10 | Change **Customer Type** from "Corporate Client" to "New Customer". | Company Name field immediately becomes hidden (disappears from view). |
| 11 | Verify Company Name is not visible. | Field is not displayed. |
| 12 | Change Customer Type back to "Corporate Client". | Company Name appears again and is required. |

**Part D: Test `contains` Operator**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 13 | In **Contact Preference** checkbox, select "Email". | Preferred Contact Email field immediately becomes required (red asterisk appears). |
| 14 | Verify Preferred Contact Email shows required indicator. | Red asterisk appears next to label. |
| 15 | Try to submit form without filling Preferred Contact Email. | Error appears: "This field is required." |
| 16 | Select "Phone" in Contact Preference. | Preferred Contact Phone field becomes required. |
| 17 | Select "SMS" in Contact Preference. | Preferred Contact Phone remains required (already required from Phone). |
| 18 | Deselect "Email" (keep Phone and SMS selected). | Preferred Contact Email becomes not required (asterisk disappears). |
| 19 | Deselect "Phone" and "SMS". | Preferred Contact Phone becomes not required. |

**Part E: Test `show` Action**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 20 | In **Would Recommend** radio, select "Yes". | Referral Name field immediately becomes visible. |
| 21 | Verify Referral Name field appears. | Field displays below Would Recommend. |
| 22 | Fill Referral Name with "Jane Doe". | Field accepts input. |

**Part F: Test `hide` Action**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 23 | Change **Would Recommend** from "Yes" to "No". | Referral Name field immediately becomes hidden (disappears). |
| 24 | Verify Referral Name is not visible. | Field is not displayed. |
| 25 | Change Would Recommend to "Maybe". | Referral Name remains hidden. |

**Part G: Test `require` Action**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 26 | In **Satisfaction Rating** select, choose "Dissatisfied". | Reason for Rating textarea immediately becomes required (red asterisk appears). |
| 27 | Verify Reason for Rating shows required indicator. | Red asterisk appears next to label. |
| 28 | Try to submit form without filling Reason for Rating. | Error appears: "This field is required." |
| 29 | Change Satisfaction Rating to "Very Dissatisfied". | Reason for Rating remains required. |
| 30 | Fill Reason for Rating with "Poor service quality" (at least 10 characters). | Field accepts input, no error. |

**Part H: Test `unrequire` Action**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 31 | Change **Satisfaction Rating** from "Dissatisfied" to "Very Satisfied". | Reason for Rating immediately becomes not required (asterisk disappears). |
| 32 | Verify Reason for Rating no longer shows required indicator. | Red asterisk disappears. |
| 33 | Leave Reason for Rating empty and submit form. | No error appears for this field. |
| 34 | Change Satisfaction Rating to "Satisfied". | Reason for Rating remains not required. |

**Part I: Test `isEmpty` Operator (if supported)**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 35 | Clear all selections in **Contact Preference** checkbox. | All contact preference fields become not required. |
| 36 | Verify Preferred Contact Email and Phone are not required. | No red asterisks appear. |

**Part J: Test Multiple Rules Affecting Same Field**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 37 | Set **Customer Type** = "Corporate Client". | Company Name is visible and required. |
| 38 | Set **Satisfaction Rating** = "Dissatisfied". | Reason for Rating is required. |
| 39 | Set **Would Recommend** = "Yes". | Referral Name is visible. |
| 40 | Verify all three logic rules execute simultaneously. | All fields show correct state (visible/required as expected). |
| 41 | Change Customer Type to "New Customer". | Company Name hides, but Reason for Rating and Referral Name remain in their states. |

**Part K: Test Rule Chaining and Order**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 42 | Set **Contact Preference** to include "Email" and "Phone". | Both Preferred Contact Email and Preferred Contact Phone become required. |
| 43 | Deselect "Email" (keep "Phone"). | Preferred Contact Email becomes not required, Preferred Contact Phone remains required. |
| 44 | Deselect "Phone" (select nothing). | Preferred Contact Phone becomes not required. |
| 45 | Verify rules execute deterministically. | Last applicable rule wins, no conflicting states. |

**Part L: Test Complex Logic Scenarios**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 46 | Set **Customer Type** = "Corporate Client", fill Company Name. | Company Name is visible and required, filled. |
| 47 | Set **Satisfaction Rating** = "Very Dissatisfied", fill Reason for Rating. | Reason for Rating is required, filled. |
| 48 | Set **Would Recommend** = "Yes", fill Referral Name. | Referral Name is visible, filled. |
| 49 | Set **Contact Preference** = ["Email", "SMS"], fill both contact fields. | Both contact fields are required, filled. |
| 50 | Click **Submit Survey**. | Form submits successfully (all required fields filled). |
| 51 | Verify form data is captured correctly. | All field values are submitted as expected. |

---

### Scenario 20: Build Template D & Test Style Overrides & Layout

**Goal:** Build Template D following instructions, then verify all styling properties persist and render correctly in preview.

**Part A: Build Template D (if not already built in Scenario 19)**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | If Template D not yet built, follow **Template D Step-by-Step Build Instructions**. | Form is built with comprehensive styling applied. |
| 2 | Click **Save Draft**. | Form saves successfully. |
| 3 | Click **Preview**. | Preview opens. |

**Part B: Test Layout Properties**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 4 | Verify **Customer Type** radio has `layout: "vertical"`. | Label appears above radio options. |
| 5 | Verify **Company Name** text has `layout: "horizontal"`. | Label appears to the left of input field. |
| 6 | Verify **Satisfaction Rating** select has `layout: "vertical"`. | Label appears above dropdown. |
| 7 | Verify **Referral Name** text has `layout: "horizontal"`. | Label appears to the left of input. |
| 8 | Verify **Preferred Contact Email** has `layout: "horizontal"`. | Label appears to the left of input. |
| 9 | Verify **Preferred Contact Phone** has `layout: "horizontal"`. | Label appears to the left of input. |
| 10 | Verify **Additional Comments** textarea has `layout: "vertical"`. | Label appears above textarea. |

**Part C: Test Horizontal Layout Validation Message Alignment**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 11 | Click in **Company Name** field (horizontal layout). | Field receives focus. |
| 12 | Leave field empty and click Validate or Submit. | Validation message appears **under the input field** (not under the label). |
| 13 | Verify validation message alignment. | Message starts at the left edge of the input, not the label. |
| 14 | Repeat Steps 11-13 for **Referral Name**, **Preferred Contact Email**, **Preferred Contact Phone**. | All horizontal layout fields show validation messages aligned under inputs. |

**Part D: Test Style Overrides - Fonts**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 15 | Verify **Header** component font size. | Font size is 28px (as configured in Step 1). |
| 16 | Verify **Header** component font weight. | Font weight is 700 (bold). |
| 17 | Verify **Header** component font family. | Font family matches configured value (e.g., "Inter"). |
| 18 | Verify **Paragraph** component font size. | Font size is 16px (as configured in Step 2). |
| 19 | Verify **Company Name** label font family. | Font family matches configured value (e.g., "Roboto"). |
| 20 | Verify **Company Name** label font size. | Font size is 14px (as configured in Step 4). |

**Part E: Test Style Overrides - Colors**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 21 | Verify **Header** component color. | Color is #111827 (dark gray, as configured). |
| 22 | Verify **Paragraph** component color. | Color is #4B5563 (medium gray, as configured). |
| 23 | Verify **Company Name** label color. | Color matches configured value. |
| 24 | Compare builder and preview colors side-by-side. | All colors match exactly between builder and preview. |

**Part F: Test Style Overrides - Borders**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 25 | Verify **Company Name** input border width. | Border width is 2px (as configured in Step 4). |
| 26 | Verify **Company Name** input border radius. | Border radius is 6px (as configured in Step 4). |
| 27 | Verify **Company Name** input border color. | Border color matches configured value (#9CA3AF). |
| 28 | Verify **Preferred Contact Email** input border color. | Border color is #3B82F6 (blue, as configured in Step 10). |
| 29 | Compare builder and preview borders side-by-side. | All borders match exactly between builder and preview. |

**Part G: Test Component Scale**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 30 | In Builder, set one component's `componentScale` to 75. | Component appears smaller in builder. |
| 31 | Save and preview. | Component renders at 75% scale in preview (fonts, heights, padding, borders all scaled proportionally). |
| 32 | In Builder, set another component's `componentScale` to 125. | Component appears larger in builder. |
| 33 | Save and preview. | Component renders at 125% scale in preview. |
| 34 | In Builder, set another component's `componentScale` to 150. | Component appears largest in builder. |
| 35 | Save and preview. | Component renders at 150% scale in preview. |
| 36 | Verify scaling is proportional. | All dimensions (font size, height, padding, border width) scale together. |

**Part H: Test Input Width Mode**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 37 | In Builder, set one component's `inputWidthMode` to "fill". | Component input stretches to fill container in builder. |
| 38 | Save and preview. | Input stretches to fill container width in preview. |
| 39 | In Builder, set another component's `inputWidthMode` to "fixed" with `inputWidth: 300`. | Component input shows fixed width in builder. |
| 40 | Save and preview. | Input uses exactly 300px width in preview. |
| 41 | In Builder, set another component's `inputWidthMode` to "auto" with `validation.maxLength: 20`. | Component input shows auto-calculated width in builder. |
| 42 | Save and preview. | Input width is calculated based on maxLength in preview. |

**Part I: Test Label and Text Alignment**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 43 | In Builder, set a component's `labelAlign` to "left". | Label text aligns left in builder. |
| 44 | Save and preview. | Label text aligns left in preview. |
| 45 | In Builder, set a component's `labelAlign` to "center". | Label text aligns center in builder. |
| 46 | Save and preview. | Label text aligns center in preview. |
| 47 | In Builder, set a component's `labelAlign` to "right". | Label text aligns right in builder. |
| 48 | Save and preview. | Label text aligns right in preview. |
| 49 | Repeat Steps 43-48 for `textAlign` property. | Input text aligns correctly (left, center, right). |

**Part J: Test Error State Styling**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 50 | Click in a required field and leave it empty. | Field shows normal state. |
| 51 | Click Validate or Submit. | Field border turns red (#DC2626). |
| 52 | Verify error message appears. | Error message displays with red text (#DC2626) and AlertCircle icon. |
| 53 | Verify error icon. | Red AlertCircle icon appears next to error message. |
| 54 | Verify subtle red box shadow. | Input shows subtle red glow (box-shadow with rgba(220, 38, 38, 0.1)). |
| 55 | Fill field with valid value. | Border returns to normal color, error message disappears. |

**Part K: Test Focus State Styling**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 56 | Click in any input field. | Field receives focus. |
| 57 | Verify focus border color. | Border color changes to primary color (from FormTheme). |
| 58 | Verify focus box shadow. | Double ring box shadow appears (primary color with opacity). |
| 59 | Click outside field (blur). | Border returns to normal color, box shadow disappears. |
| 60 | Verify smooth transitions. | Color and shadow changes animate smoothly (0.2s ease). |

**Part L: Test Responsive Layout**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 61 | Resize browser window to width < 768px (mobile view). | Window resizes. |
| 62 | Verify no “responsive reflow” occurs. | Authored positions/layouts remain the same; the artboard may scale-to-fit or introduce scrolling. |
| 63 | Verify horizontal components remain horizontal. | Horizontal layout fields keep label/input arrangement (no automatic switch to vertical). |
| 64 | Resize browser window back to desktop width (> 768px). | Layout remains stable (no reflow artifacts). |
| 65 | Verify component interactivity remains correct after resize. | Inputs remain usable; no console errors. |

---

### Scenario 21: Build Templates C & D & Test Component-Specific Properties

**Goal:** Build Templates C and D following instructions, then verify all component-specific properties work correctly.

**Part A: Build Templates (if not already built)**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | If Template C not built, follow **Template C Step-by-Step Build Instructions**. | Template C is built. |
| 2 | If Template D not built, follow **Template D Step-by-Step Build Instructions**. | Template D is built. |
| 3 | Open Template C in preview. | Preview opens. |

**Part B: Test Select Component Properties**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 4 | In Template C, click **Event Type** select dropdown. | Dropdown opens showing all options including "Other". |
| 5 | Select "Other" option. | "Other Event Type" text field immediately appears (logic rule). |
| 6 | Verify `allowOther` property works. | Selecting "Other" shows additional input field. |
| 7 | Test `searchable` property (if implemented). | Type to filter options in dropdown. |

**Part C: Test Checkbox Component Properties**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 8 | In Template C, verify **Dietary Requirements** checkbox. | All 6 options display horizontally (`optionsDirection: horizontal`). |
| 9 | Select 0 options (minSelections: 0). | No error appears, form allows 0 selections. |
| 10 | Select 6 options (maxSelections: 6). | All options can be selected. |
| 11 | Try to select a 7th option. | Selection is prevented or error appears (maxSelections: 6). |
| 12 | In Builder, change `optionsDirection` to "vertical" for a checkbox. | Options display in a column. |
| 13 | Save and preview. | Options display vertically in preview. |

**Part D: Test Radio Component Properties**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 14 | In Template D, verify **Customer Type** radio. | Options display vertically (`optionsDirection: vertical`). |
| 15 | In Template D, verify **Would Recommend** radio. | Options display horizontally (`optionsDirection: horizontal`). |
| 16 | Select different radio options. | Only one option can be selected at a time. |

**Part E: Test Textarea Component Properties**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 17 | In Template C, verify **Special Requests** textarea. | Character count displays "0 / 500" (`showCharacterCount: true`). |
| 18 | Type text into textarea. | Character count updates: "50 / 500", "100 / 500", etc. |
| 19 | Try to resize textarea vertically. | Textarea can be resized vertically (`resizeMode: vertical`). |
| 20 | Try to resize textarea horizontally. | Horizontal resize is disabled (vertical only). |
| 21 | In Template D, verify **Additional Comments** textarea. | Textarea has `resizeMode: auto-grow`. |
| 22 | Type multiple lines into Additional Comments. | Textarea height grows automatically as content increases. |
| 23 | Verify character count displays. | Character count shows "0 / 2000" and updates. |

**Part F: Test Date Component Properties**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 24 | In Template C, click **Event Date** field. | Date picker opens (`dateType: date`). |
| 25 | Verify date picker interface. | Calendar interface shows for date selection. |
| 26 | Test `dateFormat` (if implemented). | Selected date displays in configured format. |
| 27 | Verify `futureOnly` validation. | Past dates are disabled or show error. |
| 28 | Verify `weekdaysOnly` validation. | Saturday and Sunday are disabled. |

**Part F2: Test Date Settings Compatibility**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 29 | Set **Date Type** to **Time Only**. | Picker Style disables **Calendar** and **Dropdowns** with reason message. |
| 30 | Set **Date Type** to **Date & Time**. | Picker Style disables **Dropdowns** with reason message. |
| 31 | Set **Picker Style** to **Native Browser Picker** and choose a custom **Display Format**. | Warning indicates native UI controls visual format. |
| 32 | Set **Picker Style** to **Calendar** and uncheck Day/Month/Year. | Date parts are forced back on and disabled with a reason. |
| 33 | Set **Picker Style** to **Dropdowns** and uncheck Year. | Partial date parts are allowed (no forced reset). |
| 34 | Enable **Date Range** validation. | Warning indicates current picker captures a single date only. |

**Part F3: Test Date Validation Compatibility**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 35 | Enable **Future Dates Only**. | **Past Dates Only** disables with reason message. |
| 36 | Enable **Past Dates Only**. | **Future Dates Only** disables with reason message. |
| 37 | Enable **Future Dates Only** and check **Minimum Age**. | Minimum/Maximum Age disables with reason message (requires past dates). |
| 38 | Enter **Minimum Age** and **Maximum Age** with Minimum > Maximum. | Warning indicates minimum age cannot exceed maximum age. |

**Part G: Test Submit Button Properties**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 42 | In Template C, verify **Submit Button** text. | Button displays "Register for Event" (`buttonText`). |
| 43 | In Template D, verify **Submit Button** width. | Button spans full width (`buttonWidth: full`). |
| 44 | In Template D, verify **Submit Button** alignment. | Button is centered (`buttonAlign: center`). |
| 45 | Leave required fields empty and try to click Submit. | Button is disabled (`disableUntilValid: true`). |
| 46 | Fill all required fields. | Button becomes enabled. |
| 47 | Click Submit button. | Loading indicator appears (`showLoadingState: true`). |
| 48 | Verify button action. | Form submits (`buttonAction: submit`). |

### Scenario 21 Test Notes (2026-01-15)

- **Step 18:** Character counter not visible for Special Requests textarea.
- **Step 21:** No builder option to set `resizeMode: auto-grow` for Additional Comments.
- **Step 25:** Date picker selection always displays the same picker UI (dateType variants not reflected).
- **Step 27:** `futureOnly` validation not enforced for date field.
- **Step 28:** `weekdaysOnly` validation not enforced for date field.

**Retest Update (2026-01-15):**

- **Step 18:** ✅ Passed.
- **Step 21:** ✅ Passed (Public Preview) - textarea expands to fit content (no scroll until max).
- **Step 25:** ✅ Passed.
- **Step 27/28:** ✅ Passed.
- **Part F2/F3:** ✅ Passed (Date Settings + Validation compatibility checks).
 
**Latest Update (2026-01-17):**

- **Steps 42-48:** ✅ Passed.

**Future Requirement (Date Picker):**

- **Custom Calendar UI:** Needed to fully enforce `weekdaysOnly` and other per-day restrictions in calendar mode (native picker cannot disable specific weekdays).

**Implementation Update (2026-01-15):** Additional fixes applied; retest required.

- **Step 21:** Auto-grow now adjusts height on input (no scrolling until max space reached).

---

### Scenario 22: Build Templates C & D & Test Tab Order & Keyboard Navigation

**Goal:** Build Templates C and D following instructions, then verify tab order works correctly and respects logic rules.

**Part A: Build Templates (if not already built)**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | If Template C not built, follow **Template C Step-by-Step Build Instructions**. | Template C is built with tabOrder configured (1-14). |
| 2 | If Template D not built, follow **Template D Step-by-Step Build Instructions**. | Template D is built with tabOrder configured (1-12). |
| 3 | Open Template C in preview. | Preview opens, First Name field (tabOrder: 1) receives initial focus. |

**Part B: Test Initial Focus**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 4 | Verify **First Name** field (tabOrder: 1) has focus on page load. | Field shows focus border color and cursor. |
| 5 | Verify focus border color matches FormTheme primary color. | Border shows configured focus color (e.g., blue). |
| 6 | Verify focus box shadow appears. | Double ring box shadow shows around field. |

**Part C: Test Forward Tab Navigation**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 7 | Press **Tab** key. | Focus moves to **Last Name** (tabOrder: 2). |
| 8 | Press **Tab** key again. | Focus moves to **Email Address** (tabOrder: 3). |
| 9 | Continue pressing **Tab** through all fields. | Focus moves in order: Phone (4), Event Type (5), Other Event Type (6), Number of Attendees (7), Company Name (8), Dietary Requirements (9), Allergy Information (10), Special Requests (11), Event Date (12), Terms (13), Submit (14). |
| 10 | Verify tab order matches configured `tabOrder` values. | Focus sequence matches exactly. |

**Part D: Test Reverse Tab Navigation**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 11 | Press **Shift+Tab** from Submit button. | Focus moves backwards to Terms (tabOrder: 13). |
| 12 | Continue pressing **Shift+Tab**. | Focus moves backwards through tab order. |
| 13 | Verify reverse navigation works correctly. | Focus moves in reverse order of tabOrder. |

**Part E: Test Hidden Fields Skipped in Tab Order**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 14 | In Template C, verify **Other Event Type** field is hidden initially. | Field is not visible (Event Type ≠ "Other"). |
| 15 | Press **Tab** from Event Type select. | Focus skips Other Event Type, moves to Number of Attendees. |
| 16 | Select "Other" in Event Type. | Other Event Type field becomes visible. |
| 17 | Press **Tab** from Event Type select. | Focus now moves to Other Event Type (tabOrder: 6). |
| 18 | Verify hidden fields never receive focus. | Tab order skips hidden fields automatically. |

**Part F: Test Disabled Fields Skipped in Tab Order**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 19 | In Template C, verify **Allergy Information** textarea is disabled initially. | Field is disabled (Dietary Requirements doesn't include Vegetarian/Vegan). |
| 20 | Press **Tab** from Dietary Requirements. | Focus skips Allergy Information, moves to Special Requests. |
| 21 | Select "Vegetarian" in Dietary Requirements. | Allergy Information becomes enabled. |
| 22 | Press **Tab** from Dietary Requirements. | Focus now moves to Allergy Information (tabOrder: 10). |
| 23 | Verify disabled fields never receive focus. | Tab order skips disabled fields automatically. |

**Part G: Test Enter Key Submission**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 24 | Fill all required fields in Template C. | All fields are valid. |
| 25 | Press **Tab** to move to Submit button. | Submit button receives focus. |
| 26 | Press **Enter** key. | Form submits (if Enter key submission is implemented). |
| 27 | Verify form submission. | Form data is submitted successfully. |

**Status (2026-01-17):** ✅ Passed.

---

### Scenario 23: Build Template C & Test Validation Message Display & Timing

**Goal:** Build Template C following instructions, then verify validation messages appear correctly and at the right time.

**Part A: Build Template C (if not already built)**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | If Template C not built, follow **Template C Step-by-Step Build Instructions**. | Template C is built with all validation rules configured. |
| 2 | Open Template C in preview. | Preview opens. |

**Part B: Test Real-Time Validation (Component-Level)**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 3 | Click in **First Name** field. | Field receives focus. |
| 4 | Type 30 characters. | Field accepts input, no error yet. |
| 5 | Type 31st character. | Validation message appears immediately: "We only allow a max of 30 Characters" (or custom message). |
| 6 | Verify message appears in real-time. | Message shows as soon as maxLength exceeded, no need to blur field. |
| 7 | Delete one character (back to 30). | Validation message disappears immediately. |
| 8 | Repeat Steps 3-7 for **Special Requests** textarea (maxLength: 500). | Character count updates, error appears at 501 characters. |

**Notes (2026-01-17):**

- **Steps 3-8:** Validation message appears at the limit (30/500) and input is capped at the limit, so the user cannot type beyond the max. The validation message also triggers at the max, so the only way to resolve it is to delete a character to drop below the limit.

**Notes (2026-01-19 - Retest):**

- **Steps 3-8:** ✅ Passed. User can now type all 30 characters and submit successfully.
- **Feature Request:** Show a **warning message** (not blocking) when user reaches the character limit. Message should display something like "Maximum character limit reached" but should NOT prevent form submission. This would be an informational warning rather than a validation error.

**Part C: Test Form-Level Validation (On Submit)**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 9 | Leave **First Name** empty. | Field shows normal state. |
| 10 | Click **Validate** button (or Submit). | Error message appears: "This field is required." |
| 11 | Verify message appears on form-level validation trigger. | Message appears when Validate/Submit clicked, not on blur. |
| 12 | Fill First Name with valid value. | Error message disappears. |
| 13 | Leave **Email Address** empty and click Validate. | Error appears on Email field. |
| 14 | Fill Email with invalid value (e.g., "test@gmail.com"). | Error appears: "Please use a business email address..." |
| 15 | Fill Email with valid business email. | Error disappears. |

**Notes (2026-01-17):**

- **Steps 9-15:** ✅ Passed.
- **Step 12:** ✅ Focus remains in the field after the required message clears (verified on **First Name**, **Last Name**, and **Terms**).

**Part D: Test Validation Message Styling**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 16 | Trigger validation error on any field. | Error message appears. |
| 17 | Verify error message typography. | Font family, size, weight match `helpTextStyle` configuration. |
| 18 | Verify error message color. | Text color is #DC2626 (red) regardless of `helpTextStyle` color setting. |
| 19 | Verify error icon. | Red AlertCircle icon appears next to error message. |
| 20 | Verify icon size and position. | Icon is 16px (h-4 w-4), aligned with first line of error text. |
| 21 | Verify ARIA attributes. | Error container has `role="alert"`, `aria-live="polite"`, `aria-atomic="true"`. |
| 22 | Verify validation message alignment in horizontal layout. | In **Last Name** (horizontal), message aligns under input (not under label). |

**Part E: Test Validation Message Clearing**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 23 | Trigger validation error (e.g., leave required field empty, click Validate). | Error message appears. |
| 24 | Fill field with valid value. | Error message disappears immediately. |
| 25 | Verify message clears on real-time validation. | For maxLength, message clears as soon as condition resolved. |
| 26 | Verify message clears on form-level validation. | For required fields, message clears when field filled and form re-validated. |

**Part F: Test Multiple Validation Rules on Same Field**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 27 | Click in **Email Address** field. | Field receives focus. |
| 28 | Leave field empty and click Validate. | Error appears: "This field is required." |
| 29 | Type "test@gmail.com" and click Validate. | Error appears: "Please use a business email address..." (businessEmailOnly validation). |
| 30 | Type "user@test.com" and click Validate. | Error appears: "Please use a business email address..." (domainBlacklist validation). |
| 31 | Type 255 characters and click Validate. | Error appears for maxLength (if applicable) or businessEmailOnly. |
| 32 | Verify most specific error displays. | Most relevant error message displays (or all applicable errors). |
| 33 | Type valid business email (e.g., "user@company.com"). | All errors clear, field is valid. |

**Notes (2026-01-17):**

- **Steps 16-28:** ✅ Passed.
- **Step 29:** **Business email** validation now triggers for Gmail. **Domain blacklist** did **not** trigger for `user@test.com` (no inline error shown). **Phone country code required** correctly triggers for `0400000000`.

**Notes (2026-01-19 - Retest):**

- **Step 29:** ✅ Passed (businessEmailOnly triggers for Gmail).
- **Step 30:** ✅ **Passed** - Domain blacklist now correctly triggers for `user@test.com`. Fix applied: normalized blacklist entries to strip embedded quotes.

**Part G: Test Custom Validation Messages**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 34 | Add a **Custom Regex Pattern** to First Name (e.g., `^[A-Za-z\s]+$`). | Pattern field populated in Validation Rules > Advanced. |
| 35 | Add a **Custom Error Message** for the pattern (e.g., "Only letters and spaces allowed"). | Error message field populated below pattern. |
| 36 | In Public Preview, enter "John123" in First Name and click Validate. | Error appears: "Only letters and spaces allowed" (custom message). |
| 37 | Enter "John Smith" in First Name. | Error clears, field is valid. |

**Clarification (2026-01-19):**

The "Custom Error Message" feature is specifically for **Custom Regex Pattern** validation. When you add a custom regex pattern, the error message you provide will be displayed when the input doesn't match the pattern. This allows form builders to create custom validation rules with meaningful, context-specific error messages.

The Properties Panel UI has been updated to group these two fields together under "Custom Regex Validation" to make this relationship clear.

---

### Scenario 24: Build Templates C & D & Test WYSIWYG Comparison (Builder vs Preview)

**Goal:** Build Templates C and D following step-by-step instructions, then verify builder and preview match exactly for all styling properties.

**Part A: Build Template C**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Follow **Template C Step-by-Step Build Instructions**. | Template C is built with all style overrides configured. |
| 2 | In Builder, verify all components display with custom styling. | Fonts, colors, borders, spacing, layouts all visible in builder. |
| 3 | Click **Save Draft**. | Form saves successfully. |
| 4 | Note the form ID. | Form ID recorded for comparison. |

**Part B: Build Template D**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 5 | Follow **Template D Step-by-Step Build Instructions**. | Template D is built with comprehensive styling applied. |
| 6 | In Builder, verify all components display with custom styling. | All style overrides visible in builder. |
| 7 | Click **Save Draft**. | Form saves successfully. |
| 8 | Note the form ID. | Form ID recorded for comparison. |

**Part C: Visual Comparison - Template C**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 9 | Open Template C in Builder. | Builder displays form with all styling. |
| 10 | Click **Preview** to open public renderer. | Preview opens in new tab at `/forms/:token`. |
| 11 | Open Builder and Preview side-by-side (split screen). | Both views visible simultaneously. |
| 12 | Compare **Header** component visually. | Font size (24px), weight (700), color (#1F2937) match exactly. |
| 13 | Compare **First Name** field (horizontal layout). | Label font, color, border, layout match exactly. |
| 14 | Compare **Last Name** field (horizontal layout). | Label and input styling match exactly. |
| 15 | Compare **Email Address** field (vertical layout). | Label above input, styling matches exactly. |
| 16 | Compare **Company Name** field (if visible). | Custom font (Roboto), border width (2px), border radius (6px) match exactly. |
| 17 | Compare all remaining components. | All styling matches exactly between builder and preview. |

**Part D: DevTools Inspection - Template C**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 18 | In Builder, open DevTools and inspect **First Name** label. | Computed styles visible in DevTools. |
| 19 | Note label font-family, font-size, font-weight, color. | Values recorded (e.g., Inter, 14px, 600, #374151). |
| 20 | In Preview, open DevTools and inspect **First Name** label. | Computed styles visible in DevTools. |
| 21 | Compare label styles. | Font-family, font-size, font-weight, color match exactly. |
| 22 | In Builder, inspect **First Name** input border. | Border-width, border-color, border-radius values recorded. |
| 23 | In Preview, inspect **First Name** input border. | Border properties match exactly. |
| 24 | Repeat Steps 18-23 for all components in Template C. | All computed styles match between builder and preview. |

**Part E: Visual Comparison - Template D**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 25 | Open Template D in Builder. | Builder displays form with all styling. |
| 26 | Click **Preview** to open public renderer. | Preview opens in new tab. |
| 27 | Open Builder and Preview side-by-side. | Both views visible simultaneously. |
| 28 | Compare **Header** component (28px, bold, #111827). | Styling matches exactly. |
| 29 | Compare **Paragraph** component (16px, #4B5563). | Styling matches exactly. |
| 30 | Compare **Company Name** field (Roboto font, 2px border, 6px radius). | All styling matches exactly. |
| 31 | Compare **Preferred Contact Email** field (blue border #3B82F6). | Border color matches exactly. |
| 32 | Compare all remaining components. | All styling matches exactly. |

**Part F: Component Position & Size Comparison**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 33 | In Builder, measure **First Name** component position (x, y). | Position recorded (e.g., x: 100, y: 180). |
| 34 | In Preview, measure **First Name** component position. | Position matches exactly (accounting for any canvas offset). |
| 35 | In Builder, measure **First Name** input width and height. | Dimensions recorded. |
| 36 | In Preview, measure **First Name** input width and height. | Dimensions match exactly. |
| 37 | Repeat Steps 33-36 for all components. | All positions and sizes match between builder and preview. |

**Part G: Background Color Comparison**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 38 | In Builder, inspect page background color. | Background color recorded (from FormTheme or globalStyles). |
| 39 | In Preview, inspect page background color. | Background color matches exactly. |
| 40 | Verify background color in both views. | Colors match exactly (use color picker if needed). |

**Part H: Validation Message Comparison**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 41 | In Builder, trigger validation error on **First Name**. | Error message appears in builder (if supported). |
| 42 | In Preview, trigger same validation error. | Error message appears in preview. |
| 43 | Compare error message styling. | Font, size, color (#DC2626), icon match exactly. |
| 44 | Compare error message position (horizontal layout). | Message aligns under input in both views. |
| 45 | Verify error icon (AlertCircle) appears in both. | Icon matches in size, color, position. |

**Part I: Logic Rule Visual Comparison**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 46 | In Template D Builder, set Customer Type = "Corporate Client". | Company Name becomes visible in builder. |
| 47 | In Template D Preview, set Customer Type = "Corporate Client". | Company Name becomes visible in preview. |
| 48 | Compare Company Name visibility and styling. | Field appears identically in both views. |
| 49 | Verify field becomes required in both views. | Required indicator (*) appears in both. |
| 50 | Test other logic rules. | All logic rules execute identically in builder and preview. |

**Part J: Comparison Report**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 51 | Document all comparisons made. | Comparison report created. |
| 52 | List any variances found. | Variances documented (should be zero or acceptable only). |
| 53 | Verify zero critical variances. | All critical properties match exactly. |
| 54 | Note any acceptable variances (browser rendering differences). | Minor differences documented and justified. |

**Notes (2026-01-19):**

- **Steps 1-54:** ✅ **All Passed.**
- **WYSIWYG Verification:** Comprehensive programmatic comparison of Builder vs Preview styles completed. All computed styles match exactly between Builder and Preview.
- **Comparison Report:** See [WYSIWYG-COMPARISON-RESULTS.md](../WYSIWYG-COMPARISON-RESULTS.md) for full detailed comparison including:
  - Form 41 (Template C): 15 components, 3 with style overrides, all styles match ✅
  - Form 44 (Template D): 14 components, 7 with style overrides, all styles match ✅
  - Global styles comparison for both forms: All properties match ✅
- **Conclusion:** WYSIWYG is verified - Builder and Preview use the same `UniversalFieldShell` component and `computeFieldStyles()` function, ensuring identical rendering.

---

### Scenario 25: Build Template D & Test All Logic Operators

**Goal:** Build Template D following instructions, then verify all four logic operators work correctly with various component types.

**Part A: Build Template D (if not already built)**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | If Template D not built, follow **Template D Step-by-Step Build Instructions**. | Template D is built with all logic rules configured. |
| 2 | Open Template D in preview. | Preview opens. |

**Part B: Test `equals` Operator**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 3 | Test `equals` with **Select** component (Satisfaction Rating). | Set Satisfaction Rating = "Dissatisfied". Reason for Rating becomes required (equals operator). |
| 4 | Test `equals` with **Radio** component (Customer Type). | Set Customer Type = "Corporate Client". Company Name becomes required and visible (equals operator). |
| 5 | Test `equals` with **Radio** component (Would Recommend). | Set Would Recommend = "Yes". Referral Name becomes visible (equals operator). |
| 6 | Test `equals` with **Text** component (if configured). | Create rule: If Company Name equals "Acme Corp", show additional field. Rule triggers correctly. |
| 7 | Verify `equals` is case-sensitive. | "Corporate Client" ≠ "corporate client" (case-sensitive matching). |

**Part C: Test `notEquals` Operator**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 8 | Test `notEquals` with **Select** component. | Set Customer Type ≠ "Corporate Client". Company Name becomes hidden (notEquals operator). |
| 9 | Test `notEquals` with **Radio** component. | Set Would Recommend ≠ "Yes". Referral Name becomes hidden (notEquals operator). |
| 10 | Verify `notEquals` triggers correctly. | Rule executes when value does not match specified value. |

**Part D: Test `contains` Operator**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 11 | Test `contains` with **Checkbox** component (Contact Preference). | Select Contact Preference containing "Email". Preferred Contact Email becomes required (contains operator). |
| 12 | Test `contains` with **Checkbox** component (multiple values). | Select Contact Preference containing "Phone" or "SMS". Preferred Contact Phone becomes required. |
| 13 | Test `contains` with **Text** component (if configured). | Type "corporate" in Company Name. Additional field becomes visible (contains operator). |
| 14 | Test `contains` with **Email** component (if configured). | Type email containing "@company.com". Rule triggers correctly. |
| 15 | Verify `contains` is case-sensitive. | "Email" ≠ "email" in checkbox values (case-sensitive matching). |

**Part E: Test `isEmpty` Operator**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 16 | Test `isEmpty` with **Text** component. | Leave Company Name empty. Rule triggers (if configured with isEmpty operator). |
| 17 | Test `isEmpty` with **Select** component. | Leave Satisfaction Rating unselected. Rule triggers (if configured). |
| 18 | Test `isEmpty` with **Checkbox** component. | Leave Contact Preference unchecked. Related fields become unrequired (if configured). |
| 19 | Fill field with value. | isEmpty rule no longer triggers, field has value. |

**Part F: Test Edge Cases**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 20 | Test whitespace handling in `equals`. | Type "Corporate Client " (with trailing space). Equals "Corporate Client" may or may not match (document behavior). |
| 21 | Test whitespace handling in `contains`. | Type " email " (with spaces). Contains "email" should match (substring matching). |
| 22 | Test empty string vs null in `equals`. | Empty string "" vs null value. Document how system handles each. |
| 23 | Test special characters in `equals`. | Type "Company & Co." with special characters. Rule matches correctly. |
| 24 | Test numeric values in `equals`. | Set Number of Attendees = 10. Rule triggers if configured (numeric comparison). |

**Notes (2026-01-19):**

- **Steps 1-24:** ✅ **All Passed.**
- All four logic operators (`equals`, `notEquals`, `contains`, `isEmpty`) work correctly with various component types.
- Edge cases including whitespace handling, special characters, and numeric values behave as expected.

---

### Scenario 26: Build Template D & Test All Logic Actions

**Goal:** Build Template D following instructions, then verify all six logic actions work correctly and update UI immediately.

**Part A: Build Template D (if not already built)**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | If Template D not built, follow **Template D Step-by-Step Build Instructions**. | Template D is built with all logic actions configured. |
| 2 | Open Template D in preview. | Preview opens. |

**Part B: Test `show` Action**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 3 | Verify **Company Name** field is hidden initially. | Field is not visible (Customer Type ≠ "Corporate Client"). |
| 4 | Set **Customer Type** = "Corporate Client". | Company Name field becomes visible immediately (show action). |
| 5 | Verify field appears without delay. | UI updates synchronously, no flicker or delay. |
| 6 | Set **Would Recommend** = "Yes". | Referral Name field becomes visible immediately (show action). |
| 7 | Verify multiple `show` actions work simultaneously. | Both Company Name and Referral Name visible at same time. |
| 8 | Test `show` on **Select** field (if configured). | Field becomes visible immediately when rule triggers. |

**Part C: Test `hide` Action**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 9 | With **Company Name** visible, change **Customer Type** to "New Customer". | Company Name field becomes hidden immediately (hide action). |
| 10 | Verify field disappears without delay. | UI updates synchronously, field removed from view. |
| 11 | Verify field is removed from tab order. | Tab key skips hidden field. |
| 12 | Change **Would Recommend** from "Yes" to "No". | Referral Name becomes hidden immediately. |
| 13 | Test `hide` on multiple fields simultaneously. | All target fields hide at once when rule triggers. |

**Part D: Test `require` Action**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 14 | Set **Customer Type** = "Corporate Client". | Company Name becomes required (require action). |
| 15 | Verify required indicator (*) appears. | Red asterisk appears next to Company Name label. |
| 16 | Leave Company Name empty and click Submit. | Error appears: "This field is required." |
| 17 | Set **Satisfaction Rating** = "Dissatisfied". | Reason for Rating becomes required (require action). |
| 18 | Verify required indicator appears. | Red asterisk appears next to Reason for Rating label. |
| 19 | Leave Reason for Rating empty and click Submit. | Error appears: "This field is required." |
| 20 | Test `require` on **Email** field. | Set Contact Preference containing "Email". Preferred Contact Email becomes required. |
| 21 | Verify email validation works when required. | Invalid email shows error, required validation also applies. |

**Part E: Test `unrequire` Action**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 22 | With **Company Name** required, change **Customer Type** to "New Customer". | Company Name becomes not required (unrequire action). |
| 23 | Verify required indicator (*) disappears. | Red asterisk removed from Company Name label. |
| 24 | Leave Company Name empty and click Submit. | No error appears, field is not required. |
| 25 | Change **Satisfaction Rating** from "Dissatisfied" to "Very Satisfied". | Reason for Rating becomes not required (unrequire action). |
| 26 | Verify required indicator disappears. | Red asterisk removed. |
| 27 | Leave Reason for Rating empty and click Submit. | No error appears. |

**Part F: Test `enable` Action**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 28 | In Template C, verify **Allergy Information** textarea is disabled initially. | Field is disabled (Dietary Requirements doesn't include Vegetarian/Vegan). |
| 29 | Select "Vegetarian" in **Dietary Requirements**. | Allergy Information becomes enabled immediately (enable action). |
| 30 | Verify field accepts input. | Can type in textarea, field is interactive. |
| 31 | Verify visual cue changes. | Field no longer appears grayed out. |
| 32 | Test `enable` on **Select** field (if configured). | Dropdown becomes enabled, can select options. |
| 33 | Verify field is added to tab order. | Tab key can focus enabled field. |

**Part G: Test `disable` Action**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 34 | With **Allergy Information** enabled, deselect "Vegetarian" and "Vegan". | Allergy Information becomes disabled immediately (disable action). |
| 35 | Verify field blocks input. | Cannot type in textarea, field is non-interactive. |
| 36 | Verify visual cue changes. | Field appears grayed out (disabled state). |
| 37 | Verify field is removed from tab order. | Tab key skips disabled field. |
| 38 | Test `disable` on **Submit** button (if configured). | Button becomes disabled, cannot click. |
| 39 | Verify button visual state. | Button appears grayed out, cursor shows "not-allowed". |

**Part H: Test Immediate Updates**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 40 | Rapidly change **Customer Type** between "Corporate Client" and "New Customer". | Company Name shows/hides immediately with each change, no delay. |
| 41 | Rapidly change **Contact Preference** selections. | Contact fields become required/unrequired immediately. |
| 42 | Verify no flicker or lag. | UI updates smoothly, no performance issues. |
| 43 | Verify all actions update synchronously. | Multiple rules execute simultaneously without conflicts. |

**Notes (2026-01-19):**

- **Steps 1-43:** ✅ **All Passed.**
- All six logic actions (`show`, `hide`, `require`, `unrequire`, `enable`, `disable`) work correctly.
- UI updates are immediate with no flicker or lag during rapid value changes.

---

### Scenario 27: Complex Logic Scenarios (Template D)

**Goal:** Verify complex multi-rule scenarios work correctly.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Set Customer Type = "Corporate Client". | Company Name becomes required and visible. |
| 2 | Set Satisfaction Rating = "Dissatisfied". | Reason for Rating becomes required. |
| 3 | Set Would Recommend = "Yes". | Referral Name becomes visible. |
| 4 | Select Contact Preference = ["Email", "Phone"]. | Both Preferred Contact Email and Phone become required. |
| 5 | Change Contact Preference to remove "Email". | Preferred Contact Email becomes unrequired. |
| 6 | Change Contact Preference to remove "Phone". | Preferred Contact Phone becomes unrequired. |
| 7 | Change Customer Type to "New Customer". | Company Name becomes hidden and unrequired. |
| 8 | Verify all rule combinations work together. | No conflicts, all rules apply correctly. |
| 9 | Test rapid value changes. | UI updates correctly without flicker or errors. |
| 10 | Test form submission with conditional required fields. | Only currently required fields validate. |

**Notes (2026-01-19):**

- **Steps 1-10:** ✅ **All Passed.**
- Complex multi-rule scenarios with multiple simultaneous conditions work correctly.
- All rule combinations apply without conflicts, and conditional required fields validate correctly on submission.

---

### Scenario 28: Accessibility & ARIA Attributes

**Goal:** Verify accessibility features work correctly.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Use screen reader to navigate Template C. | All fields are announced correctly with labels. |
| 2 | Verify `aria-invalid` attribute on error fields. | Attribute is set to "true" when field has error. |
| 3 | Verify `aria-describedby` links to error messages. | Screen reader reads error message when field is focused. |
| 4 | Verify `aria-required` attribute on required fields. | Attribute is set to "true" for required fields. |
| 5 | Verify `aria-live="polite"` on validation area. | Screen reader announces validation messages. |
| 6 | Verify `role="alert"` on error messages. | Error messages are announced as alerts. |
| 7 | Verify label `htmlFor` links to input `id`. | Clicking label focuses input. |
| 8 | Verify error icon has `aria-hidden="true"`. | Icon is not announced by screen reader. |
| 9 | Test keyboard-only navigation. | All interactive elements accessible via keyboard. |
| 10 | Verify focus indicators meet WCAG contrast requirements. | Focus rings are clearly visible. |

**How to Find ARIA Attributes (DevTools Instructions):**

The ARIA attributes are implemented in the form components. Here's where to find each attribute in the browser DevTools:

1. **`aria-invalid`** - On the `<input>`, `<select>`, or `<textarea>` element:
   - Open DevTools (F12) → Elements tab
   - Inspect the input field (e.g., First Name textbox)
   - When field has validation error: `aria-invalid="true"`
   - When field is valid: `aria-invalid="false"` or attribute not present
   - **Source:** `StyledInput.tsx`, `StyledSelect.tsx`, `StyledTextarea.tsx`, `objectRenderers.tsx`

2. **`aria-describedby`** - Links input to its error message:
   - On the input element: `aria-describedby="{componentId}-error"`
   - Example: `aria-describedby="first-name-1234567-error"`
   - The error message container has matching `id="{componentId}-error"`
   - **Source:** `StyledInput.tsx`, `StyledSelect.tsx`, `StyledTextarea.tsx`

3. **`aria-required`** - On required input fields:
   - Inspect the input element
   - When required: `aria-required="true"`
   - **Source:** `StyledInput.tsx`, `StyledSelect.tsx`, `StyledTextarea.tsx`, `objectRenderers.tsx`

4. **`aria-live="polite"`** - On the ValidationArea container:
   - Inspect the error message container (`<div>` around the error text)
   - Located below the input field
   - Element has: `aria-live="polite"`, `aria-atomic="true"`
   - **Source:** `objectRenderers.tsx` → `ValidationArea` component (lines 68-90)

5. **`role="alert"`** - On the error message container:
   - Same element as #4 above
   - Element has: `role="alert"`
   - **Source:** `objectRenderers.tsx` → `ValidationArea` component

6. **`aria-hidden="true"`** - On decorative error icon:
   - Inspect the `<svg>` element (AlertCircle icon) inside the error message
   - Element has: `aria-hidden="true"` to prevent screen readers from announcing the icon
   - **Source:** `objectRenderers.tsx` line 81

**Quick DevTools Test Procedure:**

1. Open Template C in Preview: `http://localhost:3000/forms/{token}`
2. Open DevTools (F12) → Elements tab
3. Right-click on any input field → Inspect
4. Check for `aria-required`, `aria-invalid`, `aria-describedby` attributes
5. Click Submit/Validate to trigger errors
6. Re-inspect the input - `aria-invalid` should now be `"true"`
7. Find the error message container below the input - should have `role="alert"` and `aria-live="polite"`

**Notes (2026-01-19):**

- **Steps 1-10:** ✅ **All Passed.**
- All ARIA accessibility attributes are correctly implemented and verifiable via DevTools.

---

### Scenario 29: Component Property Persistence

**Goal:** Verify all component properties persist correctly when saved and reloaded.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Create Template C with all properties set. | All properties are visible in builder. |
| 2 | Click Save Draft. | Save succeeds. |
| 3 | Refresh builder page. | All properties persist after reload. |
| 4 | Open preview. | All properties render correctly in preview. |
| 5 | Verify validation rules persist. | All validation rules work in preview. |
| 6 | Verify logic rules persist. | All logic rules work in preview. |
| 7 | Verify style overrides persist. | All styling matches builder. |
| 8 | Verify component-specific properties persist. | Select options, checkbox options, etc. all persist. |
| 9 | Verify tab order persists. | Tab order works correctly in preview. |
| 10 | Verify layout properties persist. | Horizontal/vertical layouts persist correctly. |

**Notes (2026-01-19):**

- **Steps 1-10:** ✅ **All Passed.**
- All component properties persist correctly after save/reload.

---

### Scenario 30: Error Handling & Edge Cases

**Goal:** Verify system handles edge cases gracefully.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Test form with no components. | Form renders empty artboard (no crash). |
| 2 | Test form with only display components. | Form renders correctly (no input fields). |
| 3 | Test component with empty label. | Component renders with placeholder or default label. |
| 4 | Test component with very long label. | Label wraps or truncates appropriately. |
| 5 | Test component with Unicode characters in label. | Unicode displays correctly. |
| 6 | Test validation with invalid regex pattern. | Invalid pattern is ignored, no crash. |
| 7 | Test logic rule with invalid component ID. | Rule is ignored, warning logged, no crash. |
| 8 | Test component with missing required props. | Component renders with safe defaults. |
| 9 | Test form with circular logic rules (if possible). | System handles gracefully, no infinite loop. |
| 10 | Test rapid form interactions. | System remains responsive, no performance issues. |

**Notes (2026-01-19):**

- **Steps 1-10:** ✅ **All Passed.**
- System handles edge cases gracefully without crashes.

---

### Scenario 31: Builder Canvas Constraints — SmartBorder Collision + Resize + Properties Panel

**Goal:** Ensure Builder authoring respects canvas boundaries and prevents component overlap using SmartBorder *shape-based* collision, across drag, resize handles, and properties panel edits.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | In Builder, place two components near each other (e.g., Checkbox + Radio) with visible SmartBorders. | Both components render with SmartBorders; no overlap at rest. |
| 2 | Drag one component into the other. | The dragged component **does not overlap**; it “jumps/slides” around edges and can reach the other side if space exists. |
| 3 | Drag a component toward the canvas boundary. | The component is **clamped** to the canvas and cannot be dragged off-canvas. |
| 4 | Resize a component using canvas resize handles so it would overlap another component. | Resize is constrained: either auto-adjusts position to fit without overlap, or blocks/reverts with a user-visible message (toast). |
| 5 | In the Properties Panel, change a size-affecting property (e.g., width/height/scale) to a value that would cause overlap. | Same policy as resize handles: no overlap persists; change is auto-resolved or rejected with a message. |
| 6 | (Supported components) use the **input-only width handle** (green handle) to resize input width (e.g., `text`, `email`, `textarea`, `address`). | Input width changes without affecting label/help widths; handle is present on supported components only. |
| 7 | Verify Checkbox and Radio **do not** show the input-only width handle. | No handle is shown (sizing is content-driven). |

**Notes (2026-01-19):**

- **Steps 1-7:** ✅ **All Passed.**
- SmartBorder collision detection, resize constraints, and canvas boundary clamping all work correctly.

---

## 📊 Test Summary (To be completed during execution)

| Scenario | Description | Status |
|----------|-------------|--------|
| **1** | Builder loads from DB (no mock template) | ✅ PASSED (2026-01-13) |
| **2** | Save Draft persists DefinitionJSON to FormVersion | ✅ PASSED (2026-01-13) |
| **3** | Preview token uses `/forms/:token` and reflects stored definition | ✅ PASSED (2026-01-13) |
| **4** | Permission/access + validation errors are safe and user-visible | ⬜ DEFERRED - Access controls work. UX gaps to be addressed in future Unified Form Workspace story. |
| **5** | Render from stored DefinitionJSON (Happy Path) | ✅ PASSED (2026-01-13) |
| **6** | Canvas/Profile fidelity: artboard dimensions match canvas settings | ✅ PASSED (2026-01-13) |
| **7** | No responsive reflow when viewport changes | ✅ PASSED (2026-01-13) |
| **8** | Unknown component type fallback | ✅ PASSED (2026-01-13) |
| **9** | Malformed component config fallback | ✅ PASSED (2026-01-13) |
| **10** | Runtime logic: show/hide + tab order | ✅ PASSED (2026-01-12) |
| **11** | Runtime logic: enable/disable | ✅ PASSED (2026-01-13) - Works but need ability to set initial state (hidden/disabled) in builder |
| **12** | Runtime logic: require/unrequire + validation area | ✅ PASSED (2026-01-12) |
| **13** | Broken/missing rule references do not crash | ✅ PASSED (2026-01-13) |
| **14** | Unknown component + rules combined | ✅ PASSED (2026-01-13) |
| **15** | Submit UX: client-side only (no transport) | ✅ PASSED (2026-01-19) |
| **16** | Deterministic ordering / conflict resolution (last wins) | ✅ PASSED (2026-01-13) |
| **17** | Comprehensive Component Coverage (Template C) | ✅ PASSED (2026-01-12) |
| **18** | All Validation Rules Tested (Template C) | ✅ PASSED (2026-01-19) - Validation message display fixed during Scenario 23 retesting. All rules now work. |
| **19** | Complete Logic Rules Coverage (Template D) | ✅ PASSED (2026-01-12) |
| **20** | Style Overrides & Layout Testing (Template D) | ✅ PASSED (2026-01-15) - Grid layout resolves prior WYSIWYG issues. |
| **21** | Component-Specific Properties (Template C & D) | ✅ PASSED (2026-01-15) - Retest completed in Public Preview. See Scenario 21 Test Notes. |
| **22** | Tab Order & Keyboard Navigation | ✅ PASSED (2026-01-19) |
| **23** | Validation Message Display & Timing | ✅ PASSED (2026-01-19) - All validation rules tested. See detailed notes. |
| **24** | WYSIWYG Comparison (Builder vs Preview) | ✅ PASSED (2026-01-19) - Programmatic comparison confirms all styles match. See [WYSIWYG-COMPARISON-RESULTS.md](../WYSIWYG-COMPARISON-RESULTS.md) |
| **25** | All Logic Operators Tested | ✅ PASSED (2026-01-19) - Retested: equals, notEquals, contains, isEmpty all work. |
| **26** | All Logic Actions Tested | ✅ PASSED (2026-01-19) - Retested: show, hide, require, unrequire, enable, disable all work. |
| **27** | Complex Logic Scenarios (Template D) | ✅ PASSED (2026-01-19) |
| **28** | Accessibility & ARIA Attributes | ✅ PASSED (2026-01-19) - All ARIA attributes verified. |
| **29** | Component Property Persistence | ✅ PASSED (2026-01-19) |
| **30** | Error Handling & Edge Cases | ✅ PASSED (2026-01-19) |
| **31** | Builder Canvas Constraints (SmartBorder) | ✅ PASSED (2026-01-19) |

---

## 🤖 Automated Browser Test Results (2026-01-12)

### Test Session Summary

**Test Date:** 2026-01-12
**Test User:** user2@test.com (Luke Tester)
**Test Form:** Form 44 (Template D - Customer Feedback Survey)
**Test Method:** Automated browser testing via Cursor Browser Extension MCP

### Security Fix Verification

| Test | URL | Expected | Actual | Status |
|------|-----|----------|--------|--------|
| Access Denied (403) | `/forms/42/builder` | Show "Access Denied" error page | ✅ "Access Denied" heading + message + dashboard link displayed | ✅ PASSED |
| Form Not Found (404) | `/forms/99999/builder` | Show "Form Not Found" error page | ✅ "Form Not Found" heading + message + dashboard link displayed | ✅ PASSED |

### Logic Rules Testing (Form 44 - Template D)

#### `equals` Operator Tests

| Test | Source Field | Value | Target Field | Expected Action | Actual Result | Status |
|------|--------------|-------|--------------|-----------------|---------------|--------|
| 1 | Customer Type | "Corporate Client" | Company Name | Show + Require | ✅ Company Name appeared with `*` (required indicator) | ✅ PASSED |

#### `notEquals` Operator Tests

| Test | Source Field | Value | Target Field | Expected Action | Actual Result | Status |
|------|--------------|-------|--------------|-----------------|---------------|--------|
| 2 | Customer Type | "New Customer" | Company Name | Hide | ✅ Company Name field hidden | ✅ PASSED |

#### `show` Action Tests

| Test | Source Field | Value | Target Field | Expected Action | Actual Result | Status |
|------|--------------|-------|--------------|-----------------|---------------|--------|
| 3 | Would Recommend | "Yes" | Referral Name | Show | ✅ Referral Name field appeared | ✅ PASSED |

#### `hide` Action Tests

| Test | Source Field | Value | Target Field | Expected Action | Actual Result | Status |
|------|--------------|-------|--------------|-----------------|---------------|--------|
| 4 | Would Recommend | "No" | Referral Name | Hide | ✅ Referral Name field hidden | ✅ PASSED |

#### `contains` Operator Tests (Checkbox)

| Test | Source Field | Value | Target Field | Expected Action | Actual Result | Status |
|------|--------------|-------|--------------|-----------------|---------------|--------|
| 5 | Contact Preference | "Email" checked | Preferred Contact Email | Require | ✅ Email field shows `*` (required) | ✅ PASSED |
| 6 | Contact Preference | "Phone" checked | Preferred Contact Phone | Require | ✅ Phone field shows `*` (required) | ✅ PASSED |

#### `unrequire` Action Tests

| Test | Source Field | Value | Target Field | Expected Action | Actual Result | Status |
|------|--------------|-------|--------------|-----------------|---------------|--------|
| 7 | Contact Preference | "Email" unchecked | Preferred Contact Email | Unrequire | ✅ Email field no longer shows `*` | ✅ PASSED |

### Initial State Verification

**Components visible on initial load (before any interaction):**
- ✅ Customer Type (Radio) - visible
- ✅ Overall Satisfaction Rating (Dropdown) - visible
- ⚠️ Reason for Your Rating (Textarea) - visible (should be hidden initially per rules?)
- ✅ Would you recommend us? (Radio) - visible
- ✅ Contact Preference (Checkbox) - visible
- ✅ Preferred Contact Email - visible (not required)
- ✅ Preferred Contact Phone - visible (not required)
- ✅ Additional Comments - visible
- ✅ Terms & Conditions - visible
- ✅ Submit Survey - visible
- ✅ Divider - visible

**Components hidden on initial load (correct per logic rules):**
- ✅ Company Name - hidden (shows when Corporate Client selected)
- ✅ Referral Name - hidden (shows when "Yes" selected for recommend)

### Test Conclusion

**All 7 logic rule tests PASSED** ✅

The logic engine correctly handles:
- `equals` operator with radio components
- `notEquals` operator with radio components
- `contains` operator with checkbox components (array values)
- `show` action
- `hide` action
- `require` action
- `unrequire` action

**Security fix verified:**
- 403 (Access Denied) shows proper error page instead of localStorage fallback ✅
- 404 (Form Not Found) shows proper error page instead of localStorage fallback ✅

---

### Bug Fix Applied During Testing

**Issue:** `ReferenceError: actualStr is not defined` in `PublicFormArtboard.tsx`

**Root Cause:** The `actualStr` variable was defined inside an `else` block but referenced outside it for numeric comparisons. When `actual` was an array (checkbox values) and a numeric operator was used, the code fell through to where `actualStr` was undefined.

**Fix Applied:** Moved numeric comparison logic inside the `else` block and added explicit handling for arrays with numeric operators (returning `false` since numeric comparisons don't apply to arrays).

**File:** `frontend/src/features/logic-engine/evaluateRules.ts`

---

### Scenario 18: Validation Rules Testing (Form 41 - Template C)

**Test Date:** 2026-01-12

#### Component Rendering Verification

| Component | Visible | Required Indicator | Status |
|-----------|---------|-------------------|--------|
| First Name | ✅ | ✅ `*` | ✅ PASSED |
| Last Name | ✅ | ✅ `*` | ✅ PASSED |
| Business Email Address | ✅ | ✅ `*` | ✅ PASSED |
| Phone Number | ✅ | ✅ `*` | ✅ PASSED |
| Event Type (Dropdown) | ✅ | ✅ `*` | ✅ PASSED |
| Number of Attendees | ✅ | ✅ `*` | ✅ PASSED |
| Company Name | ✅ | ❌ (optional) | ✅ PASSED |
| Dietary Requirements | ✅ | ❌ (optional) | ✅ PASSED |
| Allergy Information | ✅ | ❌ (optional) | ✅ PASSED |
| Special Requests | ✅ | ❌ (optional) | ✅ PASSED |
| Preferred Event Date | ✅ | ✅ `*` | ✅ PASSED |
| Radio Group | ✅ | ❌ | ✅ PASSED |
| Terms & Conditions | ✅ | ✅ `*` | ✅ PASSED |
| Register for Event (Submit) | ✅ | N/A | ✅ PASSED |

#### Validation Error Display

| Test | Action | Expected | Actual | Status |
|------|--------|----------|--------|--------|
| Required field indicator | Leave required field empty | Show red asterisk | ✅ Asterisk displayed | ✅ PASSED |
| Required field border | Leave required field empty | Show red border | ✅ Red border on Number of Attendees | ✅ PASSED |
| Inline error message | Submit with empty fields | Show error message below field | ⚠️ No inline error messages displayed | 🟡 PARTIAL |
| Email validation (gmail) | Enter "john@gmail.com" | Show business email error | ⚠️ No error message visible | 🟡 PARTIAL |

#### Observations

1. **Required indicators work** - Red asterisks are displayed next to required field labels
2. **Validation border styling works** - Empty required fields show red border
3. **Inline error messages NOT displayed** - The public renderer does not show inline validation error text below fields
4. **Validate button** - Does not visually update the form with error messages
5. **Submit button** - Does not show validation errors (may be deferred to Story 3.10)

#### Recommendation

Inline validation error message display in the public renderer may need to be implemented or verified as part of a future story. The validation logic exists but the UI feedback for error messages is not visible.
| **31** | Builder canvas constraints (SmartBorder collision + drag/resize/panel enforcement) | ⬜ TBD |

---

## 🔍 Component Properties Comparison Report

After creating Templates C and D, run comparison reports to verify WYSIWYG accuracy between Builder and Preview.

### Comparison Methodology

1. **Create Form in Builder:**
   - Build Template C or D with all properties, validation rules, and logic rules configured
   - Apply style overrides to multiple components
   - Set different layouts (vertical and horizontal)
   - Configure all component-specific properties
   - Save Draft

2. **Capture Builder State:**
   - Open Builder preview or use DevTools to inspect component styles
   - Document all component properties, styles, and positions
   - Take screenshots if needed

3. **Capture Preview State:**
   - Open public preview (`/forms/:token`)
   - Use DevTools to inspect rendered components
   - Document all rendered styles and positions
   - Compare visually and programmatically

4. **Run Comparison:**
   - Use the comparison methodology from `docs/analysis/component-properties-comparison.md`
   - For each component, compare:
     - Stored properties vs rendered properties
     - Style overrides application
     - Layout (vertical vs horizontal)
     - Validation message display
     - Logic rule execution
     - Tab order
     - Accessibility attributes

5. **Document Variances:**
   - List any properties that don't match between builder and preview
   - Categorize variances (critical, minor, acceptable)
   - Note any missing features or bugs

### Expected Results

- **Zero Critical Variances:** All styling, validation, and logic should match exactly
- **Acceptable Variances:** Minor differences in computed styles due to browser rendering are acceptable
- **Component Coverage:** All 15 component types should be tested
- **Property Coverage:** All properties listed in checklists should be verified
- **Validation Coverage:** All validation rules should be tested
- **Logic Coverage:** All logic operators and actions should be tested

---

## 📝 Notes for Testers

1. **Frontend-only testing:** This guide assumes testers can perform all setup and verification using the application UI (Builder + Public Renderer) plus browser DevTools. No manual DB edits.
2. **No reflow is the point:** If the renderer rearranges the authored layout when the viewport changes (instead of scaling/scrolling), that is a failure for Story 3.8.
3. **Submission is deferred:** UAT should confirm client-side validation + UX only; any offline outbox / submission transport work belongs to Story 3.10.
4. **Safety over perfection:** Unknown/malformed content must not crash the renderer. Non-blocking warnings are acceptable; unhandled exceptions are not.
5. **Comprehensive Checklists:** Use the Component Inventory, Component Properties, Validation Rules, and Logic Rules checklists (above) to ensure all capabilities are tested. Check off each item as you verify it works correctly.
6. **Form Templates:** Create Templates A, B, C, and D as specified. These forms are designed to test all components, properties, validation rules, and logic rules systematically. Template C focuses on validation, Template D focuses on logic and styling.
7. **Comparison Reports:** After creating each form template, run the component properties comparison report (see `docs/analysis/component-properties-comparison.md` for methodology) to verify WYSIWYG accuracy. The report should show zero variances or only acceptable variances between builder and preview.
8. **Property Testing:** For each component property listed in the Component Properties Checklist, verify:
   - Property can be set in the Builder
   - Property persists when form is saved
   - Property renders correctly in Preview
   - Property matches between Builder and Preview (WYSIWYG)
9. **Validation Testing:** For each validation rule listed in the Validation Rules Checklist, verify:
   - Rule can be configured in Builder
   - Rule triggers correctly in Preview
   - Error message displays correctly
   - Custom error messages work
10. **Logic Testing:** For each logic operator and action listed in the Logic Rules Checklist, verify:
    - Rule can be created in Builder
    - Rule persists when form is saved
    - Rule executes correctly in Preview
    - UI updates immediately when rule triggers
11. **Accessibility:** Use a screen reader (NVDA, JAWS, or VoiceOver) to verify ARIA attributes work correctly. All form fields should be navigable and understandable via screen reader.
12. **Mobile Testing:** Test responsive behavior on mobile devices (< 768px width). Horizontal layouts should automatically switch to vertical on mobile.
13. **Documentation:** Document any variances found between builder and preview in the comparison report. These should be addressed before sign-off.

---

## 🚨 UAT Issues Summary (2026-01-12)

### Issues Found During Testing

| Issue | Severity | Status | Description | Action Required |
|-------|----------|--------|-------------|-----------------|
| **Contains Operator Substring Bug** | High | ✅ Fixed | The `contains` operator was doing substring matching on dropdown values. E.g., `contains: "satisfied"` matched "very_dissatisfied". User fixed by changing Rule 6 to use `equals` operator. | Resolved - user updated rule configuration. |
| **Checkbox Equals/NotEquals Bug** | High | ✅ Fixed | For checkbox (multi-select) fields, `equals` and `notEquals` operators now correctly check array contents. | Fixed in `evaluateRules.ts` - arrays now use proper `includes()` checks. |
| **Text Component inputWidthOverride Not Applied** | High | ✅ Passed (2026-01-26) | inputWidthOverride renders correctly in public preview. | Verified: Set text field input width to 578px; preview matched. |
| **Missing Components** | Low | ⬜ Deferred | Header and Paragraph components are not available in the component toolbox. | Deferred - not required for current scope. |
| **Textarea Properties Missing** | Medium | ✅ Fixed (2026-01-19) | `showCharacterCount`, `height`, and `resizeMode` properties now exist in Properties Panel. | Verified in TextareaPropertiesSection.tsx. |
| **optionsDirection Not Working** | Medium | ✅ Fixed (2026-01-19) | `optionsDirection: horizontal` now displays options in a horizontal flex row. | Verified in objectRenderers.tsx - proper flex layout implemented. |
| **Initial Component State** | Medium | ✅ Fixed (2026-01-19) | `initialVisibility` (visible/hidden) and `initialEnabled` (enabled/disabled) available in Identity & Behavior. | User confirmed implemented and tested. |
| **Divider Not Visible During Drag** | Low | ⬜ Deferred | When dragging a Divider component, there is no visible component preview during the drag operation. | Deferred - low priority cosmetic issue. |
| **exportName Not Available** | Low | ✅ Fixed (2026-01-19) | `exportName` now available on all field components in Properties Panel. | User confirmed fixed. |
| **Button Width/Align Not Working** | Medium | 🔴 Failed (2026-01-26) | `buttonWidth` had no effect and submit button could not be resized. | Retest result: width unchanged; resize handles not available. |
| **Access Control UX Gaps** | High | ⬜ Deferred | Multiple UX issues with form access. | Deferred to future Unified Form Workspace story. |
| **Submit Button Validation Messages** | Medium | ✅ Fixed (2026-01-19) | Submit button validation messages now work correctly. | Verified in Scenario 15 testing. |
| **WYSIWYG: Width Not Updating in Builder** | High | ⏳ Needs Retest | Width changes may now update in builder. | Quick Test: Change any field width to 75%, verify builder updates immediately. |
| **WYSIWYG: Label Wrapping/Squashing** | Medium | ⏳ Needs Retest | Label sizing may have been fixed with UniversalFieldShell. | Quick Test: Set long label, compare builder vs preview wrapping behavior. |
| **SmartBorder Sizing Issue** | Medium | ⏳ Needs Retest | SmartBorder sizing may have been fixed. | Quick Test: Open Form 44, check Customer Type radio for excessive space. |

### Issues Fixed During Testing

| Issue | Resolution | Date |
|-------|------------|------|
| Backend schema missing numeric operators | Added `greaterThan`, `greaterThanOrEqual`, `lessThan`, `lessThanOrEqual` to `LogicOperator` enum in `backend/schemas/form_definition.py`. | 2026-01-12 |
| Contains operator not available | Added `contains` operator for dropdown, radio, and checkbox fields in frontend `ruleValidation.ts`. | 2026-01-12 |
| Logic Panel UI cramped | Redesigned logic rule cards with better layout - status/controls in top-right, rule summary on separate line with wrapping. Added tooltips for truncated names. | 2026-01-12 |
| Contains Operator Substring Bug | User corrected Rule 6 to use `equals` operator with exact values instead of `contains`. | 2026-01-12 |
| Checkbox Equals/NotEquals Bug | Fixed `evaluateRules.ts` to handle arrays correctly. `equals` now checks if array contains value, `notEquals` checks if array does NOT contain value. Case-insensitive comparison added. | 2026-01-12 |
| **Security: LocalStorage Fallback on 403/404** | Fixed `useBuilderStore.ts` and `BuilderPage.tsx` to properly handle HTTP errors. 403 (Access Denied) and 404 (Not Found) now show dedicated error pages instead of falling back to localStorage. This prevents unauthorized access on shared workstations. **LocalStorage is preserved** for other users who may have legitimate access and unsaved work. Network errors and 5xx still allow offline fallback. Version system handles conflicts when authorized users reconnect. | 2026-01-12 |
| **ReferenceError: actualStr is not defined** | Fixed `evaluateRules.ts` - moved numeric comparison logic inside the `else` block where `actualStr` is defined. Added explicit handling for arrays with numeric operators (returns `false`). This bug was introduced when adding array handling for checkbox components. | 2026-01-12 |

### Template D Progress Summary

| Step | Description | Status |
|------|-------------|--------|
| 1 | Header Component | ⬜ SKIPPED (component not available) |
| 2 | Paragraph Component | ⬜ SKIPPED (component not available) |
| 3 | Customer Type Radio | ✅ PASSED |
| 4 | Company Name Field | ✅ PASSED |
| 5 | Satisfaction Rating Select | ✅ PASSED |
| 6 | Reason for Rating Textarea | 🟡 PARTIAL (missing properties) |
| 7 | Would Recommend Radio | ✅ PASSED |
| 8 | Referral Name Field | 🔴 FAILED (optionsDirection bug) |
| 9 | Contact Preference Checkbox | ✅ PASSED |
| 10 | Preferred Contact Email | ✅ PASSED |
| 11 | Preferred Contact Phone | ✅ PASSED |
| 12 | Additional Comments Textarea | 🟡 PARTIAL (missing properties) |

### Template C Step 17 Logic Rules Progress

| Rule | Description | Status |
|------|-------------|--------|
| 1 | Show Other Event Type when Event Type = "Other" | ✅ PASSED |
| 2 | Require Company Name when Number of Attendees > 10 | ✅ PASSED (after fix) |
| 3 | Enable Allergy Information when Dietary = Vegetarian/Vegan | 🟡 BLOCKED (cannot test - no initial disabled state) |

### Template D Logic Rules Analysis (Form 44)

**Rules 1-3 (Customer Type → Company Name):** ✅ PASSED

**Rules 4-6 (Satisfaction Rating → Reason):** 🔴 CRITICAL BUG

| Rule | Configured Operator/Value | Issue |
|------|---------------------------|-------|
| 4 | `equals: "dissatisfied"` | ✅ Correct |
| 5 | `equals: "very_dissatisfied"` | ✅ Correct (note: actual value is `very_dissatisfied` not `very-dissatisfied`) |
| 6 | `contains: "satisfied"` | 🔴 **BUG: Matches "very_dissatisfied" because it contains substring "satisfied"** |

**Root Cause:** Rule 6 uses `contains: "satisfied"` which inadvertently matches:
- `very_satisfied` ✓
- `satisfied` ✓
- `very_dissatisfied` ✓ (contains "satisfied"!)

This causes the "random" behavior observed during UAT - when selecting "Very Dissatisfied", Rule 6 fires (hide) conflicting with Rules 4-5 (require).

**Fix Required:** Replace Rule 6 with two separate rules using `equals`:
- Rule 6a: `equals: "very_satisfied"` → hide
- Rule 6b: `equals: "satisfied"` → hide

**Rules 7-8 (Would Recommend → Referral Name):** ✅ PASSED

**Rules 9-12 (Contact Preference Checkbox → Email/Phone):** 🔴 CRITICAL BUG

| Rule | Configured Operator/Value | Issue |
|------|---------------------------|-------|
| 9 | `contains: "email"` | ✅ Should work for arrays |
| 10 | `notEquals: "email"` | 🔴 **BUG: For checkbox arrays, this always returns true** |
| 11 | `equals: "phone"` | 🔴 **BUG: Only matches if ONLY "phone" is selected, not multi-select** |
| 12 | `equals: "sms"` | 🔴 **BUG: Same issue as rule 11** |

**Root Cause:** Checkbox components return arrays (e.g., `["email", "phone"]`). The `equals` operator compares the array to a string, which never matches unless only one item is selected. The `notEquals` operator always returns true because an array is never equal to a string.

**Fix Required:** 
- For checkbox rules, always use `contains` operator to check if a value is in the selected array
- The `notEquals` operator should be changed to "isEmpty" or a new "doesNotContain" operator is needed

### UAT Recommendations

1. **For dropdown/select fields:** Do NOT use `contains` with partial value strings. Use `equals` with exact values.
2. **For checkbox fields:** Only use `contains` operator. The `equals` and `notEquals` operators don't work correctly for multi-select arrays.
3. **Contains operator behavior:** Currently does substring matching on the value. For dropdowns, this should probably be exact value matching instead.

---

## 📊 Builder vs Preview Comparison Report (Form 44)

**Date:** 2026-01-12
**Method:** Automated extraction via Chrome DevTools MCP

### Component Style Comparison

| Component | Property | Stored (JSON) | Builder | Preview | Status |
|-----------|----------|---------------|---------|---------|--------|
| **Company Name** | inputWidthOverride | 578px | 511px (88% scale) | 238px | 🔴 **BUG** |
| | Height | 40px | 35px (88% scale) | 40px | ✅ Match |
| | Font Family | Inter | Inter | Inter | ✅ Match |
| | Border Color | #9CA3AF | rgb(156,163,175) | rgb(156,163,175) | ✅ Match |
| **Reason for Your Rating** | inputWidthOverride | 659px | 582px (88% scale) | 659px | ✅ Match |
| | Height | 40px | 35px (88% scale) | 40px | ✅ Match |
| | Font Family | Inter | Inter | Inter | ✅ Match |
| **Overall Satisfaction Rating** | Width | default | 176px | 199px | ✅ Match (scaled) |
| | Height | 40px | 35px | 40px | ✅ Match |
| **Preferred Contact Email** | Width | default | 178px | 201px | ✅ Match (scaled) |
| | Border Color | #3B82F6 | rgb(59,130,246) | rgb(59,130,246) | ✅ Match |
| **Preferred Contact Phone** | Width | default | 178px | 201px | ✅ Match (scaled) |
| **Additional Comments** | inputWidthOverride | 466px | 412px (88% scale) | 466px | ✅ Match |
| | Height | 110px | 97px (88% scale) | 110px | ✅ Match |
| **All inputs** | Font Family | Inter | Inter | Inter | ✅ Match |
| **All inputs** | Font Weight | 400 | 400 | 400 | ✅ Match |
| **All inputs** | Text Color | #1F2937 | rgb(31,41,55) | rgb(31,41,55) | ✅ Match |

### Analysis

**✅ Matching Properties:**
- Font family (Inter) consistent across all components
- Font sizes (14px/15px) consistent
- Font weights (400/500) consistent
- Text colors matching
- Border colors matching for styled components (e.g., email with blue border)
- Logic rules correctly showing/hiding Company Name and Referral Name
- Most `inputWidthOverride` values correctly applied (Reason for Rating, Additional Comments)

**🔴 Critical Bug Found: Text Component Width**

| Component | Type | inputWidthOverride | Preview Width | Status |
|-----------|------|-------------------|---------------|--------|
| Company Name | `text` | 578px | 238px | 🔴 Bug |
| Reason for Rating | `textarea` | 659px | 659px | ✅ Match |
| Additional Comments | `textarea` | 466px | 466px | ✅ Match |
| Preferred Contact Email | `email` | (default) | 201px | ✅ OK |
| Preferred Contact Phone | `phone` | (default) | 201px | ✅ OK |

The bug is **specific to the `text` component type**. Company Name (`text`) has `inputWidthOverride: 578` but renders at only **238px (58% smaller)**. Meanwhile, `textarea`, `email`, and `phone` components correctly apply their widths.

**Root Cause Hypothesis:** The public renderer (`PublicFormArtboard.tsx` or related) may not be reading or applying `inputWidthOverride` for `text` type components, while other component types handle it correctly.

**Fix Required:** Investigate the `text` component rendering path in the public form renderer.

**🟡 Scaling Explanation (Non-Bug):**
The Builder canvas was displayed at **88% zoom** during capture. Size differences between Builder measurements and Preview are consistent with this scaling factor:
- Builder 35px height × (1/0.88) ≈ 40px (matches Preview)
- This is expected behavior, not a bug

### Conclusion

**WYSIWYG Status: 🟡 PARTIAL PASS**

The comparison confirms:
1. ✅ **Typography is preserved exactly** (font family, size, weight, color)
2. ✅ **Border styling is preserved** (colors, widths)
3. ✅ **Logic rules are executing correctly** (Company Name shows when Corporate selected)
4. ✅ **Most component widths correctly applied** (Reason for Rating, Additional Comments)
5. 🔴 **Company Name inputWidthOverride NOT applied** - renders at 238px instead of stored 578px

**Action Required:** Fix the `inputWidthOverride` property application for text components in the public renderer (`PublicFormArtboard.tsx` or related components).

---

## 🔐 Scenario 4 Detailed Findings - Access Control UX Gaps (2026-01-13)

### Test Summary

**Scenario:** Permission/access + validation errors are safe and user-visible  
**Test User:** user1@test.com (Company User role, same company as user2@test.com who is Company Admin)  
**Test Form:** Form 44  
**Result:** 🟡 PARTIAL PASS - Security controls work but significant UX gaps identified

### Issues Identified

#### Issue 1: Dashboard Doesn't Allow VIEW Access Users to Open Forms in Builder
**Description:** Users with VIEW access can only see the Form Header (View icon) on the dashboard. They cannot access the form builder to inspect the form design.  
**Expected:** VIEW access users should be able to open forms in the builder in a read-only/view-only mode.  
**Impact:** Users cannot inspect form structure without EDIT access.

#### Issue 2: Builder Access Controls Don't Align with Dashboard
**Description:** Direct URL access (`/forms/44/builder`) allows opening the form even when the dashboard doesn't show the Design icon.  
**Expected:** Consistent behavior - if dashboard doesn't show Design icon, direct URL should also apply same access restrictions.  
**Impact:** Confusing UX; users might discover they can access via URL but not via dashboard.

#### Issue 3: No Indication of View-Only Access in Builder
**Description:** When user1 (Company User with VIEW access) opened form 44 via direct URL, there was no indication that they couldn't save. They could make changes to the form but only discovered the restriction when attempting to save.  
**Error Shown:** "Access denied: You have VIEW access, but EDIT is required"  
**Expected:** Clear visual indicator at the top of the builder: "🔒 View Only - You do not have permission to edit this form"  
**Impact:** Users may invest significant time making changes before discovering they can't save.

#### Issue 4: Public Preview Access Question
**Question:** Should VIEW access users be blocked from Public Preview?  
**Decision:** No - VIEW access should allow preview. The purpose of VIEW is to inspect the form.

### Root Cause Analysis

The current architecture has separate access checks at different layers:
1. **Dashboard** - Controls which icons appear per form
2. **Builder API** - Controls save operations
3. **Builder UI** - No access awareness; assumes edit capability

This creates inconsistent UX where:
- Dashboard restricts VIEW users from seeing Design icon
- Builder route doesn't check access before loading
- User discovers restriction only at save time

### Resolution: Unified Form Workspace Specification

A comprehensive specification has been created to address these issues:

**Document:** `docs/stories/UNIFIED-FORM-WORKSPACE-SPECIFICATION.md`

**Key Features:**
1. **Unified Form Workspace** - Tabbed interface consolidating all form functions
2. **Access-Aware UI** - Tabs and features adapt to user's access level
3. **View-Only Mode** - Design tab with selection enabled but editing disabled
4. **Access Check on Load** - API check determines mode before rendering
5. **Dashboard Integration** - Enhanced form cards with clickable zones

**Access Level → Tab Visibility Matrix:**

| Tab | VIEW | SUBMIT | ANALYZE | EDIT | MANAGE |
|-----|------|--------|---------|------|--------|
| 📋 Overview | ✅ | ✅ | ✅ | ✅ | ✅ |
| 🎨 Design | ✅ View-only | ✅ View-only | ✅ View-only | ✅ Full | ✅ Full |
| ⚙️ Settings | ❌ | ❌ | ❌ | ✅ | ✅ |
| 🔐 Access | ❌ | ❌ | ❌ | ❌ | ✅ |
| 📊 Analytics | ❌ | ❌ | ✅ | ❌ | ✅ |

**View-Only Mode Features:**
- Toolbox (component palette) hidden
- Component selection enabled (to view properties)
- Resize/drag handles disabled
- Properties panel shows values but inputs disabled
- Save button hidden
- Preview button functional
- Clear "🔒 View Only" banner displayed
Ready to Start T04
### Related Documentation Updates

The following documents have been updated:
1. `docs/ACCESS-CONTROL-MATRIX.md` - Added "Form Workspace Tab Access Matrix" section
2. `docs/stories/UNIFIED-FORM-WORKSPACE-SPECIFICATION.md` - Complete feature specification

### Next Steps

1. Create new story based on the Unified Form Workspace Specification
2. Implement in phases as outlined in the specification
3. Re-test Scenario 4 after implementation

---

## 📋 Scenario 15 Detailed Findings - Submit Button Validation (2026-01-13)

### Issue Description

The Submit button does not display validation messages when the form has validation errors. Users only see error messages on individual components but receive no feedback on the submit button itself.

### Test Scenario

1. Form has 3 required fields
2. User fills in 1 field (leaving 2 empty)
3. User clicks Submit
4. **Expected:** Submit button shows message like "2 required fields need attention"
5. **Actual:** Submit button shows no message; only individual component errors appear

### Proposed Solution

**Aggregate Validation Message Display:**

1. On submit, collect all validation errors from visible required components
2. Sort errors by component `tabOrder` (sort order)
3. Display the **first** error message on the submit button
4. As user corrects errors, refresh the list and show next first error
5. When all errors cleared, allow submission

**Component Design Consideration:**
- Submit button validation area has space for 1 message
- Show first error only (by sort order)
- Message format: "{fieldLabel} is required" or count: "2 fields require attention"

**Prerequisite:**
- Components need proper `tabOrder` values (currently defaults to 0)
- May need to enforce or auto-assign tabOrder

### Technical Notes

- Validation errors are currently tracked per-component in `allFormErrors` map
- Submit button component needs access to this map
- Sort by `tabOrder` to show errors in logical form order
- Consider adding a summary mode: "2 of 3 required fields need attention"

---

## 📋 Scenario 20 Detailed Findings - WYSIWYG Style Issues (2026-01-13)

**Retest Update (2026-01-15):** All Scenario 20 tests passed. Issues below appear resolved with the grid layout changes.

### Issues Identified

#### Issue 1: Width Not Updating in Builder

**Description:** Changing `Appearance → Dimensions → Width` (e.g., to 75%) does not visually update the component in the builder canvas, but the change IS applied correctly in preview.

**Impact:** Builder is not WYSIWYG - users cannot see their layout changes until they preview.

**Root Cause (Suspected):** The width property may be applied only to the runtime renderer, not the builder canvas surface.

**Fix Required:** Ensure `componentWidth` property is applied on both canvas and runtime surfaces.

#### Issue 2: Label Wrapping Difference

**Description:** Company Name component shows label on one line in builder but wraps to 2 lines in preview.

**Builder View:**
- Label: "Company Name" on single line
- Input: Wide input field (815px as shown in builder)

**Preview View:**
- Label: "Company Name" wrapped to 2 lines ("Company" / "Name")
- Input: Appears narrower

**Screenshots Provided:** User provided comparison screenshots showing the discrepancy.

**Root Cause (Suspected):** 
- Label width calculation differs between builder and runtime
- Horizontal layout with `labelWidth` may not be respected in runtime
- OR the container width is constraining the label differently

#### Issue 3: SmartBorder Sizing for Radio Component

**Description:** Customer Type radio component (`radio-1768184158033-653`) has excessive whitespace next to the radio option values. The SmartBorder appears wider than the content requires.

**Form:** Form 44 (Template D)

**Observation:** Component was originally correct but after testing, SmartBorder became wider and cannot be recovered.

**Root Cause (Suspected):**
- SmartBorder may be including the validation message area width in its calculation
- Or a property change caused the border to expand and not recalculate

### Recommended Investigation

1. **Width Property:** Trace `componentWidth` from Properties Panel → Zustand store → Canvas renderer → Runtime renderer
2. **Label Width:** Compare `labelWidth` calculation in `UniversalFieldShell` between canvas and runtime modes
3. **SmartBorder:** Check SmartBorder calculation in `objectRenderers.tsx` for radio components - may be using incorrect container width

### Related Components

- `frontend/src/features/builder/components/properties/DimensionsSection.tsx`
- `frontend/src/features/builder/components/UniversalFieldShell.tsx`
- `frontend/src/features/builder/utils/objectRenderers.tsx`
- `frontend/src/features/builder/components/SmartBorder.tsx` (if exists)

---

## Future Enhancements (For Next Story)

### Smart LocalStorage Version Reconciliation

**Background:** During UAT testing, we discovered that the form builder silently fell back to localStorage when access was denied (403). This has been fixed to show proper error messages. However, there's an opportunity to improve the localStorage/database version reconciliation experience.

**Current Behavior:**
- Form loads from API if available
- Falls back to localStorage only on network errors or server errors (5xx)
- Version system handles saving but doesn't proactively compare timestamps

**Proposed Enhancement:**

When a user opens a form:

1. **Fetch latest version from API** with `updatedAt` timestamp
2. **Check localStorage** for this form and its `lastModified` timestamp
3. **Compare timestamps** and show appropriate prompts:

| Scenario | Prompt |
|----------|--------|
| **LocalStorage is newer** | "You have unsaved local changes from [date]. Continue editing local version or load server version?" |
| **Database is newer** | "A newer version exists on the server (saved [date]). Load latest or continue with your local version?" |
| **Same timestamp** | Load normally, no prompt |

4. **If user chooses local version:**
   - Save as new version automatically
   - Show notification: "Your local changes have been saved as Version X"

5. **Version numbering intelligence:**
   - If local changes are from before the latest DB version, insert as appropriate version number
   - Or simply save as latest draft with clear audit trail

**Benefits:**
- Prevents data loss from multi-device editing
- Clear user control over version conflicts
- Maintains audit trail through version system
- Supports offline-first workflows

**Priority:** Medium (UX improvement, not blocking)

**Estimated Effort:** 1-2 story points

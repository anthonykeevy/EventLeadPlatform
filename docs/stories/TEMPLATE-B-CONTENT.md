#### Template B — Logic-Enabled Form (Runtime Rules Testing)

**Use Case:** A product team needs a simple form to test all logic rule actions (show/hide, enable/disable, require/unrequire) work correctly. This form uses a single source field to trigger multiple target fields, testing each action type systematically.

**Step-by-Step Build Instructions:**

**Step 1: Configure Canvas Settings**
- Open form builder for new form
- Set `canvasSettings.width`: 800
- Set `canvasSettings.height`: 700
- Set `canvasSettings.backgroundColor`: "#FFFFFF" (white)
- Verify canvas dimensions display correctly

**Step 2: Add Header Component**
- Drag **Header** component to canvas at position (100, 50)
- Set `label`: "Logic Rules Test Form"
- Set `styleOverrides.labelFontSize`: 24
- Set `styleOverrides.labelFontWeight`: 700
- Set `styleOverrides.labelColor`: "#111827"

**Step 3: Add Paragraph Component**
- Drag **Paragraph** component to canvas at position (100, 100)
- Set `label`: "Select 'Yes' or 'No' below to test logic rules. Each target field will respond differently."
- Set `styleOverrides.helpTextFontSize`: 14
- Set `styleOverrides.helpTextColor`: "#6B7280"

**Step 4: Add Field A - Source Field (Select)**
- Drag **Select** component to canvas at position (100, 180)
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


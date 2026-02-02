# DefinitionJSON Save Checklist (UAT Style)

Purpose: Ensure DefinitionJSON saved from the Builder is complete for production data capture (exportable field names, validation, options, and required props) and passes backend schema validation.

Sources:
- Backend validation contract: `backend/schemas/form_definition.py`
- Builder authoring shape: `frontend/src/features/builder/types/builder.types.ts`
- Component props + structure: `docs/COMPONENT-FRAMEWORK-REFERENCE.md`
- Persistence acceptance criteria: `docs/stories/story-3.9.md`
- UAT flow template: `docs/stories/STORY-3.8-3.9-UAT-TEST-GUIDE.md`

---

## A) UAT Checklist: Save DefinitionJSON

### Progress (live)
- Scenario 1: Passed
- Scenario 2: Passed
- Scenario 3: Passed
- Scenario 4: Passed
- Scenario 5: Passed
- Scenario 6: Passed
- Section B: Passed (DefinitionJSON fields present)
- Section C: Passed
- Section D: Passed

### Scenario 1: Save Draft persists DefinitionJSON (baseline)
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open `/forms/:formId/builder` for a form you can edit. | Builder loads the latest definition from DB (not a mock template). |
| 2 | Change a visible label on a field. | UI updates immediately. |
| 3 | Click **Save**. | Save succeeds (no validation error). |
| 4 | Hard refresh the builder. | The label persists (DefinitionJSON saved). |

### Scenario 2: Data‑capture fields persist (exportable)
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Select a text field. Set `exportName`, enable `required`, and add a validation rule (e.g., min length). | UI shows updated state. |
| 2 | Click **Save**. | Save succeeds. |
| 3 | Reload builder. | `exportName`, `required`, and validation are preserved. |

### Scenario 3: Options + defaults persist (selection fields)
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Add a dropdown or radio component. Configure options + default value. | Options appear in UI. |
| 2 | Click **Save**. | Save succeeds. |
| 3 | Reload builder. | Options + defaults persist in DefinitionJSON. |

### Scenario 4: Logic rules persist (if used)
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Add a simple rule in Logic Panel (IF field A equals value THEN show field B). | Rule appears in list. |
| 2 | Click **Save**. | Save succeeds. |
| 3 | Reload builder. | Rule persists under `logic.rules`. |

### Scenario 5: Canvas settings + positions persist
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Move a component to a new position. | Component position changes. |
| 2 | Click **Save**. | Save succeeds. |
| 3 | Reload builder. | Component position persists (absolute `x/y`). |

### Scenario 6: Backend validation guardrails
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Remove label from an input component (text/number/etc.). | UI should prevent or warn. |
| 2 | Attempt **Save**. | Save succeeds; label can be empty for inputs. |

---

## B) DefinitionJSON Required Shape (Backend Contract)

Top‑level required fields:
- `schemaVersion` (must be `"1.0"`)
- `formId` (non-empty string)
- `theme` (`primaryColor`, `backgroundColor`, `fontFamily`)
- `pages[]` with `FormPage.id` and `components[]`
- Optional: `logic.rules[]`

Component required fields:
- `id` (unique across entire form)
- `type` (must be one of builder component types)
- `props` (object; extra fields allowed)

Label requirement:
- `props.label` is **required** for input‑like types:
  `text`, `number`, `select`, `dropdown`, `date`, `checkbox`, `radio`, `textarea`, `email`, `phone`, `address`, `first-name`
- `props.label` **optional** for: `submit-button`, `header`, `divider`, `terms`

---

## C) Component Save Checklist (Data‑Capture Focus)

### Common to all components
- `id` (unique string)
- `type`
- `position`: `{ x, y }`
- `props.exportName` (for data capture/export; required for production)
- `props.required` (boolean)
- `props.validation` (rules object)
- `props.label` (required for input types)
- `props.helpText` / `props.validationMessage` (if used)
- `props.styleOverrides`, `objectLayout`, `layoutGroups` (optional, layout/styling)

### Text / Textarea / First‑Name
- `props.placeholder`
- `props.validation` (min/max length, pattern, etc.)
- `props.defaultValue` (if supported)

### Number
- `props.validation` (min/max value, step, integerOnly, etc.)

### Email / Phone
- `props.validation` (email/phone rules, domain filters)

### Dropdown (Select)
- `props.options[]` (label, value, disabled?, group?, hasExtraText?)
- `props.defaultValue`
- `props.optionsDirection` (if exposed)
- `props.extraTextValidation` / `extraTextValidationMessage` (if using “extra text” options)

### Radio
- `props.options[]`
- `props.defaultValue`
- `props.optionsDirection`

### Checkbox
- `props.options[]`
- `props.defaultChecked[]`
- `props.optionsDirection`
- `props.exportMode` / `exportSeparator` (if exporting multiple values)

### Date
- `props.validation` (min/max date, past/future only, range rules)
- `props.defaultValue` (if used)

### Terms
- `props.termsUrl` / `props.termsContent`
- `props.termsLinkText`
- `props.required`

### Submit Button
- `props.buttonText`
- `props.buttonAction`
- `props.buttonWidth`, `props.buttonAlign`
- `props.showLoadingState`, `props.disableUntilValid`, `props.showIcon`

### Header / Divider
- `props.label` (header text, if used)
- `props.width` / `props.componentScale`
- `props.styleOverrides` (for divider styles)

---

## D) Production “Must‑Have” Field Checklist

To recreate the form in production with correct data capture:
- **Every input component** has `exportName`, `label`, `required`, and `validation`.
- **Every selection component** has `options[]` + default values.
- **Every form** has `theme`, `pages[]`, `components[]`, and `position` for each component.
- **All IDs unique**.
- **Save passes backend validation** (no missing required fields for input components).


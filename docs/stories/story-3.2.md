# Story 3.2: JSON Schema Definition

**Epic:** 3 - Form Builder & Logic Engine
**Domain:** Schema & Versioning
**Status:** ✅ Complete
**Priority:** High

---

## 📖 User Story

**As a** Developer (and System Architect),
**I want to** define a strict JSON Schema (Pydantic/Zod) for the Form Definition,
**So that** the system prevents invalid or corrupt form configurations from being saved to the database, ensuring the Renderer always receives a valid contract.

---

## ✅ Acceptance Criteria

### 1. Backend Validation (Pydantic)
- [x] Create Pydantic models to represent the `DefinitionJSON` structure.
    - `FormDefinition` (Root)
    - `FormTheme` (Styles, Colors)
    - `FormComponent` (Polymorphic base for fields)
- [x] Implement validation in the `FormVersionService`.
    - Before saving to `FormVersion.DefinitionJSON`, parse the input against the Pydantic model.
    - Raise a clear `ValidationError` (400 Bad Request) if the structure is invalid.
- [x] **Component Schema:**
    - Must support standard fields: `id` (UUID/String), `type` (Enum/String), `props` (Dict).
    - `props` should validate common attributes: `label`, `required`, `placeholder`.
    - Support nested structures if necessary (e.g., containers), though a flat list is preferred for V1.

### 2. Frontend Type Safety (Zod)
- [x] Define the equivalent Zod schema in the frontend codebase (shared types if possible, or manually aligned).
- [x] Ensure the Builder UI exports data matching this schema.

### 3. Schema Structure
- [x] **Root Object:**
    - `id` (Form ID)
    - `version` (Schema Version, e.g., "1.0")
    - `theme` (Object)
    - `pages` (Array) or `components` (Array) - *Decision: Support multi-page structure? Yes, likely needed for complex forms. Let's go with `pages` array containing `components`.*
- [x] **Theme Object:**
    - `primaryColor`, `backgroundColor`, `fontFamily`.
- [x] **Component Object:**
    - `id` (unique key)
    - `type` (e.g., 'text', 'number', 'select', 'date')
    - `props` (validation rules, labels, defaults)

### 4. Testing
- [x] Unit tests for the Pydantic models (valid vs. invalid payloads).
- [x] Integration test ensuring the API rejects bad JSON.

---

## 🛠️ Technical Notes

- **Library:** `pydantic` (v2 preferred).
- **Polymorphism:** Use `Union` or `Annotated` with `Discriminator` for the `components` list if we want strict prop validation per type. For V1, a generic `props: Dict[str, Any]` might be sufficient, but strict typing is better.
    - *Recommendation:* Use `type` field as the discriminator.
- **Versioning:** Include a `schemaVersion` field in the JSON to handle future migrations of the JSON structure itself.

### Proposed JSON Structure
```json
{
  "schemaVersion": "1.0",
  "formId": "...",
  "theme": {
    "primaryColor": "#000000"
  },
  "pages": [
    {
      "id": "page-1",
      "title": "Personal Info",
      "components": [
        {
          "id": "comp-1",
          "type": "text",
          "props": {
            "label": "First Name",
            "required": true
          }
        }
      ]
    }
  ]
}
```

### Pydantic Model Sketch
```python
class ComponentProps(BaseModel):
    label: str
    required: bool = False
    # ... other common props

class FormComponent(BaseModel):
    id: str
    type: str  # Literal['text', 'select', ...]
    props: ComponentProps # or Union based on type

class FormPage(BaseModel):
    id: str
    components: List[FormComponent]

class FormDefinition(BaseModel):
    schemaVersion: str = "1.0"
    pages: List[FormPage]
    # ...
```

---

## 📋 Completion Report

### Implementation Summary
- **Pydantic Models:** Implemented in `backend/schemas/form_definition.py`. Supports `schemaVersion`, `theme`, `pages`, `components` and polymorphic types.
- **Strict Validation:** 
    - Implemented unique ID checking across the entire form structure.
    - Enforced `schemaVersion` as "1.0".
    - Validated component types against a strictly defined Enum.
- **Service Integration:** Updated `FormVersionService` to run validation before saving any Draft.
- **Error Handling:** Implemented `validation_service.py` to catch Pydantic errors and return clean 400 Bad Request messages.

### Artifacts Created
- `backend/schemas/form_definition.py`
- `backend/modules/forms/validation_service.py`

### Test Results
All UAT scenarios passed:
- [x] Valid Complete Schema (Happy Path)
- [x] Reject Invalid Root Structure (Missing Pages)
- [x] Reject Malformed Component (Missing ID/Type)
- [x] Enforce Schema Versioning
- [x] Reject Unknown Component Type

---

## 🧪 UAT Test Guide

*(See full guide in `docs/stories/STORY-3.2-UAT-TEST-GUIDE.md`)*

# Story 3.2 UAT Test Guide: JSON Schema Validation

**Story:** [3.2 - JSON Schema Definition](story-3.2.md)  
**Epic:** 3 - Form Builder & Logic Engine  
**Status:** ✅ Complete  
**Focus:** Backend Validation (Pydantic) & Schema Integrity  

---

## 📋 Pre-requisites

1.  **Environment:**
    - Backend API is running (`uvicorn backend.main:app`).
    - Database is accessible.
    - A test Form exists in the DB (e.g., `FormID: 1`).

2.  **Tools:**
    - Swagger UI (`/docs`) or Postman.
    - `curl` or a Python test script.

3.  **State:**
    - `FormVersionService` must have the new Pydantic validation logic integrated.
    - `DefinitionJSON` column in `FormVersion` table is ready.

---

## 🧪 Test Scenarios

### Scenario 1: Validate Valid Complete Schema (Happy Path)

**Goal:** Verify that a fully formed, valid JSON definition is accepted and saved.

1.  **Step:** Send a `POST` request to `/forms/{form_id}/versions` (or the update draft endpoint) with the following `definition`:
    ```json
    {
      "schemaVersion": "1.0",
      "formId": "test-form-1",
      "theme": {
        "primaryColor": "#0055FF",
        "backgroundColor": "#FFFFFF",
        "fontFamily": "Arial"
      },
      "pages": [
        {
          "id": "page-1",
          "title": "Introduction",
          "components": [
            {
              "id": "comp-1",
              "type": "text",
              "props": {
                "label": "Full Name",
                "required": true,
                "placeholder": "Enter your name"
              }
            }
          ]
        }
      ]
    }
    ```
2.  **Expected Result:**
    - **Status:** `200 OK` (or `201 Created`).
    - **Response:** Returns the created/updated Version object.
    - **DB Verification:** `FormVersion.DefinitionJSON` contains the exact JSON payload.

**Status:** ✅ PASSED

---

### Scenario 2: Reject Invalid Root Structure

**Goal:** Verify that the schema rejects missing root-level keys.

1.  **Step:** Send a payload missing the `pages` array:
    ```json
    {
      "schemaVersion": "1.0",
      "theme": { "primaryColor": "red" }
    }
    ```
2.  **Expected Result:**
    - **Status:** `400 Bad Request` (or `422 Unprocessable Entity`).
    - **Error Message:** Should indicate that `pages` field is required.

**Status:** ✅ PASSED

---

### Scenario 3: Reject Malformed Component

**Goal:** Verify that components inside pages are validated for required fields (`id`, `type`).

1.  **Step:** Send a payload with a broken component:
    ```json
    {
      "schemaVersion": "1.0",
      "pages": [
        {
          "id": "p1",
          "components": [
            {
              "id": "c1",
              "props": { "label": "Missing Type" }
            }
          ]
        }
      ]
    }
    ```
2.  **Expected Result:**
    - **Status:** `400 Bad Request`.
    - **Error Message:** Should indicate validation error for `type` field in component.

**Status:** ✅ PASSED

---

### Scenario 4: Enforce Schema Versioning

**Goal:** Ensure `schemaVersion` is required to handle future migrations.

1.  **Step:** Send a payload missing `schemaVersion`:
    ```json
    {
      "pages": []
    }
    ```
2.  **Expected Result:**
    - **Status:** `400 Bad Request`.
    - **Error Message:** `Field required: schemaVersion`.

**Status:** ✅ PASSED

---

### Scenario 5: Edge Case - Unknown Component Type

**Goal:** Verify behavior when an unknown component type is provided.
*Note: Depending on implementation strictness (Enum vs String), this might pass or fail. If strict Enum is used (recommended), it should fail.*

1.  **Step:** Send a payload with `type: "flux-capacitor"`:
    ```json
    {
      "schemaVersion": "1.0",
      "pages": [
        {
          "id": "p1",
          "components": [
            {
              "id": "c1",
              "type": "flux-capacitor",
              "props": {}
            }
          ]
        }
      ]
    }
    ```
2.  **Expected Result:**
    - **Status:** `400 Bad Request`.
    - **Error Message:** `Input should be 'text', 'select', 'number', ...` (or similar Enum validation error).

**Status:** ✅ PASSED

---

## 📝 Validation Checklist

- [x] **Pydantic Models:** Ensure `FormDefinition`, `FormPage`, `FormComponent` are defined.
- [x] **Service Layer:** Ensure `FormVersionService.create_version` calls `.model_validate()` or equivalent.
- [x] **Error Handling:** Ensure Pydantic `ValidationError` is caught and re-raised as an HTTP exception (400) with a clear message, not a 500 Internal Server Error.

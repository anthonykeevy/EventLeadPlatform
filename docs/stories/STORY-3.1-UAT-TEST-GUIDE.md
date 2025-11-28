# UAT Test Guide - Story 3.1: Form Versioning Architecture

**Story:** [Story 3.1: Form Versioning Architecture](story-3.1.md)  
**Epic:** 3 - Form Builder & Logic Engine  
**Status:** ✅ Complete  
**Document Owner:** QA / Dev Team  

---

## 1. Introduction

This document outlines the User Acceptance Testing (UAT) scenarios for **Story 3.1: Form Versioning Architecture**. The goal is to verify that the backend correctly handles the creation, storage, retrieval, and publishing of form schema versions, ensuring data integrity and correct version incrementing.

## 2. Prerequisites

Before executing these tests, ensure the following:

*   **Environment:** API and Database are running.
*   **Database State:**
    *   Migration for `FormVersion` table has been applied.
    *   A valid `User` exists (for `CreatedBy` fields).
    *   A valid `Form` exists (to link versions to).
*   **Tools:** Swagger UI (`/docs`) or Postman/Curl.

---

## 3. Test Scenarios

### Scenario 1: Create Initial Draft Version

**Objective:** Verify that a new version can be created for a form, starting as a DRAFT with Version 1.

| Step | Action | Input Data | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Call `POST /forms/{form_id}/versions` | `form_id`: [Existing Form ID]<br>Body: `{ "definition": { "pages": [] }, "comment": "Initial Draft" }` | **HTTP 201 Created**<br>Response includes:<br>- `versionNumber`: 1<br>- `status`: "DRAFT"<br>- `isActive`: false<br>- `definition`: matches input | ✅ PASSED |
| 2 | Query Database | `SELECT * FROM FormVersion WHERE FormID = {form_id}` | Record exists with:<br>- `VersionNumber` = 1<br>- `Status` = 'DRAFT'<br>- `IsActive` = 0 | ✅ PASSED |

### Scenario 2: Version Incrementing

**Objective:** Verify that creating subsequent versions auto-increments the version number.

| Step | Action | Input Data | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Ensure Scenario 1 is complete | (Version 1 exists) | (Proceed) | ✅ PASSED |
| 2 | Call `POST /forms/{form_id}/versions` | `form_id`: [Same Form ID]<br>Body: `{ "definition": { "pages": [...] }, "comment": "V2 Update" }` | **HTTP 201 Created**<br>Response includes:<br>- `versionNumber`: **2** (Incremented)<br>- `status`: "DRAFT"<br>- `isActive`: false | ✅ PASSED |
| 3 | Repeat Creation | Call POST again | **HTTP 201 Created**<br>Response includes:<br>- `versionNumber`: **3** | ✅ PASSED |

### Scenario 3: Publishing a Version

**Objective:** Verify that publishing a version makes it active and (conceptually) archives others.

| Step | Action | Input Data | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Identify Version 2 | `form_id`: [Same Form ID], `version`: 2 | (Target Version 2) | ✅ PASSED |
| 2 | Call `POST /forms/{form_id}/versions/2/publish` | None | **HTTP 200 OK**<br>Response confirms Version 2 is now `PUBLISHED` and `Active`. | ✅ PASSED |
| 3 | Query Database | `SELECT * FROM FormVersion WHERE FormID = {form_id}` | - Version 2: `Status`='PUBLISHED', `IsActive`=1<br>- Version 1: `IsActive`=0<br>- Version 3: `IsActive`=0 | ✅ PASSED |
| 4 | Publish Version 3 | Call Publish for Version 3 | **HTTP 200 OK** | ✅ PASSED |
| 5 | Query Database | `SELECT * FROM FormVersion WHERE FormID = {form_id}` | - Version 3: `Status`='PUBLISHED', `IsActive`=1<br>- Version 2: `Status` changed (to ARCHIVED or just IsActive=0 depending on impl), `IsActive`=0 | ✅ PASSED |

### Scenario 4: Retrieving Versions (Specific vs Active)

**Objective:** Verify API can retrieve the specific history and the current live version.

| Step | Action | Input Data | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Call `GET /forms/{form_id}/versions` | `form_id`: [Same Form ID] | **HTTP 200 OK**<br>Returns list of all versions (1, 2, 3) with their correct statuses. | ✅ PASSED |
| 2 | Call `GET /forms/{form_id}/versions/2` | `version`: 2 | **HTTP 200 OK**<br>Returns details for Version 2 specifically. | ✅ PASSED |
| 3 | Call `GET /forms/{form_id}/live` (or equivalent) | `form_id`: [Same Form ID] | **HTTP 200 OK**<br>Returns **Version 3** (The currently Published/Active one). | ✅ PASSED |

---

## 4. Edge Cases & Negative Testing

### Edge Case 1: Immutable Published Versions

**Objective:** Ensure a PUBLISHED version cannot be modified.

| Step | Action | Input Data | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Attempt Update on Published V3 | `PUT /forms/{form_id}/versions/3` | **HTTP 400/409 Error**<br>Message: "Cannot modify a published version." | ✅ PASSED |

### Edge Case 2: Retrieve Non-Existent Version

**Objective:** specific 404 handling.

| Step | Action | Input Data | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Call `GET /forms/{form_id}/versions/999` | `version`: 999 | **HTTP 404 Not Found** | ✅ PASSED |

### Edge Case 3: Invalid JSON Validation

**Objective:** Ensure the schema validation works.

| Step | Action | Input Data | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Call `POST /forms/{form_id}/versions` | Body: Invalid JSON or Missing required root keys (if defined) | **HTTP 422 Unprocessable Entity** (or 400 Bad Request) | ✅ PASSED |

---

## 5. Success Criteria

*   All CRUD operations for versions function correctly.
*   Version numbers strictly increment per form.
*   **Only one** version is `IsActive=true` at any time for a given form.
*   Published versions are protected from modification.

# Story 3.1: Form Versioning Architecture

**Epic:** 3 - Form Builder & Logic Engine
**Domain:** Schema & Versioning
**Status:** ✅ Complete
**Priority:** High

---

## 📖 User Story

**As a** Form Builder (User),
**I want to** save and retrieve different versions of my form design (Schema),
**So that** I can iterate on changes safely without breaking the live form being used by the public.

---

## ✅ Acceptance Criteria

### 1. Database Schema
- [x] Create `FormVersion` table in `dbo` schema.
- [x] Columns:
    - `FormVersionID` (PK, Identity, BigInt)
    - `FormID` (FK to `Form`, BigInt, Required)
    - `VersionNumber` (Int, Required, Ascending per Form)
    - `DefinitionJSON` (NVARCHAR(MAX), Required) - Stores the full form schema
    - `VersionComment` (NVARCHAR(500), Optional) - "Added new questions"
    - `Status` (String/Enum: 'DRAFT', 'PUBLISHED', 'ARCHIVED')
    - `IsActive` (Boolean, Default False) - Quick lookup for current live version
    - `CreatedDate`, `CreatedBy` (Audit fields)
    - `PublishedDate`, `PublishedBy` (Audit fields)

### 2. Backend Logic (Service Layer)
- [x] **Create Version:**
    - Ability to create a new version (starts as DRAFT).
    - Auto-increments `VersionNumber` based on the latest version for that `FormID`.
- [x] **Get Version:**
    - Retrieve a specific version by `FormID` + `VersionNumber`.
    - Retrieve the currently "Published" (Active) version for the Renderer.
- [x] **Publish Version:**
    - Atomically set the target version to `PUBLISHED` (and `IsActive = True`).
    - Set all other versions for that Form to `IsActive = False` (or move previous published to ARCHIVED).
- [x] **Safety:**
    - Ensure `DefinitionJSON` is valid JSON before saving.

### 3. API Endpoints
- [x] `POST /forms/{form_id}/versions` - Create new draft (copy from previous or blank).
- [x] `GET /forms/{form_id}/versions` - List history.
- [x] `GET /forms/{form_id}/versions/{version_number}` - Get specific definition.
- [x] `PUT /forms/{form_id}/versions/{version_number}` - Update draft definition.
- [x] `POST /forms/{form_id}/versions/{version_number}/publish` - Activate version.

---

## 🛠️ Technical Notes

- **Database:** SQL Server (Azure SQL).
- **ORM:** SQLAlchemy.
- **JSON Storage:** Use `NVARCHAR(MAX)` for `DefinitionJSON`. ensure the ORM handles JSON serialization/deserialization transparently if possible, or just treat as string in DB and Parse in Pydantic.
- **Concurrency:** When publishing, use a transaction to ensure only one version is Active at a time.

### Data Model Snippet
```python
class FormVersion(Base):
    __tablename__ = "FormVersion"
    FormVersionID = Column(BigInteger, primary_key=True, autoincrement=True)
    FormID = Column(BigInteger, ForeignKey("dbo.Form.FormID"), nullable=False)
    VersionNumber = Column(Integer, nullable=False)
    DefinitionJSON = Column(String(None), nullable=False) # NVARCHAR(MAX)
    # ... status, audit ...
```

---

## 📋 Completion Report

### Implementation Summary
- **Database:** Created `FormVersion` table with audit columns and proper foreign keys (Migration `030`).
- **Service:** Implemented `FormVersionService` with:
    - Atomic publishing logic (switch active flags in one transaction).
    - Version auto-incrementing.
    - Immutability checks (only DRAFT versions can be updated).
- **API:** Full CRUD endpoints implemented in `version_router.py`.
- **Testing:** Verified all scenarios via `validate_story_3_1.py` script.

### Artifacts Created
- `backend/models/form_version.py`
- `backend/migrations/versions/030_add_form_version_table.py`
- `backend/modules/forms/version_service.py`
- `backend/modules/forms/version_router.py`
- `backend/schemas/form_version.py`
- `docs/stories/STORY-3.1-UAT-TEST-GUIDE.md`

### Test Results
All UAT scenarios passed:
- [x] Creation of drafts.
- [x] Version number incrementing.
- [x] Publishing versions (Active switching).
- [x] Updating drafts.
- [x] Blocking updates to published versions.

---

## 🧪 UAT Test Guide

*(See full guide in `docs/stories/STORY-3.1-UAT-TEST-GUIDE.md`)*

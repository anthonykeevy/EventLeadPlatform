# Lessons Learned — Story 5.2

This file is updated after each task retro.

---

## Entries

### T01 — Database Form Defaults + Component Catalog (2026-02-14)

**Pattern: MSSQL migrations — use mssql.NVARCHAR**

- **Fixed-length strings:** `mssql.NVARCHAR(length=N)` — produces NVARCHAR(N).
- **MAX-length strings:** `mssql.NVARCHAR(length=None)` — produces NVARCHAR(MAX).
- **Avoid:** `sa.Text()` (→ VARCHAR(MAX)), `sa.NVARCHAR` (may not render same as mssql.NVARCHAR for DDL).
- **Reference:** `backend/migrations/versions/036_kb_knowledge_base.py`, `038_asset_metadata_tables.py`.
- **Source:** T01 retro; VARCHAR columns discovered at UAT; fix applied per existing pattern.

---

### (Previous entries above)

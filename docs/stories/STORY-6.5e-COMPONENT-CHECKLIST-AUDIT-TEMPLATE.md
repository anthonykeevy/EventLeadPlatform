# Story 6.x — Component Checklist Audit (AC-4 matrix)

**Use when:** Story adds or changes any `FormBuilderComponent` row.  
**Reference:** `docs/workflows/ADD-COMPONENT-TO-PLATFORM-CHECKLIST.md` (target v1.3).

Copy this table into `STORY-6.x-CLOSEOUT-REPORT.md` § "Component checklist audit" and mark each cell **Done** / **N/A** / **Deferred** with evidence link.

---

## Per-component matrix

| ComponentCode | §0 Scope | §0a/0b EDF | §1 ref.ComponentType | §2 catalog row | §3 renderer | §4 four-consumer | §5 validation/export | §6 prompt | §7 tests | UAT submit JSON |
|---------------|----------|------------|----------------------|----------------|-------------|------------------|---------------------|-----------|----------|-----------------|
| *(example)* `rating` | Done | N/A | Done | Done | Done | Done | Done | Done | Done | Done — FormSubmission #___ |

| | | | | | | | | | | |

---

## Automation gates (story-level)

| Gate | Command | Result |
|------|---------|--------|
| Four-consumer alignment | `python backend/scripts/verify_component_catalog_alignment.py` | |
| EDF props wired (if EDF touched) | `python backend/scripts/verify_edf_props_wired.py` | |

---

*Template introduced Story 6.5e-vision Track 0 (AC-T0-3).*

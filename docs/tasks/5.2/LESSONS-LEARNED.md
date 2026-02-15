# Lessons Learned — Story 5.2

This file is updated after each task retro.

---

## Entries

### T05 (2026-02-15): Builder Init API + Inherit/Override UX

- **Graceful degradation:** Form Builder Init API client returns `null` on 404/5xx; Builder falls back to hardcoded defaults. Enables T05 to merge before T03.
- **Type alignment:** When passing GlobalStyles to generic API payload (Record<string, unknown>), use type assertion to avoid TS2322.
- **Toolbox from Init:** Filter ComponentRegistry by `initComponents[].componentCode` when API provides catalog; otherwise show full registry.

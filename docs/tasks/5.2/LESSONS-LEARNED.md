# Lessons Learned — Story 5.2

This file is updated after each task retro.

---

## Entries

### T05 (2026-02-15): Builder Init API + Inherit/Override UX

- **Graceful degradation:** Form Builder Init API client returns `null` on 404/5xx; Builder falls back to hardcoded defaults. Enables T05 to merge before T03.
- **Type alignment:** When passing GlobalStyles to generic API payload (Record<string, unknown>), use type assertion to avoid TS2322.
- **Toolbox from Init:** Filter ComponentRegistry by `initComponents[].componentCode` when API provides catalog; otherwise show full registry.

### T06 (2026-02-15): Resolver — Apply Defaults in Renderer

- **Symmetric logic:** Backend `resolve_definition_for_render` and frontend `resolveDefinitionForRender` use identical merge order (Global → Company → Form) for preview/public parity.
- **Type assertions:** FormTheme/GlobalStyles/CanvasSettings require `as unknown as T` when merging Record<string, unknown>; TS strict overlap check rejects direct cast.
- **Fallback on missing Global defaults:** Public form API returns raw definition when `resolve_merged_defaults` raises ValueError (e.g. migration 039 not run).

### T07 (2026-02-16): Builder Defaults on New Form + Save to Company Defaults

- **formContext from companyId alone:** Set formContext whenever companyId exists; Init API only when eventId present. Enables Save to Company Defaults for forms with company context but null eventId (e.g. event creation flow).
- **Logic engine value extraction:** Radio/dropdown/checkbox emit `{value}` or `{values}`; evaluateRules must extract logical value before string comparison. JSON.stringify caused rules to fail (e.g. "yes" vs `'{"value":"yes","extraTextByValue":{}}'`).
- **Integration task scope:** When prior task (T05) delivers core UX, integration task can focus on edge cases; minimal code change expected.
- **Logic rules regression:** Add UAT step for forms with radio/dropdown + logic rules; add unit tests for evaluateRules with compound value payloads.

**Links:**
- Completion: T07-builder-defaults-new-form-save-company.completion.md
- UAT: T07-builder-defaults-new-form-save-company.uat-results.md
- Retro: T07-builder-defaults-new-form-save-company.retro.md

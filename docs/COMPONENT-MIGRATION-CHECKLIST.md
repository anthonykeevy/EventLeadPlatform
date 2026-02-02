# Component Migration Checklist (UniversalFieldShell + Surface Capabilities)

This document is a **working checklist** to ensure every component:

- Uses **`UniversalFieldShell`** (single rendering contract)
- Is wired to **`componentSurfaceCapabilities`** (toolbox/canvas/runtime behavior is explicit + consistent)

Authoritative source files:
- `frontend/src/features/builder/registry/ComponentRegistry.tsx` (component list)
- `frontend/src/features/builder/utils/componentSurfaceCapabilities.ts` (surface capability truth table)

---

## Component list (from `ComponentRegistry`)

### Input
- `first-name`
- `text`
- `number`
- `email`
- `textarea`
- `dropdown`
- `date`
- `checkbox`
- `radio`
- `phone`
- `address`
- `terms`
- `submit-button`

### Display
- `header`
- `divider`

---

## Checklist template (apply to every component)

### A) UniversalFieldShell-only
- [ ] `ComponentRegistry[type].structure` exists and is correct
- [ ] Toolbox preview uses **UniversalFieldShell** (no bespoke `previewComponent` rendering)
- [ ] Canvas uses **UniversalFieldShell** (no bespoke canvas branch)
- [ ] Preview/Production uses **UniversalFieldShell** (no `FieldShell` runtime)
- [ ] No remaining `FieldShell` usage for this component
- [ ] No remaining special-case rendering in `SortableComponent` for this type (beyond generic infra)

### B) componentSurfaceCapabilities wired
- [ ] Rendering reads surface behavior from `componentSurfaceCapabilities`
- [ ] Toolbox surface validated (compact; no crowded aids)
- [ ] Canvas surface validated (builder sizing aids where intended)
- [ ] Runtime surface validated (production parity; no builder aids)

---

## Surface capabilities matrix (current intended settings)

Legend:
- **TLI** = Text Length Indicator
- **TLI(bar/label/lines)** = show bar / show label / show textarea line estimate
- **Dropdown mode** = `placeholder` | `longest-option` | `selected-value`
- **Submit status** = `never` | `while-submitting`

| Component | Toolbox | Canvas | Runtime |
|---|---|---|---|
| `first-name` | TLI ✅ (✅/✅/n/a) | TLI ✅ (✅/✅/n/a) | TLI ❌ |
| `text` | TLI ✅ (✅/✅/n/a) | TLI ✅ (✅/✅/n/a) | TLI ❌ |
| `email` | TLI ✅ (✅/✅/n/a) | TLI ✅ (✅/✅/n/a) | TLI ❌ |
| `address` | TLI ✅ (✅/✅/n/a) | TLI ✅ (✅/✅/n/a) | TLI ❌ |
| `textarea` | TLI ❌ | TLI ✅ (✅/✅/✅) | TLI ❌ |
| `dropdown` | mode: `placeholder` | mode: `longest-option` | mode: `placeholder` |
| `submit-button` | status: `never`, icon ✅, resize ❌ | status: `never`, icon ✅, resize ✅ | status: `while-submitting`, icon ✅ |
| all others | (defaults) TLI ❌ | (defaults) TLI ❌ | (defaults) TLI ❌ |

Note: This matrix is expected to stay aligned with:
`frontend/src/features/builder/utils/componentSurfaceCapabilities.ts`

---

## Per-component migration task list (A + B)

### `first-name`
- [ ] A) UniversalFieldShell-only
- [ ] B) Surface capabilities wired

### `text`
- [ ] A) UniversalFieldShell-only
- [ ] B) Surface capabilities wired

### `number`
- [ ] A) UniversalFieldShell-only
- [ ] B) Surface capabilities wired

### `email`
- [ ] A) UniversalFieldShell-only
- [ ] B) Surface capabilities wired

### `textarea`
- [ ] A) UniversalFieldShell-only
- [ ] B) Surface capabilities wired

### `dropdown`
- [ ] A) UniversalFieldShell-only
- [ ] B) Surface capabilities wired

### `date`
- [ ] A) UniversalFieldShell-only
- [ ] B) Surface capabilities wired

### `checkbox`
- [ ] A) UniversalFieldShell-only
- [ ] B) Surface capabilities wired

### `radio`
- [ ] A) UniversalFieldShell-only
- [ ] B) Surface capabilities wired

### `phone`
- [ ] A) UniversalFieldShell-only
- [ ] B) Surface capabilities wired

### `address`
- [ ] A) UniversalFieldShell-only
- [ ] B) Surface capabilities wired

### `terms`
- [ ] A) UniversalFieldShell-only
- [ ] B) Surface capabilities wired

### `submit-button`
- [ ] A) UniversalFieldShell-only
- [ ] B) Surface capabilities wired

### `header`
- [ ] A) UniversalFieldShell-only
- [ ] B) Surface capabilities wired

### `divider`
- [ ] A) UniversalFieldShell-only
- [ ] B) Surface capabilities wired





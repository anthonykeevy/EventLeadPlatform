# TypeScript Errors – Prioritized Resolution Guide

Generated from `npx tsc --noEmit`. Use for `chore/lint-resolution` branch; fix in order below.

---

## Priority 1: Quick wins (unused only – no type logic)

Remove or prefix with `_`. One commit per area.

| Area | File | Unused |
|------|------|--------|
| **DataTable** | `src/components/common/DataTable.tsx` | useMemo, Edit2, X, enableInlineEditing, onRowEdit, onCellEdit, editingCell, setEditingCell |
| **Examples** | `src/examples/FormBuilderExample.tsx` | setIsDirty |
| **Audit** | `src/features/audit/components/AuditTable.tsx` | PaginatedActivityLog |
| **Builder** | ComponentPreview.tsx | RowComponent, ColumnComponent |
| **Builder** | FirstNameField.tsx | User, helpText |
| **Builder** | StandardInput.tsx | Icon, baseGuideColor |
| **Builder** | AppearanceSection.tsx | globalValue |
| **Builder** | DatePropertiesSection.tsx | PropertyToggle |
| **Builder** | CategoryFontSelect.tsx | FontCategoryInfo, LANGUAGE_SUPPORT_INFO |
| **Builder** | ObjectLayoutSection.tsx | X, AlignVertical*, closestCenter, handleReorderInGroup |
| **Builder** | OptionsSection.tsx | Settings2 |
| **Builder** | StyleOverridesSection.tsx | globalValue |
| **Builder** | TypographyColorsSection.tsx | useState |
| **Builder** | ValidationSection.tsx | isRuleHidden |
| **Builder** | PropertiesPanel.tsx | sharedType |
| **Builder** | RuntimeFormView.tsx | type |
| **Builder** | SortableComponent.tsx | currentInputWidthPx, currentX, currentY, appliedShift, parentWidth, isAuto, displayHeight, effectiveLayout |
| **Builder** | GridLayoutEditor.tsx | getObjectGridArea |
| **Builder** | ResizeHandles.tsx | newWidth, newHeight |
| **Builder** | UniversalFieldShell.tsx | ComputedFieldStyles, previewScale |
| **Builder** | useComponentStyles.ts | effectiveGlobalStyles (x2) |
| **Builder** | useFonts.ts | useQueryClient, FontFamilyDetail, FontCategoryInfo |
| **Builder** | BuilderPage.tsx | FirstNameField, getDefaultStructure, ghostRect |
| **Builder** | ComponentRegistry.tsx | useRef, useState, useEffect, Loader2, TOOLBOX_FIRST_NAME_RENDERERS |
| **Builder** | useBuilderStore.ts | selectAuthoredPagesForState |
| **Builder** | collisionDetection.ts | computeAllowedX, computeAllowedY |
| **Builder** | objectRenderers.tsx | availableExtraWidthPx |
| **Builder** | phoneValidation.ts | isValidPhoneNumber |
| **Builder** | scaleUtils.ts | canvasScale |
| **Builder** | structureDefaults.ts | ObjectLayoutType |
| **Builder** | structureValidation.ts | allObjectIds |
| **Builder** | validationEngine.ts | CountryValidationConfig, formatPhone, context |
| **Builder** | componentRenderers.ts | componentType, component, handlers |
| **Config** | ConfigProvider.tsx | React |
| **Dashboard** | CompanyList.tsx, DashboardLayout.tsx, EmptyState.tsx, KPISection.tsx, ThemeSettingsPopup.tsx, UserMenu.tsx, DashboardPage.tsx | React and/or logout, saveToLocalStorage |
| **Dashboard** | EditRoleModal.tsx | EditUserRoleRequest |
| **Dashboard** | FormStatusBadge.tsx | getApprovalColor |
| **Dashboard** | GrantAccessForm.tsx | Loader2, searchUsers, searchCompanies |
| **Events** | EditEventModal.tsx | Tag, Globe |
| **Events** | EventSelector.tsx | Check |
| **Events** | ReviewStatusBadge.tsx | AlertCircle |
| **Events** | ShareEventModal.tsx | CheckCircle, Search |
| **Events** | StatusBadge.tsx | React |
| **Events** | EventsPage.tsx | FormDetailView, isLoadingEvents, filters, setFilters |
| **Forms** | BulkTransferOwnershipModal, DeleteFormConfirmModal, FormAccessControlModal, FormDetailView, FormStatusBadge | React and/or companyName, Globe, submitFormForApproval, isLoadingAccess, canView, getApprovalColor |

---

## Priority 2: Null/undefined and UMD React (small, localized)

| File | Issue | Fix |
|------|--------|-----|
| AuditTimeline.tsx | newData possibly null (~150) | Guard: `newData != null` or default |
| AuthContext.tsx | response.user possibly undefined; User \| undefined vs User \| null; setState return | Use `response.user ?? null`; ensure all setters return `User \| null` |
| SortableComponent.tsx | React UMD (2778, 2779) | Add `import React from 'react'` |
| BuilderPage.tsx | React UMD (61, 83–86, 105, 255) | Add `import React from 'react'` |
| BuilderPage.tsx | activePage possibly undefined (370, 492, 972, 1028) | Guard before use: `if (!activePage) return ...` or `activePage!` where safe |
| SortableComponent.tsx | oldPosition.x/y, currentPosition, expectedPosition, finalPosition possibly undefined | Optional chaining or `!` / guards where invariants hold |
| collisionDetection.ts | RefObject \| undefined vs \| null | Use `ref ?? null` or widen param to `undefined` |
| GrantAccessForm.tsx | string \| null \| undefined → string \| null | Coerce: `value ?? null` |

---

## Priority 3: Single-file type fixes (no API changes)

| File | Error | Fix |
|------|--------|-----|
| LogicPanel.tsx | Record&lt;LogicOperator, string&gt; missing 4 keys | Add greaterThan, greaterThanOrEqual, lessThan, lessThanOrEqual to object (or type as Partial) |
| StandardInput.tsx, CategoryFontSelect.tsx | Lucide `title` prop | Use `aria-label` (and optional wrapper `title`) or spread with type assertion |
| GeneralSection.tsx | Element not assignable to string | Change prop type to `ReactNode` or pass string label |
| GridLayoutSection.tsx | null not assignable to GridLayoutConfig \| undefined | Use `config ?? undefined` |
| GridLayoutSection.tsx, ObjectLayoutSection.tsx, GridLayoutEditor.tsx | Property 'label' does not exist on ComponentObject | Use correct key from types (e.g. title/label from structure) or extend type |
| TypographyColorsSection.tsx | divider missing; ComponentType vs LucideIcon; keyof GlobalStyles \| undefined | Add divider entry; fix icon type; narrow before use (e.g. `if (key != null)`) |
| ValidationSection.tsx | unknown → ReactNode; minSelections/maxSelections not on ValidationRules | Cast or narrow; add to ValidationRules type or remove usage |
| ValidationSection.tsx | Many: Element not assignable to string | Change prop types to `ReactNode` where label/content can be JSX |
| PropertiesPanel.tsx | newOverrides implicitly any | Add explicit type: `StyleOverrides` or inferred type |
| SortableComponent.tsx | "percentage-calculated" etc. not in union | Add to source type union or map to existing literal |
| SortableComponent.tsx | SubmitButtonField showIcon; ref callback vs RefObject | Remove showIcon or add to props; use useRef+callback or fix type |
| UniversalFieldShell.tsx | string[] vs Record; RefObject null | Normalize options type; use RefObject&lt;... \| null&gt; or allow null in consumer |
| BuilderPage.tsx | ClientRect missing right, bottom | Add right, bottom to object or use a type that allows partial |
| collisionDetection.ts | rect vs rr; rect on type | Align property names (rect vs rr) in type and usages |
| conditionalEvaluation.ts | boolean \| undefined → boolean | Default: `value ?? false` or narrow |
| dateSettingsCompatibility.ts | undefined as index | Guard key before indexing |
| gridLayoutUtils.ts | Record&lt;ComponentType, ...&gt; missing keys | Use Partial or add all ComponentType keys |
| styleUtils.ts | unknown → boolean; action* / divider* not on EffectiveStyles | Cast/narrow; add action/divider props to EffectiveStyles or use existing names |
| phoneValidation.ts | Expected 2 arguments, got 1 | Pass second argument or make optional in signature |
| CreateFormModal.tsx | "number" not assignable; string \| number → string | Use correct input type; ensure string (e.g. String(x)) |
| DashboardLayout.tsx, TeamManagementPanel.tsx | "Company Viewer" not in role union | Extend union to include "Company Viewer" where intended |
| EditEventModal.tsx | "medium"/"small" vs "sm"\|"md"\|"lg"\|"xl"; IndustrySummary.name | Use "md"/"sm" or extend type; use correct IndustrySummary field |

---

## Priority 4: Cross-file or type-definition changes

- **TypographyCardProps (GlobalStylesPanel):** Add `hasBorder?: boolean` and type callback params (`labelHasBorder: boolean` etc.) so GlobalStylesPanel and TypographyCard stay in sync.
- **ComponentType (builder.types):** Add `'row' | 'column' | 'select' | 'paragraph'` if they are real component types; otherwise remove or narrow comparisons in ComponentPreview, OptionsSection, RuntimeFormView.
- **ValidationRules:** Add `minSelections` / `maxSelections` if used by ValidationSection.
- **EffectiveStyles (styleUtils):** Add action* and divider* (or map from existing) so styleUtils and consumers agree.
- **ClientRect / position types:** Centralize in one type (e.g. `CanvasRect` or DOM ClientRect) and use consistently in BuilderPage, SortableComponent, collisionDetection.

---

## Suggested commit order on `chore/lint-resolution`

1. **DataTable + Audit + examples** – Priority 1 (DataTable, FormBuilderExample, AuditTable).
2. **Auth + AuditTimeline** – Priority 2 (AuthContext, AuditTimeline).
3. **React UMD** – Priority 2 (SortableComponent, BuilderPage add `import React` where needed).
4. **Builder unused (batch 1)** – Priority 1: ComponentPreview, FirstNameField, StandardInput (unused only), AppearanceSection, DatePropertiesSection, ObjectLayoutSection, OptionsSection, StyleOverridesSection, TypographyColorsSection (useState), ValidationSection (isRuleHidden).
5. **Builder unused (batch 2)** – PropertiesPanel, RuntimeFormView, SortableComponent (unused vars), GridLayoutEditor, ResizeHandles, UniversalFieldShell, hooks, BuilderPage, ComponentRegistry, useBuilderStore, utils (unused only).
6. **Config + Dashboard + Events + Forms unused** – Priority 1 for those areas.
7. **Lucide title → aria-label** – StandardInput, CategoryFontSelect (Priority 3).
8. **LogicPanel + GeneralSection + GridLayout + ObjectLayout** – Priority 3 (LogicOperator record, GeneralSection string/Element, label on ComponentObject).
9. **GlobalStylesPanel (TypographyCard)** – Add hasBorder + callback types (Priority 4).
10. **ValidationSection (Element/string + ValidationRules)** – Priority 3/4.
11. **Remaining Priority 3–4** – SortableComponent (position/ref/SubmitButton), UniversalFieldShell, collisionDetection, styleUtils, BuilderPage (ClientRect, activePage), dashboard/events/forms type fixes.

Use this file as the single checklist; tick off as you commit each block.

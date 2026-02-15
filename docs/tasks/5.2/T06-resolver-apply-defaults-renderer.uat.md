# T06 UAT: Resolver — Apply Defaults in Renderer

**Task:** T06 - Resolver: Apply Defaults in Renderer  
**Story:** 5.2 - Company Form Defaults (Brand System)  

---

## Prerequisites

- T02, T05 complete
- Company defaults set (Form Branding Defaults)
- Form with inherited/overridden values

---

## UAT Steps

### AC1: Resolver applies inheritance

| Step | Status | Notes |
|------|--------|-------|
| Global → Company → Form → Component resolution order | | |
| Form overrides from DefinitionJSON override company defaults | | |

### AC2: Preview uses resolver

| Step | Status | Notes |
|------|--------|-------|
| Builder preview renders with resolved defaults | | |
| Matches public renderer behavior | | |

### AC3: Public renderer uses resolver

| Step | Status | Notes |
|------|--------|-------|
| Production/public form render uses same resolution | | |
| No hardcoded fallbacks that bypass resolver | | |

### AC4: Inheritance documented

| Step | Status | Notes |
|------|--------|-------|
| Resolution rules documented | | Aligned with STORY-5.2-DATA-SCHEMA.md |

---

*Record results in T06-resolver-apply-defaults-renderer.uat-results.md*

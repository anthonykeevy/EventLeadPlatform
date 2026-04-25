# Story 6.4.4 Hypothesis Evidence

**Story:** 6.4.4 — Prompt Shrink Sweeps H1/H2/H4  
**Branch:** `story/epic6-6.4.4-prompt-shrink-sweeps`  
**PR:** [#72](https://github.com/anthonykeevy/EventLeadPlatform/pull/72)  
**Status:** Template — Dev to complete  

---

## 1) Evidence Summary

| Hypothesis | Variant Label | Run IDs | Prompt Size Delta | Structural Verdict | Semantic Verdict | Final Decision |
|------------|---------------|---------|-------------------|--------------------|------------------|----------------|
| H1 locale shrink | TBD | TBD | TBD | TBD | TBD | TBD |
| H2 consent/legal shrink | TBD | TBD | TBD | TBD | TBD | TBD |
| H4 operational notes trim | TBD | TBD | TBD | TBD | TBD | TBD |
| Combined H1+H2+H4 | TBD | TBD | TBD | TBD | TBD | TBD |

Decision values:

- `ship`
- `revert`
- `inconclusive-follow-up`

---

## 2) Baseline

| Field | Value |
|-------|-------|
| Baseline run ID | TBD |
| Baseline artifact path | TBD |
| Benchmark version | `prompts-v1.0` |
| Model/provider | TBD |
| Repetitions | TBD |
| Judge package path | TBD |
| Judge ingest summary | TBD |
| Notes | TBD |

---

## 3) H1 — AU/NZ Locale One-Line Directive

### Variant

```text
Form audience: Australia/New Zealand. Use AU/NZ spelling, address, phone, date conventions.
```

### Commands

```powershell
# Dev records exact commands here.
```

### Outputs

| Artifact | Path |
|----------|------|
| Eval run | TBD |
| Judge package | TBD |
| Judge ingest summary | TBD |
| Diff report | TBD |
| Diff summary JSON | TBD |
| Diff details CSV | TBD |

### Results

| Metric | Baseline | Variant | Delta | Verdict |
|--------|----------|---------|-------|---------|
| schema_valid rate | TBD | TBD | TBD | TBD |
| boundary_violation_count | TBD | TBD | TBD | TBD |
| component_count | TBD | TBD | TBD | TBD |
| collision_count | TBD | TBD | TBD | TBD |
| field_coverage_recall | TBD | TBD | TBD | TBD |
| copy_quality_score | TBD | TBD | TBD | TBD |
| AU/NZ locale correctness | TBD | TBD | TBD | TBD |

### Decision

**Decision:** TBD  
**Rationale:** TBD  
**Code retained/reverted:** TBD  

---

## 4) H2 — Consent/Legal Compact Decision Table

### Variant

Summarize the compact decision table here.

### Commands

```powershell
# Dev records exact commands here.
```

### Outputs

| Artifact | Path |
|----------|------|
| Eval run | TBD |
| Judge package | TBD |
| Judge ingest summary | TBD |
| Diff report | TBD |
| Diff summary JSON | TBD |
| Diff details CSV | TBD |

### Results

| Metric | Baseline | Variant | Delta | Verdict |
|--------|----------|---------|-------|---------|
| schema_valid rate | TBD | TBD | TBD | TBD |
| boundary_violation_count | TBD | TBD | TBD | TBD |
| terms component accuracy | TBD | TBD | TBD | TBD |
| checkbox fallback accuracy | TBD | TBD | TBD | TBD |
| company-managed terms behavior | TBD | TBD | TBD | TBD |
| copy_quality_score | TBD | TBD | TBD | TBD |

### Decision

**Decision:** TBD  
**Rationale:** TBD  
**Code retained/reverted:** TBD  

---

## 5) H4 — Operational Notes Trim

### Variant

Summarize removed/trimmed duplicated operational guidance here.

### Commands

```powershell
# Dev records exact commands here.
```

### Outputs

| Artifact | Path |
|----------|------|
| Eval run | TBD |
| Judge package | TBD |
| Judge ingest summary | TBD |
| Diff report | TBD |
| Diff summary JSON | TBD |
| Diff details CSV | TBD |

### Results

| Metric | Baseline | Variant | Delta | Verdict |
|--------|----------|---------|-------|---------|
| schema_valid rate | TBD | TBD | TBD | TBD |
| boundary_violation_count | TBD | TBD | TBD | TBD |
| collision_count | TBD | TBD | TBD | TBD |
| row grouping quality | TBD | TBD | TBD | TBD |
| tab order/layout behavior | TBD | TBD | TBD | TBD |
| supported catalog compliance | TBD | TBD | TBD | TBD |

### Decision

**Decision:** TBD  
**Rationale:** TBD  
**Code retained/reverted:** TBD  

---

## 6) Combined H1+H2+H4

### Commands

```powershell
# Dev records exact commands here.
```

### Outputs

| Artifact | Path |
|----------|------|
| Eval run | TBD |
| Judge package | TBD |
| Judge ingest summary | TBD |
| Diff report | TBD |
| Diff summary JSON | TBD |
| Diff details CSV | TBD |

### Results

| Metric | Baseline | Variant | Delta | Verdict |
|--------|----------|---------|-------|---------|
| schema_valid rate | TBD | TBD | TBD | TBD |
| boundary_violation_count | TBD | TBD | TBD | TBD |
| Category B aggregate | TBD | TBD | TBD | TBD |
| GPT-5 mini bias delta | TBD | TBD | TBD | TBD |
| rerun recommendation | TBD | TBD | TBD | TBD |

### Decision

**Decision:** TBD  
**Rationale:** TBD  
**Code retained/reverted:** TBD  

---

## 7) Final Shipped Prompt Changes

| Prompt Area | Final State | Evidence Link | Notes |
|-------------|-------------|---------------|-------|
| Locale block | TBD | TBD | TBD |
| Consent/legal block | TBD | TBD | TBD |
| Operational notes | TBD | TBD | TBD |

---

## 8) Carry-Forward

| Item | Owner | Target Story | Reason |
|------|-------|--------------|--------|
| TBD | TBD | TBD | TBD |

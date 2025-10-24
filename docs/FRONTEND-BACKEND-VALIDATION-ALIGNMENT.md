# Frontend-Backend Validation Alignment Mechanism

**Story 1.20:** Ensuring 100% Alignment Between Frontend and Backend Validation  
**Author:** Anthony Keevy (Product Owner) + Amelia (Dev Agent)  
**Critical Principle:** Backend is ALWAYS the single source of truth

---

## 🎯 Core Principle

**"Frontend validation constraints MUST come from backend, NEVER be hardcoded."**

### ❌ **WRONG Approach (Causes Misalignment):**

```typescript
// Frontend hardcodes rules
<input maxLength={4} />  // ❌ Hardcoded!
<input pattern="^\d{4}$" />  // ❌ Hardcoded!

// Backend has different rules
maxLength: 10  // USA ZIP can be 5+4 = 9 chars
pattern: "^\d{5}(-\d{4})?$"

Result: User types 5 digits → Frontend blocks
        Backend expects up to 10 → Mismatch!
```

### ✅ **CORRECT Approach (Backend-Driven):**

```typescript
// Frontend fetches constraints from backend
useEffect(() => {
  const metadata = await fetch('/api/countries/15/validation-rules/postal_code')
  setMaxLength(metadata.max_length)  // Gets 10 from backend
}, [countryId])

<input maxLength={maxLength} />  // ✅ Dynamic from backend

Result: Frontend constraints MATCH backend exactly
```

---

## 🔧 The Alignment Mechanism

### **Layer 1: Database (Source of Truth)**

```sql
[config].[ValidationRule]
  RuleKey: POSTAL_CODE_US
  MinLength: 5
  MaxLength: 10
  ValidationPattern: ^\d{5}(-\d{4})?$
  ExampleValue: 94102
```

**All validation metadata lives here.**

---

### **Layer 2: Backend API (Exposes Truth)**

**Endpoint 1: Get Validation Metadata**
```
GET /api/countries/{id}/validation-rules/{type}

Response:
{
  "has_rules": true,
  "min_length": 5,
  "max_length": 10,      ← Frontend uses this for maxLength
  "example_value": "94102",
  "display_format": "XXXXX",
  "spacing_pattern": "XXXXX"
}
```

**Endpoint 2: Validate Value**
```
POST /api/countries/{id}/validate
{
  "rule_type": "postal_code",
  "value": "94102"
}

Response:
{
  "is_valid": true,
  "formatted_value": "94102",
  "error_message": null
}
```

---

### **Layer 3: Frontend (Consumes Truth)**

**Step 1: Fetch Constraints on Mount/Country Change**
```typescript
useEffect(() => {
  // Fetch validation metadata
  const metadata = await fetch(
    `/api/countries/${countryId}/validation-rules/postal_code`
  )
  
  // Apply backend constraints to frontend
  setMaxLength(metadata.max_length)
  setMinLength(metadata.min_length)
  setPlaceholder(metadata.example_value)
}, [countryId])
```

**Step 2: Render Input with Backend Constraints**
```typescript
<input
  type="text"
  minLength={minLength}        // From backend
  maxLength={maxLength}        // From backend
  placeholder={placeholder}    // From backend
  onBlur={validateWithBackend}
/>
```

**Step 3: Validate with Backend**
```typescript
const result = await POST('/api/countries/15/validate', {
  rule_type: 'postal_code',
  value: userInput
})

// Backend says valid/invalid (final authority)
```

---

## ✅ How We Maintain 100% Alignment

### **Rule #1: No Hardcoded Validation Logic in Frontend**

**❌ NEVER:**
```typescript
maxLength={4}                    // Hardcoded
pattern={/^\d{4}$/}              // Hardcoded
validate: (v) => v.length === 4  // Hardcoded logic
```

**✅ ALWAYS:**
```typescript
maxLength={backendMaxLength}     // From API
// No pattern validation in frontend (backend does it)
// No logic duplication
```

---

### **Rule #2: Backend Metadata Endpoint for Every Input Type**

**For each validation type, frontend calls:**
```
GET /api/countries/{id}/validation-rules/phone
GET /api/countries/{id}/validation-rules/postal_code  
GET /api/countries/{id}/validation-rules/tax_id
```

**Returns constraints:**
- `min_length`, `max_length` → Set input limits
- `example_value` → Set placeholder
- `display_format` → Show formatting hint

---

### **Rule #3: Backend Does All Actual Validation**

**Frontend role:** UX constraints (prevent typing 100 characters)  
**Backend role:** Validation authority (is value actually valid?)

```
Frontend: maxLength=10  (prevents typing more, improves UX)
Backend: Validates pattern ^\d{5}(-\d{4})?$  (final authority)

If frontend allows through, backend still validates ✅
```

---

### **Rule #4: Single Configuration Point**

**Update Rule:**
1. Change database: `UPDATE ValidationRule SET MaxLength=12 WHERE RuleKey='POSTAL_CODE_US'`
2. Frontend automatically adapts (fetches new maxLength)
3. No code deployment needed

**NO frontend code changes required!**

---

## 📋 Implementation Checklist

**For Each New Validation Input Component:**

- [ ] Fetch validation metadata from backend on mount
- [ ] Fetch metadata when country changes  
- [ ] Apply `maxLength` from backend (not hardcoded)
- [ ] Apply `minLength` from backend (not hardcoded)
- [ ] Use `example_value` from backend for placeholder
- [ ] Validate with backend on blur (POST /validate)
- [ ] Display backend error messages (not custom)
- [ ] NO hardcoded patterns/regex in frontend
- [ ] NO hardcoded validation logic in frontend

---

## 🐛 How Misalignment Happened in Story 1.20

### **Bug: PostalCodeInput maxLength=4**

**What Happened:**
```typescript
// PostalCodeInput.tsx (hardcoded)
<input maxLength={4} />  // Developer assumed all postcodes are 4 digits

// Database (actual rules)
AU: MaxLength=4  ✅ Works
USA: MaxLength=10  ❌ Frontend blocks at 4 digits
UK: MaxLength=8   ❌ Frontend blocks at 4 digits
```

**Why It Happened:**
- Developer copied from AU postal code component
- Didn't check backend rules for other countries
- Hardcoded instead of fetching

**Fix:**
```typescript
// Fetch from backend
const metadata = await GET('/api/countries/15/validation-rules/postal_code')
setMaxLength(metadata.max_length)  // Gets 10 from database

<input maxLength={maxLength} />  // ✅ Now accepts up to 10 digits
```

---

## ✅ Automated Alignment Checks (Future)

**Test to Prevent Misalignment:**

```typescript
// test: frontend-backend-alignment.test.ts
describe('Validation Alignment', () => {
  it('PostalCodeInput maxLength should match backend', async () => {
    const backendMeta = await fetch('/api/countries/15/validation-rules/postal_code')
    const component = render(<PostalCodeInput countryId={15} />)
    
    const input = screen.getByRole('textbox')
    
    // Frontend maxLength must match backend
    expect(input).toHaveAttribute('maxLength', backendMeta.max_length.toString())
  })
})
```

---

## 🎯 Summary: The Mechanism

### **How It Works:**

```
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE (Truth)                         │
│  ValidationRule: MaxLength=10, MinLength=5, Pattern=...     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              BACKEND API (Exposes Truth)                    │
│  GET /validation-rules/{type} → Returns metadata            │
│  POST /validate → Validates values                          │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              FRONTEND (Consumes Truth)                      │
│  1. Fetch metadata → GET /validation-rules                  │
│  2. Apply to input → maxLength={fromBackend}                │
│  3. User types → Frontend prevents overflow (UX)            │
│  4. On blur → POST /validate (backend confirms)             │
└─────────────────────────────────────────────────────────────┘
```

### **Guarantees:**

1. ✅ **Single Source of Truth:** Database only
2. ✅ **No Duplication:** No rules in frontend code
3. ✅ **Auto-Sync:** Frontend always matches backend
4. ✅ **Config-Driven:** Change DB, no code deployment
5. ✅ **Testable:** Can verify alignment automatically

---

**This mechanism ensures frontend and backend are ALWAYS 100% aligned!** 🎯

---

## 🚀 Fixes Applied in Story 1.20

1. ✅ PostalCodeInput fetches `maxLength` from backend (no more hardcoded 4)
2. ✅ Country passes from Step 1 → Step 2 (maintains user selection)
3. ✅ All constraints come from database via API
4. ✅ Backend is single source of truth



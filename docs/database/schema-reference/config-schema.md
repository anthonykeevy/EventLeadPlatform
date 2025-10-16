# `config` Schema - Runtime Configuration

**Schema Purpose:** Application configuration parameters (business rules, feature flags)  
**Table Count:** 2  
**Retention:** Permanent with change history  
**Backup Priority:** HIGH (critical for application behavior)  
**Write Volume:** VERY LOW (admin changes only)

---

## Schema Overview

Configuration tables store runtime parameters that control application behavior without requiring code deployments. These are critical for operational flexibility (e.g., changing password policies, validation rules) and should be carefully managed with audit trails.

---

## Table Overview

| # | Table | Purpose | Record Count | Access Level |
|---|-------|---------|--------------|--------------|
| 1 | `AppSetting` | Runtime business rules and configuration | ~15 | Admin only |
| 2 | `ValidationRule` | Country-specific validation patterns | ~20 | Admin only |

---

## 1. `config.AppSetting` - Runtime Business Rules

**Purpose:** Store application-level configuration parameters that control business logic

**Use Cases:**
- Password policy (min length, expiry, complexity requirements)
- Token expiry times (access token, refresh token, verification token)
- Rate limiting thresholds (login attempts, API requests)
- Feature toggles (enable/disable features without deployment)

**Primary Key:** `AppSettingID` (BIGINT IDENTITY)

**Foreign Keys:**
- `SettingCategoryID` → `ref.SettingCategory.SettingCategoryID`
- `SettingTypeID` → `ref.SettingType.SettingTypeID`

**Unique Constraints:**
- `(SettingKey, SettingCategoryID)` - Unique key within category

**Key Columns:**
- `SettingKey` (NVARCHAR(100)) - Machine-readable key (e.g., 'PASSWORD_MIN_LENGTH')
- `SettingValue` (NVARCHAR(MAX)) - Value (stored as string, parsed per SettingType)
- `SettingCategoryID` - Category for UI organization (authentication, email, etc.)
- `SettingTypeID` - Data type (integer, boolean, string, json, decimal)
- `DefaultValue` (NVARCHAR(MAX)) - Factory default (for reset functionality)
- `Description` (NVARCHAR(500)) - Admin-facing explanation
- `IsEditable` (BIT) - Can be changed via admin UI (false for system-critical settings)
- `ValidationRegex` (NVARCHAR(500)) - Optional regex for value validation
- `MinValue`, `MaxValue` (DECIMAL) - Optional range constraints for numeric values

**Seed Data Examples:**

| SettingKey | SettingValue | Category | Type | Description |
|------------|--------------|----------|------|-------------|
| `PASSWORD_MIN_LENGTH` | `8` | authentication | integer | Minimum password length |
| `PASSWORD_REQUIRE_UPPERCASE` | `false` | authentication | boolean | Require uppercase letter in password |
| `PASSWORD_REQUIRE_NUMBER` | `true` | authentication | boolean | Require number in password |
| `PASSWORD_EXPIRY_DAYS` | `90` | authentication | integer | Password expiry (days, 0 = never) |
| `ACCESS_TOKEN_EXPIRY_MINUTES` | `15` | authentication | integer | JWT access token lifetime |
| `REFRESH_TOKEN_EXPIRY_DAYS` | `7` | authentication | integer | JWT refresh token lifetime |
| `EMAIL_VERIFICATION_EXPIRY_HOURS` | `24` | authentication | integer | Email verification token lifetime |
| `PASSWORD_RESET_EXPIRY_HOURS` | `1` | authentication | integer | Password reset token lifetime |
| `MAX_LOGIN_ATTEMPTS` | `5` | security | integer | Max failed logins before lockout |
| `ACCOUNT_LOCKOUT_MINUTES` | `15` | security | integer | Account lockout duration |
| `INVITATION_EXPIRY_DAYS` | `7` | authentication | integer | Team invitation lifetime |
| `SESSION_TIMEOUT_MINUTES` | `30` | security | integer | Idle session timeout |

**Benefits:**
- Change behavior without code deployment (e.g., increase token expiry)
- A/B testing (temporarily change thresholds)
- Emergency response (disable features via admin UI)
- Compliance (audit trail of who changed what when)

**Security:**
- Admin-only access (regular users cannot view/edit)
- Audit trail via `UpdatedBy`, `UpdatedDate`
- Consider encrypting sensitive values (API keys, secrets)

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: config.AppSetting)

---

## 2. `config.ValidationRule` - Country-Specific Validation

**Purpose:** Store country-specific validation patterns (phone, postal code, tax ID formats)

**Use Cases:**
- Phone number format validation per country
- Postal/zip code format validation
- Tax identifier validation (ABN, EIN, VAT number)
- Email domain validation (corporate vs personal)
- Address format validation

**Primary Key:** `ValidationRuleID` (BIGINT IDENTITY)

**Foreign Keys:**
- `RuleTypeID` → `ref.RuleType.RuleTypeID` (phone, postal_code, tax_id, etc.)
- `CountryID` → `ref.Country.CountryID` (NULL for global rules)

**Unique Constraints:**
- `(RuleKey, CountryID, RuleTypeID)` - Unique rule per country + type

**Key Columns:**
- `RuleKey` (NVARCHAR(100)) - Machine-readable key (e.g., 'PHONE_MOBILE_FORMAT')
- `RuleTypeID` - Type of validation (phone, postal_code, tax_id, etc.)
- `CountryID` - Country-specific (NULL = global rule)
- `ValidationPattern` (NVARCHAR(500)) - Regex pattern for validation
- `ValidationMessage` (NVARCHAR(500)) - Error message shown to user
- `Description` (NVARCHAR(500)) - Admin-facing explanation
- `IsActive` (BIT, default 1) - Can be disabled without deletion
- `Priority` (INT, default 0) - Order of execution (higher = earlier)

**Seed Data Examples:**

**Australia (Phone Validation):**
- `PHONE_MOBILE_FORMAT` - `^04\d{8}$` - "Mobile number must start with 04 and be 10 digits"
- `PHONE_LANDLINE_FORMAT` - `^0[2-8]\d{8}$` - "Landline must be 10 digits starting with 02-08"

**Australia (Postal Code):**
- `POSTAL_CODE_FORMAT` - `^\d{4}$` - "Australian postcode must be 4 digits"

**Australia (Tax ID - ABN):**
- `TAX_ID_FORMAT` - `^\d{11}$` - "ABN must be 11 digits"
- `TAX_ID_CHECKSUM` - (complex checksum algorithm) - "Invalid ABN checksum"

**Global (Email):**
- `EMAIL_FORMAT` - (standard email regex) - "Invalid email format"
- `EMAIL_BLOCK_TEMP_PROVIDERS` - `tempmail|guerrillamail` - "Temporary email addresses not allowed"

**Benefits:**
- Support international expansion (add country-specific rules)
- Adjust validation without code deployment
- A/B test validation strictness
- Emergency relaxation (temporarily disable strict validation)

**Usage Pattern:**
```python
# Service layer
def validate_phone(phone: str, country_id: int):
    rules = db.query(ValidationRule).filter(
        ValidationRule.rule_type == 'phone',
        ValidationRule.country_id == country_id,
        ValidationRule.is_active == True
    ).order_by(ValidationRule.priority.desc()).all()
    
    for rule in rules:
        if not re.match(rule.validation_pattern, phone):
            raise ValidationError(rule.validation_message)
```

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: config.ValidationRule)

---

## Common Patterns

### **Configuration as Data (Not Code)**

**Anti-Pattern (Hard-Coded):**
```python
# ❌ BAD: Hard-coded in application code
PASSWORD_MIN_LENGTH = 8
TOKEN_EXPIRY_MINUTES = 15
MAX_LOGIN_ATTEMPTS = 5
```

**Good Pattern (Database-Driven):**
```python
# ✅ GOOD: Read from database
config = get_setting('PASSWORD_MIN_LENGTH')
password_min_length = int(config.setting_value)
```

**Benefits:**
- Change without deployment (no downtime)
- Environment-specific values (dev vs prod)
- Audit trail (who changed what when)
- Rollback capability (restore previous value)

---

### **Caching Strategy**

**Problem:** Querying config table on every request is inefficient

**Solution:** Aggressive caching with invalidation

```python
# Cache AppSettings in memory (Redis or application cache)
CACHE_TTL = 300  # 5 minutes

@cached(ttl=CACHE_TTL)
def get_setting(key: str) -> AppSetting:
    return db.query(AppSetting).filter(AppSetting.setting_key == key).first()

# Invalidate cache when admin updates setting
def update_setting(key: str, new_value: str, admin_user_id: int):
    setting = db.query(AppSetting).filter(AppSetting.setting_key == key).first()
    setting.setting_value = new_value
    setting.updated_by = admin_user_id
    setting.updated_date = datetime.utcnow()
    db.commit()
    
    # Invalidate cache
    cache.delete(f'setting:{key}')
```

---

### **Type-Safe Value Parsing**

```python
# Helper to parse SettingValue based on SettingType
def get_setting_value(key: str) -> Any:
    setting = get_setting(key)
    
    if setting.setting_type == 'integer':
        return int(setting.setting_value)
    elif setting.setting_type == 'boolean':
        return setting.setting_value.lower() in ('true', '1', 'yes')
    elif setting.setting_type == 'decimal':
        return Decimal(setting.setting_value)
    elif setting.setting_type == 'json':
        return json.loads(setting.setting_value)
    else:  # string
        return setting.setting_value
```

---

### **Admin UI Patterns**

**Settings Management Page:**
- Group by SettingCategory (tabs for authentication, email, security)
- Show Description as tooltip
- Validate against ValidationRegex before saving
- Enforce MinValue/MaxValue for numeric settings
- Show "Reset to Default" button (restores DefaultValue)
- Log all changes to audit table

**Validation Rules Management:**
- Group by Country + RuleType
- Test regex pattern with sample inputs
- Show ValidationMessage preview
- Disable/enable rules without deletion
- Priority ordering (drag-and-drop)

---

## Security Considerations

### **Access Control**

```python
# Only system admins can view/edit config tables
@router.get("/api/admin/settings")
async def list_settings(current_user: User = Depends(require_role("system_admin"))):
    return db.query(AppSetting).all()

# Regular users and company admins CANNOT access config tables
```

### **Sensitive Values**

**Problem:** Some settings contain secrets (API keys, SMTP passwords)

**Solution:** Encrypt sensitive values

```python
# Mark sensitive settings
sensitive_keys = ['SMTP_PASSWORD', 'API_SECRET_KEY', 'ENCRYPTION_KEY']

# Encrypt before storing
if setting_key in sensitive_keys:
    setting_value = encrypt(setting_value, master_key)
```

### **Audit Trail**

**All config changes MUST be logged:**
```sql
-- Record in audit.ActivityLog
INSERT INTO audit.ActivityLog (UserID, Action, EntityType, EntityID, OldValue, NewValue)
VALUES (
    @admin_user_id,
    'config.update',
    'AppSetting',
    @setting_id,
    @old_value,
    @new_value
);
```

---

## Performance Considerations

**Read Performance:**
- Configuration tables are tiny (< 100 rows total)
- Read volume: HIGH (every request may check settings)
- **Strategy:** Aggressive caching (5-minute TTL, invalidate on update)

**Write Performance:**
- Write volume: VERY LOW (admin changes only, maybe 1-2 per day)
- **Strategy:** No optimization needed

**Query Patterns:**
```sql
-- Single setting lookup (cached)
SELECT SettingValue, SettingTypeID 
FROM config.AppSetting 
WHERE SettingKey = 'PASSWORD_MIN_LENGTH';

-- All settings for a category (admin UI)
SELECT * 
FROM config.AppSetting 
WHERE SettingCategoryID = @category_id 
ORDER BY SortOrder;
```

---

## Related Documentation

**Architecture:**
- `docs/solution-architecture.md` - Configuration Management Architecture section
- `docs/architecture/decisions/ADR-004-database-normalization-for-enum-like-fields.md`

**Database:**
- `docs/database/REBUILD-PLAN-SUMMARY.md`
- `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` - Full SQL definitions

---

**Winston** 🏗️  
*"Configuration is code that changes without deploying code."*


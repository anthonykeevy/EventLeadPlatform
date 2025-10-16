# User Domain Comparison - Dimitri vs Rebuild Plan

**Date:** October 16, 2025  
**Author:** Solomon 📜 (Database Migration Validator)  
**Purpose:** Compare Dimitri's comprehensive User domain design with current rebuild plan

---

## 📊 **SUMMARY OF DIFFERENCES**

| **Category** | **Dimitri's Design** | **Rebuild Plan** | **Status** |
|-------------|---------------------|------------------|------------|
| **User table fields** | 28 fields | 20 fields | ❌ **8 fields missing** |
| **Token management** | Tokens in User table | Separate token tables | ⚠️ **Different approach** |
| **Session management** | SessionToken + Versions | Not included | ❌ **MISSING** |
| **Profile fields** | RoleTitle, ProfilePictureUrl, TimezoneIdentifier | Not included | ❌ **MISSING** |
| **Status approach** | StatusCode (string FK) | StatusID (int FK) | ⚠️ **Different approach** |
| **UserCompany fields** | 15 fields | 12 fields | ❌ **3 fields missing** |
| **Invitation fields** | 23 fields | 14 fields | ❌ **9 fields missing** |

---

## 🔴 **CRITICAL MISSING FIELDS**

### **1. User Table - Missing Fields (8 fields)**

| **Field** | **Dimitri's Design** | **Rebuild Plan** | **Impact** |
|-----------|---------------------|------------------|------------|
| **RoleTitle** | NVARCHAR(100) | ❌ Not included | UX: Can't display user's job title |
| **ProfilePictureUrl** | NVARCHAR(500) | ❌ Not included | UX: No avatar support |
| **TimezoneIdentifier** | NVARCHAR(50) DEFAULT 'Australia/Sydney' | ❌ Not included | 🚨 **Critical**: Wrong timestamps in UI |
| **SessionToken** | NVARCHAR(255) | ❌ Not included | 🚨 **Critical**: Can't invalidate sessions |
| **AccessTokenVersion** | INT DEFAULT 1 | ❌ Not included | 🚨 **Critical**: Can't force re-login |
| **RefreshTokenVersion** | INT DEFAULT 1 | ❌ Not included | 🚨 **Critical**: Can't logout all devices |
| **EmailVerifiedAt** | DATETIME2 | ❌ Not included | Audit: When verification happened |
| **LastPasswordChange** | DATETIME2 | ❌ Not included | Security: Password age tracking |

---

### **2. UserCompany Table - Missing Fields (3 fields)**

| **Field** | **Dimitri's Design** | **Rebuild Plan** | **Impact** |
|-----------|---------------------|------------------|------------|
| **Status** | NVARCHAR(20) ('active', 'suspended', 'removed') | ❌ Not included | Can't suspend user from company |
| **JoinedVia** | NVARCHAR(20) ('signup', 'invitation', 'transfer') | ❌ Not included | Audit: How user joined company |
| **RemovalReason** | NVARCHAR(500) | ❌ Not included | UX: Why user was removed |

**Rebuild plan has:**
- `IsPrimaryCompany` (BIT) - Maps to Dimitri's `IsDefaultCompany` ✅
- But missing `RemovedDate`, `RemovedByUserID` fields

---

### **3. Invitation Table - Missing Fields (9 fields)**

| **Field** | **Dimitri's Design** | **Rebuild Plan** | **Impact** |
|-----------|---------------------|------------------|------------|
| **InvitedFirstName** | NVARCHAR(100) | `FirstName` ✅ | Included (different name) |
| **InvitedLastName** | NVARCHAR(100) | `LastName` ✅ | Included (different name) |
| **AssignedRole** | NVARCHAR(20) | ❌ Not included | 🚨 **Critical**: What role to assign? |
| **CancelledAt** | DATETIME2 | ❌ Not included | Audit: When invitation cancelled |
| **CancelledByUserID** | BIGINT | ❌ Not included | Audit: Who cancelled invitation |
| **CancellationReason** | NVARCHAR(500) | ❌ Not included | UX: Why invitation cancelled |
| **DeclinedAt** | DATETIME2 | ❌ Not included | Phase 2: When invitee declined |
| **DeclineReason** | NVARCHAR(500) | ❌ Not included | Phase 2: Why invitee declined |
| **ResendCount** | INT DEFAULT 0 | ❌ Not included | Rate limiting: Prevent spam |
| **LastResentAt** | DATETIME2 | ❌ Not included | Rate limiting: Last resend time |
| **EmailSentAt** | DATETIME2 | ❌ Not included | Email tracking: When sent |
| **EmailSentStatus** | NVARCHAR(20) | ❌ Not included | Email tracking: Delivery status |
| **EmailBounceReason** | NVARCHAR(500) | ❌ Not included | Email tracking: Why bounced |

**Rebuild plan has:**
- Table renamed to `UserInvitation` ✅ (better hierarchical naming)
- `UserCompanyRoleID` (FK to ref.UserCompanyRole) ✅ (better than AssignedRole string)

---

## 🟡 **ARCHITECTURAL DIFFERENCES**

### **1. Token Management - Different Approaches**

**Dimitri's Design (Tokens in User table):**
```sql
-- User table
EmailVerificationToken NVARCHAR(255) NULL,
EmailVerificationExpiresAt DATETIME2 NULL,
PasswordResetToken NVARCHAR(255) NULL,
PasswordResetExpiresAt DATETIME2 NULL,
```

**Rebuild Plan (Separate token tables):**
```sql
-- Separate tables
EmailVerificationToken (EmailVerificationTokenID, UserID, Token, ExpiresAt, IsUsed, UsedAt)
PasswordResetToken (PasswordResetTokenID, UserID, Token, ExpiresAt, IsUsed, UsedAt)
```

**Analysis:**
| **Approach** | **Pros** | **Cons** | **Recommendation** |
|-------------|----------|----------|-------------------|
| **Dimitri's** | ✅ Simpler queries<br>✅ Fewer joins<br>✅ Faster lookups | ❌ Can't track token history<br>❌ Can't see who created token<br>❌ Limited audit trail | ⭐ **Better for MVP** |
| **Rebuild** | ✅ Full token history<br>✅ Security context (IP, UserAgent)<br>✅ Complete audit trail | ❌ More complex queries<br>❌ Extra joins<br>❌ More tables | **Better for compliance** |

**Decision Required:** Anthony, which approach do you prefer?

---

### **2. Status Approach - String vs Integer FK**

**Dimitri's Design:**
```sql
-- User table
Status NVARCHAR(20) NOT NULL DEFAULT 'unverified',
CONSTRAINT FK_User_Status FOREIGN KEY (Status) REFERENCES [UserStatus](StatusCode)

-- UserStatus table
StatusCode NVARCHAR(20) PRIMARY KEY  -- 'active', 'unverified', 'suspended'
```

**Rebuild Plan:**
```sql
-- User table
StatusID BIGINT NOT NULL,
CONSTRAINT FK_User_Status FOREIGN KEY (StatusID) REFERENCES [ref].[UserStatus](UserStatusID)

-- ref.UserStatus table
UserStatusID BIGINT IDENTITY(1,1) PRIMARY KEY
StatusCode NVARCHAR(20) NOT NULL UNIQUE  -- 'active', 'pending', 'locked'
```

**Analysis:**
| **Approach** | **Pros** | **Cons** | **Recommendation** |
|-------------|----------|----------|-------------------|
| **Dimitri's** | ✅ Self-documenting (code visible in queries)<br>✅ No joins for display<br>✅ Human-readable | ❌ String comparisons slower<br>❌ More storage (20 bytes vs 8) | ⭐ **Better for readability** |
| **Rebuild** | ✅ Smaller storage (BIGINT)<br>✅ Faster joins<br>✅ Standard pattern | ❌ Requires join to see code<br>❌ Less readable in queries | **Better for performance** |

**Industry Research:**
- Stripe: Uses string codes (`'active'`, `'inactive'`)
- Salesforce: Uses integer IDs with separate lookup
- **Recommendation:** Rebuild plan's approach is more standard, but Dimitri's is more readable

---

## 🚨 **CRITICAL SESSION MANAGEMENT MISSING**

Dimitri's design includes sophisticated JWT session management that's **completely missing** from rebuild plan:

```sql
-- Dimitri's User table
SessionToken NVARCHAR(255) NULL,         -- "Logout all devices" feature
AccessTokenVersion INT NOT NULL DEFAULT 1,   -- Force re-login on all devices
RefreshTokenVersion INT NOT NULL DEFAULT 1,  -- Invalidate all refresh tokens
```

**Use Cases:**
1. **Password Reset** → Increment `RefreshTokenVersion` → All devices logged out
2. **Suspicious Activity** → Increment `AccessTokenVersion` → Force re-login everywhere
3. **"Logout All Devices"** → Update `SessionToken` → All JWTs invalid

**Impact of Missing These:**
- ❌ Can't implement "Logout all devices" button
- ❌ Password reset doesn't logout other devices (security risk)
- ❌ Can't force re-login on security events
- ❌ Users can't remotely logout stolen device

**Recommendation:** 🚨 **MUST ADD** - Critical security feature

---

## 🟢 **GOOD ADDITIONS IN REBUILD PLAN**

### **1. Schema Organization ⭐**
```sql
-- Dimitri's design
UserStatus, InvitationStatus (dbo schema, no prefix)

-- Rebuild plan
ref.UserStatus, ref.InvitationStatus (ref schema)
```
✅ **Better organization** - Clear separation of reference data

### **2. System-Level Roles ⭐**
```sql
-- Rebuild plan User table
UserRoleID BIGINT NULL,  -- FK to ref.UserRole (system-level role: system_admin)
```
✅ **Better RBAC** - Separates system roles (platform admin) from company roles

### **3. Hierarchical Role Design ⭐**
```sql
-- Rebuild plan
ref.UserRole (system-level: system_admin)
ref.UserCompanyRole (company-level: company_admin, company_user, company_viewer)
ref.AuditRole (role change audit trail)
```
✅ **Better design** - Clear separation of system vs company roles

### **4. Internationalization ⭐**
```sql
-- Rebuild plan User table
CountryID BIGINT NULL,
PreferredLanguageID BIGINT NULL,
```
✅ **Better i18n** - Prepares for international expansion

### **5. Onboarding Progress ⭐**
```sql
-- Rebuild plan User table
OnboardingStep INT NOT NULL DEFAULT 1,
```
✅ **Better UX** - Track exact onboarding progress

---

## 📋 **RECOMMENDATIONS**

### **Priority 1: Critical Session Management 🚨**
**Add to User table:**
```sql
SessionToken NVARCHAR(255) NULL,
AccessTokenVersion INT NOT NULL DEFAULT 1,
RefreshTokenVersion INT NOT NULL DEFAULT 1,
```

**Why:** Security-critical for JWT invalidation, "logout all devices", password reset security

---

### **Priority 2: Profile & UX Fields 🎯**
**Add to User table:**
```sql
RoleTitle NVARCHAR(100) NULL,           -- Job title (e.g., "Marketing Manager")
ProfilePictureUrl NVARCHAR(500) NULL,   -- Avatar URL (Azure Blob Storage)
TimezoneIdentifier NVARCHAR(50) NULL DEFAULT 'Australia/Sydney',  -- Timezone for date display
EmailVerifiedAt DATETIME2 NULL,         -- Audit: When email was verified
LastPasswordChange DATETIME2 NULL,      -- Security: Password age tracking
```

**Why:** Essential UX features, timezone critical for correct date/time display

---

### **Priority 3: UserCompany Enhancements 💼**
**Add to UserCompany table:**
```sql
Status NVARCHAR(20) NOT NULL DEFAULT 'active',  -- 'active', 'suspended', 'removed'
JoinedVia NVARCHAR(20) NOT NULL,                -- 'signup', 'invitation', 'transfer'
RemovedDate DATETIME2 NULL,
RemovedByUserID BIGINT NULL,
RemovalReason NVARCHAR(500) NULL,
```

**Why:** Enables suspending users from companies (without full removal), better audit trail

---

### **Priority 4: Invitation Enhancements 📧**
**Add to UserInvitation table:**
```sql
UserCompanyRoleID BIGINT NOT NULL,  -- FK to ref.UserCompanyRole (already in rebuild ✅)
CancelledAt DATETIME2 NULL,
CancelledByUserID BIGINT NULL,
CancellationReason NVARCHAR(500) NULL,
ResendCount INT NOT NULL DEFAULT 0,
LastResentAt DATETIME2 NULL,
```

**Why:** Rate limiting (prevent invitation spam), audit trail for cancellations

---

## 🎯 **TOKEN MANAGEMENT DECISION**

**Option A: Dimitri's Approach (Tokens in User table)**
```sql
-- Simpler, faster, good for MVP
EmailVerificationToken NVARCHAR(255) NULL,
EmailVerificationExpiresAt DATETIME2 NULL,
PasswordResetToken NVARCHAR(255) NULL,
PasswordResetExpiresAt DATETIME2 NULL,
```

**Option B: Rebuild Plan (Separate token tables)**
```sql
-- More complex, better audit trail, better for compliance
EmailVerificationToken (TokenID, UserID, Token, ExpiresAt, IsUsed, UsedAt, CreatedDate)
PasswordResetToken (TokenID, UserID, Token, ExpiresAt, IsUsed, UsedAt, IPAddress, UserAgent, CreatedDate)
```

**Hybrid Option C: Best of Both**
```sql
-- User table (for quick lookups)
CurrentEmailVerificationToken NVARCHAR(255) NULL,
CurrentPasswordResetToken NVARCHAR(255) NULL,

-- Separate token tables (for audit history)
EmailVerificationToken (full history)
PasswordResetToken (full history with security context)
```

---

## 📊 **FIELD COUNT SUMMARY**

| **Table** | **Dimitri's Design** | **Rebuild Plan** | **Gap** |
|-----------|---------------------|------------------|---------|
| **User** | 28 fields | 20 fields | ❌ -8 fields |
| **UserCompany** | 15 fields | 12 fields | ❌ -3 fields |
| **Invitation / UserInvitation** | 23 fields | 14 fields | ❌ -9 fields |
| **Total** | 66 fields | 46 fields | ❌ **-20 fields** |

---

## ✅ **ACTION ITEMS**

1. **Critical (Must Add):**
   - [ ] Add SessionToken, AccessTokenVersion, RefreshTokenVersion to User table
   - [ ] Add TimezoneIdentifier to User table (default: 'Australia/Sydney')
   - [ ] Add UserCompanyRoleID FK to UserInvitation table (already in rebuild ✅)

2. **High Priority (Should Add):**
   - [ ] Add RoleTitle, ProfilePictureUrl to User table
   - [ ] Add EmailVerifiedAt, LastPasswordChange to User table
   - [ ] Add Status, JoinedVia fields to UserCompany table
   - [ ] Add ResendCount, LastResentAt to UserInvitation table

3. **Medium Priority (Nice to Have):**
   - [ ] Add CancelledAt, CancelledByUserID, CancellationReason to UserInvitation table
   - [ ] Add DeclinedAt, DeclineReason to UserInvitation (Phase 2)
   - [ ] Add RemovedDate, RemovedByUserID, RemovalReason to UserCompany table

4. **Architectural Decision Required:**
   - [ ] Anthony: Choose token management approach (Option A, B, or C)
   - [ ] Anthony: Approve Status approach (string FK vs integer FK)

---

## 🏆 **CONCLUSION**

Dimitri's User domain design is **exceptionally comprehensive** and includes many features missing from the rebuild plan. The most critical gaps are:

1. 🚨 **Session management** (SessionToken, AccessTokenVersion, RefreshTokenVersion)
2. 🚨 **Timezone support** (TimezoneIdentifier)
3. 🎯 **Profile fields** (RoleTitle, ProfilePictureUrl)
4. 💼 **UserCompany status** (active, suspended, removed)
5. 📧 **Invitation rate limiting** (ResendCount, LastResentAt)

**Recommendation:** Merge Dimitri's comprehensive design into the rebuild plan, prioritizing critical session management and timezone support for MVP.

---

**Solomon** 📜  
*"Dimitri's design shows exceptional attention to detail. These fields aren't bloat—they're essential for a production-ready authentication system."*


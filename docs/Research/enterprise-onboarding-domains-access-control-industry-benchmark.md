# Enterprise Onboarding, Domains, and Access Control
## Industry Benchmark & Decision Paper

**Purpose:** Evaluate how leading platforms handle custom domains, SSO, internal vs external access, and enterprise onboarding — and assess customer complexity, platform enablement complexity, and operational/cost implications.  
**Note:** This paper supports architecture and product decisions; it does not define MVP scope.  
**Saved:** 2026-02-07

---

## Platforms Benchmarked

The following platforms were selected because together they cover:
- Internal workflows
- External/public data collection
- Enterprise security expectations
- Multi-tenant SaaS at scale

Benchmarked platforms:
- Notion
- Airtable
- ServiceNow
- Microsoft Forms / Power Platform
- Typeform (Enterprise tier)

---

## 1. Industry Patterns (Executive Summary)

Across all platforms studied, three consistent patterns emerge:

### Domains are branding + routing, not security
- Security is enforced via authentication and access policy
- Domains alone never determine access rights

### SSO users are authenticated, not automatically trusted
- First login ≠ access
- Most platforms gate access via:
  - admin approval
  - invitation
  - group/role mapping

### Enterprise features are deliberately opt-in and paid
- SSO, custom domains, audit logs, and access controls are rarely included in base plans
- This reduces abuse risk and support overhead

These patterns are extremely consistent across vendors.

---

## 2. Platform-by-Platform Analysis

### Notion

**What it supports**
- Custom domains (workspace access + public pages)
- SSO via SAML / OIDC (Enterprise only)
- Internal-only workspaces
- Public sharing per page

**Access model**
- Users authenticate via SSO
- Access is not automatic
- Admin controls:
  - who can join
  - whether email domain auto-join is enabled
  - default role on join

**Internal vs external**
- Internal pages: require authentication
- Public pages: explicitly published
- Domain does not control access; page permissions do

**Complexity**
- Customer complexity: Medium (SSO setup requires IT involvement)
- Platform complexity: High (identity federation, role mapping, audit)
- Cost: Enterprise tier only

**Key takeaway:** Notion enforces authentication first, access second.

---

### Airtable

**What it supports**
- Workspace-level SSO (Enterprise)
- Public forms, views, and internal bases
- Role-based access at base/table level

**Access model**
- SSO authenticates identity
- User must still:
  - be invited, or
  - be auto-provisioned into a role

**Internal vs external**
- Internal workflows require login
- Public forms are anonymous
- Same domain for both; access controls differ

**Complexity**
- Customer complexity: Medium–High
- Platform complexity: High
- Cost: Enterprise tier

**Key takeaway:** Airtable clearly separates identity verification from workspace authorization.

---

### ServiceNow

**What it supports**
- Full enterprise IAM integration
- Multiple IdPs
- Internal portals + external portals
- Role, group, and workflow-based access

**Access model**
- SSO authenticates user
- Access strictly governed by:
  - roles
  - groups
  - approval workflows

**Internal vs external**
- Internal portals require authentication
- External portals are explicitly configured
- Domains and network controls are optional enhancements

**Complexity**
- Customer complexity: High
- Platform complexity: Very High
- Cost: Very High (enterprise contracts)

**Key takeaway:** This is the extreme end of enterprise control and cost.

---

### Microsoft Forms / Power Platform

**What it supports**
- Entra ID (Azure AD) native SSO
- “Only people in my organisation can respond”
- External anonymous forms

**Access model**
- Identity comes from Entra ID
- Access tied to tenant membership
- No approval workflow by default

**Internal vs external**
- Simple toggle per form:
  - internal only
  - public

**Complexity**
- Customer complexity: Low (if already on Microsoft)
- Platform complexity: High but subsidised by Microsoft ecosystem
- Cost: Bundled with Microsoft licenses

**Key takeaway:** Strong SSO, but limited flexibility and branding.

---

### Typeform (Enterprise)

**What it supports**
- Custom domains (Enterprise)
- SSO (SAML)
- Public and private forms

**Access model**
- SSO authenticates
- Admin assigns workspace access
- Forms can still be public

**Complexity**
- Customer complexity: Medium
- Platform complexity: Medium–High
- Cost: Enterprise pricing

**Key takeaway:** Similar model to Notion/Airtable but narrower scope.

---

## 3. Comparative Matrix

| Capability | Industry Norm |
|---|---|
| Custom domains | Enterprise-only feature |
| Multiple domains per tenant | Supported by advanced platforms |
| SSO (OIDC/SAML) | Enterprise-only |
| SSO auto-access | ❌ Almost never |
| Admin approval flow | ✅ Common |
| Internal vs external forms | Audience-based, not domain-based |
| Domain-based security | ❌ Avoided |
| IP allowlists | Optional, enterprise add-on |

---

## 4. Access Control: The Critical Decision

### The dominant industry model

Authenticate first → then authorise → then grant access

This means:
- SSO confirms identity
- Platform decides access
- Admin retains control

### Common patterns for first SSO login

| Pattern | Used by | Risk |
|---|---|---|
| Auto-join full workspace | Rare | High (data exposure) |
| Auto-join minimal role | Common | Medium |
| Access request pending admin approval | Very common | Low |
| Invitation-only even with SSO | Enterprise | Very Low |

**Industry preference:** Authenticate via SSO, then gate access until admin approval or role assignment.

---

## 5. Domains: Internal vs External

### Industry consensus

Do NOT rely on “internal-only domains” as your primary security control.

Reasons:
- Split-horizon DNS is brittle
- VPN reliance reduces usability
- Cloud/SaaS users expect access from anywhere

### Preferred model

Use audience + authentication:
- PUBLIC → anonymous
- COMPANY_ONLY → SSO required

Domains control branding and routing, not trust.

Some enterprises add:
- IP allowlists
- Conditional Access (Entra)

But these are add-ons, not foundations.

---

## 6. Cost & Enablement Reality

### Platform-side cost drivers
- Identity federation (OIDC + SAML)
- Secure domain + TLS automation
- Audit logging
- Abuse prevention
- Support overhead

### Customer-side cost drivers
- IT involvement for SSO
- DNS changes
- Ongoing identity management

This is why every platform monetises these features separately.

---

## 7. Implications for Your Platform (Neutral Observations)

Based on industry norms:
- Supporting multiple domains per company is aligned with enterprise expectations
- Allowing SSO login without automatic access is the safest default
- Internal forms should always require authentication
- External forms should remain anonymous-capable
- Domain ≠ access control
- Audience + SSO is the correct abstraction

---

## 8. Final Industry-Aligned Position (Decision Support)

If you align with leading platforms, the most defensible stance is:
- ✅ Allow SSO authentication
- ❌ Do not auto-grant access
- ✅ Require admin approval or role assignment
- ✅ Use form audience rules to separate internal/external
- ✅ Use domains for branding and routing
- ❌ Do not use domains as a security boundary

This gives you:
- Enterprise credibility
- Lower breach risk
- Predictable operational cost
- Familiar behaviour for IT teams


# Australian Business Naming Strategy

**Author:** Solomon 📜 (SQL Standards Sage)  
**Date:** October 13, 2025  
**Compliance:** Australian Business Register (ABR) naming standards

---

## 🏢 **Australian Business Name Types**

### **1. Entity (Legal) Name**
- **Source:** ASIC registration
- **Purpose:** Legal contracts, tax invoices, official documents
- **Example:** "INTERNATIONAL CONVENTION CENTRE SYDNEY PTY LTD"
- **ABR Field:** `<mainName><organisationName>`

### **2. Business Names (Current)**
- **Source:** ASIC registered business names (post-2012)
- **Purpose:** Trading operations, marketing, customer-facing
- **Example:** "ICC Sydney", "Sydney Convention Centre"
- **ABR Field:** `<businessName><organisationName>`

### **3. Trading Names (Legacy)**
- **Source:** Pre-2012 informal names (deprecated)
- **Status:** Discontinued by ABR (no longer collected/updated)
- **Sunset:** October 31, 2025 (ABR will stop displaying)
- **ABR Field:** `<tradingName><organisationName>` (legacy only)

---

## 🔍 **ABR API Response Structure**

```xml
<ABRPayloadSearchResults>
  <response>
    <businessEntity>
      <ABN>53004085616</ABN>
      
      <!-- LEGAL NAME (Always Present) -->
      <mainName>
        <organisationName>INTERNATIONAL CONVENTION CENTRE SYDNEY PTY LTD</organisationName>
      </mainName>
      
      <!-- CURRENT BUSINESS NAMES (Post-2012) -->
      <businessName>
        <organisationName>ICC SYDNEY</organisationName>
        <effectiveFrom>2015-01-01</effectiveFrom>
      </businessName>
      <businessName>
        <organisationName>SYDNEY CONVENTION CENTRE</organisationName>
        <effectiveFrom>2018-03-15</effectiveFrom>
      </businessName>
      
      <!-- LEGACY TRADING NAMES (Pre-2012, Deprecated) -->
      <tradingName>
        <organisationName>ICC SYDNEY</organisationName>
      </tradingName>
      
    </businessEntity>
  </response>
</ABRPayloadSearchResults>
```

---

## 💡 **Recommended Schema Design**

### **Enhanced Company Table Structure**

```sql
CREATE TABLE [Company] (
    CompanyID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Display Names (User-Facing)
    -- =====================================================================
    DisplayName NVARCHAR(200) NOT NULL,
    -- ^ Primary display name (user's choice)
    -- Used for: Event cards, dashboards, search results
    -- Can be: Legal name, business name, or custom override
    -- Example: "ICC Sydney" (user-friendly)
    
    -- =====================================================================
    -- Legal Names (ABR-Sourced)
    -- =====================================================================
    LegalEntityName NVARCHAR(200) NOT NULL,
    -- ^ Legal entity name from ABR API
    -- Used for: Tax invoices, legal documents, contracts
    -- Example: "INTERNATIONAL CONVENTION CENTRE SYDNEY PTY LTD"
    -- Source: ABR <mainName><organisationName>
    
    -- =====================================================================
    -- Business Names (ABR-Sourced, Current)
    -- =====================================================================
    BusinessNames NVARCHAR(MAX) NULL,
    -- ^ JSON array of current business names from ABR
    -- Used for: Dropdown selection, validation
    -- Example: ["ICC SYDNEY", "SYDNEY CONVENTION CENTRE"]
    -- Source: ABR <businessName><organisationName> (current only)
    
    -- =====================================================================
    -- Name Override (User Customization)
    -- =====================================================================
    CustomDisplayName NVARCHAR(200) NULL,
    -- ^ User-defined display name (override)
    -- Used when: User wants different name than ABR provides
    -- Example: "ICC Sydney Events" (custom branding)
    -- NULL = Use DisplayName (default)
    
    -- =====================================================================
    -- Name Source Tracking (Data Lineage)
    -- =====================================================================
    DisplayNameSource NVARCHAR(20) NOT NULL DEFAULT 'User',
    -- ^ Source of DisplayName: 'Legal', 'Business', 'Custom', 'User'
    -- Used for: Audit trail, data quality
    -- 'Legal' = LegalEntityName
    -- 'Business' = First business name from BusinessNames
    -- 'Custom' = CustomDisplayName
    -- 'User' = User-selected from available options
    
    -- ... other existing fields ...
);
```

### **Enhanced CompanyBillingDetails**

```sql
CREATE TABLE [CompanyBillingDetails] (
    CompanyID BIGINT PRIMARY KEY,
    
    -- =====================================================================
    -- Tax Invoice Names (ABR-Compliant)
    -- =====================================================================
    TaxInvoiceLegalName NVARCHAR(200) NOT NULL,
    -- ^ Legal name for tax invoices (ABR <mainName>)
    -- MUST match ABR records (ATO requirement)
    -- Example: "INTERNATIONAL CONVENTION CENTRE SYDNEY PTY LTD"
    
    TaxInvoiceDisplayName NVARCHAR(200) NULL,
    -- ^ Display name on tax invoices (user choice)
    -- Can be: Legal name or business name
    -- Example: "ICC Sydney" (shorter, user-friendly)
    -- NULL = Use TaxInvoiceLegalName
    
    -- =====================================================================
    -- ABN Name Cache (Performance)
    -- =====================================================================
    ABNLegalName NVARCHAR(200) NOT NULL,
    -- ^ Cached legal name from last ABN lookup
    -- Used for: Validation, comparison with current ABR data
    
    ABNBusinessNames NVARCHAR(MAX) NULL,
    -- ^ Cached business names from last ABN lookup (JSON)
    -- Used for: Dropdown options, name selection UI
    
    ABNNamesLastUpdated DATETIME2 NULL,
    -- ^ When names were last fetched from ABR API
    -- Re-fetch if > 30 days old (ABR terms)
    
    -- ... other existing fields ...
);
```

---

## 🎯 **Business Logic Implementation**

### **1. ABN Lookup & Name Population**

```python
class ABNService:
    """Handle ABN lookup and name management"""
    
    async def validate_abn_and_populate_names(self, abn: str, company_id: int) -> dict:
        """
        Validate ABN and populate all name fields
        """
        # Fetch from ABR API
        abr_data = await self.abr_client.lookup_abn(abn)
        
        # Extract names
        legal_name = abr_data['mainName']['organisationName']
        business_names = [bn['organisationName'] for bn in abr_data.get('businessName', [])]
        
        # Default display name logic
        if business_names:
            display_name = business_names[0]  # Use first business name
            display_name_source = 'Business'
        else:
            display_name = legal_name  # Fallback to legal name
            display_name_source = 'Legal'
        
        return {
            'legal_entity_name': legal_name,
            'business_names': business_names,
            'display_name': display_name,
            'display_name_source': display_name_source,
            'tax_invoice_legal_name': legal_name,
            'tax_invoice_display_name': business_names[0] if business_names else None
        }
```

### **2. Name Selection UI**

```typescript
interface NameSelectionProps {
  legalName: string;
  businessNames: string[];
  currentDisplayName: string;
  onNameSelected: (name: string, source: string) => void;
}

const NameSelection: React.FC<NameSelectionProps> = ({
  legalName,
  businessNames,
  currentDisplayName,
  onNameSelected
}) => {
  return (
    <div className="name-selection">
      <h3>Select Company Display Name</h3>
      
      {/* Legal Name Option */}
      <div className="name-option">
        <input 
          type="radio" 
          name="displayName" 
          value="legal"
          checked={currentDisplayName === legalName}
          onChange={() => onNameSelected(legalName, 'Legal')}
        />
        <label>
          <strong>Legal Name:</strong> {legalName}
          <small>(Used for tax invoices and legal documents)</small>
        </label>
      </div>
      
      {/* Business Name Options */}
      {businessNames.map((businessName, index) => (
        <div key={index} className="name-option">
          <input 
            type="radio" 
            name="displayName" 
            value={`business-${index}`}
            checked={currentDisplayName === businessName}
            onChange={() => onNameSelected(businessName, 'Business')}
          />
          <label>
            <strong>Business Name:</strong> {businessName}
            <small>(Registered with ASIC, customer-facing)</small>
          </label>
        </div>
      ))}
      
      {/* Custom Override Option */}
      <div className="name-option">
        <input 
          type="radio" 
          name="displayName" 
          value="custom"
          checked={currentDisplayName !== legalName && !businessNames.includes(currentDisplayName)}
          onChange={() => setShowCustomInput(true)}
        />
        <label>
          <strong>Custom Name:</strong>
          <input 
            type="text" 
            placeholder="Enter custom display name"
            value={customName}
            onChange={(e) => {
              setCustomName(e.target.value);
              onNameSelected(e.target.value, 'Custom');
            }}
          />
          <small>(Override with your preferred name)</small>
        </label>
      </div>
    </div>
  );
};
```

---

## 📋 **Implementation Strategy**

### **Phase 1: Enhanced ABN Integration**
1. **Update ABN API client** to extract all name types
2. **Add name fields** to Company and CompanyBillingDetails tables
3. **Implement name population** logic from ABR response

### **Phase 2: User Interface**
1. **Create name selection component** for company setup
2. **Add name override capability** for custom branding
3. **Implement name validation** (legal name must match ABR)

### **Phase 3: Business Logic**
1. **Tax invoice generation** uses appropriate names
2. **Event display** uses user-selected display name
3. **Search and filtering** uses display name

---

## 🔧 **Migration Strategy**

### **Existing Data Migration**

```sql
-- Migration script for existing companies
UPDATE [Company] 
SET 
    LegalEntityName = Name,  -- Assume current Name is legal name
    DisplayName = Name,      -- Keep current name as display
    DisplayNameSource = 'User'  -- Mark as user-provided
WHERE LegalEntityName IS NULL;

-- For companies with ABN, fetch proper names
UPDATE [Company] c
JOIN [CompanyBillingDetails] bd ON c.CompanyID = bd.CompanyID
SET 
    LegalEntityName = bd.TaxInvoiceName,  -- Use existing tax invoice name
    DisplayName = c.Name,                 -- Keep user's display preference
    DisplayNameSource = 'User'            -- Mark as user-selected
WHERE bd.ABN IS NOT NULL;
```

---

## ✅ **Benefits of This Approach**

### **1. Compliance**
- ✅ **ATO Compliant:** Tax invoices use legal entity name
- ✅ **ABR Accurate:** Names sourced from official registry
- ✅ **Future-Proof:** Handles ABR naming changes

### **2. User Experience**
- ✅ **Flexible Display:** Users choose customer-facing name
- ✅ **Brand Consistency:** Custom names for marketing
- ✅ **Clear Options:** Legal vs. business vs. custom names

### **3. Data Quality**
- ✅ **Source Tracking:** Know where each name came from
- ✅ **Validation:** Ensure legal names match ABR
- ✅ **Audit Trail:** Track name changes over time

---

## 🎯 **Recommended Implementation**

### **For EventLead Platform:**

1. **Keep existing `Name` field** as `DisplayName`
2. **Add `LegalEntityName`** from ABR API
3. **Add `BusinessNames`** JSON array from ABR API
4. **Add `CustomDisplayName`** for user overrides
5. **Add `DisplayNameSource`** for tracking

### **Default Behavior:**
- **Display Name:** First business name (if available), else legal name
- **Tax Invoice Name:** Always legal entity name (ATO requirement)
- **User Override:** Allow custom display name for branding

---

**This approach provides maximum flexibility while maintaining Australian compliance!** 🇦🇺

---

*Solomon - SQL Standards Sage* 📜  
*"Handle Australian business names with the precision they deserve!"*



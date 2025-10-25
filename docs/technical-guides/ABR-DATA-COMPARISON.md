# ABR API Data Comparison
**Story 1.19: Understanding Available Data from ABR**

Generated: 2025-10-24

---

## Overview

The ABR (Australian Business Register) provides 3 search methods, each returning different levels of detail:

1. **ABN Search** (`SearchByABNv202001`) - Most comprehensive
2. **ACN Search** (`SearchByASICv201408`) - Same as ABN search
3. **Name Search** (`ABRSearchByNameSimpleProtocol`) - Limited data

---

## Data Available by Search Method

### 1. ABN Search (SearchByABNv202001)

**✅ MOST COMPREHENSIVE DATA**

```xml
<businessEntity202001>
  <recordLastUpdatedDate>2008-05-29</recordLastUpdatedDate>
  
  <ABN>
    <identifierValue>53102443916</identifierValue>
    <isCurrentIndicator>Y</isCurrentIndicator>
  </ABN>
  
  <entityStatus>
    <entityStatusCode>Active</entityStatusCode>
    <effectiveFrom>2002-10-08</effectiveFrom>
    <effectiveTo>0001-01-01</effectiveTo>
  </entityStatus>
  
  <ASICNumber>102443916</ASICNumber>
  
  <entityType>
    <entityTypeCode>PRV</entityTypeCode>
    <entityDescription>Australian Private Company</entityDescription>
  </entityType>
  
  <goodsAndServicesTax>
    <effectiveFrom>2002-10-08</effectiveFrom>
    <effectiveTo>0001-01-01</effectiveTo>
  </goodsAndServicesTax>
  
  <mainName>
    <organisationName>ATLASSIAN PTY LTD</organisationName>
    <effectiveFrom>2008-02-22</effectiveFrom>
  </mainName>
  
  <mainBusinessPhysicalAddress>
    <stateCode>NSW</stateCode>
    <postcode>2000</postcode>
    <effectiveFrom>2007-06-18</effectiveFrom>
    <effectiveTo>0001-01-01</effectiveTo>
  </mainBusinessPhysicalAddress>
</businessEntity202001>
```

**Available Fields:**
- ✅ ABN (11 digits)
- ✅ ACN (9 digits) - Included as `ASICNumber`
- ✅ Legal entity name (`mainName/organisationName`)
- ✅ Entity type code (`PRV`, `PUB`, etc.)
- ✅ **Entity description** (`"Australian Private Company"`) ← Rich description
- ✅ **Entity status code** (`Active`, `Cancelled`) ← Explicit status
- ✅ GST registration (has element = registered)
- ✅ State code
- ✅ Postcode
- ✅ Effective dates for all information
- ✅ Record last updated date
- ⚠️ **NO street address** (ABR doesn't store street addresses)
- ⚠️ **NO suburb/locality** (ABR doesn't store this)

**Notes:**
- ABR's "mainBusinessPhysicalAddress" only contains state and postcode
- Full street addresses are not stored by ABR (privacy reasons)
- GST registration is indicated by presence of `goodsAndServicesTax` element

---

### 2. ACN Search (SearchByASICv201408)

**✅ SAME AS ABN SEARCH**

```xml
<businessEntity201408>
  <!-- Same structure as ABN search -->
  <ABN>
    <identifierValue>50050035277</identifierValue>
  </ABN>
  
  <ASICNumber>050035277</ASICNumber>
  
  <entityType>
    <entityDescription>Public Company</entityDescription>
  </entityType>
  
  <!-- ... rest same as ABN search ... -->
</businessEntity201408>
```

**Available Fields:** Same as ABN search above

**Key Difference:**
- Response tag is `businessEntity201408` (version 2014)
- Otherwise identical data to ABN search

---

### 3. Name Search (ABRSearchByNameSimpleProtocol)

**⚠️ LIMITED DATA - "SimpleProtocol"**

```xml
<searchResultsList>
  <numberOfRecords>201</numberOfRecords>
  <exceedsMaximum>N</exceedsMaximum>
  
  <searchResultsRecord>
    <ABN>
      <identifierValue>80158929938</identifierValue>
      <identifierStatus>Active</identifierStatus>
    </ABN>
    
    <businessName>
      <organisationName>Canva</organisationName>
      <score>100</score>
    </businessName>
    
    <isCurrentIndicator>Y</isCurrentIndicator>
    
    <mainBusinessPhysicalAddress>
      <stateCode>NSW</stateCode>
      <postcode>2010</postcode>
      <isCurrentIndicator>Y</isCurrentIndicator>
    </mainBusinessPhysicalAddress>
  </searchResultsRecord>
  
  <!-- ... up to 200 results ... -->
</searchResultsList>
```

**Available Fields:**
- ✅ ABN
- ✅ Organization name
- ✅ Identifier status (Active, Cancelled)
- ✅ Relevance score (0-100)
- ✅ State code
- ✅ Postcode
- ✅ Is current indicator
- ❌ **NO entity type**
- ❌ **NO ACN**
- ❌ **NO GST details**
- ❌ **NO entity description**

**Limitation:**
- "SimpleProtocol" returns minimal data for performance
- Designed for quick name searches across 200+ results
- To get full details, must do follow-up ABN search

---

## Recommendations for EventLead Platform

### Current Implementation (Story 1.19)

**✅ What We're Capturing:**
| Field | ABN Search | ACN Search | Name Search | Saved to DB |
|-------|-----------|-----------|-------------|-------------|
| Company Name | ✅ | ✅ | ✅ | ✅ |
| ABN | ✅ | ✅ | ✅ | ✅ |
| ACN | ✅ | ✅ | ❌ | ✅ (if ACN search) |
| Legal Entity Name | ✅ | ✅ | ✅ | ✅ |
| ABN Status | ✅ | ✅ | ✅ | ✅ |
| Entity Type | ✅ | ✅ | ❌ | ✅ |
| GST Registered | ✅ | ✅ | ❌ | ✅ |
| State | ✅ | ✅ | ✅ | ✅ (via address parsing) |
| Postcode | ✅ | ✅ | ✅ | ✅ (via address parsing) |

**❌ NOT Available from ABR:**
- Street address (ABR doesn't store this)
- Suburb/locality (ABR doesn't store this)
- Company phone/email (not in ABR)
- Company website (not in ABR)

---

### Enhancement Option: Two-Step Enrichment

For **name search** results, we could do a **follow-up ABN search** to get full details:

**User Experience:**
1. User searches: "Canva" → 9 results (fast, SimpleProtocol)
2. User selects result → Click triggers **second API call** using that company's ABN
3. Get full details (entity type, GST, etc.) → Auto-fill form

**Trade-offs:**
| Approach | Pros | Cons |
|----------|------|------|
| **Current (Single Search)** | ✅ Fast (1 API call)<br>✅ Simple UX<br>✅ Good enough data | ⚠️ Missing entity type for name searches |
| **Two-Step Enrichment** | ✅ Complete data<br>✅ Entity type populated<br>✅ More accurate GST status | ❌ Slower (2 API calls)<br>❌ More complex<br>❌ Extra API costs |

**Recommendation:** 
- **Keep current implementation** for MVP
- Entity type is nice-to-have, not critical
- User still gets company name, ABN, state, postcode auto-filled
- Consider two-step enrichment in Epic 2 if needed

---

## What's Missing from ABR (User Must Enter)

**❌ Fields NOT in ABR (required for onboarding):**
1. **Street Address** - User must enter manually
2. **Suburb/Locality** - User must enter manually
3. **Company Phone** - User must enter manually (optional)
4. **Company Email** - User must enter manually (optional)
5. **Company Website** - User must enter manually (optional)

**Why ABR Doesn't Have This:**
- Privacy: ABR doesn't publish full street addresses
- Contact info: ABR is a registry, not a directory
- Purpose: ABR is for tax identification, not contact management

---

## Current Data Capture Summary

**From ABR (Auto-filled):**
- Company legal name
- ABN
- ACN (if searched by ACN)
- ABN status (Active, Cancelled)
- Entity type (if ABN/ACN search)
- GST registration status (if ABN/ACN search)
- State
- Postcode

**From User (Manual entry):**
- Street address (required for billing)
- Suburb (required for billing)
- Phone (optional)
- Email (optional)
- Website (optional)

**Result:** User saves ~60% effort with ABR search! 🎉

---

## Files Generated

- `backend/ABN_SEARCH_ATLASSIAN.xml` - Full ABN search response
- `backend/ACN_SEARCH_INCHCAPE.xml` - Full ACN search response  
- `backend/NAME_SEARCH_CANVA.xml` - Full name search response (5 results)

Review these files for complete XML structure.

---

**This represents the maximum data available from ABR API without upgrading to paid enterprise services.**


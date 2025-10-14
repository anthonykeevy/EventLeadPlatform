# GeoScape Implementation Validation Checklist

## 🎯 **Purpose**
This checklist ensures that the GeoScape service is properly integrated and all PSMA data is being stored correctly in the database.

## ✅ **Pre-Implementation Validation**

### **1. Service Integration Check**
- [ ] Enhanced GeoScape service is imported in address validation endpoints
- [ ] Legacy validation functions are replaced with enhanced service calls
- [ ] API endpoints use `GeoscapeService.validate_address()` instead of legacy functions
- [ ] Profile save endpoint links addresses to PSMA data via `PSMAAddressDetailID`

### **2. Database Schema Validation**
- [ ] All PSMA tables exist in database
- [ ] Foreign key relationships are properly configured
- [ ] `ProfileAddress.PSMAAddressDetailID` field exists and is nullable
- [ ] Indexes are created for performance

## ✅ **Post-Implementation Validation**

### **3. API Integration Test**
```bash
# Test address search
curl -X GET "http://localhost:8000/api/v1/address/search?q=George Street" \
  -H "Content-Type: application/json"

# Test address validation
curl -X POST "http://localhost:8000/api/v1/address/validate" \
  -H "Content-Type: application/json" \
  -d '{"address": "George Street, Sydney NSW 2000", "country": "AU"}'
```

**Expected Results:**
- [ ] Search returns address suggestions with PSMA IDs
- [ ] Validation returns structured address data
- [ ] No errors in backend logs

### **4. Database Storage Validation**

#### **4.1 PSMA Tables Data Check**
Run this SQL query to verify PSMA data storage:

```sql
-- Check PSMA tables have data
SELECT 
    'PSMAAddressDetails' AS TableName, COUNT(*) AS RecordCount FROM PSMAAddressDetails
UNION ALL
SELECT 'PSMAAddressGeographicCoordinates', COUNT(*) FROM PSMAAddressGeographicCoordinates
UNION ALL
SELECT 'PSMAAddressLocalGovernmentArea', COUNT(*) FROM PSMAAddressLocalGovernmentArea
UNION ALL
SELECT 'PSMAAddressStateElectorate', COUNT(*) FROM PSMAAddressStateElectorate
UNION ALL
SELECT 'PSMAAddressCommonwealthElectorate', COUNT(*) FROM PSMAAddressCommonwealthElectorate
UNION ALL
SELECT 'PSMAAddressASGSMain', COUNT(*) FROM PSMAAddressASGSMain
UNION ALL
SELECT 'PSMAAddressASGSRemoteness', COUNT(*) FROM PSMAAddressASGSRemoteness
UNION ALL
SELECT 'PSMAAddressDetailInfo', COUNT(*) FROM PSMAAddressDetailInfo
UNION ALL
SELECT 'PSMAAddressRelatedBuildings', COUNT(*) FROM PSMAAddressRelatedBuildings
UNION ALL
SELECT 'PSMAAddressSearchHistory', COUNT(*) FROM PSMAAddressSearchHistory;
```

**Expected Results:**
- [ ] `PSMAAddressSearchHistory` > 0 (search activity)
- [ ] `PSMAAddressDetails` > 0 (address details stored)
- [ ] Other PSMA tables > 0 (normalized data stored)

#### **4.2 ProfileAddress Linkage Check**
```sql
-- Check ProfileAddress records are linked to PSMA data
SELECT 
    pa.ProfileAddressID,
    pa.StreetName,
    pa.Suburb,
    pa.PSMAAddressDetailID,
    pad.AddressID AS PSMA_AddressID,
    pad.AddressRecordType
FROM ProfileAddress pa
LEFT JOIN PSMAAddressDetails pad ON pa.PSMAAddressDetailID = pad.PSMAAddressDetailID
WHERE pa.IsActive = 1
ORDER BY pa.lastUpdated DESC;
```

**Expected Results:**
- [ ] Active addresses have `PSMAAddressDetailID` populated
- [ ] Links to valid `PSMAAddressDetails` records
- [ ] `AddressValidationSource` = 'geoscape'

### **5. End-to-End Flow Validation**

#### **5.1 Frontend Integration Test**
1. [ ] Navigate to Profile Builder V3
2. [ ] Enter an address in the address field
3. [ ] Verify address suggestions appear
4. [ ] Select an address suggestion
5. [ ] Save the profile
6. [ ] Verify no console errors

#### **5.2 Backend Log Validation**
Check backend logs for:
- [ ] GeoScape service initialization
- [ ] PSMA API calls with successful responses
- [ ] Database storage operations
- [ ] No errors in address validation flow

### **6. Performance Validation**

#### **6.1 Response Time Check**
```bash
# Test response times
time curl -X GET "http://localhost:8000/api/v1/address/search?q=George Street"
time curl -X POST "http://localhost:8000/api/v1/address/validate" \
  -H "Content-Type: application/json" \
  -d '{"address": "George Street, Sydney NSW 2000", "country": "AU"}'
```

**Expected Results:**
- [ ] Search response time < 2 seconds
- [ ] Validation response time < 3 seconds
- [ ] No timeout errors

#### **6.2 Database Performance Check**
```sql
-- Check query performance
SET STATISTICS TIME ON;
SELECT COUNT(*) FROM PSMAAddressDetails;
SELECT COUNT(*) FROM ProfileAddress WHERE PSMAAddressDetailID IS NOT NULL;
SET STATISTICS TIME OFF;
```

**Expected Results:**
- [ ] Query execution time < 100ms
- [ ] No blocking or deadlock issues

## ❌ **Common Failure Points**

### **Integration Failures**
- [ ] **Legacy Functions Still Used**: Check if `validate_address()` calls the enhanced service
- [ ] **Missing Import**: Verify `GeoscapeService` is imported in address endpoints
- [ ] **Wrong Service Method**: Ensure `validate_address()` not `search_addresses()` is used for validation

### **Database Failures**
- [ ] **Empty PSMA Tables**: All tables show 0 records
- [ ] **Missing Foreign Keys**: `PSMAAddressDetailID` is NULL in ProfileAddress
- [ ] **Transaction Failures**: PSMA data not committed due to errors

### **API Failures**
- [ ] **Authentication Errors**: Check API key configuration
- [ ] **Rate Limiting**: Too many requests to PSMA API
- [ ] **Network Issues**: PSMA API unavailable

## 🔧 **Troubleshooting Steps**

### **If PSMA Tables Are Empty**
1. Check if `_store_psma_data()` is being called
2. Verify PSMA API responses contain expected data
3. Check database transaction commits
4. Review error logs for storage failures

### **If ProfileAddress Not Linked**
1. Verify `PSMAAddressDetailID` is set during address save
2. Check if validation returns `psma_detail_id`
3. Ensure profile save endpoint uses validation result

### **If API Calls Fail**
1. Verify API key is valid and not expired
2. Check rate limiting (2 requests/second)
3. Test API endpoints directly with curl
4. Review PSMA API documentation for changes

## 📋 **Final Validation Report**

After completing all checks, document:

```markdown
## Implementation Validation Report
**Date**: [Date]
**Developer**: [Name]
**Environment**: [Dev/Staging/Production]

### ✅ Passed Checks
- [List of passed checks]

### ❌ Failed Checks
- [List of failed checks with details]

### 🔧 Actions Taken
- [List of fixes applied]

### 📊 Results Summary
- PSMA Tables with Data: [X/10]
- ProfileAddress Records Linked: [X/Y]
- API Response Time: [Average]
- Error Rate: [Percentage]
```

## 🎯 **Success Criteria**

Implementation is considered successful when:
- [ ] All PSMA tables contain data after address operations
- [ ] ProfileAddress records are linked to PSMA data
- [ ] Address validation returns structured data with PSMA IDs
- [ ] Frontend address selection and saving works without errors
- [ ] Response times are within acceptable limits (< 3 seconds)
- [ ] No critical errors in backend logs

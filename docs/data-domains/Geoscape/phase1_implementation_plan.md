# GeoScape Phase 1 Implementation Plan

## 🎯 **Objective**
Implement Phase 1 of GeoScape address validation using working PSMA APIs and store all rich data in our database.

## ✅ **Working APIs Discovered**

### **1. Predictive API** - Address Search
- **Endpoint**: `https://api.psma.com.au/v1/predictive/address`
- **Method**: GET
- **Parameters**: `query`, `limit`
- **Authentication**: Simple API key
- **Returns**: Address suggestions with IDs

### **2. Addresses API** - Rich Address Details
- **Endpoint**: `https://api.psma.com.au/v1/addresses/{id}`
- **Method**: GET
- **Parameters**: Address ID
- **Authentication**: Simple API key
- **Returns**: 22+ fields of rich address data

## 📊 **Rich Data Available**

### **Core Address Fields**
- `addressId` - Unique PSMA identifier
- `addressRecordType` - Primary/Secondary
- `buildingsRolloutStatus` - RELEASED status

### **Geographic Data Links**
- `links.geo` - Geographic coordinates
- `links.localGovernmentArea` - Local government info
- `links.stateElectorate` - State electorate
- `links.commonwealthElectorate` - Federal electorate
- `links.asgsMain` - ABS Statistical Geography
- `links.asgsRemoteness` - Remoteness classification

### **Property Information**
- `relatedBuildingIds` - Associated building IDs
- `buildingsRolloutStatus` - Building data availability

## 🗄️ **Database Schema Design (Data Engineer Coordination)**

### **New Tables Required**

#### **1. PSMAAddressDetails**
```sql
CREATE TABLE PSMAAddressDetails (
    PSMAAddressDetailID INT IDENTITY(1,1) PRIMARY KEY,
    AddressID NVARCHAR(50) NOT NULL,  -- PSMA address ID
    AddressRecordType NVARCHAR(20),   -- Primary/Secondary
    BuildingsRolloutStatus NVARCHAR(20), -- RELEASED status
    RelatedBuildingIDs NVARCHAR(MAX), -- JSON array of building IDs
    CreatedDate DATETIME2 DEFAULT GETDATE(),
    UpdatedDate DATETIME2 DEFAULT GETDATE()
);
```

#### **2. PSMAAddressGeographicData**
```sql
CREATE TABLE PSMAAddressGeographicData (
    PSMAAddressGeoID INT IDENTITY(1,1) PRIMARY KEY,
    PSMAAddressDetailID INT FOREIGN KEY REFERENCES PSMAAddressDetails(PSMAAddressDetailID),
    GeographicDataType NVARCHAR(50),  -- geo, localGovernmentArea, etc.
    GeographicDataURL NVARCHAR(500),  -- API endpoint URL
    GeographicDataValue NVARCHAR(MAX), -- Actual data (JSON)
    CreatedDate DATETIME2 DEFAULT GETDATE()
);
```

#### **3. PSMAAddressSearchHistory**
```sql
CREATE TABLE PSMAAddressSearchHistory (
    PSMASearchID INT IDENTITY(1,1) PRIMARY KEY,
    SearchQuery NVARCHAR(500) NOT NULL,
    SearchResults NVARCHAR(MAX),      -- JSON array of suggestions
    SelectedAddressID NVARCHAR(50),   -- User selected address ID
    SearchTimestamp DATETIME2 DEFAULT GETDATE(),
    UserID INT FOREIGN KEY REFERENCES Users(UserID)
);
```

### **Enhanced ProfileAddress Table**
```sql
-- Add new columns to existing ProfileAddress table
ALTER TABLE ProfileAddress ADD
    PSMAAddressDetailID INT FOREIGN KEY REFERENCES PSMAAddressDetails(PSMAAddressDetailID),
    PSMAAddressID NVARCHAR(50),       -- PSMA address identifier
    AddressValidationSource NVARCHAR(20) DEFAULT 'geoscape',
    ValidationConfidence DECIMAL(3,2), -- 0.00 to 1.00
    GeographicCoordinates NVARCHAR(100), -- lat,long format
    LocalGovernmentArea NVARCHAR(100),
    StateElectorate NVARCHAR(100),
    CommonwealthElectorate NVARCHAR(100),
    RemotenessClassification NVARCHAR(50);
```

## 🔄 **Implementation Workflow**

### **Phase 1A: Database Schema (Data Engineer)**
1. **Create new tables** for PSMA data storage
2. **Enhance ProfileAddress table** with PSMA fields
3. **Create SQLAlchemy models** for new tables
4. **Generate Alembic migration** for schema changes

### **Phase 1B: Service Layer Enhancement**
1. **Update GeoscapeService** to use both APIs
2. **Implement two-step process**: Search → Get Details
3. **Add data parsing** for all 22+ fields
4. **Implement caching** for performance

### **Phase 1C: API Integration**
1. **Update address validation endpoints** to use new service
2. **Store rich data** in database
3. **Return enhanced responses** with geographic data
4. **Add error handling** and user feedback

## 🚀 **Implementation Steps**

### **Step 1: Coordinate with Data Engineer**
- [ ] Design database schema for PSMA data
- [ ] Create SQLAlchemy models
- [ ] Generate and apply Alembic migration
- [ ] Test database integration

### **Step 2: Enhance GeoscapeService**
- [ ] Update service to use both Predictive and Addresses APIs
- [ ] Implement two-step search process
- [ ] Add data parsing for all fields
- [ ] Implement caching and rate limiting

### **Step 3: Update API Endpoints**
- [ ] Modify address validation endpoints
- [ ] Store rich data in database
- [ ] Return enhanced responses
- [ ] Add comprehensive error handling

### **Step 4: Testing and Validation**
- [ ] Test with Anthony addresses
- [ ] Verify database storage
- [ ] Test error scenarios
- [ ] Performance testing

## 📋 **Success Criteria**

### **Functional Requirements**
- ✅ Address search returns suggestions with PSMA IDs
- ✅ Address validation retrieves full details
- ✅ All 22+ fields stored in database
- ✅ Geographic data available for mapping
- ✅ Error handling with user-friendly messages

### **Performance Requirements**
- ✅ Response time < 2 seconds
- ✅ Rate limiting (2 requests/second)
- ✅ Caching for repeated searches
- ✅ Database queries optimized

### **Data Quality Requirements**
- ✅ All PSMA data fields captured
- ✅ Data validation and sanitization
- ✅ Audit trail for searches
- ✅ Confidence scoring for matches

## 🔧 **Technical Implementation**

### **Enhanced GeoscapeService Methods**
```python
class GeoscapeService:
    async def search_addresses(self, query: str) -> List[AddressSuggestion]
    async def get_address_details(self, address_id: str) -> AddressDetails
    async def validate_address(self, address: str) -> AddressValidationResult
    async def store_address_data(self, details: AddressDetails) -> int
```

### **New Data Models**
```python
class PSMAAddressDetails(Base):
    __tablename__ = "PSMAAddressDetails"
    # ... model definition

class PSMAAddressGeographicData(Base):
    __tablename__ = "PSMAAddressGeographicData"
    # ... model definition
```

### **API Response Enhancement**
```python
class AddressValidationResponse:
    is_valid: bool
    confidence: float
    address_details: AddressDetails
    geographic_data: GeographicData
    psma_address_id: str
    validation_source: str
```

## 🎯 **Ready for Implementation**

**Phase 1 is ready to proceed** with:
- ✅ Working PSMA APIs identified
- ✅ Rich data fields documented
- ✅ Database schema designed
- ✅ Implementation plan complete

**Next Step**: Coordinate with Data Engineer to implement database schema and begin Phase 1A.

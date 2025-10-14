# GeoScape Domain - Architecture Notes

## Overview

This document captures architectural decisions, patterns, and considerations for the GeoScape address validation domain. It serves as a reference for current architecture and guides future development decisions.

## Current Architecture

### 1. Service Layer Architecture

#### **Service Hierarchy**
```
AddressValidationService (Unified Interface)
├── GeoscapeService (Australian Addresses)
├── SmartyStreetsService (US Addresses) - Planned
└── FallbackService (Basic Validation)
```

**Architecture Pattern**: **Facade Pattern** with **Strategy Pattern**

**Benefits:**
- ✅ **Unified Interface**: Single service interface for all providers
- ✅ **Provider Abstraction**: Easy to add new address providers
- ✅ **Fallback Support**: Graceful degradation when primary provider fails
- ✅ **Regional Routing**: Automatic provider selection based on country

**Current Implementation:**
```python
class AddressValidationService:
    def __init__(self):
        self.providers = {}
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize available API providers based on configuration."""
        if APIConfig.validate_geoscape_config():
            self.providers['geoscape'] = GeoscapeService()
        # Future: Add other providers
    
    async def validate_address(self, address: str, country: str = "AU") -> Dict:
        """Route to appropriate provider based on country."""
        provider_name = self._get_provider_for_country(country)
        provider = self.providers.get(provider_name)
        
        if provider:
            return await provider.validate_address(address)
        else:
            return self._create_fallback_response(address, country)
```

### 2. API Layer Architecture

#### **RESTful API Design**
```
/api/address/
├── GET /search - Address autocomplete
├── POST /validate - Address validation
├── POST /coordinates - Coordinate retrieval
└── GET /health - Health check
```

**Architecture Pattern**: **REST API** with **Resource-Oriented Design**

**Design Principles:**
- ✅ **Resource-Based URLs**: Clear resource identification
- ✅ **HTTP Method Semantics**: Proper use of GET, POST
- ✅ **Consistent Response Format**: Standardized JSON responses
- ✅ **Error Handling**: Consistent error response structure

**Current Implementation:**
```python
@router.post("/validate", response_model=AddressValidationResponse)
async def validate_address(
    request_data: AddressValidationRequest,
    request: Request = None,
    db: Session = Depends(get_db_session)
):
    """Validate and geocode an address."""
    try:
        address_service = AddressValidationService()
        validation_result = await address_service.validate_address(
            address=request_data.address,
            property_id=request_data.property_id,
            country=request_data.country
        )
        return AddressValidationResponse(**validation_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 3. Data Layer Architecture

#### **Database Schema Design**
```
ProfileAddress (Core Address Data)
├── Standard Address Fields
├── GeoScape Integration Fields
└── Validation Metadata

APIUsageTracking (Usage Analytics)
├── API Call Metrics
├── Performance Data
└── Billing Information
```

**Architecture Pattern**: **Repository Pattern** with **Active Record**

**Design Decisions:**
- ✅ **Normalized Schema**: Proper normalization for data integrity
- ✅ **Audit Trail**: Complete tracking of address validation history
- ✅ **Performance Optimization**: Indexed fields for common queries
- ✅ **Extensibility**: Flexible schema for future enhancements

### 4. External API Integration

#### **Geoscape API Integration**
```
GeoscapeService
├── Authentication Layer
├── Request/Response Handling
├── Error Management
└── Data Transformation
```

**Architecture Pattern**: **Adapter Pattern** with **Circuit Breaker**

**Integration Features:**
- ✅ **Simple Authentication**: API key-based authentication
- ✅ **Retry Logic**: Exponential backoff for transient failures
- ✅ **Timeout Handling**: Configurable timeout values
- ✅ **Error Mapping**: Consistent error handling across providers

## Architectural Decisions

### 1. **Service Layer Separation**

**Decision**: Separate service layer from API layer

**Rationale:**
- **Testability**: Services can be unit tested independently
- **Reusability**: Services can be used by multiple API endpoints
- **Maintainability**: Clear separation of concerns
- **Scalability**: Services can be deployed independently

**Alternatives Considered:**
- ❌ **Monolithic API**: All logic in API endpoints
- ❌ **Direct Database Access**: API endpoints directly accessing database

### 2. **Provider Abstraction**

**Decision**: Abstract address providers behind unified interface

**Rationale:**
- **Flexibility**: Easy to add new address providers
- **Reliability**: Fallback options when primary provider fails
- **Regional Support**: Different providers for different regions
- **Vendor Independence**: Not locked into single provider

**Alternatives Considered:**
- ❌ **Direct Provider Integration**: Hard-coded provider calls
- ❌ **Single Provider**: Only Geoscape for all addresses

### 3. **Database Schema Design**

**Decision**: Separate address storage from usage tracking

**Rationale:**
- **Data Integrity**: Address data separate from operational data
- **Performance**: Optimized queries for different use cases
- **Compliance**: Easier to implement data retention policies
- **Analytics**: Dedicated table for usage analytics

**Alternatives Considered:**
- ❌ **Single Table**: All data in one table
- ❌ **No Usage Tracking**: No tracking of API usage

### 4. **Error Handling Strategy**

**Decision**: Graceful degradation with user-friendly messages

**Rationale:**
- **User Experience**: Users can continue even when validation fails
- **Reliability**: System remains functional during provider outages
- **Debugging**: Clear error messages for troubleshooting
- **Monitoring**: Structured error logging for monitoring

**Alternatives Considered:**
- ❌ **Fail Fast**: Return errors immediately
- ❌ **Silent Failures**: Hide errors from users

## Performance Architecture

### 1. **Response Time Optimization**

**Current Performance Targets:**
- **Address Search**: < 500ms
- **Address Validation**: < 800ms
- **Coordinates Retrieval**: < 600ms

**Optimization Strategies:**
```python
# Async Processing
async def validate_address(self, address: str) -> Dict:
    # Non-blocking external API calls
    response = await self._make_request(endpoint, params)
    return self._standardize_response(response)

# Connection Pooling
async def _make_request(self, endpoint: str, params: Dict) -> Dict:
    async with httpx.AsyncClient(timeout=self.timeout) as client:
        response = await client.get(url, headers=headers, params=params)
        return response.json()
```

### 2. **Caching Strategy**

**Current Caching:**
- **Mock Data**: Development/testing with realistic mock responses
- **No Production Caching**: Direct API calls to Geoscape

**Planned Caching:**
```python
# Redis-based caching
class CachedGeoscapeService:
    def __init__(self):
        self.cache = redis.Redis()
        self.cache_ttl = 3600  # 1 hour
    
    async def validate_address(self, address: str) -> Dict:
        cache_key = f"address_validation:{hash(address)}"
        
        # Check cache first
        cached_result = await self.cache.get(cache_key)
        if cached_result:
            return json.loads(cached_result)
        
        # Call external API
        result = await self._call_geoscape_api(address)
        
        # Cache result
        await self.cache.setex(cache_key, self.cache_ttl, json.dumps(result))
        return result
```

### 3. **Database Optimization**

**Current Indexing:**
```sql
-- Basic indexes
CREATE INDEX IX_ProfileAddress_PropertyID ON ProfileAddress(PropertyID);
CREATE INDEX IX_APIUsageTracking_Provider_Date ON APIUsageTracking(APIProvider, CreatedAt);
```

**Planned Optimizations:**
```sql
-- Spatial indexing for coordinate queries
CREATE SPATIAL INDEX IX_ProfileAddress_Coordinates ON ProfileAddress(Latitude, Longitude);

-- Composite indexes for common queries
CREATE INDEX IX_ProfileAddress_State_Postcode ON ProfileAddress(State, Postcode);
CREATE INDEX IX_APIUsageTracking_Status_Date ON APIUsageTracking(ResponseStatus, CreatedAt);
```

## Security Architecture

### 1. **Authentication & Authorization**

**Current Security:**
- **API Key Authentication**: Simple API key for Geoscape
- **No User Authentication**: Public API endpoints

**Security Considerations:**
```python
# API Key Management
class SecureGeoscapeService:
    def __init__(self):
        self.api_key = self._get_api_key_from_vault()
        self.consumer_secret = self._get_consumer_secret_from_vault()
    
    def _get_api_key_from_vault(self) -> str:
        # Secure key retrieval from Azure Key Vault
        return key_vault_client.get_secret("geoscape-api-key")
```

### 2. **Data Protection**

**Current Protection:**
- **HTTPS**: All API communications encrypted
- **Input Validation**: Basic input validation
- **Error Logging**: Structured error logging

**Enhanced Protection:**
```python
# Address Anonymization
def anonymize_address_for_logging(address: str) -> str:
    """Anonymize address data for logging purposes."""
    parts = address.split(',')
    if len(parts) >= 2:
        street_part = parts[0]
        street_words = street_part.split()
        if len(street_words) >= 2:
            street_words[0] = 'XX'  # Anonymize street number
            anonymized_street = ' '.join(street_words)
            return f"{anonymized_street}, {', '.join(parts[1:])}"
    return "ANONYMIZED"
```

## Scalability Architecture

### 1. **Horizontal Scaling**

**Current Scaling:**
- **Single Instance**: Single FastAPI application instance
- **Database Scaling**: Azure SQL Database with auto-scaling

**Scaling Strategy:**
```python
# Load Balancing Ready
class AddressValidationService:
    def __init__(self):
        # Stateless service design
        self.providers = {}
        self._initialize_providers()
    
    async def validate_address(self, address: str, country: str = "AU") -> Dict:
        # Stateless operation - can be scaled horizontally
        provider = self._get_provider(country)
        return await provider.validate_address(address)
```

### 2. **Database Scaling**

**Current Database:**
- **Azure SQL Database**: Managed database service
- **Auto-scaling**: Automatic performance scaling

**Scaling Considerations:**
```sql
-- Read Replicas for Analytics
-- Primary: Write operations
-- Replica: Read operations for analytics

-- Table Partitioning for Large Datasets
CREATE PARTITION FUNCTION PF_AddressByDate (datetime)
AS RANGE RIGHT FOR VALUES ('2025-01-01', '2025-02-01', '2025-03-01');

CREATE PARTITION SCHEME PS_AddressByDate
AS PARTITION PF_AddressByDate TO (FG1, FG2, FG3, FG4);
```

## Monitoring Architecture

### 1. **Application Monitoring**

**Current Monitoring:**
- **Structured Logging**: JSON-formatted logs
- **API Usage Tracking**: Database-based usage tracking
- **Error Logging**: Comprehensive error logging

**Monitoring Strategy:**
```python
# Comprehensive Monitoring
class MonitoredAddressService:
    async def validate_address(self, address: str) -> Dict:
        start_time = time.time()
        
        try:
            result = await self._validate_address_internal(address)
            
            # Log success metrics
            self._log_success_metrics(start_time, address)
            return result
            
        except Exception as e:
            # Log error metrics
            self._log_error_metrics(start_time, address, e)
            raise
```

### 2. **Performance Monitoring**

**Key Metrics:**
- **Response Time**: Average response time per endpoint
- **Error Rate**: Percentage of failed requests
- **Throughput**: Requests per second
- **Cache Hit Rate**: Percentage of cached responses

**Alerting Strategy:**
```python
# Performance Alerts
class PerformanceMonitor:
    def __init__(self):
        self.alert_thresholds = {
            'response_time_ms': 2000,  # 2 seconds
            'error_rate_percent': 5,   # 5% error rate
            'cache_hit_rate_percent': 80  # 80% cache hit rate
        }
    
    def check_performance_metrics(self, metrics: Dict):
        if metrics['avg_response_time'] > self.alert_thresholds['response_time_ms']:
            self._send_alert("High response time detected")
```

## Future Architecture Considerations

### 1. **Microservices Architecture**

**Potential Migration:**
```
Current: Monolithic FastAPI Application
├── Address Validation Service
├── User Management Service
├── Resume Processing Service
└── Skills Management Service

Future: Microservices Architecture
├── Address-Service (Dedicated)
├── User-Service
├── Resume-Service
└── Skills-Service
```

**Benefits:**
- **Independent Scaling**: Scale address service independently
- **Technology Diversity**: Use different technologies per service
- **Fault Isolation**: Service failures don't affect others
- **Team Autonomy**: Independent development teams

### 2. **Event-Driven Architecture**

**Potential Implementation:**
```python
# Event-Driven Address Validation
class EventDrivenAddressService:
    async def validate_address(self, address: str) -> Dict:
        # Publish validation event
        await self.event_bus.publish("address.validation.requested", {
            "address": address,
            "timestamp": datetime.now(),
            "request_id": str(uuid.uuid4())
        })
        
        # Return immediate response with request ID
        return {"request_id": request_id, "status": "processing"}
    
    async def handle_validation_completed(self, event: Dict):
        # Handle completed validation
        await self.notify_user(event["request_id"], event["result"])
```

### 3. **GraphQL Integration**

**Potential Benefits:**
- **Flexible Queries**: Clients can request only needed data
- **Reduced Over-fetching**: Optimize data transfer
- **Real-time Updates**: Subscription-based updates
- **Schema Evolution**: Backward-compatible API changes

**Implementation Considerations:**
```python
# GraphQL Schema
type Address {
  streetNumber: String
  streetName: String!
  suburb: String!
  state: String!
  postcode: String!
  coordinates: Coordinates
  validation: ValidationInfo
}

type Query {
  validateAddress(address: String!): Address
  searchAddresses(query: String!, limit: Int): [Address]
}
```

## Architecture Trade-offs

### 1. **Simplicity vs. Flexibility**

**Current Choice**: Simplicity
- **Pros**: Easy to understand, maintain, and debug
- **Cons**: Limited flexibility for complex use cases

**Future Consideration**: Increased flexibility
- **Pros**: Support for complex address validation scenarios
- **Cons**: Increased complexity and maintenance overhead

### 2. **Performance vs. Reliability**

**Current Choice**: Reliability
- **Pros**: Graceful degradation, comprehensive error handling
- **Cons**: Potential performance overhead

**Future Consideration**: Performance optimization
- **Pros**: Faster response times, better user experience
- **Cons**: Potential reliability trade-offs

### 3. **Centralization vs. Distribution**

**Current Choice**: Centralization
- **Pros**: Simple deployment, easy monitoring
- **Cons**: Single point of failure, scaling limitations

**Future Consideration**: Distribution
- **Pros**: Better scalability, fault tolerance
- **Cons**: Increased complexity, operational overhead

## Conclusion

The current GeoScape domain architecture provides a solid foundation for address validation services. The service layer separation, provider abstraction, and comprehensive error handling create a maintainable and extensible system.

Key architectural strengths:
1. **Clear Separation of Concerns**: Service, API, and data layers are well-defined
2. **Provider Flexibility**: Easy to add new address validation providers
3. **Error Resilience**: Graceful degradation and comprehensive error handling
4. **Monitoring Ready**: Structured logging and usage tracking

Future architectural improvements should focus on:
1. **Performance Optimization**: Caching, database optimization, and async processing
2. **Scalability**: Horizontal scaling and microservices architecture
3. **Security Enhancement**: Advanced authentication and data protection
4. **Monitoring Enhancement**: Real-time monitoring and alerting

The architecture is designed to evolve with the growing needs of the address validation domain while maintaining simplicity and reliability.

---

*Last Updated: 2025-01-21*
*Architecture Version: 1.0*
*Next Review: 2025-02-21*


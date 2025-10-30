# Epic 2 Story 0: Enhanced Diagnostic Logging System Implementation

**Story ID:** Epic 2.0.0  
**Priority:** CRITICAL - Foundation Story  
**Estimated Effort:** 2-3 days  
**Dependencies:** None  

---

## 🎯 **Story Overview**

**As a** developer and BMAD agent  
**I want to** implement an enhanced diagnostic logging system with comprehensive visibility  
**So that** I can debug issues faster, validate implementations, and monitor system performance throughout Epic 2 development  

---

## 📋 **Detailed Implementation Plan**

### **Phase 1: Database Schema Implementation (Day 1)**

#### **1.1 Enhanced Existing Tables**
```sql
-- Enhance ApiRequest table
ALTER TABLE log.ApiRequest ADD
    RequestPayload NVARCHAR(MAX) NULL,
    ResponsePayload NVARCHAR(MAX) NULL,
    Headers NVARCHAR(MAX) NULL,
    QueryParams NVARCHAR(MAX) NULL;

-- Enhance ApplicationError table
ALTER TABLE log.ApplicationError ADD
    StackTrace NVARCHAR(MAX) NULL,
    ExceptionType NVARCHAR(100) NULL;

-- Enhance AuthEvent table
ALTER TABLE log.AuthEvent ADD
    UserAgent NVARCHAR(500) NULL,
    SessionID NVARCHAR(100) NULL;

-- Enhance EmailDelivery table
ALTER TABLE log.EmailDelivery ADD
    ProviderResponse NVARCHAR(MAX) NULL,
    RetryCount INT NOT NULL DEFAULT 0;
```

#### **1.2 New Epic 2 Logging Tables**
```sql
-- User Action logging
CREATE TABLE log.UserAction (
    UserActionID BIGINT IDENTITY(1,1) PRIMARY KEY,
    UserID BIGINT NOT NULL,
    Action NVARCHAR(100) NOT NULL,
    Details NVARCHAR(MAX) NULL,
    Path NVARCHAR(500) NULL,
    RequestID NVARCHAR(100) NULL,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (UserID) REFERENCES dbo.User(UserID)
);

-- Performance Metric logging
CREATE TABLE log.PerformanceMetric (
    PerformanceMetricID BIGINT IDENTITY(1,1) PRIMARY KEY,
    MetricType NVARCHAR(50) NOT NULL,
    Endpoint NVARCHAR(500) NULL,
    Value DECIMAL(10,2) NOT NULL,
    StatusCode INT NULL,
    UserID BIGINT NULL,
    Details NVARCHAR(MAX) NULL,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (UserID) REFERENCES dbo.User(UserID)
);

-- Integration Event logging
CREATE TABLE log.IntegrationEvent (
    IntegrationEventID BIGINT IDENTITY(1,1) PRIMARY KEY,
    EventType NVARCHAR(100) NOT NULL,
    SourceDomain NVARCHAR(50) NOT NULL,
    TargetDomain NVARCHAR(50) NOT NULL,
    EntityID BIGINT NULL,
    Details NVARCHAR(MAX) NULL,
    UserID BIGINT NULL,
    RequestID NVARCHAR(100) NULL,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (UserID) REFERENCES dbo.User(UserID)
);

-- Approval Audit Trail (already exists from Epic 2 schema)
-- This table should already be created by Solomon's migrations
```

#### **1.3 Database Indexes**
```sql
-- Performance indexes for new tables
CREATE INDEX IX_UserAction_UserID_CreatedDate ON log.UserAction(UserID, CreatedDate);
CREATE INDEX IX_UserAction_Action_CreatedDate ON log.UserAction(Action, CreatedDate);
CREATE INDEX IX_PerformanceMetric_MetricType_CreatedDate ON log.PerformanceMetric(MetricType, CreatedDate);
CREATE INDEX IX_PerformanceMetric_Value_CreatedDate ON log.PerformanceMetric(Value, CreatedDate);
CREATE INDEX IX_IntegrationEvent_EventType_CreatedDate ON log.IntegrationEvent(EventType, CreatedDate);
CREATE INDEX IX_IntegrationEvent_SourceDomain_CreatedDate ON log.IntegrationEvent(SourceDomain, CreatedDate);
```

### **Phase 2: Backend Implementation (Day 1-2)**

#### **2.1 Enhanced Request Logger Middleware**
```python
# backend/middleware/enhanced_request_logger.py
class EnhancedRequestLogger:
    def __init__(self, db: Session):
        self.db = db
    
    def log_request(self, request: Request, response: Response, duration_ms: int):
        """Enhanced API request logging with payloads"""
        api_request = ApiRequest(
            Method=request.method,
            Path=request.url.path,
            StatusCode=response.status_code,
            DurationMs=duration_ms,
            RequestID=request.state.request_id,
            UserID=request.state.user_id,
            CreatedDate=datetime.utcnow(),
            # Enhanced payload logging
            RequestPayload=self._sanitize_payload(self._get_request_payload(request)),
            ResponsePayload=self._sanitize_payload(self._get_response_payload(response)),
            Headers=json.dumps(dict(request.headers)),
            QueryParams=json.dumps(dict(request.query_params))
        )
        
        self.db.add(api_request)
        self.db.commit()
    
    def _sanitize_payload(self, payload: dict) -> str:
        """Remove sensitive data from payloads"""
        if not payload:
            return None
        
        sensitive_fields = ['password', 'token', 'secret', 'key', 'authorization']
        sanitized = self._remove_sensitive_fields(payload, sensitive_fields)
        return json.dumps(sanitized)
```

#### **2.2 Enhanced Error Logger**
```python
# backend/middleware/enhanced_error_logger.py
class EnhancedErrorLogger:
    def __init__(self, db: Session):
        self.db = db
    
    def log_error(self, error: Exception, request: Request, user_id: int = None):
        """Enhanced error logging with stack traces"""
        app_error = ApplicationError(
            ErrorType=type(error).__name__,
            ErrorMessage=str(error),
            Severity='ERROR',
            Path=request.url.path,
            Method=request.method,
            RequestID=request.state.request_id,
            UserID=user_id,
            CreatedDate=datetime.utcnow(),
            StackTrace=traceback.format_exc(),
            ExceptionType=type(error).__name__
        )
        
        self.db.add(app_error)
        self.db.commit()
```

#### **2.3 New Logging Services**
```python
# backend/services/user_action_logger.py
class UserActionLogger:
    def __init__(self, db: Session):
        self.db = db
    
    def log_theme_change(self, user_id: int, old_theme: str, new_theme: str, request_id: str = None):
        """Log theme preference changes"""
        action = UserAction(
            UserID=user_id,
            Action='THEME_CHANGED',
            Details=json.dumps({
                'old_theme': old_theme,
                'new_theme': new_theme,
                'component': 'ThemeSelector'
            }),
            Path='/api/users/preferences',
            RequestID=request_id,
            CreatedDate=datetime.utcnow()
        )
        
        self.db.add(action)
        self.db.commit()

# backend/services/performance_logger.py
class PerformanceLogger:
    def __init__(self, db: Session):
        self.db = db
    
    def log_api_performance(self, endpoint: str, duration_ms: int, status_code: int, user_id: int = None):
        """Log API performance metrics"""
        if duration_ms > 1000:  # Log slow requests
            perf_metric = PerformanceMetric(
                MetricType='API_RESPONSE_TIME',
                Endpoint=endpoint,
                Value=duration_ms,
                StatusCode=status_code,
                UserID=user_id,
                CreatedDate=datetime.utcnow()
            )
            
            self.db.add(perf_metric)
            self.db.commit()

# backend/services/integration_logger.py
class IntegrationLogger:
    def __init__(self, db: Session):
        self.db = db
    
    def log_theme_integration(self, user_id: int, theme: str, affected_components: list, request_id: str = None):
        """Log theme changes affecting multiple components"""
        integration_event = IntegrationEvent(
            EventType='THEME_CHANGE_PROPAGATION',
            SourceDomain='User',
            TargetDomain='UI',
            EntityID=user_id,
            Details=json.dumps({
                'theme': theme,
                'affected_components': affected_components
            }),
            UserID=user_id,
            RequestID=request_id,
            CreatedDate=datetime.utcnow()
        )
        
        self.db.add(integration_event)
        self.db.commit()
```

### **Phase 3: Frontend Implementation (Day 2)**

#### **3.1 Enhanced Error Boundary**
```typescript
// frontend/src/components/ErrorBoundary.tsx
class EnhancedErrorBoundary extends React.Component {
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log to ApplicationError table
    this.logError({
      ErrorType: error.name,
      ErrorMessage: error.message,
      Severity: 'ERROR',
      Path: window.location.pathname,
      Method: 'GET',
      RequestID: this.getCurrentRequestId(),
      UserID: this.getCurrentUserId(),
      StackTrace: error.stack,
      ExceptionType: error.constructor.name,
      CreatedDate: new Date().toISOString()
    });
  }
  
  private async logError(errorData: any) {
    try {
      await api.post('/logs/application-error', errorData);
    } catch (logError) {
      console.error('Failed to log error:', logError);
    }
  }
}
```

#### **3.2 User Action Logging Hook**
```typescript
// frontend/src/hooks/useUserAction.ts
export const useUserAction = () => {
  const logUserAction = async (action: string, details: any = {}) => {
    try {
      await api.post('/logs/user-action', {
        Action: action,
        Details: JSON.stringify(details),
        Path: window.location.pathname,
        UserID: getCurrentUserId(),
        CreatedDate: new Date().toISOString()
      });
    } catch (error) {
      console.error('Failed to log user action:', error);
    }
  };
  
  return { logUserAction };
};
```

### **Phase 4: Enhanced Diagnostic Tool (Day 2-3)**

#### **4.1 Enhanced Diagnostic Tool Implementation**
The enhanced diagnostic tool (`backend/enhanced_diagnostic_logs.py`) is already created and includes:
- Comprehensive log analysis across all tables
- Correlation analysis for failed requests
- Performance metrics analysis
- Agent integration commands

#### **4.2 Agent Integration Testing**
- Test diagnostic tool with all BMAD agents
- Verify agent rules are working correctly
- Test logging validation in story completion

### **Phase 5: Testing and Validation (Day 3)**

#### **5.1 Database Testing**
- Verify all tables are created correctly
- Test indexes for performance
- Validate foreign key relationships

#### **5.2 Logging Testing**
- Test enhanced API request logging
- Test error logging with stack traces
- Test user action logging
- Test performance metric logging
- Test integration event logging

#### **5.3 Diagnostic Tool Testing**
- Test all diagnostic tool commands
- Verify correlation analysis works
- Test performance metrics analysis
- Test agent integration

---

## 🎯 **Acceptance Criteria Validation**

### **Enhanced Logging Tables**
- [ ] ApiRequest table enhanced with payload fields
- [ ] ApplicationError table enhanced with stack trace fields
- [ ] AuthEvent table enhanced with user agent fields
- [ ] EmailDelivery table enhanced with provider response fields
- [ ] UserAction table created and functional
- [ ] PerformanceMetric table created and functional
- [ ] IntegrationEvent table created and functional
- [ ] ApprovalAuditTrail table accessible (from Epic 2 schema)

### **Enhanced Logging Services**
- [ ] Enhanced request logger captures all required data
- [ ] Enhanced error logger captures stack traces
- [ ] User action logger functional for theme changes
- [ ] Performance logger functional for slow operations
- [ ] Integration logger functional for cross-domain events

### **Frontend Logging Integration**
- [ ] Enhanced error boundary logs to database
- [ ] User action hook functional
- [ ] Theme changes logged as user actions
- [ ] Cross-domain events logged as integration events

### **Diagnostic Tool**
- [ ] Enhanced diagnostic tool runs without errors
- [ ] All log tables accessible via diagnostic tool
- [ ] Correlation analysis functional
- [ ] Performance metrics analysis functional
- [ ] Agent integration commands working

### **Agent Integration**
- [ ] Developer agent uses diagnostic logs automatically
- [ ] Architect agent uses diagnostic logs for analysis
- [ ] Story completion validation includes logging checks
- [ ] All agents have access to diagnostic tool commands

---

## 🚀 **Implementation Timeline**

### **Day 1: Database and Backend Foundation**
- Morning: Database schema implementation and migration
- Afternoon: Enhanced logging middleware and services

### **Day 2: Frontend and Diagnostic Tool**
- Morning: Frontend logging integration
- Afternoon: Enhanced diagnostic tool testing and agent integration

### **Day 3: Testing and Validation**
- Morning: Comprehensive testing of all logging features
- Afternoon: Agent integration testing and validation

---

## 📊 **Success Metrics**

### **Logging Coverage**
- [ ] 100% of API requests logged with payloads
- [ ] 100% of errors logged with stack traces
- [ ] 100% of user actions logged for Epic 2 features
- [ ] 100% of performance metrics logged for slow operations

### **Agent Effectiveness**
- [ ] Agents can debug 90% of issues using diagnostic logs
- [ ] Average debugging time reduced by 50%
- [ ] Error resolution time improved by 40%
- [ ] Story validation includes logging verification

### **System Performance**
- [ ] Logging adds <5ms to API response time
- [ ] Diagnostic tool runs in <2 seconds
- [ ] Log storage grows <1GB per month
- [ ] All logging operations complete successfully

---

**This enhanced logging system will provide the foundation for successful Epic 2 development with complete visibility and debugging capabilities!** 🚀

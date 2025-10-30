# Epic 2 Logging Strategy - Agent Visibility & Debugging

**Author:** Winston (System Architect)  
**Date:** 2025-01-15  
**Purpose:** Comprehensive logging strategy for Epic 2 development with enhanced agent visibility  

---

## 🎯 **Logging Philosophy**

**"Log Everything, Debug Anything"** - Every user action, API call, error, and system event should be logged to provide complete visibility for BMAD agents during development and troubleshooting.

---

## 📊 **Enhanced Logging Tables (Epic 2)**

### **Existing Epic 1 Tables (Enhanced)**

| Table | Purpose | Epic 2 Enhancements |
|-------|---------|-------------------|
| `log.AuthEvent` | Authentication events | Add UserAgent, SessionID |
| `log.ApplicationError` | Frontend/Backend errors | Add StackTrace, ExceptionType |
| `log.ApiRequest` | API request/response | **Add RequestPayload, ResponsePayload, Headers, QueryParams** |
| `log.EmailDelivery` | Email sending events | Add ProviderResponse, RetryCount |

### **New Epic 2 Tables**

| Table | Purpose | When to Use |
|-------|---------|-------------|
| `audit.ApprovalAuditTrail` | Approval workflow actions | Every approval decision, comment, status change |
| `log.UserAction` | User interface actions | Theme changes, preference updates, navigation |
| `log.PerformanceMetric` | Performance monitoring | Slow queries, API response times, frontend render times |
| `log.IntegrationEvent` | Cross-domain events | Theme changes affecting components, approval notifications |

---

## 🔧 **Enhanced Diagnostic Tool Usage**

### **Basic Usage (Epic 1 Pattern)**
```bash
# Get last 5 entries from each table
python backend/enhanced_diagnostic_logs.py

# Get last 10 entries
python backend/enhanced_diagnostic_logs.py --limit 10

# Analyze specific request
python backend/enhanced_diagnostic_logs.py --request-id "req_12345"
```

### **Advanced Usage (Epic 2 Features)**
```bash
# Performance analysis (last 48 hours)
python backend/enhanced_diagnostic_logs.py --performance-hours 48

# Focus on specific request with full correlation
python backend/enhanced_diagnostic_logs.py --request-id "req_12345" --limit 20
```

### **Agent Integration Commands**
```bash
# Quick error check (last 3 entries)
python backend/enhanced_diagnostic_logs.py --limit 3

# Full diagnostic for complex issues
python backend/enhanced_diagnostic_logs.py --limit 10 --performance-hours 24
```

---

## 🎯 **When to Use Diagnostic Logs**

### **For BMAD Agents - Use Diagnostic Logs When:**

1. **Authentication Issues**
   - User can't login/signup
   - JWT token problems
   - Email verification failures
   - Password reset issues

2. **API Errors**
   - 4xx/5xx status codes
   - Slow API responses
   - Request/response payload issues
   - CORS or header problems

3. **Frontend Errors**
   - Component rendering failures
   - State management issues
   - Theme switching problems
   - Real-time update failures

4. **Epic 2 Specific Issues**
   - Approval workflow problems
   - Cross-domain integration failures
   - Performance degradation
   - Audit trail missing entries

5. **Email Delivery Problems**
   - Invitation emails not sent
   - Notification delivery failures
   - Email template rendering issues

### **For Developers - Use Diagnostic Logs When:**

1. **Debugging User Stories**
   - Story implementation not working
   - Integration between components failing
   - Data not flowing correctly

2. **Performance Investigation**
   - Slow dashboard loading
   - Theme switching delays
   - Real-time update lag

3. **Testing Validation**
   - End-to-end test failures
   - Regression testing issues
   - Cross-browser compatibility

---

## 📝 **Logging Implementation Guidelines**

### **1. API Request Logging (Enhanced)**

**Backend Implementation:**
```python
# In middleware/request_logger.py
class EnhancedRequestLogger:
    def log_request(self, request: Request, response: Response, duration_ms: int):
        # Log basic request info
        api_request = ApiRequest(
            Method=request.method,
            Path=request.url.path,
            StatusCode=response.status_code,
            DurationMs=duration_ms,
            RequestID=request.state.request_id,
            UserID=request.state.user_id,
            CreatedDate=datetime.utcnow(),
            # NEW: Enhanced payload logging
            RequestPayload=self._sanitize_payload(request.json()) if request.json() else None,
            ResponsePayload=self._sanitize_payload(response.json()) if response.json() else None,
            Headers=json.dumps(dict(request.headers)),
            QueryParams=json.dumps(dict(request.query_params))
        )
        
        self.db.add(api_request)
        self.db.commit()
    
    def _sanitize_payload(self, payload: dict) -> str:
        """Remove sensitive data from payloads"""
        if not payload:
            return None
        
        # Remove sensitive fields
        sensitive_fields = ['password', 'token', 'secret', 'key']
        sanitized = self._remove_sensitive_fields(payload, sensitive_fields)
        
        return json.dumps(sanitized)
```

### **2. Application Error Logging (Enhanced)**

**Frontend Implementation:**
```typescript
// In ErrorBoundary.tsx
class EnhancedErrorBoundary extends React.Component {
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log to ApplicationError table
    this.logError({
      ErrorType: error.name,
      ErrorMessage: error.message,
      Severity: 'ERROR',
      Path: window.location.pathname,
      Method: 'GET', // or from current request
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

### **3. Epic 2 Audit Trail Logging**

**Backend Implementation:**
```python
# In services/audit_service.py
class Epic2AuditService:
    def log_approval_action(self, entity_type: str, entity_id: int, action: str, 
                          user_id: int = None, external_email: str = None, 
                          comments: str = None):
        """Log approval workflow actions"""
        audit_record = ApprovalAuditTrail(
            EntityType=entity_type,
            EntityID=entity_id,
            Action=action,
            UserID=user_id,
            ExternalApproverEmail=external_email,
            Comments=comments,
            CreatedDate=datetime.utcnow()
        )
        
        self.db.add(audit_record)
        self.db.commit()
    
    def log_theme_change(self, user_id: int, old_theme: str, new_theme: str):
        """Log theme preference changes"""
        self.log_approval_action(
            entity_type="User",
            entity_id=user_id,
            action="THEME_CHANGED",
            user_id=user_id,
            comments=f"Changed from {old_theme} to {new_theme}"
        )
    
    def log_approval_decision(self, request_id: int, decision: str, 
                            approver_id: int, comments: str = None):
        """Log approval decisions"""
        self.log_approval_action(
            entity_type="CompanySwitchRequest",
            entity_id=request_id,
            action=f"APPROVAL_{decision.upper()}",
            user_id=approver_id,
            comments=comments
        )
```

### **4. User Action Logging (New)**

**Frontend Implementation:**
```typescript
// In hooks/useUserAction.ts
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

// Usage in components
const ThemeSelector = () => {
  const { logUserAction } = useUserAction();
  
  const handleThemeChange = async (newTheme: string) => {
    // Update theme
    await updateTheme(newTheme);
    
    // Log the action
    await logUserAction('THEME_CHANGED', {
      oldTheme: currentTheme,
      newTheme: newTheme,
      component: 'ThemeSelector'
    });
  };
  
  return (
    // Component JSX
  );
};
```

### **5. Performance Metric Logging (New)**

**Backend Implementation:**
```python
# In middleware/performance_logger.py
class PerformanceLogger:
    def log_api_performance(self, endpoint: str, duration_ms: int, 
                          status_code: int, user_id: int = None):
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
    
    def log_database_query(self, query: str, duration_ms: int, 
                          row_count: int = None):
        """Log slow database queries"""
        if duration_ms > 500:  # Log slow queries
            perf_metric = PerformanceMetric(
                MetricType='DATABASE_QUERY_TIME',
                Endpoint=query[:100],  # Truncate long queries
                Value=duration_ms,
                Details=json.dumps({'row_count': row_count}),
                CreatedDate=datetime.utcnow()
            )
            
            self.db.add(perf_metric)
            self.db.commit()
```

---

## 🤖 **Agent Integration Guide**

### **For BMAD Agents - How to Use Diagnostic Logs**

1. **When Debugging Stories:**
   ```bash
   # Run diagnostic after implementing a story
   python backend/enhanced_diagnostic_logs.py --limit 5
   
   # Look for errors related to your story
   # Check API requests for your new endpoints
   # Verify audit trail entries for user actions
   ```

2. **When Testing Integration:**
   ```bash
   # Run diagnostic after testing cross-domain features
   python backend/enhanced_diagnostic_logs.py --limit 10
   
   # Check for IntegrationEvent logs
   # Verify UserAction logs for theme changes
   # Look for PerformanceMetric logs for slow operations
   ```

3. **When Troubleshooting Issues:**
   ```bash
   # Get specific request analysis
   python backend/enhanced_diagnostic_logs.py --request-id "req_12345"
   
   # Check performance over time
   python backend/enhanced_diagnostic_logs.py --performance-hours 48
   ```

### **Agent Logging Checklist**

**Before Implementing a Story:**
- [ ] Understand what logs should be generated
- [ ] Plan logging points in the implementation
- [ ] Consider error scenarios and logging needs

**During Implementation:**
- [ ] Add logging to all API endpoints
- [ ] Log user actions in frontend components
- [ ] Add audit trail entries for business logic
- [ ] Log performance metrics for slow operations

**After Implementation:**
- [ ] Run diagnostic logs to verify logging
- [ ] Test error scenarios and check error logs
- [ ] Verify audit trail completeness
- [ ] Check performance metrics

---

## 📈 **Monitoring and Observability Integration**

### **Azure Application Insights Integration**

**Backend Configuration:**
```python
# In core/config.py
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

# Configure Azure Application Insights
def setup_azure_logging():
    logger = logging.getLogger(__name__)
    logger.addHandler(AzureLogHandler(
        connection_string=os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')
    ))
    
    # Custom properties for Epic 2
    logger.setLevel(logging.INFO)
    return logger

# Usage in services
class UserService:
    def __init__(self):
        self.logger = setup_azure_logging()
    
    def update_theme(self, user_id: int, theme: str):
        self.logger.info(f"User {user_id} changed theme to {theme}", extra={
            'user_id': user_id,
            'theme': theme,
            'action': 'theme_change',
            'epic': 'epic2'
        })
```

### **Custom Metrics Dashboard**

**Performance Monitoring:**
```python
# In services/metrics_service.py
class MetricsService:
    def track_theme_switching_performance(self, duration_ms: int):
        """Track theme switching performance"""
        if duration_ms > 500:  # Alert if slow
            self.logger.warning(f"Slow theme switching: {duration_ms}ms")
        
        # Log to PerformanceMetric table
        self.log_performance_metric(
            metric_type='THEME_SWITCHING_TIME',
            value=duration_ms,
            threshold=500
        )
    
    def track_approval_workflow_performance(self, workflow_id: int, duration_ms: int):
        """Track approval workflow performance"""
        self.log_performance_metric(
            metric_type='APPROVAL_WORKFLOW_TIME',
            value=duration_ms,
            details={'workflow_id': workflow_id}
        )
```

---

## 🚀 **Epic 2 Logging Implementation Plan**

### **Phase 1: Enhanced Existing Logs (Week 1)**
- [ ] Add RequestPayload/ResponsePayload to ApiRequest logging
- [ ] Add StackTrace to ApplicationError logging
- [ ] Add UserAgent to AuthEvent logging
- [ ] Update diagnostic tool to show enhanced data

### **Phase 2: New Epic 2 Logs (Week 2)**
- [ ] Implement ApprovalAuditTrail logging
- [ ] Add UserAction logging for theme changes
- [ ] Create IntegrationEvent logging for cross-domain events
- [ ] Add PerformanceMetric logging for slow operations

### **Phase 3: Agent Integration (Week 3)**
- [ ] Update all BMAD agents to use diagnostic tool
- [ ] Create logging checklists for each agent
- [ ] Add logging validation to story completion
- [ ] Create logging best practices documentation

### **Phase 4: Monitoring Integration (Week 4)**
- [ ] Integrate with Azure Application Insights
- [ ] Create custom metrics dashboard
- [ ] Set up alerting for critical errors
- [ ] Create performance monitoring reports

---

## 📋 **Logging Best Practices**

### **Do's ✅**
- Log every user action that changes state
- Log all API requests with payloads (sanitized)
- Log all errors with stack traces
- Log performance metrics for slow operations
- Use structured logging (JSON format)
- Include correlation IDs for request tracking
- Log business logic decisions in audit trail

### **Don'ts ❌**
- Don't log sensitive data (passwords, tokens)
- Don't log too frequently (avoid performance impact)
- Don't log without context (include user_id, request_id)
- Don't ignore log errors (handle logging failures gracefully)
- Don't log without purpose (every log should be actionable)

---

## 🔍 **Troubleshooting Guide**

### **Common Issues and Solutions**

1. **"No logs found"**
   - Check database connection
   - Verify table exists
   - Check date range (logs might be older)

2. **"Request payload too large"**
   - Implement payload truncation
   - Remove sensitive fields
   - Use compression for large payloads

3. **"Logging performance impact"**
   - Use async logging
   - Batch log writes
   - Implement log level filtering

4. **"Missing correlation data"**
   - Ensure RequestID is passed through all layers
   - Add correlation ID to all log entries
   - Verify request context is maintained

---

## 📊 **Success Metrics**

### **Logging Coverage**
- [ ] 100% of API endpoints logged
- [ ] 100% of user actions logged
- [ ] 100% of errors logged with stack traces
- [ ] 100% of approval decisions logged

### **Agent Effectiveness**
- [ ] Agents can debug 90% of issues using logs
- [ ] Average debugging time reduced by 50%
- [ ] Error resolution time improved by 40%

### **Performance Impact**
- [ ] Logging adds <5ms to API response time
- [ ] Log storage grows <1GB per month
- [ ] Diagnostic tool runs in <2 seconds

---

**This comprehensive logging strategy will provide BMAD agents with complete visibility into Epic 2 development, enabling faster debugging, better error resolution, and more effective story implementation.** 🚀

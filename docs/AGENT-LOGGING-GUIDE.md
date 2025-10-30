# BMAD Agent Logging Integration Guide

**Purpose:** Quick reference for BMAD agents on when and how to use diagnostic logs during Epic 2 development.

---

## 🚀 **Quick Start**

### **Basic Commands**
```bash
# Quick error check (last 5 entries)
python backend/enhanced_diagnostic_logs.py

# Detailed analysis (last 10 entries)
python backend/enhanced_diagnostic_logs.py --limit 10

# Analyze specific request
python backend/enhanced_diagnostic_logs.py --request-id "req_12345"
```

---

## 🎯 **When to Use Diagnostic Logs**

### **Always Use When:**
- ❌ **Story implementation fails** - Check for errors and API issues
- ❌ **User can't login/signup** - Check AuthEvent and ApplicationError
- ❌ **API returns 4xx/5xx errors** - Check ApiRequest with payloads
- ❌ **Frontend components crash** - Check ApplicationError with stack traces
- ❌ **Theme switching not working** - Check UserAction and IntegrationEvent
- ❌ **Approval workflows failing** - Check ApprovalAuditTrail

### **Use for Validation:**
- ✅ **After implementing a story** - Verify logging is working
- ✅ **After testing integration** - Check cross-domain events
- ✅ **After performance testing** - Check PerformanceMetric logs
- ✅ **Before marking story complete** - Ensure all actions are logged

---

## 📊 **What to Look For**

### **Authentication Issues**
```
RECENT AUTH EVENTS
[2025-01-15 10:30:00] LOGIN_FAILED
  UserID: 123
  Email: user@example.com
  Reason: {"error": "Invalid password"}
  IP: 192.168.1.1 | RequestID: req_12345
```

### **API Errors**
```
RECENT API REQUESTS
[2025-01-15 10:30:00] POST /api/v1/users/profile
  Status: 400 | Duration: 150ms
  UserID: 123 | RequestID: req_12345
  Request Payload: {"theme": "dark", "density": "compact"}
  Response Payload: {"error": "Invalid theme value"}
```

### **Frontend Errors**
```
RECENT APPLICATION ERRORS
[2025-01-15 10:30:00] ThemeError - ERROR
  Path: GET /dashboard
  Message: Theme 'invalid-theme' not found
  UserID: 123 | RequestID: req_12345
  Stack Trace: ThemeProvider.tsx:45:12
```

### **Epic 2 Audit Trail**
```
EPIC 2 AUDIT TRAIL
[2025-01-15 10:30:00] THEME_CHANGED on User 123
  User: 123
  Comments: Changed from light to dark theme
```

---

## 🔧 **Agent Workflow**

### **1. Before Starting a Story**
```bash
# Check current system state
python backend/enhanced_diagnostic_logs.py --limit 3
```

### **2. During Implementation**
```bash
# Check for errors as you build
python backend/enhanced_diagnostic_logs.py --limit 5
```

### **3. After Implementation**
```bash
# Verify your story is working and logged
python backend/enhanced_diagnostic_logs.py --limit 10
```

### **4. When Debugging Issues**
```bash
# Get specific request analysis
python backend/enhanced_diagnostic_logs.py --request-id "req_12345"

# Check performance impact
python backend/enhanced_diagnostic_logs.py --performance-hours 24
```

---

## 📋 **Logging Checklist for Agents**

### **For Every Story Implementation:**

**Backend Stories:**
- [ ] API endpoints log requests with payloads
- [ ] Errors are logged with stack traces
- [ ] Business logic decisions are logged in audit trail
- [ ] Performance metrics are logged for slow operations

**Frontend Stories:**
- [ ] User actions are logged (theme changes, navigation)
- [ ] Component errors are logged with stack traces
- [ ] API calls are logged with request/response
- [ ] Cross-domain events are logged

**Integration Stories:**
- [ ] Cross-domain data flow is logged
- [ ] Real-time updates are logged
- [ ] Error propagation is logged
- [ ] Performance impact is measured

---

## 🚨 **Common Issues and Solutions**

### **"No logs found"**
- Check if you're in the right directory
- Verify database connection
- Check if tables exist (Epic 2 tables might not be created yet)

### **"Request payload too large"**
- This is normal for large requests
- Check the sanitized version in logs
- Look for the essential data you need

### **"Missing correlation data"**
- Ensure RequestID is being passed through all layers
- Check if request context is maintained
- Verify logging is happening at the right level

### **"Performance impact"**
- Check PerformanceMetric logs for slow operations
- Look for database query performance
- Check API response times

---

## 📈 **Success Indicators**

### **Good Logging:**
- ✅ All user actions are logged
- ✅ All API calls have request/response payloads
- ✅ All errors have stack traces
- ✅ All business decisions are in audit trail
- ✅ Performance metrics show acceptable times

### **Poor Logging:**
- ❌ Missing user action logs
- ❌ API calls without payloads
- ❌ Errors without stack traces
- ❌ Missing audit trail entries
- ❌ No performance metrics

---

## 🎯 **Epic 2 Specific Logging**

### **Theme System:**
- UserAction: Theme changes, density changes, font size changes
- IntegrationEvent: Theme changes affecting components
- PerformanceMetric: Theme switching time

### **Approval Workflows:**
- ApprovalAuditTrail: Every approval decision, comment, status change
- UserAction: Approval requests, decisions, comments
- IntegrationEvent: Approval notifications, status updates

### **Event Management:**
- UserAction: Event creation, editing, deletion
- IntegrationEvent: Event-form relationships
- PerformanceMetric: Event listing performance

### **Form Foundation:**
- UserAction: Form creation, access control changes
- IntegrationEvent: Form-event associations
- PerformanceMetric: Form loading performance

---

**Remember: The more you log, the easier it is to debug and validate your implementations!** 🚀

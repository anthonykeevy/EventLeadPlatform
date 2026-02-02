# Session Management Improvements

## Problem
Users were being logged out frequently while actively working on forms, causing interruptions and potential work loss.

## Root Causes Identified
1. **Short token expiry**: Access tokens expire after 15 minutes
2. **Passive refresh**: Tokens only refreshed 5 minutes before expiry (every 10 minutes)
3. **No activity detection**: Tokens weren't refreshed based on user activity
4. **Reactive refresh**: Tokens only refreshed after 401 errors, not proactively

## Solutions Implemented

### 1. Activity-Based Token Refresh ✅
**Location**: `frontend/src/features/auth/context/AuthContext.tsx`

- **User Activity Detection**: Listens for mouse clicks, keyboard input, scrolling, touch events
- **Proactive Refresh**: If token expires within 5 minutes and user is active, refresh automatically
- **Periodic Check**: Checks every 2 minutes if user was active in last 2 minutes
- **Silent Operation**: Refreshes in background without interrupting user

**Benefits**:
- Tokens refresh automatically while user is working
- No interruptions during active sessions
- Maintains security by refreshing before expiry

### 2. More Aggressive Refresh Scheduling ✅
**Location**: `frontend/src/features/auth/context/AuthContext.tsx`

- **Previous**: Refreshed 5 minutes before expiry (every 10 minutes for 15-min tokens)
- **New**: Refreshes at 50% of token lifetime (every ~7.5 minutes for 15-min tokens)
- **Minimum Buffer**: Still maintains at least 5-minute buffer for safety

**Benefits**:
- More frequent refreshes prevent tokens from expiring unexpectedly
- Better balance between security and UX

### 3. Proactive Refresh Before API Calls ✅
**Location**: `frontend/src/lib/apiClient.ts`

- **Pre-Request Check**: Before making API calls, checks if token expires within 2 minutes
- **Silent Refresh**: If expiring soon, refreshes token automatically before the request
- **Seamless Operation**: User never sees 401 errors during active work

**Benefits**:
- Prevents 401 errors during active sessions
- Tokens are always fresh when making API calls
- No user-visible interruptions

### 4. Enhanced Error Handling ✅
**Location**: `frontend/src/features/auth/context/AuthContext.tsx`

- **Session Expired Modal**: Shows modal instead of immediate logout
- **Re-authentication**: User can re-login without losing work
- **Work Preservation**: All changes saved locally, preserved across re-auth

**Benefits**:
- Users can recover from expired sessions without losing work
- Better UX during edge cases

## Configuration Options

### Increase Token Expiry Time (Recommended for Development)

**Option 1: Database Configuration (Recommended)**
```sql
-- Update ACCESS_TOKEN_EXPIRY_MINUTES in database
UPDATE [ref].[AppSetting]
SET SettingValue = '60'  -- 60 minutes instead of 15
WHERE SettingKey = 'ACCESS_TOKEN_EXPIRY_MINUTES'
```

**Option 2: Environment Variable (Development Only)**
```bash
# In .env file
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**Note**: Increasing token expiry improves UX but reduces security. Balance based on your needs:
- **Development**: 60 minutes (1 hour) - Better for active development
- **Production**: 15-30 minutes - Better security, still manageable with activity-based refresh

## How It Works Now

### Token Refresh Flow

1. **User Logs In**
   - Access token: 15 minutes (configurable)
   - Refresh token: 7 days
   - Activity detection starts

2. **User Works Actively**
   - Activity detected → Check token expiry
   - If expires within 5 minutes → Refresh automatically
   - Scheduled refresh also runs at 50% of token lifetime

3. **User Makes API Call**
   - Pre-request check: Token expires within 2 minutes?
   - If yes → Refresh silently before request
   - Request proceeds with fresh token

4. **Token Refresh Fails**
   - Show session expired modal (not immediate logout)
   - User can re-authenticate
   - Work is preserved locally

### Timeline Example (15-minute tokens)

```
Time 0:00  - User logs in, token expires at 0:15
Time 0:07  - Scheduled refresh (50% of lifetime)
Time 0:10  - User clicks button → Activity refresh (if within 5 min)
Time 0:13  - User saves form → Pre-request refresh (if within 2 min)
Time 0:15  - Token would expire, but already refreshed
Time 0:22  - Next scheduled refresh (new token expires at 0:37)
```

## Monitoring & Debugging

### Check Token Refresh Success
```bash
# View recent token refresh events
python backend/enhanced_diagnostic_logs.py --limit 20
```

Look for:
- `TOKEN_REFRESH` events (success)
- `TOKEN_REFRESH_FAILED` events (with detailed failure reasons)

### Check Token Expiry Configuration
```sql
-- Check current token expiry settings
SELECT SettingKey, SettingValue, Description
FROM [ref].[AppSetting]
WHERE SettingKey IN ('ACCESS_TOKEN_EXPIRY_MINUTES', 'REFRESH_TOKEN_EXPIRY_DAYS')
```

## Security Considerations

1. **Activity-Based Refresh**: Only refreshes when user is active, not for idle sessions
2. **Proactive Refresh**: Still respects token expiry, just refreshes earlier
3. **Session Expired Modal**: Allows re-authentication without exposing tokens
4. **Refresh Token Security**: Refresh tokens still expire after 7 days (configurable)

## Future Enhancements

1. **"Remember Me" Option**: Extend refresh token lifetime for trusted devices
2. **Idle Timeout**: Logout after extended inactivity (e.g., 2 hours)
3. **Token Refresh Retry**: Retry failed refreshes with exponential backoff
4. **Background Refresh**: Refresh tokens in service worker for offline support

## Testing

### Test Activity-Based Refresh
1. Log in
2. Wait 10 minutes (token expires at 15 min)
3. Click anywhere on page
4. Check console: Should see "User activity detected - refreshing token proactively"
5. Verify no session expired modal appears

### Test Proactive API Refresh
1. Log in
2. Wait 13 minutes (token expires at 15 min)
3. Click Save button
4. Check network tab: Should see token refresh request before save request
5. Verify save succeeds without 401 error

### Test Session Expired Modal
1. Log in
2. Manually expire refresh token (or wait 7 days)
3. Try to save form
4. Verify session expired modal appears (not immediate logout)
5. Re-login and verify work is preserved

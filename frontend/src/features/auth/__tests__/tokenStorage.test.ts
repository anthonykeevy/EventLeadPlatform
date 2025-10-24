/**
 * Token Storage Unit Tests - Story 1.9 (AC-1.9.3)
 * Tests for token storage utilities
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import * as tokenStorage from '../utils/tokenStorage'

describe('Token Storage Utilities', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear()
    vi.clearAllMocks()
  })
  
  describe('storeTokens', () => {
    it('should store tokens in localStorage', () => {
      const accessToken = 'access_token_123'
      const refreshToken = 'refresh_token_456'
      const expiresIn = 3600
      
      tokenStorage.storeTokens(accessToken, refreshToken, expiresIn)
      
      expect(localStorage.getItem('eventlead_access_token')).toBe(accessToken)
      expect(localStorage.getItem('eventlead_refresh_token')).toBe(refreshToken)
      expect(localStorage.getItem('eventlead_token_expiry')).toBeTruthy()
    })
    
    it('should calculate correct expiry timestamp', () => {
      const accessToken = 'access_token_123'
      const refreshToken = 'refresh_token_456'
      const expiresIn = 3600
      const beforeTime = Math.floor(Date.now() / 1000)
      
      tokenStorage.storeTokens(accessToken, refreshToken, expiresIn)
      
      const expiresAt = parseInt(localStorage.getItem('eventlead_token_expiry') || '0', 10)
      const afterTime = Math.floor(Date.now() / 1000)
      
      expect(expiresAt).toBeGreaterThanOrEqual(beforeTime + expiresIn)
      expect(expiresAt).toBeLessThanOrEqual(afterTime + expiresIn)
    })
  })
  
  describe('getStoredTokens', () => {
    it('should retrieve stored tokens', () => {
      const accessToken = 'access_token_123'
      const refreshToken = 'refresh_token_456'
      const expiresIn = 3600
      
      tokenStorage.storeTokens(accessToken, refreshToken, expiresIn)
      const tokens = tokenStorage.getStoredTokens()
      
      expect(tokens).toBeTruthy()
      expect(tokens?.accessToken).toBe(accessToken)
      expect(tokens?.refreshToken).toBe(refreshToken)
      expect(tokens?.expiresAt).toBeGreaterThan(0)
    })
    
    it('should return null if no tokens exist', () => {
      const tokens = tokenStorage.getStoredTokens()
      expect(tokens).toBeNull()
    })
    
    it('should return null if tokens are incomplete', () => {
      localStorage.setItem('eventlead_access_token', 'access_token_123')
      // Missing refresh token
      
      const tokens = tokenStorage.getStoredTokens()
      expect(tokens).toBeNull()
    })
  })
  
  describe('getAccessToken', () => {
    it('should retrieve access token only', () => {
      const accessToken = 'access_token_123'
      localStorage.setItem('eventlead_access_token', accessToken)
      
      expect(tokenStorage.getAccessToken()).toBe(accessToken)
    })
    
    it('should return null if no access token exists', () => {
      expect(tokenStorage.getAccessToken()).toBeNull()
    })
  })
  
  describe('getRefreshToken', () => {
    it('should retrieve refresh token only', () => {
      const refreshToken = 'refresh_token_456'
      localStorage.setItem('eventlead_refresh_token', refreshToken)
      
      expect(tokenStorage.getRefreshToken()).toBe(refreshToken)
    })
    
    it('should return null if no refresh token exists', () => {
      expect(tokenStorage.getRefreshToken()).toBeNull()
    })
  })
  
  describe('clearTokens', () => {
    it('should remove all tokens from localStorage', () => {
      tokenStorage.storeTokens('access', 'refresh', 3600)
      tokenStorage.clearTokens()
      
      expect(localStorage.getItem('eventlead_access_token')).toBeNull()
      expect(localStorage.getItem('eventlead_refresh_token')).toBeNull()
      expect(localStorage.getItem('eventlead_token_expiry')).toBeNull()
    })
  })
  
  describe('isTokenExpiringSoon', () => {
    it('should return false if token expires in more than buffer time', () => {
      const expiresAt = Math.floor(Date.now() / 1000) + 600 // 10 minutes
      localStorage.setItem('eventlead_token_expiry', expiresAt.toString())
      
      expect(tokenStorage.isTokenExpiringSoon(300)).toBe(false) // 5 min buffer
    })
    
    it('should return true if token expires within buffer time', () => {
      const expiresAt = Math.floor(Date.now() / 1000) + 200 // 3 minutes 20 seconds
      localStorage.setItem('eventlead_token_expiry', expiresAt.toString())
      
      expect(tokenStorage.isTokenExpiringSoon(300)).toBe(true) // 5 min buffer
    })
    
    it('should return true if no expiry exists', () => {
      expect(tokenStorage.isTokenExpiringSoon()).toBe(true)
    })
  })
  
  describe('isTokenExpired', () => {
    it('should return false if token has not expired', () => {
      const expiresAt = Math.floor(Date.now() / 1000) + 3600
      localStorage.setItem('eventlead_token_expiry', expiresAt.toString())
      
      expect(tokenStorage.isTokenExpired()).toBe(false)
    })
    
    it('should return true if token has expired', () => {
      const expiresAt = Math.floor(Date.now() / 1000) - 100
      localStorage.setItem('eventlead_token_expiry', expiresAt.toString())
      
      expect(tokenStorage.isTokenExpired()).toBe(true)
    })
    
    it('should return true if no expiry exists', () => {
      expect(tokenStorage.isTokenExpired()).toBe(true)
    })
  })
  
  describe('decodeJWT', () => {
    it('should decode valid JWT payload', () => {
      // JWT: {"user_id": 1, "email": "test@example.com"}
      const token = 'header.' + btoa('{"user_id":1,"email":"test@example.com"}') + '.signature'
      
      const decoded = tokenStorage.decodeJWT(token)
      
      expect(decoded).toBeTruthy()
      expect(decoded.user_id).toBe(1)
      expect(decoded.email).toBe('test@example.com')
    })
    
    it('should return null for invalid JWT', () => {
      const decoded = tokenStorage.decodeJWT('invalid_token')
      expect(decoded).toBeNull()
    })
  })
})


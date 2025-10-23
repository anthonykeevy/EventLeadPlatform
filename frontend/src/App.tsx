import React, { useEffect, useState } from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import { SignupForm, EmailVerification, LoginForm, AuthProvider, PasswordResetRequest, PasswordResetConfirm } from './features/auth'
import { DashboardPage } from './features/dashboard'

interface HealthStatus {
  status: string
  service: string
  environment: string
}

function HomePage() {
  const [apiStatus, setApiStatus] = useState<'loading' | 'connected' | 'error'>('loading')
  const [healthData, setHealthData] = useState<HealthStatus | null>(null)

  useEffect(() => {
    // Test API connection
    fetch('http://localhost:8000/api/health')
      .then(res => res.json())
      .then(data => {
        setHealthData(data)
        setApiStatus('connected')
      })
      .catch(err => {
        console.error('API connection failed:', err)
        setApiStatus('error')
      })
  }, [])

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full bg-white rounded-lg shadow-lg p-8">
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-teal-600 mb-2">
            EventLead Platform
          </h1>
          <p className="text-gray-500 text-lg">
            Multi-Tenant Event Lead Collection Platform
          </p>
        </div>

        <div className="space-y-4">
          {/* Environment Status */}
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <h2 className="font-semibold text-green-900 mb-2 flex items-center">
              <span className="mr-2">✅</span>
              Development Environment Ready
            </h2>
            <ul className="text-sm text-green-700 space-y-1">
              <li>• Python 3.13.3 installed</li>
              <li>• Node.js 22.17.1 installed</li>
              <li>• SQL Server 2022 running</li>
              <li>• Docker 28.4.0 installed</li>
              <li>• Frontend dependencies installed (511 packages)</li>
              <li>• Backend dependencies installed</li>
            </ul>
          </div>

          {/* API Connection Status */}
          <div className={`border rounded-lg p-4 ${
            apiStatus === 'connected' ? 'bg-green-50 border-green-200' :
            apiStatus === 'error' ? 'bg-red-50 border-red-200' :
            'bg-blue-50 border-blue-200'
          }`}>
            <h2 className="font-semibold mb-2 flex items-center">
              {apiStatus === 'connected' && <span className="mr-2 text-green-900">✅ Backend API Connected</span>}
              {apiStatus === 'error' && <span className="mr-2 text-red-900">❌ Backend API Not Running</span>}
              {apiStatus === 'loading' && <span className="mr-2 text-blue-900">🔄 Connecting to API...</span>}
            </h2>
            
            {healthData && (
              <div className="text-sm text-green-700">
                <p>• Service: {healthData.service}</p>
                <p>• Status: {healthData.status}</p>
                <p>• Environment: {healthData.environment}</p>
              </div>
            )}
            
            {apiStatus === 'error' && (
              <div className="text-sm text-red-700">
                <p>Backend not running. Start it with:</p>
                <code className="block bg-red-100 px-2 py-1 rounded mt-2">
                  cd backend && python main.py
                </code>
              </div>
            )}
          </div>

          {/* Authentication Links - Story 1.1 */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h2 className="font-semibold text-blue-900 mb-3">
              🔐 Story 1.1: User Signup & Email Verification
            </h2>
            <div className="space-y-2">
              <Link 
                to="/signup" 
                className="block w-full py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors text-center font-medium"
              >
                Sign Up
              </Link>
              <Link 
                to="/login" 
                className="block w-full py-2 px-4 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition-colors text-center font-medium"
              >
                Log In
              </Link>
            </div>
          </div>

          {/* Useful Links */}
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <h2 className="font-semibold text-gray-900 mb-2">
              🔗 Useful Links
            </h2>
            <ul className="text-sm text-gray-700 space-y-1">
              <li>• <a href="http://localhost:8000/docs" target="_blank" className="text-teal-600 hover:underline">API Docs (Swagger UI)</a></li>
              <li>• <a href="http://localhost:8000/api/test-database" target="_blank" className="text-teal-600 hover:underline">Database Connection Test</a></li>
              <li>• <a href="http://localhost:8025" target="_blank" className="text-teal-600 hover:underline">MailHog (Email Testing)</a></li>
            </ul>
          </div>
        </div>

        <div className="mt-8 text-center text-sm text-gray-500">
          <p>Built with React 18.2.0 + FastAPI 0.115.7 + SQL Server 2022</p>
          <p className="mt-1">Architecture: Modular Monolith | Repository: Monorepo</p>
        </div>
      </div>
    </div>
  )
}

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/signup" element={<SignupForm />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/verify-email" element={<EmailVerification />} />
        <Route path="/reset-password" element={<PasswordResetRequest />} />
        <Route path="/reset-password/confirm" element={<PasswordResetConfirm />} />
        <Route path="/dashboard" element={<DashboardPage />} />
      </Routes>
    </AuthProvider>
  )
}

export default App


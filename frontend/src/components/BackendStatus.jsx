import React, { useState, useEffect } from 'react'
import { getApiEndpoint } from '../utils/api'

export default function BackendStatus() {
  const [isConnected, setIsConnected] = useState(false)
  const [checking, setChecking] = useState(true)

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const controller = new AbortController()
        const timeoutId = setTimeout(() => controller.abort(), 2000) // 2 second timeout
        
        const res = await fetch(getApiEndpoint('/status'), { 
          method: 'GET',
          signal: controller.signal
        })
        
        clearTimeout(timeoutId)
        setIsConnected(res.ok)
      } catch (error) {
        setIsConnected(false)
      } finally {
        setChecking(false)
      }
    }

    checkBackend()
    const interval = setInterval(checkBackend, 5000) // Check every 5 seconds

    return () => clearInterval(interval)
  }, [])

  if (checking) {
    return null
  }

  if (!isConnected) {
    return (
      <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-4 rounded-md">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <i className="fas fa-exclamation-triangle text-red-500 text-xl"></i>
          </div>
          <div className="ml-3 flex-1">
            <h3 className="text-sm font-medium text-red-800">
              Backend Server Not Connected
            </h3>
            <div className="mt-2 text-sm text-red-700">
              <p>The frontend cannot connect to the backend API.</p>
              
              {import.meta.env.PROD && !import.meta.env.VITE_API_URL ? (
                <div className="mt-3 p-3 bg-yellow-50 border border-yellow-300 rounded-lg">
                  <p className="font-semibold text-yellow-800 mb-2">⚠️ Missing Environment Variable</p>
                  <p className="text-xs text-yellow-700 mb-2">
                    The <code className="bg-yellow-100 px-1 rounded font-mono">VITE_API_URL</code> environment variable is not set in Vercel.
                  </p>
                  <p className="text-xs text-yellow-700 font-semibold mb-1">To fix this:</p>
                  <ol className="text-xs text-yellow-700 list-decimal list-inside space-y-1 ml-2">
                    <li>Go to Vercel Dashboard → Your Project → <strong>Settings</strong> → <strong>Environment Variables</strong></li>
                    <li>Click <strong>"Add New"</strong></li>
                    <li>Set:
                      <div className="bg-yellow-100 p-2 rounded mt-1 font-mono text-xs">
                        Key: VITE_API_URL<br/>
                        Value: https://swe-fog-latency-optimization.onrender.com
                      </div>
                      <span className="text-yellow-600 text-xs block mt-1">⚠️ No trailing slash!</span>
                    </li>
                    <li>Select all environments (Production, Preview, Development)</li>
                    <li>Click <strong>"Save"</strong></li>
                    <li>Go to <strong>Deployments</strong> tab → Click <strong>"Redeploy"</strong></li>
                  </ol>
                </div>
              ) : (
                <>
                  <p className="text-xs mt-1">
                    {import.meta.env.VITE_API_URL 
                      ? `Backend URL: ${import.meta.env.VITE_API_URL}`
                      : 'Backend URL not configured.'}
                  </p>
                  {!import.meta.env.PROD && (
                    <>
                      <p className="mt-2 font-semibold">To fix this (Development):</p>
                      <ol className="list-decimal list-inside mt-1 space-y-1">
                        <li>Open a new terminal/command prompt</li>
                        <li>Navigate to the <code className="bg-red-100 px-1 rounded">backend</code> folder</li>
                        <li>Run: <code className="bg-red-100 px-1 rounded">python app.py</code></li>
                        <li>Wait for the message: <code className="bg-red-100 px-1 rounded">Starting Fog Computing Simulator Backend API</code></li>
                      </ol>
                      <p className="mt-2 text-xs">Or use the startup script: <code className="bg-red-100 px-1 rounded">start.bat</code> (Windows) or <code className="bg-red-100 px-1 rounded">./start.sh</code> (Linux/Mac)</p>
                    </>
                  )}
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-green-50 border-l-4 border-green-500 p-2 mb-4 rounded-md">
      <div className="flex items-center">
        <i className="fas fa-check-circle text-green-500 mr-2"></i>
        <span className="text-sm font-medium text-green-800">Backend connected</span>
      </div>
    </div>
  )
}


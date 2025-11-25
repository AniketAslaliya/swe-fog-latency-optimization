import React, { useState, useEffect } from 'react'

export default function BackendStatus() {
  const [isConnected, setIsConnected] = useState(false)
  const [checking, setChecking] = useState(true)

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const controller = new AbortController()
        const timeoutId = setTimeout(() => controller.abort(), 2000) // 2 second timeout
        
        const res = await fetch('/api/status', { 
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
              <p>The frontend cannot connect to the backend API at <code className="bg-red-100 px-1 rounded">http://localhost:5000</code></p>
              <p className="mt-2 font-semibold">To fix this:</p>
              <ol className="list-decimal list-inside mt-1 space-y-1">
                <li>Open a new terminal/command prompt</li>
                <li>Navigate to the <code className="bg-red-100 px-1 rounded">backend</code> folder</li>
                <li>Run: <code className="bg-red-100 px-1 rounded">python app.py</code></li>
                <li>Wait for the message: <code className="bg-red-100 px-1 rounded">Starting Fog Computing Simulator Backend API</code></li>
              </ol>
              <p className="mt-2 text-xs">Or use the startup script: <code className="bg-red-100 px-1 rounded">start.bat</code> (Windows) or <code className="bg-red-100 px-1 rounded">./start.sh</code> (Linux/Mac)</p>
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


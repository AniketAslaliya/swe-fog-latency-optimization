import React from 'react'

export default function LoadingScreen() {
  return (
    <div className="fixed inset-0 bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center z-50">
      <div className="text-center">
        <div className="inline-block animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-primary mb-4"></div>
        <h2 className="text-2xl font-semibold text-gray-800 mb-2">Checking Authentication...</h2>
        <p className="text-gray-600">Please wait while we verify your access</p>
      </div>
    </div>
  )
}



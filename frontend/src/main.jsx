import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

// Suppress Google API loading errors (they're expected if Google Sign-In isn't configured)
const originalError = console.error
console.error = (...args) => {
  const message = args[0]?.toString() || ''
  // Filter out Google API loading errors
  if (
    message.includes('apis.google.com') ||
    message.includes('gapi') ||
    message.includes('ERR_CONNECTION_TIMED_OUT') ||
    message.includes('Failed to load resource')
  ) {
    return // Suppress these errors
  }
  originalError.apply(console, args)
}

// Suppress uncaught promise errors from browser extensions
window.addEventListener('unhandledrejection', (event) => {
  if (
    event.reason?.message?.includes('message channel closed') ||
    event.reason?.message?.includes('asynchronous response')
  ) {
    event.preventDefault() // Suppress browser extension errors
  }
})

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)



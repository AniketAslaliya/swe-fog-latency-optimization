// API utility for making requests to backend
// Uses environment variable in production, proxy in development

const getApiUrl = () => {
  // In production (Vercel), use the backend URL from environment variable
  if (import.meta.env.PROD) {
    return import.meta.env.VITE_API_URL || ''
  }
  // In development, use proxy (Vite handles /api -> localhost:5000)
  return ''
}

export const apiUrl = getApiUrl()

// Helper to get full API endpoint URL
export const getApiEndpoint = (endpoint) => {
  const baseUrl = getApiUrl()
  // Remove leading slash from endpoint if present
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`
  
  if (baseUrl) {
    // Production: use full URL
    return `${baseUrl}${cleanEndpoint}`
  }
  // Development: use proxy path
  return `/api${cleanEndpoint}`
}

export const fetchApi = async (endpoint, options = {}) => {
  const url = getApiEndpoint(endpoint)
  return fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  })
}


// API utility for making requests to backend
// Uses environment variable in production, localhost in development

const getApiUrl = () => {
  // In production (Vercel), use the backend URL from environment variable
  if (import.meta.env.PROD && import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  // In development, use proxy (Vite handles this)
  return ''
}

export const apiUrl = getApiUrl()

export const fetchApi = async (endpoint, options = {}) => {
  const url = `${apiUrl}${endpoint}`
  return fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  })
}


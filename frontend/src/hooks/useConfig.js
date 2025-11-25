import { useState, useEffect } from 'react'
import { getApiEndpoint } from '../utils/api'

export function useConfig() {
  const [config, setConfig] = useState({
    simulation: { duration: 100, enable_failures: true, failure_probability: 0.1 },
    network: { fog_nodes: 3, iot_devices: 10 },
    tasks: { rate_range: [0.1, 0.3], complexity_range: [50, 2000] },
    latency: { base_latency: 0.01, cloud_latency: 5.0 },
    offloading: { complexity_threshold: 1000, utilization_threshold: 0.8 }
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchConfig()
  }, [])

  const fetchConfig = async () => {
    try {
      const res = await fetch(getApiEndpoint('/config'))
      if (res.ok) {
        const data = await res.json()
        setConfig(data)
      }
    } catch (error) {
      // Silently handle connection errors - BackendStatus component will show warning
      // Keep default config values
    } finally {
      setLoading(false)
    }
  }

  const saveConfig = async (newConfig) => {
    try {
      const res = await fetch(getApiEndpoint('/config'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newConfig)
      })
      if (res.ok) {
        setConfig(newConfig)
        return true
      }
    } catch (error) {
      console.error('Error saving config:', error)
    }
    return false
  }

  return { config, loading, fetchConfig, saveConfig, setConfig }
}



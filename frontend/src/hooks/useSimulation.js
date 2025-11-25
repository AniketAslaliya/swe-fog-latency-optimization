import { useState, useEffect, useCallback } from 'react'
import { getApiEndpoint } from '../utils/api'

export function useSimulation() {
  const [status, setStatus] = useState({ running: false, progress: 0 })
  const [metrics, setMetrics] = useState({
    tasks_generated: 0,
    tasks_processed: 0,
    avg_latency: 0,
    failure_events: 0,
    offloading_rate: 0,
    fog_queue_length: 0,
    cloud_queue_length: 0,
    priority_distribution: { HIGH: 0, MODERATE: 0, LOW: 0 }
  })

  const fetchStatus = useCallback(async () => {
    try {
      const res = await fetch(getApiEndpoint('/status'))
      if (!res.ok) throw new Error('Backend not responding')
      const data = await res.json()
      setStatus({
        running: data.running,
        progress: data.progress || 0
      })
      setMetrics(data.metrics || metrics)
    } catch (error) {
      // Silently handle connection errors - BackendStatus component will show warning
      if (error.name !== 'AbortError') {
        // Only log non-abort errors
      }
    }
  }, [])

  useEffect(() => {
    const interval = setInterval(fetchStatus, 1000)
    return () => clearInterval(interval)
  }, [fetchStatus])

  const startSimulation = async (duration) => {
    try {
      const res = await fetch(getApiEndpoint('/simulation/start'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ duration })
      })
      if (res.ok) {
        fetchStatus()
      }
    } catch (error) {
      console.error('Error starting simulation:', error)
    }
  }

  const stopSimulation = async () => {
    try {
      const res = await fetch(getApiEndpoint('/simulation/stop'), {
        method: 'POST'
      })
      if (res.ok) {
        fetchStatus()
      }
    } catch (error) {
      console.error('Error stopping simulation:', error)
    }
  }

  return { status, metrics, startSimulation, stopSimulation, fetchStatus }
}



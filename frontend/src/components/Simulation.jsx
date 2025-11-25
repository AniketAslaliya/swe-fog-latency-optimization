import React, { useState, useEffect } from 'react'
import { useSimulation } from '../hooks/useSimulation'
import { useConfig } from '../hooks/useConfig'
import { getApiEndpoint } from '../utils/api'

export default function Simulation() {
  const { status, metrics, startSimulation, stopSimulation } = useSimulation()
  const { config } = useConfig()
  const [duration, setDuration] = useState(100)
  const [enableFailures, setEnableFailures] = useState(true)
  const [failureProb, setFailureProb] = useState(0.1)
  const [events, setEvents] = useState([])
  const [queueInfo, setQueueInfo] = useState({ fog_queue_length: 0, cloud_queue_length: 0 })

  useEffect(() => {
    setDuration(config?.simulation?.duration || 100)
    setEnableFailures(config?.simulation?.enable_failures ?? true)
    setFailureProb(config?.simulation?.failure_probability || 0.1)
  }, [config])

  useEffect(() => {
    const fetchQueueInfo = () => {
      fetch(getApiEndpoint('/status'))
        .then(res => res.json())
        .then(data => {
          setQueueInfo({
            fog_queue_length: data.fog_queue_length || 0,
            cloud_queue_length: data.cloud_queue_length || 0
          })
        })
        .catch(console.error)
    }

    const interval = setInterval(() => {
      fetch(getApiEndpoint('/simulation/events'))
        .then(res => res.json())
        .then(data => {
          if (data.events && data.events.length > 0) {
            setEvents(prev => [...data.events, ...prev].slice(0, 20))
          }
        })
        .catch(console.error)
      fetchQueueInfo()
    }, 1000)

    fetchQueueInfo()
    return () => clearInterval(interval)
  }, [])

  const handleRun = () => {
    if (status.running) {
      stopSimulation()
    } else {
      startSimulation(duration)
    }
  }

  const getStatusColor = () => {
    if (status.running) return 'bg-blue-500'
    if (status.progress >= 100) return 'bg-green-500'
    return 'bg-gray-400'
  }

  return (
    <div className="space-y-6">
      <div className="mb-6 pb-4 border-b-2 border-gray-200">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Simulation Control</h1>
        <p className="text-gray-600">Configure and run fog computing simulations</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Simulation Parameters</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Duration (seconds)
              </label>
              <input
                type="number"
                value={isNaN(duration) ? '' : duration}
                onChange={(e) => {
                  const val = parseInt(e.target.value)
                  if (!isNaN(val) && val > 0) {
                    setDuration(val)
                  } else if (e.target.value === '') {
                    setDuration(100) // Default value
                  }
                }}
                min="10"
                max="3600"
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary focus:border-transparent"
              />
            </div>
            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="enableFailures"
                checked={enableFailures}
                onChange={(e) => setEnableFailures(e.target.checked)}
                className="w-4 h-4 text-primary border-gray-300 rounded focus:ring-primary"
              />
              <label htmlFor="enableFailures" className="text-sm font-medium text-gray-700">
                Enable Node Failures
              </label>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Failure Probability: {failureProb}
              </label>
              <input
                type="range"
                min="0"
                max="0.5"
                step="0.01"
                value={failureProb}
                onChange={(e) => setFailureProb(parseFloat(e.target.value))}
                className="w-full"
              />
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Simulation Status</h3>
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className={`w-3 h-3 rounded-full ${getStatusColor()} animate-pulse`}></div>
              <span className="text-sm font-medium text-gray-700">
                {status.running ? 'Running' : status.progress >= 100 ? 'Completed' : 'Ready'}
              </span>
            </div>
            <div>
              <div className="w-full bg-gray-200 rounded-full h-2.5 mb-2">
                <div
                  className="bg-primary h-2.5 rounded-full transition-all duration-300"
                  style={{ width: `${status.progress}%` }}
                ></div>
              </div>
              <div className="text-xs text-gray-500 text-right">{status.progress.toFixed(1)}%</div>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 pt-2">
              <div>
                <span className="text-xs text-gray-600">Elapsed Time:</span>
                <p className="text-sm font-semibold text-gray-900">
                  {((status.progress * duration) / 100).toFixed(1)}s
                </p>
              </div>
              <div>
                <span className="text-xs text-gray-600">Tasks Generated:</span>
                <p className="text-sm font-semibold text-gray-900">{metrics.tasks_generated}</p>
              </div>
              <div>
                <span className="text-xs text-gray-600">Tasks Processed:</span>
                <p className="text-sm font-semibold text-gray-900">{metrics.tasks_processed}</p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-200">
              <div className="bg-indigo-50 p-3 rounded-lg">
                <span className="text-xs text-gray-600 block mb-1">Fog Queue Length</span>
                <p className="text-2xl font-bold text-indigo-700">{queueInfo.fog_queue_length}</p>
                <p className="text-xs text-gray-500 mt-1">HIGH priority tasks</p>
              </div>
              <div className="bg-purple-50 p-3 rounded-lg">
                <span className="text-xs text-gray-600 block mb-1">Cloud Queue Length</span>
                <p className="text-2xl font-bold text-purple-700">{queueInfo.cloud_queue_length}</p>
                <p className="text-xs text-gray-500 mt-1">MODERATE/LOW priority tasks</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Simulation Output</h3>
          <button
            onClick={handleRun}
            className={`btn ${status.running ? 'btn-danger' : 'btn-primary'}`}
          >
            <i className={`fas ${status.running ? 'fa-stop' : 'fa-play'}`}></i>
            {status.running ? 'Stop Simulation' : 'Run Simulation'}
          </button>
        </div>
        <div className="bg-gray-900 text-green-400 p-4 rounded-md font-mono text-sm max-h-96 overflow-y-auto">
          {events.length === 0 ? (
            <div className="text-gray-500">
              <span className="text-gray-600">[00:00:00]</span> Simulation environment ready
            </div>
          ) : (
            events.map((event, index) => (
              <div key={index} className="mb-1">
                <span className="text-gray-600">
                  [{new Date(event.timestamp).toLocaleTimeString()}]
                </span>{' '}
                <span>{event.message}</span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}



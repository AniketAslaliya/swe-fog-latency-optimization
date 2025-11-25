import React, { useState, useEffect, useRef } from 'react'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Line, Doughnut, Bar } from 'react-chartjs-2'
import { useConfig } from '../hooks/useConfig'
import { getApiEndpoint } from '../utils/api'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
)

export default function Analytics() {
  const { config } = useConfig()
  const [analytics, setAnalytics] = useState(null)
  const [loading, setLoading] = useState(true)
  const [updateKey, setUpdateKey] = useState(0) // Force chart re-render

  useEffect(() => {
    fetchAnalytics()
    const interval = setInterval(() => {
      fetchAnalytics()
      setUpdateKey(prev => prev + 1) // Force chart update
    }, 2000) // Update every 2 seconds for better responsiveness
    return () => clearInterval(interval)
  }, [])

  const fetchAnalytics = async () => {
    try {
      const res = await fetch(getApiEndpoint('/analytics/metrics'))
      if (res.ok) {
        const data = await res.json()
        setAnalytics(data)
        setLoading(false)
      } else {
        // If response is not ok, still try to set data to prevent infinite loading
        console.error('Analytics API returned error:', res.status)
        setLoading(false)
      }
    } catch (error) {
      console.error('Error fetching analytics:', error)
      setLoading(false)
    }
  }

  const handleExport = async () => {
    try {
      const res = await fetch(getApiEndpoint('/export/data'))
      if (res.ok) {
        const data = await res.json()
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `fog_simulation_${new Date().toISOString()}.json`
        a.click()
      }
    } catch (error) {
      console.error('Error exporting data:', error)
    }
  }

  if (loading && !analytics) {
    return <div className="text-center py-12">Loading analytics...</div>
  }

  const latencyData = analytics?.latency_data || {
    fog_processing: [45, 52, 48, 55, 50, 47],
    cloud_processing: [120, 125, 130, 128, 132, 129],
    timestamps: ['0s', '20s', '40s', '60s', '80s', '100s']
  }

  const distributionData = analytics?.task_distribution || {
    fog_processing: 65,
    cloud_processing: 30,
    failed: 5
  }

  const utilizationData = analytics?.resource_utilization || {
    fog_nodes: [45, 52, 48],
    cloud_server: 35
  }

  const failureData = analytics?.failure_events || {}
  const priorityDist = analytics?.priority_distribution || { HIGH: 0, MODERATE: 0, LOW: 0 }

  const numFogNodes = config?.network?.fog_nodes || 3

  return (
    <div className="space-y-6">
      <div className="mb-6 pb-4 border-b-2 border-gray-200">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Performance Analytics</h1>
        <p className="text-gray-600">Analyze simulation results and performance metrics</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Priority Distribution</h3>
          <div className="h-64">
            <Doughnut
              key={`priority-${updateKey}`}
              data={{
                labels: ['HIGH', 'MODERATE', 'LOW'],
                datasets: [{
                  data: [priorityDist.HIGH || 0, priorityDist.MODERATE || 0, priorityDist.LOW || 0],
                  backgroundColor: ['#ef4444', '#f97316', '#22c55e'],
                  borderWidth: 0
                }]
              }}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                  animateRotate: true,
                  animateScale: true
                },
                plugins: {
                  legend: { position: 'bottom' }
                }
              }}
            />
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Latency Comparison</h3>
          <div className="h-64">
            <Line
              key={`latency-${updateKey}`}
              data={{
                labels: latencyData.timestamps,
                datasets: [
                  {
                    label: 'Fog Processing',
                    data: latencyData.fog_processing,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4
                  },
                  {
                    label: 'Cloud Processing',
                    data: latencyData.cloud_processing,
                    borderColor: '#764ba2',
                    backgroundColor: 'rgba(118, 75, 162, 0.1)',
                    tension: 0.4
                  }
                ]
              }}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                  duration: 500
                },
                plugins: {
                  legend: { position: 'top' }
                },
                scales: {
                  y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Latency (ms)' }
                  }
                }
              }}
            />
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Task Distribution</h3>
          <div className="h-64">
            <Doughnut
              key={`task-dist-${updateKey}`}
              data={{
                labels: ['Fog Processing (HIGH)', 'Cloud Processing (LOW/MOD)', 'Failed'],
                datasets: [{
                  data: [distributionData.fog_processing, distributionData.cloud_processing, distributionData.failed],
                  backgroundColor: ['#667eea', '#764ba2', '#f56565'],
                  borderWidth: 0
                }]
              }}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                  animateRotate: true,
                  animateScale: true
                },
                plugins: {
                  legend: { position: 'bottom' }
                }
              }}
            />
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Resource Utilization</h3>
          <div className="h-64">
            <Bar
              key={`utilization-${updateKey}`}
              data={{
                labels: [
                  ...Array.from({ length: numFogNodes }, (_, i) => `Fog Node ${i + 1}`),
                  'Cloud Server'
                ],
                datasets: [{
                  label: 'CPU Utilization (%)',
                  data: [...utilizationData.fog_nodes, utilizationData.cloud_server],
                  backgroundColor: [
                    ...Array.from({ length: numFogNodes }, (_, i) => ['#667eea', '#764ba2', '#f093fb', '#48bb78'][i % 4]),
                    '#38b2ac'
                  ],
                  borderRadius: 4
                }]
              }}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                  duration: 500
                },
                plugins: {
                  legend: { display: false }
                },
                scales: {
                  y: {
                    beginAtZero: true,
                    max: 100,
                    title: { display: true, text: 'Utilization (%)' }
                  }
                }
              }}
            />
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Failure Events</h3>
          <div className="h-64">
            <Bar
              key={`failure-${updateKey}`}
              data={{
                labels: Array.from({ length: numFogNodes }, (_, i) => `Node ${i + 1}`),
                datasets: [{
                  label: 'Failure Events',
                  data: Array.from({ length: numFogNodes }, (_, i) => failureData[`node_${i + 1}`] || 0),
                  backgroundColor: '#f56565',
                  borderRadius: 4
                }]
              }}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                  duration: 500
                },
                plugins: {
                  legend: { display: false }
                },
                scales: {
                  y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Failure Count' }
                  }
                }
              }}
            />
          </div>
        </div>
      </div>

      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Performance Summary</h3>
          <button onClick={handleExport} className="btn btn-primary">
            <i className="fas fa-download"></i>
            Export Simulation Data
          </button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
          <div>
            <h4 className="text-sm font-medium text-gray-600 mb-1">Average Response Time</h4>
            <p className="text-2xl font-bold text-gray-900">
              {analytics?.performance_summary?.avg_response_time || '0.0s'}
            </p>
          </div>
          <div>
            <h4 className="text-sm font-medium text-gray-600 mb-1">Success Rate</h4>
            <p className="text-2xl font-bold text-gray-900">
              {analytics?.performance_summary?.success_rate || '100%'}
            </p>
          </div>
          <div>
            <h4 className="text-sm font-medium text-gray-600 mb-1">Offloading Rate</h4>
            <p className="text-2xl font-bold text-gray-900">
              {analytics?.performance_summary?.offloading_rate || '0%'}
            </p>
          </div>
          <div>
            <h4 className="text-sm font-medium text-gray-600 mb-1">Energy Efficiency</h4>
            <p className="text-2xl font-bold text-gray-900">
              {analytics?.performance_summary?.energy_efficiency || 'N/A'}
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t border-gray-200">
          <div>
            <h4 className="text-sm font-medium text-gray-600 mb-1">Fog Queue Length</h4>
            <p className="text-2xl font-bold text-indigo-600">
              {analytics?.fog_queue_length || 0}
            </p>
          </div>
          <div>
            <h4 className="text-sm font-medium text-gray-600 mb-1">Cloud Queue Length</h4>
            <p className="text-2xl font-bold text-purple-600">
              {analytics?.cloud_queue_length || 0}
            </p>
          </div>
          <div>
            <h4 className="text-sm font-medium text-gray-600 mb-1">Total HIGH Priority</h4>
            <p className="text-2xl font-bold text-red-600">
              {priorityDist.HIGH || 0}
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}



import React, { useState, useEffect } from 'react'
import { useSimulation } from '../hooks/useSimulation'
import { useConfig } from '../hooks/useConfig'
import TaskQueue from './TaskQueue'

export default function Dashboard() {
  const { status, metrics } = useSimulation()
  const { config } = useConfig()
  const [topology, setTopology] = useState(null)
  const [queueInfo, setQueueInfo] = useState({ fog_queue_length: 0, cloud_queue_length: 0, priority_distribution: {} })

  useEffect(() => {
    fetch('/api/network/topology')
      .then(res => {
        if (res.ok) {
          return res.json()
        }
        throw new Error('Backend not responding')
      })
      .then(data => setTopology(data))
      .catch(() => {
        // Silently handle - BackendStatus component shows warning
      })
    
    const fetchStatus = () => {
      fetch('/api/status')
        .then(res => {
          if (res.ok) {
            return res.json()
          }
          throw new Error('Backend not responding')
        })
        .then(data => {
          setQueueInfo({
            fog_queue_length: data.fog_queue_length || 0,
            cloud_queue_length: data.cloud_queue_length || 0,
            priority_distribution: data.priority_distribution || {}
          })
        })
        .catch(() => {
          // Silently handle - BackendStatus component shows warning
        })
    }
    
    fetchStatus()
    const interval = setInterval(fetchStatus, 2000)
    return () => clearInterval(interval)
  }, [])

  const fogNodes = config?.network?.fog_nodes || 3
  const iotDevices = config?.network?.iot_devices || 10

  return (
    <div className="space-y-6">
      <div className="mb-6 pb-4 border-b-2 border-gray-200">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">Fog Computing Simulation Dashboard</h1>
        <p className="text-sm sm:text-base text-gray-600">Advanced platform for fog computing research and analysis</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <div className="stat-card">
          <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
            <i className="fas fa-server text-blue-600 text-xl"></i>
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-2xl font-bold text-gray-900">{fogNodes}</h3>
            <p className="text-gray-600 text-sm">Fog Nodes</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
            <i className="fas fa-microchip text-green-600 text-xl"></i>
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-2xl font-bold text-gray-900">{iotDevices}</h3>
            <p className="text-gray-600 text-sm">IoT Devices</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center flex-shrink-0">
            <i className="fas fa-tasks text-purple-600 text-xl"></i>
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-2xl font-bold text-gray-900">{metrics?.tasks_processed || 0}</h3>
            <p className="text-gray-600 text-sm">Tasks Processed</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center flex-shrink-0">
            <i className="fas fa-clock text-orange-600 text-xl"></i>
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-2xl font-bold text-gray-900">{metrics?.avg_latency?.toFixed(1) || 0}ms</h3>
            <p className="text-gray-600 text-sm">Avg Latency</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        <div className="stat-card bg-indigo-50 border-2 border-indigo-200">
          <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center flex-shrink-0">
            <i className="fas fa-layer-group text-indigo-600 text-xl"></i>
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-2xl font-bold text-indigo-700">{queueInfo.fog_queue_length}</h3>
            <p className="text-gray-600 text-sm">Fog Queue Length</p>
            <p className="text-xs text-gray-500 mt-1">HIGH priority tasks</p>
          </div>
        </div>

        <div className="stat-card bg-purple-50 border-2 border-purple-200">
          <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center flex-shrink-0">
            <i className="fas fa-cloud text-purple-600 text-xl"></i>
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-2xl font-bold text-purple-700">{queueInfo.cloud_queue_length}</h3>
            <p className="text-gray-600 text-sm">Cloud Queue Length</p>
            <p className="text-xs text-gray-500 mt-1">MODERATE/LOW priority tasks</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center flex-shrink-0">
            <i className="fas fa-exclamation-triangle text-red-600 text-xl"></i>
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-2xl font-bold text-gray-900">{queueInfo.priority_distribution?.HIGH || 0}</h3>
            <p className="text-gray-600 text-sm">HIGH Priority Tasks</p>
          </div>
        </div>
      </div>

      <TaskQueue />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        <div className="card">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 sm:gap-0 mb-4">
            <h2 className="text-lg sm:text-xl font-semibold text-gray-900">Network Topology</h2>
            <button
              onClick={() => {
                fetch('/api/network/topology')
                  .then(res => res.json())
                  .then(data => setTopology(data))
              }}
              className="btn btn-secondary text-xs sm:text-sm"
            >
              <i className="fas fa-sync"></i>
              Refresh
            </button>
          </div>
          <NetworkTopology topology={topology} fogNodes={fogNodes} iotDevices={iotDevices} queueInfo={queueInfo} />
        </div>

        <div className="card">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 sm:gap-0 mb-4">
            <h2 className="text-lg sm:text-xl font-semibold text-gray-900">Recent Activity</h2>
            <button className="btn btn-secondary text-xs sm:text-sm">
              <i className="fas fa-trash"></i>
              Clear
            </button>
          </div>
          <ActivityLog />
        </div>
      </div>
    </div>
  )
}

function NetworkTopology({ topology, fogNodes, iotDevices, queueInfo }) {
  const centerX = 400
  const centerY = 200
  const radius = 120

  const generateFogNodes = () => {
    const nodes = []
    for (let i = 0; i < fogNodes; i++) {
      const angle = (2 * Math.PI * i) / fogNodes
      const x = centerX + radius * Math.cos(angle)
      const y = centerY + radius * Math.sin(angle)
      nodes.push({ id: i + 1, x, y })
    }
    return nodes
  }

  const fogNodesList = generateFogNodes()

  return (
    <div className="relative">
      <svg width="100%" height="400" viewBox="0 0 800 400" className="w-full">
        {/* Cloud Server */}
        <g>
          <circle cx="400" cy="50" r="30" fill="#38b2ac" stroke="#2c7a7b" strokeWidth="2" />
          <text x="400" y="55" textAnchor="middle" fill="white" fontWeight="bold" fontSize="12">
            CLOUD
          </text>
        </g>

        {/* Fog Nodes */}
        {fogNodesList.map((node, index) => {
          const tasksPerNode = Math.floor(queueInfo.fog_queue_length / fogNodes) + (index < (queueInfo.fog_queue_length % fogNodes) ? 1 : 0)
          return (
            <g key={node.id}>
              <circle cx={node.x} cy={node.y} r="25" fill="#667eea" stroke="#5a67d8" strokeWidth="2" />
              <text x={node.x} y={node.y + 5} textAnchor="middle" fill="white" fontWeight="bold" fontSize="10">
                F{node.id}
              </text>
              {tasksPerNode > 0 && (
                <text x={node.x} y={node.y + 20} textAnchor="middle" fill="#ef4444" fontWeight="bold" fontSize="9">
                  {tasksPerNode} tasks
                </text>
              )}
              <line
                x1="400"
                y1="80"
                x2={node.x}
                y2={node.y - 25}
                stroke="#a0aec0"
                strokeWidth="2"
                strokeDasharray="5,5"
              />
            </g>
          )
        })}

        {/* IoT Devices */}
        {Array.from({ length: Math.min(iotDevices, 12) }).map((_, i) => {
          const fogNodeIndex = i % fogNodes
          const fogNode = fogNodesList[fogNodeIndex]
          const deviceAngle = (2 * Math.PI * (i / fogNodes)) / (iotDevices / fogNodes)
          const deviceRadius = 60
          const x = fogNode.x + deviceRadius * Math.cos(deviceAngle)
          const y = fogNode.y + deviceRadius * Math.sin(deviceAngle)

          return (
            <g key={i}>
              <circle cx={x} cy={y} r="12" fill="#48bb78" stroke="#38a169" strokeWidth="1" />
              <text x={x} y={y + 3} textAnchor="middle" fill="white" fontWeight="bold" fontSize="8">
                I{i + 1}
              </text>
              <line
                x1={fogNode.x}
                y1={fogNode.y - 25}
                x2={x}
                y2={y - 12}
                stroke="#68d391"
                strokeWidth="1"
              />
            </g>
          )
        })}
      </svg>

      <div className="flex gap-4 mt-4 justify-center">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-teal-500 rounded-full"></div>
          <span className="text-sm text-gray-600">Cloud Server</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-indigo-500 rounded-full"></div>
          <span className="text-sm text-gray-600">Fog Nodes</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-green-500 rounded-full"></div>
          <span className="text-sm text-gray-600">IoT Devices</span>
        </div>
      </div>
    </div>
  )
}

function ActivityLog() {
  const [activities, setActivities] = useState([
    { message: 'Simulation environment initialized', timestamp: 'Just now', type: 'info' }
  ])

  useEffect(() => {
    const interval = setInterval(() => {
      fetch('/api/simulation/events')
        .then(res => res.json())
        .then(data => {
          if (data.events && data.events.length > 0) {
            setActivities(prev => [
              ...data.events.map(e => ({
                message: e.message,
                timestamp: new Date(e.timestamp).toLocaleTimeString(),
                type: e.type || 'info'
              })),
              ...prev
            ].slice(0, 15))
          }
        })
        .catch(console.error)
    }, 2000)

    return () => clearInterval(interval)
  }, [])

  const getIcon = (type) => {
    const icons = {
      info: 'fa-info-circle',
      warning: 'fa-exclamation-triangle',
      success: 'fa-check-circle',
      error: 'fa-exclamation-circle'
    }
    return icons[type] || 'fa-info-circle'
  }

  const getColor = (type) => {
    const colors = {
      info: 'bg-blue-100 text-blue-600',
      warning: 'bg-yellow-100 text-yellow-600',
      success: 'bg-green-100 text-green-600',
      error: 'bg-red-100 text-red-600'
    }
    return colors[type] || 'bg-blue-100 text-blue-600'
  }

  return (
    <div className="space-y-3 max-h-96 overflow-y-auto">
      {activities.map((activity, index) => (
        <div key={index} className="flex items-start gap-3">
          <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${getColor(activity.type)}`}>
            <i className={`fas ${getIcon(activity.type)} text-sm`}></i>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm text-gray-900">{activity.message}</p>
            <span className="text-xs text-gray-500">{activity.timestamp}</span>
          </div>
        </div>
      ))}
    </div>
  )
}



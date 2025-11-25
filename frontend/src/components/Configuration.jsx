import React, { useState, useEffect } from 'react'
import { useConfig } from '../hooks/useConfig'
import { getApiEndpoint } from '../utils/api'

export default function Configuration() {
  const { config, saveConfig, fetchConfig } = useConfig()
  const [activeTab, setActiveTab] = useState('network')
  const [formData, setFormData] = useState(config)
  const [notification, setNotification] = useState(null)
  const [devicePriorities, setDevicePriorities] = useState({})
  const [loadingPriorities, setLoadingPriorities] = useState(true)

  useEffect(() => {
    if (config && Object.keys(config).length > 0) {
      setFormData(config)
    }
  }, [config])

  useEffect(() => {
    fetchDevicePriorities()
  }, [])

  const fetchDevicePriorities = async () => {
    try {
      const res = await fetch(getApiEndpoint('/device-priorities'))
      if (res.ok) {
        const data = await res.json()
        setDevicePriorities(data.device_priorities || {})
      }
    } catch (error) {
      console.error('Error fetching device priorities:', error)
    } finally {
      setLoadingPriorities(false)
    }
  }

  const updateDevicePriority = async (deviceId, priority) => {
    const updated = { ...devicePriorities, [deviceId]: priority }
    setDevicePriorities(updated)
    
    try {
      const res = await fetch(getApiEndpoint('/device-priorities'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ device_priorities: { [deviceId]: priority } })
      })
      if (res.ok) {
        showNotification(`Device ${deviceId} priority updated to ${priority}`, 'success')
      }
    } catch (error) {
      console.error('Error updating device priority:', error)
      showNotification('Failed to update device priority', 'error')
      // Revert on error
      fetchDevicePriorities()
    }
  }

  const updateField = (path, value) => {
    const keys = path.split('.')
    setFormData(prev => {
      const newData = JSON.parse(JSON.stringify(prev)) // Deep clone
      let current = newData
      for (let i = 0; i < keys.length - 1; i++) {
        if (!current[keys[i]]) {
          current[keys[i]] = {}
        } else {
          current[keys[i]] = { ...current[keys[i]] }
        }
        current = current[keys[i]]
      }
      current[keys[keys.length - 1]] = value
      return newData
    })
  }

  const handleSave = async () => {
    if (!formData || Object.keys(formData).length === 0) {
      showNotification('No configuration data to save', 'error')
      return
    }
    
    // Ensure all required fields are present
    const configToSave = {
      simulation: formData.simulation || config.simulation || {
        duration: 100,
        enable_failures: true,
        failure_probability: 0.1
      },
      network: formData.network || config.network || {
        fog_nodes: 3,
        iot_devices: 10
      },
      tasks: formData.tasks || config.tasks || {
        rate_range: [0.1, 0.3],
        complexity_range: [50, 2000]
      },
      latency: formData.latency || config.latency || {
        base_latency: 0.01,
        cloud_latency: 5.0
      },
      offloading: formData.offloading || config.offloading || {
        complexity_threshold: 1000,
        utilization_threshold: 0.8
      }
    }
    
    const success = await saveConfig(configToSave)
    if (success) {
      showNotification('Configuration saved successfully!', 'success')
      // Refresh device priorities if device count changed
      if (configToSave.network.iot_devices !== (config?.network?.iot_devices || 10)) {
        fetchDevicePriorities()
      }
    } else {
      showNotification('Failed to save configuration', 'error')
    }
  }

  const handleReset = async () => {
    await fetchConfig()
    // Wait a bit for config to load
    setTimeout(() => {
      if (config && Object.keys(config).length > 0) {
        setFormData(config)
      }
      showNotification('Configuration reset to defaults', 'info')
    }, 500)
  }

  const showNotification = (message, type) => {
    setNotification({ message, type })
    setTimeout(() => setNotification(null), 3000)
  }

  const tabs = [
    { id: 'network', label: 'Network' },
    { id: 'tasks', label: 'Tasks' },
    { id: 'latency', label: 'Latency' },
    { id: 'offloading', label: 'Offloading' },
    { id: 'device-priorities', label: 'Device Priorities' }
  ]

  return (
    <div className="space-y-6">
      {notification && (
        <div className={`p-4 rounded-md ${
          notification.type === 'success' ? 'bg-green-50 text-green-700' :
          notification.type === 'error' ? 'bg-red-50 text-red-700' :
          'bg-blue-50 text-blue-700'
        }`}>
          {notification.message}
        </div>
      )}

      <div className="mb-6 pb-4 border-b-2 border-gray-200">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Configuration Management</h1>
        <p className="text-gray-600">Configure simulation parameters and network topology</p>
      </div>

      <div className="card">
        <div className="flex gap-2 mb-6 bg-gray-100 p-1 rounded-lg">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex-1 py-2 px-4 rounded-md font-medium transition-all ${
                activeTab === tab.id
                  ? 'bg-white text-primary shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        <div className="space-y-6">
          {activeTab === 'network' && (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Number of Fog Nodes
                </label>
                <input
                  type="number"
                  value={formData?.network?.fog_nodes ?? 3}
                  onChange={(e) => {
                    const val = parseInt(e.target.value)
                    if (!isNaN(val) && val > 0) {
                      updateField('network.fog_nodes', val)
                    }
                  }}
                  min="1"
                  max="20"
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Number of IoT Devices
                </label>
                <input
                  type="number"
                  value={formData?.network?.iot_devices ?? 10}
                  onChange={(e) => {
                    const val = parseInt(e.target.value)
                    if (!isNaN(val) && val > 0) {
                      updateField('network.iot_devices', val)
                    }
                  }}
                  min="1"
                  max="100"
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Cloud CPU (MIPS)
                </label>
                <input
                  type="number"
                  value={10000}
                  disabled
                  className="w-full px-4 py-2 border border-gray-300 rounded-md bg-gray-100"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Cloud Memory (MB)
                </label>
                <input
                  type="number"
                  value={32000}
                  disabled
                  className="w-full px-4 py-2 border border-gray-300 rounded-md bg-gray-100"
                />
              </div>
            </div>
          )}

          {activeTab === 'tasks' && (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Task Rate (min)
                </label>
                <input
                  type="number"
                  value={isNaN(formData?.tasks?.rate_range?.[0]) ? 0.1 : (formData?.tasks?.rate_range?.[0] ?? 0.1)}
                  onChange={(e) => {
                    const val = parseFloat(e.target.value)
                    if (!isNaN(val) && val >= 0) {
                      const newRange = [...(formData?.tasks?.rate_range || [0.1, 0.3])]
                      newRange[0] = val
                      updateField('tasks.rate_range', newRange)
                    }
                  }}
                  min="0.01"
                  max="1"
                  step="0.01"
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Task Rate (max)
                </label>
                <input
                  type="number"
                  value={isNaN(formData?.tasks?.rate_range?.[1]) ? 0.3 : (formData?.tasks?.rate_range?.[1] ?? 0.3)}
                  onChange={(e) => {
                    const val = parseFloat(e.target.value)
                    if (!isNaN(val) && val >= 0) {
                      const newRange = [...(formData?.tasks?.rate_range || [0.1, 0.3])]
                      newRange[1] = val
                      updateField('tasks.rate_range', newRange)
                    }
                  }}
                  min="0.01"
                  max="1"
                  step="0.01"
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Complexity (min MIPS)
                </label>
                <input
                  type="number"
                  value={isNaN(formData?.tasks?.complexity_range?.[0]) ? 50 : (formData?.tasks?.complexity_range?.[0] ?? 50)}
                  onChange={(e) => {
                    const val = parseInt(e.target.value)
                    if (!isNaN(val) && val > 0) {
                      const newRange = [...(formData?.tasks?.complexity_range || [50, 2000])]
                      newRange[0] = val
                      updateField('tasks.complexity_range', newRange)
                    }
                  }}
                  min="1"
                  max="10000"
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Complexity (max MIPS)
                </label>
                <input
                  type="number"
                  value={isNaN(formData?.tasks?.complexity_range?.[1]) ? 2000 : (formData?.tasks?.complexity_range?.[1] ?? 2000)}
                  onChange={(e) => {
                    const val = parseInt(e.target.value)
                    if (!isNaN(val) && val > 0) {
                      const newRange = [...(formData?.tasks?.complexity_range || [50, 2000])]
                      newRange[1] = val
                      updateField('tasks.complexity_range', newRange)
                    }
                  }}
                  min="1"
                  max="10000"
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary"
                />
              </div>
            </div>
          )}

          {activeTab === 'latency' && (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Base Latency per Distance
                </label>
                <input
                  type="number"
                  value={isNaN(formData?.latency?.base_latency) ? 0.01 : (formData?.latency?.base_latency ?? 0.01)}
                  onChange={(e) => {
                    const val = parseFloat(e.target.value)
                    if (!isNaN(val) && val >= 0) {
                      updateField('latency.base_latency', val)
                    }
                  }}
                  min="0.001"
                  max="0.1"
                  step="0.001"
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Cloud Base Latency
                </label>
                <input
                  type="number"
                  value={isNaN(formData?.latency?.cloud_latency) ? 5.0 : (formData?.latency?.cloud_latency ?? 5.0)}
                  onChange={(e) => {
                    const val = parseFloat(e.target.value)
                    if (!isNaN(val) && val >= 0) {
                      updateField('latency.cloud_latency', val)
                    }
                  }}
                  min="0.1"
                  max="50"
                  step="0.1"
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Fog-to-Cloud Multiplier
                </label>
                <input
                  type="number"
                  value={0.02}
                  disabled
                  className="w-full px-4 py-2 border border-gray-300 rounded-md bg-gray-100"
                />
              </div>
            </div>
          )}

          {activeTab === 'offloading' && (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Complexity Threshold
                </label>
                <input
                  type="number"
                  value={isNaN(formData?.offloading?.complexity_threshold) ? 1000 : (formData?.offloading?.complexity_threshold ?? 1000)}
                  onChange={(e) => {
                    const val = parseInt(e.target.value)
                    if (!isNaN(val) && val > 0) {
                      updateField('offloading.complexity_threshold', val)
                    }
                  }}
                  min="100"
                  max="10000"
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Utilization Threshold
                </label>
                <input
                  type="number"
                  value={isNaN(formData?.offloading?.utilization_threshold) ? 0.8 : (formData?.offloading?.utilization_threshold ?? 0.8)}
                  onChange={(e) => {
                    const val = parseFloat(e.target.value)
                    if (!isNaN(val) && val >= 0 && val <= 1) {
                      updateField('offloading.utilization_threshold', val)
                    }
                  }}
                  min="0.1"
                  max="1"
                  step="0.1"
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Deadline Threshold
                </label>
                <input
                  type="number"
                  value={5.0}
                  disabled
                  className="w-full px-4 py-2 border border-gray-300 rounded-md bg-gray-100"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Queue Length Threshold
                </label>
                <input
                  type="number"
                  value={5}
                  disabled
                  className="w-full px-4 py-2 border border-gray-300 rounded-md bg-gray-100"
                />
              </div>
            </div>
          )}

          {activeTab === 'device-priorities' && (
            <div className="space-y-4">
              <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-md">
                <p className="text-sm text-blue-800">
                  <strong>How it works:</strong> Each IoT device can be assigned a priority level. 
                  Tasks generated by a device will inherit that device's priority. 
                  HIGH priority tasks go to fog, LOW/MODERATE go to cloud.
                </p>
              </div>
              
              {loadingPriorities ? (
                <div className="text-center py-8 text-gray-500">Loading device priorities...</div>
              ) : (
                <div className="space-y-3">
                  {Array.from({ length: formData?.network?.iot_devices || 10 }, (_, i) => {
                    const deviceId = `device_${i + 1}`
                    const currentPriority = devicePriorities[deviceId] || 'MODERATE'
                    
                    return (
                      <div key={deviceId} className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 gap-3 sm:gap-0">
                        <div className="flex items-center gap-3 sm:gap-4">
                          <div className="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center flex-shrink-0">
                            <i className="fas fa-microchip text-indigo-600"></i>
                          </div>
                          <div>
                            <h4 className="font-semibold text-gray-900">Device {i + 1}</h4>
                            <p className="text-xs sm:text-sm text-gray-500">ID: {deviceId}</p>
                          </div>
                        </div>
                        
                        <div className="flex items-center gap-2 sm:gap-3 w-full sm:w-auto">
                          <span className="text-xs sm:text-sm text-gray-600">Priority:</span>
                          <select
                            value={currentPriority}
                            onChange={(e) => updateDevicePriority(deviceId, e.target.value)}
                            className="flex-1 sm:flex-none px-2 sm:px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary text-sm"
                          >
                            <option value="HIGH">HIGH</option>
                            <option value="MODERATE">MODERATE</option>
                            <option value="LOW">LOW</option>
                          </select>
                          <span className={`px-2 sm:px-3 py-1 rounded text-xs font-semibold ${
                            currentPriority === 'HIGH' ? 'bg-red-100 text-red-700' :
                            currentPriority === 'MODERATE' ? 'bg-orange-100 text-orange-700' :
                            'bg-green-100 text-green-700'
                          }`}>
                            {currentPriority}
                          </span>
                        </div>
                      </div>
                    )
                  })}
                </div>
              )}
              
              <div className="mt-6 p-4 bg-gray-50 rounded-md">
                <h4 className="font-semibold text-gray-900 mb-2">Quick Actions</h4>
                <div className="flex flex-wrap gap-2">
                  <button
                    onClick={() => {
                      const updated = {}
                      const numDevices = formData?.network?.iot_devices || 10
                      for (let i = 1; i <= numDevices; i++) {
                        updated[`device_${i}`] = 'HIGH'
                      }
                      setDevicePriorities(updated)
                      fetch(getApiEndpoint('/device-priorities'), {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ device_priorities: updated })
                      }).then(() => showNotification('All devices set to HIGH priority', 'success'))
                    }}
                    className="btn btn-secondary text-sm"
                  >
                    Set All HIGH
                  </button>
                  <button
                    onClick={() => {
                      const updated = {}
                      const numDevices = formData?.network?.iot_devices || 10
                      for (let i = 1; i <= numDevices; i++) {
                        updated[`device_${i}`] = 'MODERATE'
                      }
                      setDevicePriorities(updated)
                      fetch(getApiEndpoint('/device-priorities'), {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ device_priorities: updated })
                      }).then(() => showNotification('All devices set to MODERATE priority', 'success'))
                    }}
                    className="btn btn-secondary text-sm"
                  >
                    Set All MODERATE
                  </button>
                  <button
                    onClick={() => {
                      const updated = {}
                      const numDevices = formData?.network?.iot_devices || 10
                      for (let i = 1; i <= numDevices; i++) {
                        updated[`device_${i}`] = 'LOW'
                      }
                      setDevicePriorities(updated)
                      fetch(getApiEndpoint('/device-priorities'), {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ device_priorities: updated })
                      }).then(() => showNotification('All devices set to LOW priority', 'success'))
                    }}
                    className="btn btn-secondary text-sm"
                  >
                    Set All LOW
                  </button>
                  <button
                    onClick={() => {
                      fetchDevicePriorities()
                      showNotification('Device priorities reloaded', 'info')
                    }}
                    className="btn btn-secondary text-sm"
                  >
                    <i className="fas fa-sync"></i>
                    Reload
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="flex gap-3 mt-6 pt-6 border-t border-gray-200">
          <button onClick={handleSave} className="btn btn-primary">
            <i className="fas fa-save"></i>
            Save Configuration
          </button>
          <button onClick={fetchConfig} className="btn btn-secondary">
            <i className="fas fa-upload"></i>
            Load Configuration
          </button>
          <button onClick={handleReset} className="btn btn-secondary">
            <i className="fas fa-undo"></i>
            Reset to Default
          </button>
        </div>
      </div>
    </div>
  )
}


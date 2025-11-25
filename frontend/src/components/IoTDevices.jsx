import React, { useState, useEffect } from 'react'
import { collection, getDocs, addDoc, deleteDoc, doc } from 'firebase/firestore'
import { db } from '../firebase'

export default function IoTDevices({ user }) {
  const [devices, setDevices] = useState([])
  const [loading, setLoading] = useState(true)
  const [devicePriorities, setDevicePriorities] = useState({})

  useEffect(() => {
    loadDevices()
    fetchDevicePriorities()
  }, [user])

  const fetchDevicePriorities = async () => {
    try {
      const res = await fetch('/api/device-priorities')
      if (res.ok) {
        const data = await res.json()
        setDevicePriorities(data.device_priorities || {})
      }
    } catch (error) {
      console.error('Error fetching device priorities:', error)
    }
  }

  const updateDevicePriority = async (deviceId, priority) => {
    try {
      const res = await fetch('/api/device-priorities', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ device_priorities: { [deviceId]: priority } })
      })
      if (res.ok) {
        setDevicePriorities(prev => ({ ...prev, [deviceId]: priority }))
        alert(`Device priority updated to ${priority}`)
      }
    } catch (error) {
      console.error('Error updating device priority:', error)
      alert('Failed to update device priority')
    }
  }

  const getPriorityBadge = (priority) => {
    const colors = {
      HIGH: 'bg-red-100 text-red-700 border-red-300',
      MODERATE: 'bg-orange-100 text-orange-700 border-orange-300',
      LOW: 'bg-green-100 text-green-700 border-green-300'
    }
    
    return (
      <span className={`px-2 py-1 rounded text-xs font-semibold border ${colors[priority] || 'bg-gray-100 text-gray-700'}`}>
        {priority || 'MODERATE'}
      </span>
    )
  }

  const loadDevices = async () => {
    if (!user || !db) {
      // Demo devices for guest mode
      setDevices(getDemoDevices())
      setLoading(false)
      return
    }

    try {
      const querySnapshot = await getDocs(collection(db, 'iot_devices'))
      const deviceList = []
      querySnapshot.forEach((doc) => {
        deviceList.push({ id: doc.id, ...doc.data() })
      })
      setDevices(deviceList)
    } catch (error) {
      console.error('Error loading devices:', error)
      setDevices(getDemoDevices())
    } finally {
      setLoading(false)
    }
  }

  const getDemoDevices = () => {
    const deviceTypes = ['Sensor', 'Actuator', 'Camera', 'Thermostat']
    return Array.from({ length: 10 }, (_, i) => {
      const deviceId = `device_${i + 1}`
      return {
        id: `demo_${i + 1}`,
        device_id: deviceId,
        name: `IoT Device ${i + 1}`,
        type: deviceTypes[i % 4],
        location: `Zone ${Math.ceil((i + 1) / 3)}`,
        status: 'active',
        priority: devicePriorities[deviceId] || 'MODERATE'
      }
    })
  }

  const handleAddDevice = async () => {
    if (!user) {
      alert('Please login to add devices')
      return
    }

    const name = prompt('Device name:')
    const type = prompt('Device type (Sensor, Actuator, etc.):')
    const location = prompt('Device location:')

    if (name && type && location) {
      try {
        await addDoc(collection(db, 'iot_devices'), {
          name,
          type,
          location,
          status: 'active',
          userId: user.uid,
          createdAt: new Date()
        })
        loadDevices()
      } catch (error) {
        console.error('Error adding device:', error)
        alert('Failed to add device')
      }
    }
  }

  const handleDeleteDevice = async (deviceId) => {
    if (!user || deviceId.startsWith('demo_')) {
      alert('Cannot delete demo devices. Please login to manage devices.')
      return
    }

    if (confirm('Are you sure you want to delete this device?')) {
      try {
        await deleteDoc(doc(db, 'iot_devices', deviceId))
        loadDevices()
      } catch (error) {
        console.error('Error deleting device:', error)
        alert('Failed to delete device')
      }
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading devices...</div>
  }

  return (
    <div className="space-y-6">
      <div className="mb-6 pb-4 border-b-2 border-gray-200">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">IoT Device Management</h1>
        <p className="text-gray-600">Manage and configure IoT devices for your fog computing simulation</p>
      </div>

      <div className="flex gap-3 mb-6">
        <button onClick={handleAddDevice} className="btn btn-primary">
          <i className="fas fa-plus"></i>
          Add IoT Device
        </button>
        <button onClick={loadDevices} className="btn btn-secondary">
          <i className="fas fa-sync"></i>
          Refresh Devices
        </button>
      </div>

      {devices.length === 0 ? (
        <div className="card text-center py-12">
          <i className="fas fa-microchip text-5xl text-gray-300 mb-4"></i>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No IoT Devices</h3>
          <p className="text-gray-600">Add your first IoT device to get started</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
          {devices.map(device => {
            const deviceId = device.device_id || `device_${device.id?.replace('demo_', '') || '1'}`
            const currentPriority = devicePriorities[deviceId] || device.priority || 'MODERATE'
            
            return (
              <div key={device.id} className="card">
                <div className="flex items-start justify-between mb-4">
                  <h4 className="text-lg font-semibold text-gray-900">{device.name || 'IoT Device'}</h4>
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleDeleteDevice(device.id)}
                      className="text-red-500 hover:text-red-700"
                    >
                      <i className="fas fa-trash"></i>
                    </button>
                  </div>
                </div>
                <div className="space-y-3 text-sm">
                  <p>
                    <strong className="text-gray-700">Type:</strong>{' '}
                    <span className="text-gray-600">{device.type || 'Sensor'}</span>
                  </p>
                  <p>
                    <strong className="text-gray-700">Location:</strong>{' '}
                    <span className="text-gray-600">{device.location || 'Unknown'}</span>
                  </p>
                  <p>
                    <strong className="text-gray-700">Status:</strong>{' '}
                    <span className={`inline-block px-2 py-1 rounded text-xs font-medium ${
                      device.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
                    }`}>
                      {device.status || 'Active'}
                    </span>
                  </p>
                  <div>
                    <strong className="text-gray-700 block mb-2">Task Priority:</strong>
                    <div className="flex items-center gap-2">
                      <select
                        value={currentPriority}
                        onChange={(e) => updateDevicePriority(deviceId, e.target.value)}
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-primary"
                      >
                        <option value="HIGH">HIGH</option>
                        <option value="MODERATE">MODERATE</option>
                        <option value="LOW">LOW</option>
                      </select>
                      {getPriorityBadge(currentPriority)}
                    </div>
                    <p className="text-xs text-gray-500 mt-1">
                      Tasks from this device will be {currentPriority === 'HIGH' ? 'processed on fog' : 'offloaded to cloud'}
                    </p>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}



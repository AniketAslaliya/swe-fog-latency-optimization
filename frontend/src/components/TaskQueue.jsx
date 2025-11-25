import React, { useState, useEffect } from 'react'
import { getApiEndpoint } from '../utils/api'

export default function TaskQueue() {
  const [tasks, setTasks] = useState({ fog_queue: [], cloud_queue: [], active_tasks: [] })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchTasks = () => {
      fetch(getApiEndpoint('/tasks'))
        .then(res => res.json())
        .then(data => {
          setTasks(data)
          setLoading(false)
        })
        .catch(console.error)
    }

    fetchTasks()
    const interval = setInterval(fetchTasks, 2000)
    return () => clearInterval(interval)
  }, [])

  const getPriorityBadge = (priority) => {
    const colors = {
      HIGH: 'bg-red-100 text-red-700 border-red-300',
      MODERATE: 'bg-orange-100 text-orange-700 border-orange-300',
      LOW: 'bg-green-100 text-green-700 border-green-300'
    }
    
    return (
      <span className={`px-2 py-1 rounded text-xs font-semibold border ${colors[priority] || 'bg-gray-100 text-gray-700'}`}>
        {priority}
      </span>
    )
  }

  const formatTime = (timestamp) => {
    if (!timestamp) return 'N/A'
    return new Date(timestamp).toLocaleTimeString()
  }

  if (loading) {
    return <div className="text-center py-4 text-gray-500">Loading tasks...</div>
  }

  const allTasks = [
    ...tasks.fog_queue.map(t => ({ ...t, queue: 'fog' })),
    ...tasks.cloud_queue.map(t => ({ ...t, queue: 'cloud' })),
    ...tasks.active_tasks.map(t => ({ ...t, queue: 'active' }))
  ].sort((a, b) => b.task_id - a.task_id)

  return (
    <div className="card">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 sm:gap-0 mb-4">
        <h2 className="text-xl font-semibold text-gray-900">Task Queue</h2>
        <div className="flex flex-wrap gap-3 sm:gap-4 text-sm">
          <span className="text-gray-600 whitespace-nowrap">
            Fog: <span className="font-semibold text-indigo-600">{tasks.fog_queue.length}</span>
          </span>
          <span className="text-gray-600 whitespace-nowrap">
            Cloud: <span className="font-semibold text-purple-600">{tasks.cloud_queue.length}</span>
          </span>
          <span className="text-gray-600 whitespace-nowrap">
            Active: <span className="font-semibold text-blue-600">{tasks.active_tasks.length}</span>
          </span>
        </div>
      </div>

      <div className="overflow-x-auto -mx-6 sm:mx-0">
        <table className="w-full text-sm border-collapse">
          <thead className="bg-gray-50">
            <tr className="border-b-2 border-gray-200">
              <th className="text-left py-3 px-4 sm:px-6 font-semibold text-gray-700">Task ID</th>
              <th className="text-left py-3 px-4 sm:px-6 font-semibold text-gray-700">Priority</th>
              <th className="text-left py-3 px-4 sm:px-6 font-semibold text-gray-700">Complexity</th>
              <th className="text-left py-3 px-4 sm:px-6 font-semibold text-gray-700">Assigned To</th>
              <th className="text-left py-3 px-4 sm:px-6 font-semibold text-gray-700">Arrival Time</th>
              <th className="text-left py-3 px-4 sm:px-6 font-semibold text-gray-700">Status</th>
            </tr>
          </thead>
          <tbody>
            {allTasks.length === 0 ? (
              <tr>
                <td colSpan="6" className="text-center py-12 text-gray-500">
                  <div className="flex flex-col items-center gap-2">
                    <i className="fas fa-inbox text-4xl text-gray-300"></i>
                    <p>No tasks in queue</p>
                  </div>
                </td>
              </tr>
            ) : (
              allTasks.slice(0, 20).map(task => (
                <tr key={task.task_id} className="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                  <td className="py-3 px-4 sm:px-6 font-mono text-gray-900 font-medium">#{task.task_id}</td>
                  <td className="py-3 px-4 sm:px-6">{getPriorityBadge(task.priority)}</td>
                  <td className="py-3 px-4 sm:px-6 text-gray-700">{task.complexity}</td>
                  <td className="py-3 px-4 sm:px-6">
                    <span className={`inline-block px-2 py-1 rounded text-xs font-medium ${
                      task.node_assigned === 'fog' 
                        ? 'bg-indigo-100 text-indigo-700' 
                        : 'bg-purple-100 text-purple-700'
                    }`}>
                      {task.node_assigned?.toUpperCase() || 'N/A'}
                    </span>
                  </td>
                  <td className="py-3 px-4 sm:px-6 text-gray-600">{task.arrival_time?.toFixed(2) || 'N/A'}s</td>
                  <td className="py-3 px-4 sm:px-6">
                    <span className={`inline-block px-2 py-1 rounded text-xs font-medium ${
                      task.queue === 'active' 
                        ? 'bg-blue-100 text-blue-700' 
                        : task.queue === 'fog'
                        ? 'bg-yellow-100 text-yellow-700'
                        : 'bg-gray-100 text-gray-700'
                    }`}>
                      {task.queue === 'active' ? 'Processing' : task.queue === 'fog' ? 'Fog Queue' : 'Cloud Queue'}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}



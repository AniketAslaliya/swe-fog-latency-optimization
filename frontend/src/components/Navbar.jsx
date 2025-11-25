import React from 'react'
import { signOut } from 'firebase/auth'
import { auth } from '../firebase'
import { useSimulation } from '../hooks/useSimulation'
import { useConfig } from '../hooks/useConfig'

export default function Navbar({ currentSection, setCurrentSection, user, setShowLogin }) {
  const { status, startSimulation, stopSimulation } = useSimulation()
  const { config } = useConfig()
  const sections = [
    { id: 'dashboard', label: 'Dashboard', icon: 'fa-tachometer-alt' },
    { id: 'simulation', label: 'Simulation', icon: 'fa-play-circle' },
    { id: 'configuration', label: 'Configuration', icon: 'fa-cog' },
    { id: 'iot-devices', label: 'IoT Devices', icon: 'fa-microchip' },
    { id: 'analytics', label: 'Analytics', icon: 'fa-chart-line' },
    { id: 'documentation', label: 'Docs', icon: 'fa-book' },
  ]

  const handleLogout = async () => {
    try {
      await signOut(auth)
      setShowLogin(true)
    } catch (error) {
      console.error('Logout error:', error)
    }
  }

  return (
    <nav className="bg-white border-b-2 border-gray-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between h-auto sm:h-16 py-2 sm:py-0">
        <div className="flex items-center gap-2 mb-2 sm:mb-0">
          <i className="fas fa-cloud text-primary text-xl sm:text-2xl"></i>
          <span className="text-lg sm:text-xl font-bold text-gray-900">Fog Computing Simulator</span>
        </div>

        <div className="flex items-center gap-1 flex-wrap justify-center mb-2 sm:mb-0">
          {sections.map(section => (
            <button
              key={section.id}
              onClick={() => setCurrentSection(section.id)}
              className={`flex items-center gap-1 sm:gap-2 px-2 sm:px-4 py-1 sm:py-2 rounded-md font-medium text-xs sm:text-sm transition-all ${
                currentSection === section.id
                  ? 'bg-primary text-white'
                  : 'text-gray-600 hover:bg-gray-100 hover:text-primary'
              }`}
            >
              <i className={`fas ${section.icon}`}></i>
              <span className="hidden sm:inline">{section.label}</span>
            </button>
          ))}
        </div>

        <div className="flex items-center gap-2 flex-wrap justify-center">
          <button
            onClick={() => {
              if (status.running) {
                stopSimulation()
              } else {
                startSimulation(config?.simulation?.duration || 100)
              }
            }}
            className={`btn ${status.running ? 'btn-danger' : 'btn-primary'}`}
          >
            <i className={`fas ${status.running ? 'fa-stop' : 'fa-play'}`}></i>
            {status.running ? 'Stop Simulation' : 'Run Simulation'}
          </button>
          {user ? (
            <div className="flex items-center gap-2 sm:gap-3">
              <span className="text-xs sm:text-sm text-gray-700 hidden sm:inline">{user.email}</span>
              <button onClick={handleLogout} className="btn btn-secondary text-xs sm:text-sm">
                <i className="fas fa-sign-out-alt"></i>
                <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <span className="text-xs sm:text-sm text-gray-600 hidden sm:inline">Guest Mode</span>
              <button onClick={() => setShowLogin(true)} className="btn btn-secondary text-xs sm:text-sm">
                <i className="fas fa-sign-in-alt"></i>
                <span className="hidden sm:inline">Login</span>
              </button>
              <button onClick={() => setShowLogin(true)} className="btn btn-primary text-xs sm:text-sm">
                <i className="fas fa-user-plus"></i>
                <span className="hidden sm:inline">Sign Up</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  )
}


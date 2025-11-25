import React, { useState } from 'react'
import { signOut } from 'firebase/auth'
import { auth } from '../firebase'
import { useSimulation } from '../hooks/useSimulation'
import { useConfig } from '../hooks/useConfig'

export default function Navbar({ currentSection, setCurrentSection, user, setShowLogin }) {
  const { status, startSimulation, stopSimulation } = useSimulation()
  const { config } = useConfig()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
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
    <nav className="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo Section */}
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg shadow-sm">
              <i className="fas fa-cloud text-white text-lg"></i>
            </div>
            <div className="flex flex-col">
              <span className="text-base font-bold text-gray-900 leading-tight">Fog Computing</span>
              <span className="text-xs text-gray-500 leading-tight">Simulator</span>
            </div>
          </div>

          {/* Navigation Links - Desktop */}
          <div className="hidden md:flex items-center gap-1">
            {sections.map(section => (
              <button
                key={section.id}
                onClick={() => setCurrentSection(section.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium text-sm transition-all duration-200 ${
                  currentSection === section.id
                    ? 'bg-indigo-50 text-indigo-700 shadow-sm'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                }`}
              >
                <i className={`fas ${section.icon} ${currentSection === section.id ? 'text-indigo-600' : ''}`}></i>
                <span>{section.label}</span>
              </button>
            ))}
          </div>

          {/* Right Section */}
          <div className="flex items-center gap-3">
            {/* Simulation Control */}
            <button
              onClick={() => {
                if (status.running) {
                  stopSimulation()
                } else {
                  startSimulation(config?.simulation?.duration || 100)
                }
              }}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium text-sm transition-all duration-200 shadow-sm ${
                status.running
                  ? 'bg-red-500 hover:bg-red-600 text-white'
                  : 'bg-indigo-600 hover:bg-indigo-700 text-white'
              }`}
            >
              <i className={`fas ${status.running ? 'fa-stop' : 'fa-play'}`}></i>
              <span className="hidden sm:inline">{status.running ? 'Stop' : 'Run'}</span>
            </button>

            {/* User Section */}
            {user ? (
              <div className="flex items-center gap-3">
                <div className="hidden lg:flex flex-col items-end">
                  <span className="text-xs font-medium text-gray-900">{user.email?.split('@')[0]}</span>
                  <span className="text-xs text-gray-500">{user.email?.split('@')[1]}</span>
                </div>
                <div className="w-8 h-8 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-full flex items-center justify-center text-white text-sm font-semibold shadow-sm">
                  {user.email?.charAt(0).toUpperCase()}
                </div>
                <button 
                  onClick={handleLogout} 
                  className="hidden sm:flex items-center gap-2 px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-all duration-200"
                  title="Logout"
                >
                  <i className="fas fa-sign-out-alt"></i>
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <span className="hidden lg:inline text-xs text-gray-500 px-2">Guest Mode</span>
                <button 
                  onClick={() => setShowLogin(true)} 
                  className="flex items-center gap-2 px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-all duration-200"
                >
                  <i className="fas fa-sign-in-alt"></i>
                  <span className="hidden sm:inline text-sm">Login</span>
                </button>
              </div>
            )}

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden flex items-center justify-center w-10 h-10 text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-all"
            >
              <i className={`fas ${mobileMenuOpen ? 'fa-times' : 'fa-bars'} text-lg`}></i>
            </button>
          </div>
        </div>

        {/* Mobile Navigation Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden pb-4 border-t border-gray-100 mt-2 pt-4">
            <div className="grid grid-cols-2 gap-2">
              {sections.map(section => (
                <button
                  key={section.id}
                  onClick={() => {
                    setCurrentSection(section.id)
                    setMobileMenuOpen(false)
                  }}
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg font-medium text-sm transition-all ${
                    currentSection === section.id
                      ? 'bg-indigo-50 text-indigo-700'
                      : 'text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  <i className={`fas ${section.icon}`}></i>
                  <span>{section.label}</span>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}


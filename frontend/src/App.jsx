import React, { useState, useEffect } from 'react'
import { onAuthStateChanged } from 'firebase/auth'
import { auth } from './firebase'
import Navbar from './components/Navbar'
import Dashboard from './components/Dashboard'
import Simulation from './components/Simulation'
import Configuration from './components/Configuration'
import IoTDevices from './components/IoTDevices'
import Analytics from './components/Analytics'
import Documentation from './components/Documentation'
import Login from './components/Login'
import LoadingScreen from './components/LoadingScreen'
import BackendStatus from './components/BackendStatus'

function App() {
  const [currentSection, setCurrentSection] = useState('dashboard')
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showLogin, setShowLogin] = useState(false)

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user)
      setLoading(false)
      // Don't force login - allow guest mode
      // if (!user) {
      //   setShowLogin(true)
      // }
    })

    return () => unsubscribe()
  }, [])

  if (loading) {
    return <LoadingScreen />
  }

  // Show login only if explicitly requested, otherwise show app in guest mode
  if (showLogin) {
    return <Login onLoginSuccess={() => setShowLogin(false)} />
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Navbar 
        currentSection={currentSection}
        setCurrentSection={setCurrentSection}
        user={user}
        setShowLogin={setShowLogin}
      />
      
      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 py-4 sm:py-8">
        <BackendStatus />
        {currentSection === 'dashboard' && <Dashboard />}
        {currentSection === 'simulation' && <Simulation />}
        {currentSection === 'configuration' && <Configuration />}
        {currentSection === 'iot-devices' && <IoTDevices user={user} />}
        {currentSection === 'analytics' && <Analytics />}
        {currentSection === 'documentation' && <Documentation />}
      </main>
    </div>
  )
}

export default App



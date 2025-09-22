import { useState, useEffect } from 'react'
import DriversSection from './components/DriversSection'
import VehiclesSection from './components/VehiclesSection'
import LogsSection from './components/LogsSection'
import TripsSection from './components/TripsSection'
import './App.css'

function App() {
  const [activeSection, setActiveSection] = useState('drivers')
  const [apiStatus, setApiStatus] = useState('checking')

  useEffect(() => {
    checkApiStatus()
    const interval = setInterval(checkApiStatus, 30000)
    return () => clearInterval(interval)
  }, [])

  const checkApiStatus = async () => {
    try {
      const response = await fetch('/api/status/')
      if (response.ok) {
        setApiStatus('online')
      } else {
        setApiStatus('offline')
      }
    } catch (error) {
      setApiStatus('offline')
    }
  }

  const sections = {
    drivers: { component: DriversSection, label: '👥 Drivers', icon: '👥' },
    vehicles: { component: VehiclesSection, label: '🚚 Vehicles', icon: '🚚' },
    logs: { component: LogsSection, label: '📊 Duty Logs', icon: '📊' },
    trips: { component: TripsSection, label: '🛣️ Trips', icon: '🛣️' }
  }

  const ActiveComponent = sections[activeSection]?.component || DriversSection

  return (
    <div className="container">
      <div className="header">
        <h1>🚛 ELD Driver Management</h1>
        <p>Electronic Logging Device - Fleet Management System</p>
        <div className={`status-badge ${apiStatus === 'online' ? 'status-online' : 'status-offline'}`}>
          {apiStatus === 'online' ? '🟢 API Online' : apiStatus === 'offline' ? '🔴 API Offline' : '🔄 Checking...'}
        </div>
      </div>

      <nav className="nav">
        {Object.entries(sections).map(([key, section]) => (
          <button
            key={key}
            className={`nav-btn ${activeSection === key ? 'active' : ''}`}
            onClick={() => setActiveSection(key)}
          >
            {section.label}
          </button>
        ))}
      </nav>

      <div className="content-card">
        <ActiveComponent />
      </div>
    </div>
  )
}

export default App
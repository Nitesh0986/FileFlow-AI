import { useState, useEffect } from 'react'
import Dashboard from './components/Dashboard'
import Files from './components/Files'
import Organize from './components/Organize'
import Duplicates from './components/Duplicates'
import Rename from './components/Rename'
import Settings from './components/settings'
import Sidebar from './components/Sidebar'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/stats')
      const data = await response.json()

      if (data.success) {
        setStats(data.data)
      }
    } catch (error) {
      console.error('Failed to fetch stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return (
          <Dashboard
            stats={stats}
            loading={loading}
            onRefresh={fetchStats}
          />
        )

      case 'files':
        return <Files />

      case 'organize':
        return <Organize />

      case 'duplicates':
        return <Duplicates />

      case 'rename':
        return <Rename />

      case 'settings':
        return <Settings />

      default:
        return (
          <Dashboard
            stats={stats}
            loading={loading}
            onRefresh={fetchStats}
          />
        )
    }
  }

  return (
    <div className="app">
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
      />

      <main className="main-content">
        {renderContent()}
      </main>
    </div>
  )
}

export default App
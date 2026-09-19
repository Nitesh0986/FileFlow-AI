import './Sidebar.css'

function Sidebar({ activeTab, setActiveTab }) {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'files', label: 'Files', icon: '📁' },
    { id: 'organize', label: 'Organize', icon: '🗂️' },
    { id: 'duplicates', label: 'Duplicates', icon: '🔍' },
    { id: 'rename', label: 'Rename', icon: '✏️' },
    { id: 'settings', label: 'Settings', icon: '⚙️' },
  ]

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h1>FileFlow-AI</h1>
        <p className="subtitle">Intelligent File Organization</p>
      </div>
      
      <nav className="sidebar-nav">
        {menuItems.map(item => (
          <button
            key={item.id}
            className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
            onClick={() => setActiveTab(item.id)}
          >
            <span className="nav-icon">{item.icon}</span>
            <span className="nav-label">{item.label}</span>
          </button>
        ))}
      </nav>
      
      <div className="sidebar-footer">
        <p className="version">v1.0.0</p>
      </div>
    </aside>
  )
}

export default Sidebar

import { useState } from 'react'
import './Settings.css'

function Settings() {
  const [notifications, setNotifications] = useState(true)
  const [darkMode, setDarkMode] = useState(false)

  const handleDarkMode = (value) => {
    setDarkMode(value)
    document.body.classList.toggle('dark-mode', value)
  }

  const resetSettings = () => {
    setNotifications(true)
    handleDarkMode(false)
  }

  return (
    <div className="settings-page">
      <div className="settings-header">
        <h2>Settings</h2>
        <p>Manage your FileFlow-AI preferences</p>
      </div>

      <div className="settings-card">
        <h3>⚙️ General</h3>

        <div className="setting-item">
          <div>
            <strong>Notifications</strong>
            <p>Receive updates about file operations</p>
          </div>

          <label className="switch">
            <input
              type="checkbox"
              checked={notifications}
              onChange={(e) => setNotifications(e.target.checked)}
            />
            <span className="slider"></span>
          </label>
        </div>

        <div className="setting-item">
          <div>
            <strong>Dark Mode</strong>
            <p>Switch between light and dark appearance</p>
          </div>

          <label className="switch">
            <input
              type="checkbox"
              checked={darkMode}
              onChange={(e) => handleDarkMode(e.target.checked)}
            />
            <span className="slider"></span>
          </label>
        </div>
      </div>

      <div className="settings-card">
        <h3>🛡️ Safety</h3>

        <div className="safety-info">
          <p>✓ Dry Run supported for file operations</p>
          <p>✓ Duplicate detection available</p>
          <p>✓ Path traversal protection enabled</p>
          <p>✓ Existing files are protected from overwrite</p>
        </div>
      </div>

      <div className="settings-card">
        <h3>🔄 Preferences</h3>

        <button className="reset-btn" onClick={resetSettings}>
          Reset Settings
        </button>
      </div>

      <div className="settings-footer">
        <span>FileFlow-AI</span>
        <span>v1.0.0</span>
      </div>
    </div>
  )
}

export default Settings
import { useState, useEffect } from 'react'
import './Dashboard.css'

function Dashboard({ stats, loading, onRefresh }) {
  const [recentFiles, setRecentFiles] = useState([])

  useEffect(() => {
    fetchRecentFiles()
  }, [])

  const fetchRecentFiles = async () => {
    try {
      const response = await fetch('/api/files?limit=10')
      const data = await response.json()
      if (data.success) {
        setRecentFiles(data.data)
      }
    } catch (error) {
      console.error('Failed to fetch recent files:', error)
    }
  }

  const formatBytes = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
  }

  if (loading) {
    return (
      <div className="dashboard">
        <div className="loading">Loading dashboard...</div>
      </div>
    )
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Dashboard</h2>
        <button className="refresh-btn" onClick={onRefresh}>
          🔄 Refresh
        </button>
      </div>

      {/* Statistics Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📁</div>
          <div className="stat-content">
            <h3>Total Files</h3>
            <p className="stat-value">{stats?.total_files || 0}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🔍</div>
          <div className="stat-content">
            <h3>Duplicates</h3>
            <p className="stat-value">{stats?.total_duplicates || 0}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">💾</div>
          <div className="stat-content">
            <h3>Total Size</h3>
            <p className="stat-value">{formatBytes(stats?.total_size_bytes || 0)}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📂</div>
          <div className="stat-content">
            <h3>Categories</h3>
            <p className="stat-value">{Object.keys(stats?.by_category || {}).length}</p>
          </div>
        </div>
      </div>

      {/* Files by Category */}
      <div className="section">
        <h3>Files by Category</h3>
        <div className="category-list">
          {stats?.by_category && Object.keys(stats.by_category).length > 0 ? (
            Object.entries(stats.by_category).map(([category, count]) => (
              <div key={category} className="category-item">
                <span className="category-name">{category}</span>
                <span className="category-count">{count}</span>
              </div>
            ))
          ) : (
            <p className="no-data">No files categorized yet</p>
          )}
        </div>
      </div>

      {/* Recent Files */}
      <div className="section">
        <h3>Recent Files</h3>
        <div className="files-list">
          {recentFiles.length > 0 ? (
            recentFiles.map(file => (
              <div key={file.id} className="file-item">
                <div className="file-info">
                  <span className="file-name">{file.name}</span>
                  <span className="file-category">{file.category || 'Uncategorized'}</span>
                </div>
                <span className="file-size">{formatBytes(file.size_bytes)}</span>
              </div>
            ))
          ) : (
            <p className="no-data">No files recorded yet</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default Dashboard

import { useState, useEffect } from 'react'
import './Files.css'

function Files() {
  const [files, setFiles] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchFiles()
  }, [selectedCategory])

  const fetchFiles = async () => {
    try {
      setLoading(true)
      const url = selectedCategory === 'all' 
        ? '/api/files?limit=50'
        : `/api/files?category=${selectedCategory}&limit=50`
      
      const response = await fetch(url)
      const data = await response.json()
      if (data.success) {
        setFiles(data.data)
      }
    } catch (error) {
      console.error('Failed to fetch files:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatBytes = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
  }

  const categories = ['all', 'Documents', 'Images', 'Videos', 'Audio', 'Archives', 'Code', 'Executables', 'Fonts', 'Data', 'Other']

  const filteredFiles = files.filter(file => 
    file.name.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="files-page">
      <div className="files-header">
        <h2>Files Management</h2>
        <button className="refresh-btn" onClick={fetchFiles}>
          🔄 Refresh
        </button>
      </div>

      {/* Filters */}
      <div className="filters">
        <div className="search-box">
          <input
            type="text"
            placeholder="Search files..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>
        
        <div className="category-filter">
          <label>Category:</label>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="category-select"
          >
            {categories.map(cat => (
              <option key={cat} value={cat}>
                {cat === 'all' ? 'All Categories' : cat}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Files Table */}
      <div className="files-container">
        {loading ? (
          <div className="loading">Loading files...</div>
        ) : filteredFiles.length === 0 ? (
          <div className="no-data">No files found</div>
        ) : (
          <table className="files-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Category</th>
                <th>Size</th>
                <th>Extension</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredFiles.map(file => (
                <tr key={file.id} className="file-row">
                  <td className="file-name-cell">
                    <span className="file-icon">📄</span>
                    <span className="file-name">{file.name}</span>
                  </td>
                  <td>
                    <span className={`category-badge ${file.category?.toLowerCase() || 'other'}`}>
                      {file.category || 'Uncategorized'}
                    </span>
                  </td>
                  <td>{formatBytes(file.size_bytes)}</td>
                  <td>{file.extension || '-'}</td>
                  <td>{new Date(file.created_at).toLocaleDateString()}</td>
                  <td>
                    <div className="action-buttons">
                      <button className="action-btn view-btn" title="View Details">
                        👁️
                      </button>
                      <button className="action-btn organize-btn" title="Organize">
                        📁
                      </button>
                      <button className="action-btn rename-btn" title="Rename">
                        ✏️
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Stats */}
      <div className="files-stats">
        <span>Total: {filteredFiles.length} files</span>
        <span>Category: {selectedCategory}</span>
      </div>
    </div>
  )
}

export default Files

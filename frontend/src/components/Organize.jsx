import { useState } from 'react'
import './Organize.css'

function Organize() {
  const [sourceFolder, setSourceFolder] = useState('')
  const [targetFolder, setTargetFolder] = useState('')
  const [dryRun, setDryRun] = useState(true)
  const [recursive, setRecursive] = useState(true)
  const [organizing, setOrganizing] = useState(false)
  const [results, setResults] = useState(null)

  const handleOrganize = async () => {
    if (!sourceFolder || !targetFolder) {
      alert('Please provide both source and target folders')
      return
    }

    setOrganizing(true)
    setResults(null)

    try {
      const response = await fetch('/api/organize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          source: sourceFolder,
          target: targetFolder,
          dry_run: dryRun,
          recursive: recursive
        })
      })

      const data = await response.json()
      if (data.success) {
        setResults(data.data)
      } else {
        alert(`Organization failed: ${data.detail || 'Unknown error'}`)
      }
    } catch (error) {
      console.error('Organization error:', error)
      alert(`Error organizing files: ${error.message || 'Failed to connect to server'}`)
    } finally {
      setOrganizing(false)
    }
  }

  const formatBytes = (bytes) => {
    if (!bytes) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
  }

  return (
    <div className="organize-page">
      <div className="organize-header">
        <h2>Organize Files</h2>
        <p className="subtitle">Automatically organize files into category folders</p>
      </div>

      {/* Configuration */}
      <div className="organize-config">
        <div className="form-group">
          <label htmlFor="source">Source Folder *</label>
          <input
            id="source"
            type="text"
            placeholder="e.g., C:\Users\Downloads"
            value={sourceFolder}
            onChange={(e) => setSourceFolder(e.target.value)}
            className="form-input"
          />
        </div>

        <div className="form-group">
          <label htmlFor="target">Target Folder *</label>
          <input
            id="target"
            type="text"
            placeholder="e.g., C:\Users\Organized"
            value={targetFolder}
            onChange={(e) => setTargetFolder(e.target.value)}
            className="form-input"
          />
        </div>

        <div className="checkbox-group">
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={dryRun}
              onChange={(e) => setDryRun(e.target.checked)}
              className="checkbox"
            />
            <span>Dry Run (preview without moving)</span>
          </label>

          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={recursive}
              onChange={(e) => setRecursive(e.target.checked)}
              className="checkbox"
            />
            <span>Recursive (include subdirectories)</span>
          </label>
        </div>

        <button
          onClick={handleOrganize}
          disabled={organizing || !sourceFolder || !targetFolder}
          className={`organize-btn ${organizing ? 'organizing' : ''}`}
        >
          {organizing ? '⏳ Organizing...' : '🚀 Start Organization'}
        </button>
      </div>

      {/* Results */}
      {results && (
        <div className="organize-results">
          <h3>Organization Results</h3>
          
          <div className="results-summary">
            <div className="summary-item">
              <span className="summary-label">Total Files:</span>
              <span className="summary-value">{results.total_files}</span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Organized:</span>
              <span className="summary-value success">{results.organized}</span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Failed:</span>
              <span className="summary-value error">{results.failed}</span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Skipped:</span>
              <span className="summary-value">{results.skipped}</span>
            </div>
          </div>

          {results.by_category && Object.keys(results.by_category).length > 0 && (
            <div className="category-breakdown">
              <h4>Files by Category</h4>
              <div className="category-list">
                {Object.entries(results.by_category).map(([category, count]) => (
                  <div key={category} className="category-item">
                    <span className="category-name">{category}</span>
                    <span className="category-count">{count}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {results.errors && results.errors.length > 0 && (
            <div className="errors-section">
              <h4>Errors</h4>
              <div className="errors-list">
                {results.errors.map((error, index) => (
                  <div key={index} className="error-item">
                    <span className="error-file">{error.file}</span>
                    <span className="error-message">{error.error}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {dryRun && (
            <div className="dry-run-notice">
              ⚠️ This was a DRY RUN. No files were actually moved.
              Uncheck "Dry Run" to perform the actual organization.
            </div>
          )}
        </div>
      )}

      {/* Info */}
      <div className="organize-info">
        <h4>ℹ️ How it works</h4>
        <ul>
          <li>Files are analyzed and classified into categories</li>
          <li>Category folders are automatically created in the target directory</li>
          <li>Files are moved to their respective category folders</li>
          <li>Filename conflicts are handled with automatic numbering</li>
          <li>Use Dry Run first to preview changes before executing</li>
        </ul>
      </div>
    </div>
  )
}

export default Organize

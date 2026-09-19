import { useState } from 'react'
import './Rename.css'

function Rename() {
  const [filePath, setFilePath] = useState('')
  const [newName, setNewName] = useState('')
  const [dryRun, setDryRun] = useState(true)
  const [renaming, setRenaming] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleRename = async () => {
    if (!filePath || !newName) {
      alert('Please provide both file path and new name')
      return
    }

    setRenaming(true)
    setResult(null)
    setError(null)

    try {
      const response = await fetch('/api/rename/single', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          source_path: filePath,
          new_name: newName,
          dry_run: dryRun
        })
      })

      const data = await response.json()
      if (data.success) {
        setResult(data.data)
        if (!data.data.success) {
          setError(data.data.error)
        }
      } else {
        setError(data.detail || 'Unknown error')
      }
    } catch (err) {
      console.error('Rename error:', err)
      setError(err.message || 'Failed to connect to server')
    } finally {
      setRenaming(false)
    }
  }

  return (
    <div className="rename-page">
      <div className="rename-header">
        <h2>Rename File</h2>
        <p className="subtitle">Safely rename individual files with validation</p>
      </div>

      {/* Configuration */}
      <div className="rename-config">
        <div className="form-group">
          <label htmlFor="filePath">File Path *</label>
          <input
            id="filePath"
            type="text"
            placeholder="e.g., C:\Users\Downloads\document.txt"
            value={filePath}
            onChange={(e) => setFilePath(e.target.value)}
            className="form-input"
          />
        </div>

        <div className="form-group">
          <label htmlFor="newName">New Name *</label>
          <input
            id="newName"
            type="text"
            placeholder="e.g., renamed_document.txt"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
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
            <span>Dry Run (preview without renaming)</span>
          </label>
        </div>

        <button
          onClick={handleRename}
          disabled={renaming || !filePath || !newName}
          className={`rename-btn ${renaming ? 'renaming' : ''}`}
        >
          {renaming ? '⏳ Renaming...' : '✏️ Rename File'}
        </button>
      </div>

      {/* Result */}
      {result && (
        <div className="rename-result">
          {result.success ? (
            <div className="result-success">
              <h3>✓ Rename Successful</h3>
              <div className="result-details">
                <div className="result-item">
                  <span className="result-label">Old Name:</span>
                  <span className="result-value">{result.old_name}</span>
                </div>
                <div className="result-item">
                  <span className="result-label">New Name:</span>
                  <span className="result-value">{result.new_name}</span>
                </div>
                <div className="result-item">
                  <span className="result-label">Old Path:</span>
                  <span className="result-value">{result.old_path}</span>
                </div>
                <div className="result-item">
                  <span className="result-label">New Path:</span>
                  <span className="result-value">{result.new_path}</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="result-error">
              <h3>✗ Rename Failed</h3>
              <p className="error-message">{result.error}</p>
            </div>
          )}

          {dryRun && result.success && (
            <div className="dry-run-notice">
              ⚠️ This was a DRY RUN. No file was actually renamed.
              Uncheck "Dry Run" to perform the actual rename.
            </div>
          )}
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="rename-error">
          <h3>✗ Error</h3>
          <p className="error-message">{error}</p>
        </div>
      )}

      {/* Info */}
      <div className="rename-info">
        <h4>ℹ️ Safety Features</h4>
        <ul>
          <li>Source file must exist and be a valid file</li>
          <li>New filename cannot be empty</li>
          <li>Invalid characters are automatically sanitized</li>
          <li>Path traversal attempts are blocked</li>
          <li>Existing files are never overwritten</li>
          <li>File extension is preserved if not specified</li>
          <li>Use Dry Run first to preview changes</li>
        </ul>
      </div>
    </div>
  )
}

export default Rename

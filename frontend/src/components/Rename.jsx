import { useState } from 'react'
import { API_BASE_URL } from '../config'
import './Rename.css'

const API_URL = API_BASE_URL

function Rename() {
  const [filePath, setFilePath] = useState('')
  const [newName, setNewName] = useState('')
  const [dryRun, setDryRun] = useState(true)
  const [renaming, setRenaming] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleRename = async () => {
    if (!filePath.trim() || !newName.trim()) {
      alert('Please provide both file path and new name')
      return
    }

    setRenaming(true)
    setResult(null)
    setError(null)

    try {
      const response = await fetch(
        `${API_URL}/api/rename/single`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          body: JSON.stringify({
            source_path: filePath.trim(),
            new_name: newName.trim(),
            dry_run: dryRun,
          }),
        }
      )

      const data = await response.json()

      console.log('Rename API response:', data)

      if (!response.ok) {
        setError(
          data.detail ||
          data.message ||
          `Request failed with status ${response.status}`
        )
        return
      }

      if (data.success) {
        setResult(data.data)

        if (data.data && !data.data.success) {
          setError(data.data.error || 'Rename operation failed')
        }
      } else {
        setError(
          data.detail ||
          data.message ||
          'Rename operation failed'
        )
      }

    } catch (err) {
      console.error('Rename error:', err)

      setError(
        'Could not connect to FileFlow-AI backend. Please try again.'
      )
    } finally {
      setRenaming(false)
    }
  }

  const handleClear = () => {
    setFilePath('')
    setNewName('')
    setResult(null)
    setError(null)
  }

  return (
    <div className="rename-page">

      <div className="rename-header">
        <h2>Rename File</h2>
        <p className="subtitle">
          Safely rename individual files with validation
        </p>
      </div>

      <div className="rename-config">

        <div className="form-group">
          <label htmlFor="filePath">
            File Path <span>*</span>
          </label>

          <input
            id="filePath"
            type="text"
            placeholder="e.g., C:\Users\Downloads\document.txt"
            value={filePath}
            onChange={(e) => setFilePath(e.target.value)}
            className="form-input"
            disabled={renaming}
          />
        </div>

        <div className="form-group">
          <label htmlFor="newName">
            New Name <span>*</span>
          </label>

          <input
            id="newName"
            type="text"
            placeholder="e.g., renamed_document.txt"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            className="form-input"
            disabled={renaming}
          />
        </div>

        <div className="checkbox-group">
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={dryRun}
              onChange={(e) => setDryRun(e.target.checked)}
              className="checkbox"
              disabled={renaming}
            />

            <span>
              Dry Run (preview without renaming)
            </span>
          </label>
        </div>

        <div className="rename-actions">

          <button
            onClick={handleRename}
            disabled={
              renaming ||
              !filePath.trim() ||
              !newName.trim()
            }
            className={`rename-btn ${renaming ? 'renaming' : ''}`}
          >
            {renaming ? '⏳ Renaming...' : '✏️ Rename File'}
          </button>

          <button
            onClick={handleClear}
            disabled={renaming}
            className="clear-btn"
          >
            Clear
          </button>

        </div>
      </div>

      {result && (
        <div className="rename-result">

          {result.success ? (
            <div className="result-success">

              <h3>✓ Rename Successful</h3>

              <div className="result-details">

                <div className="result-item">
                  <span className="result-label">
                    Old Name:
                  </span>

                  <span className="result-value">
                    {result.old_name || 'N/A'}
                  </span>
                </div>

                <div className="result-item">
                  <span className="result-label">
                    New Name:
                  </span>

                  <span className="result-value">
                    {result.new_name || 'N/A'}
                  </span>
                </div>

                <div className="result-item">
                  <span className="result-label">
                    Old Path:
                  </span>

                  <span className="result-value">
                    {result.old_path || 'N/A'}
                  </span>
                </div>

                <div className="result-item">
                  <span className="result-label">
                    New Path:
                  </span>

                  <span className="result-value">
                    {result.new_path || 'N/A'}
                  </span>
                </div>

              </div>
            </div>

          ) : (

            <div className="result-error">
              <h3>✗ Rename Failed</h3>

              <p className="error-message">
                {result.error || 'Rename operation failed'}
              </p>
            </div>

          )}

          {dryRun && result.success && (
            <div className="dry-run-notice">
              ⚠️ This was a <strong>DRY RUN</strong>.
              No file was actually renamed.
              Uncheck "Dry Run" to perform the actual rename.
            </div>
          )}

        </div>
      )}

      {error && (
        <div className="rename-error">

          <h3>✗ Error</h3>

          <p className="error-message">
            {error}
          </p>

        </div>
      )}

      <div className="rename-info">

        <h4>ℹ️ Safety Features</h4>

        <ul>
          <li>
            Source file must exist and be a valid file
          </li>

          <li>
            New filename cannot be empty
          </li>

          <li>
            Invalid characters are automatically sanitized
          </li>

          <li>
            Path traversal attempts are blocked
          </li>

          <li>
            Existing files are never overwritten
          </li>

          <li>
            File extension is preserved if not specified
          </li>

          <li>
            Use Dry Run first to preview changes
          </li>
        </ul>

      </div>

    </div>
  )
}

export default Rename
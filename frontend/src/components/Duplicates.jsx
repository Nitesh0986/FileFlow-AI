import { useState } from 'react'
import './Duplicates.css'

function Duplicates() {
  const [folderPath, setFolderPath] = useState('')
  const [algorithm, setAlgorithm] = useState('sha256')
  const [scanning, setScanning] = useState(false)
  const [duplicates, setDuplicates] = useState(null)

  const handleScan = async () => {
    if (!folderPath) {
      alert('Please provide a folder path')
      return
    }

    setScanning(true)
    setDuplicates(null)

    try {
      const response = await fetch(`/api/duplicates?folder_path=${encodeURIComponent(folderPath)}&algorithm=${algorithm}`)
      const data = await response.json()
      if (data.success) {
        setDuplicates(data.data)
      } else {
        alert('Duplicate scan failed')
      }
    } catch (error) {
      console.error('Scan error:', error)
      alert('Error scanning for duplicates')
    } finally {
      setScanning(false)
    }
  }

  const formatBytes = (bytes) => {
    if (!bytes) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
  }

  const totalDuplicates = duplicates?.reduce((sum, group) => sum + group.duplicates.length, 0) || 0
  const totalSpaceSaved = duplicates?.reduce((sum, group) => {
    return sum + group.duplicates.reduce((groupSum, dup) => {
      try {
        return groupSum + (dup.size || 0)
      } catch {
        return groupSum
      }
    }, 0)
  }, 0) || 0

  return (
    <div className="duplicates-page">
      <div className="duplicates-header">
        <h2>Duplicate Detection</h2>
        <p className="subtitle">Find and manage duplicate files to save space</p>
      </div>

      {/* Scan Configuration */}
      <div className="duplicates-config">
        <div className="form-group">
          <label htmlFor="folder">Folder Path *</label>
          <input
            id="folder"
            type="text"
            placeholder="e.g., C:\Users\Downloads"
            value={folderPath}
            onChange={(e) => setFolderPath(e.target.value)}
            className="form-input"
          />
        </div>

        <div className="form-group">
          <label htmlFor="algorithm">Hash Algorithm</label>
          <select
            id="algorithm"
            value={algorithm}
            onChange={(e) => setAlgorithm(e.target.value)}
            className="form-select"
          >
            <option value="md5">MD5 (Fast)</option>
            <option value="sha1">SHA1 (Balanced)</option>
            <option value="sha256">SHA256 (Secure)</option>
          </select>
        </div>

        <button
          onClick={handleScan}
          disabled={scanning || !folderPath}
          className={`scan-btn ${scanning ? 'scanning' : ''}`}
        >
          {scanning ? '🔍 Scanning...' : '🚀 Start Scan'}
        </button>
      </div>

      {/* Results */}
      {duplicates !== null && (
        <div className="duplicates-results">
          {duplicates.length === 0 ? (
            <div className="no-duplicates">
              <div className="no-duplicates-icon">✅</div>
              <h3>No Duplicates Found</h3>
              <p>Your folder is clean! No duplicate files were detected.</p>
            </div>
          ) : (
            <>
              <div className="duplicates-summary">
                <div className="summary-card">
                  <div className="summary-icon">📦</div>
                  <div className="summary-content">
                    <h4>Duplicate Groups</h4>
                    <p className="summary-value">{duplicates.length}</p>
                  </div>
                </div>

                <div className="summary-card">
                  <div className="summary-icon">📄</div>
                  <div className="summary-content">
                    <h4>Total Duplicates</h4>
                    <p className="summary-value">{totalDuplicates}</p>
                  </div>
                </div>

                <div className="summary-card">
                  <div className="summary-icon">💾</div>
                  <div className="summary-content">
                    <h4>Space Savings</h4>
                    <p className="summary-value">{formatBytes(totalSpaceSaved)}</p>
                  </div>
                </div>
              </div>

              <div className="duplicate-groups">
                <h3>Duplicate Groups</h3>
                {duplicates.map((group, index) => (
                  <div key={index} className="duplicate-group">
                    <div className="group-header">
                      <span className="group-title">Group #{index + 1}</span>
                      <span className="group-count">{group.count} files</span>
                    </div>

                    <div className="group-hash">
                      <span className="hash-label">Hash:</span>
                      <span className="hash-value">{group.hash}</span>
                    </div>

                    <div className="group-files">
                      <div className="file-item original">
                        <span className="file-label">Original:</span>
                        <span className="file-path">{group.original}</span>
                        <span className="file-badge original-badge">Keep</span>
                      </div>

                      {group.duplicates.map((dup, dupIndex) => (
                        <div key={dupIndex} className="file-item duplicate">
                          <span className="file-label">Duplicate {dupIndex + 1}:</span>
                          <span className="file-path">{dup}</span>
                          <div className="file-actions">
                            <button className="action-btn delete-btn" title="Delete">
                              🗑️
                            </button>
                            <button className="action-btn view-btn" title="View">
                              👁️
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      )}

      {/* Info */}
      <div className="duplicates-info">
        <h4>ℹ️ How duplicate detection works</h4>
        <ul>
          <li>Files are analyzed using cryptographic hash algorithms</li>
          <li>Files with identical hashes are exact duplicates</li>
          <li>The first file found is marked as the original</li>
          <li>You can review and delete duplicates manually</li>
          <li>SHA256 provides the most accurate detection</li>
        </ul>
      </div>
    </div>
  )
}

export default Duplicates

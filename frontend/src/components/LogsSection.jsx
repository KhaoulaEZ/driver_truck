import { useState, useEffect } from 'react'
import apiService from '../services/apiService'

function LogsSection() {
  const [logs, setLogs] = useState([])
  const [drivers, setDrivers] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [formData, setFormData] = useState({
    driver: '',
    status: 'on_duty',
    location: '',
    notes: ''
  })

  const statusOptions = [
    { value: 'on_duty', label: 'On Duty' },
    { value: 'driving', label: 'Driving' },
    { value: 'sleeper_berth', label: 'Sleeper Berth' },
    { value: 'off_duty', label: 'Off Duty' }
  ]

  useEffect(() => {
    fetchLogs()
    fetchDrivers()
  }, [])

  const fetchLogs = async () => {
    try {
      setLoading(true)
      const response = await apiService.getDutyLogs()
      setLogs(response.results || response)
      setError('')
    } catch (err) {
      setError('Failed to fetch duty logs: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const fetchDrivers = async () => {
    try {
      const response = await apiService.getDrivers()
      setDrivers(response.results || response)
    } catch (err) {
      console.error('Failed to fetch drivers:', err)
    }
  }

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      setLoading(true)
      await apiService.createDutyLog(formData)
      setSuccess('Duty log created successfully!')
      setError('')
      setFormData({
        driver: '',
        status: 'on_duty',
        location: '',
        notes: ''
      })
      fetchLogs()
    } catch (err) {
      setError('Failed to create duty log: ' + err.message)
      setSuccess('')
    } finally {
      setLoading(false)
    }
  }

  const getStatusBadge = (status) => {
    const statusClasses = {
      'driving': 'status-driving',
      'on_duty': 'status-online',
      'off_duty': 'status-offline',
      'sleeper_berth': 'status-offline'
    }
    return `status-badge ${statusClasses[status] || 'status-badge'}`
  }

  return (
    <div>
      <h2>📊 Duty Log Management</h2>
      
      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}

      <div className="form-grid">
        <div className="form-section">
          <h3>Log Duty Status</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Driver *</label>
              <select
                name="driver"
                value={formData.driver}
                onChange={handleInputChange}
                required
              >
                <option value="">Select a driver</option>
                {drivers.map((driver) => (
                  <option key={driver.id} value={driver.id}>
                    {driver.first_name} {driver.last_name} ({driver.username})
                  </option>
                ))}
              </select>
            </div>
            
            <div className="form-group">
              <label>Status *</label>
              <select
                name="status"
                value={formData.status}
                onChange={handleInputChange}
                required
              >
                {statusOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
            
            <div className="form-group">
              <label>Location *</label>
              <input
                type="text"
                name="location"
                value={formData.location}
                onChange={handleInputChange}
                required
                placeholder="e.g., Interstate 95, Mile 150"
              />
            </div>
            
            <div className="form-group">
              <label>Notes</label>
              <textarea
                name="notes"
                value={formData.notes}
                onChange={handleInputChange}
                rows="3"
                placeholder="Optional notes about this duty status change"
              />
            </div>
            
            <button type="submit" className="btn" disabled={loading}>
              {loading ? 'Logging...' : 'Log Status'}
            </button>
            <button type="button" className="btn btn-success" onClick={fetchLogs}>
              Refresh Logs
            </button>
          </form>
        </div>

        <div className="response-section">
          <h3>Recent Duty Logs</h3>
          {loading ? (
            <div className="loading">Loading duty logs...</div>
          ) : (
            <div className="response-content">
              {logs.length === 0 ? (
                <p>No duty logs found. Create your first log entry!</p>
              ) : (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Driver</th>
                      <th>Status</th>
                      <th>Location</th>
                      <th>Timestamp</th>
                      <th>Notes</th>
                    </tr>
                  </thead>
                  <tbody>
                    {logs.slice(0, 10).map((log) => (
                      <tr key={log.id}>
                        <td>{log.driver_name || `Driver ${log.driver}`}</td>
                        <td>
                          <span className={getStatusBadge(log.status)}>
                            {statusOptions.find(s => s.value === log.status)?.label || log.status}
                          </span>
                        </td>
                        <td>{log.location}</td>
                        <td>{new Date(log.timestamp).toLocaleString()}</td>
                        <td>{log.notes || '-'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default LogsSection
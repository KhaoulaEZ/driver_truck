import { useState, useEffect } from 'react'
import apiService from '../services/apiService'

function DriversSection() {
  const [drivers, setDrivers] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [formData, setFormData] = useState({
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    license_number: '',
    password: 'defaultpass123'
  })

  useEffect(() => {
    fetchDrivers()
  }, [])

  const fetchDrivers = async () => {
    try {
      setLoading(true)
      const response = await apiService.getDrivers()
      setDrivers(response.results || response)
      setError('')
    } catch (err) {
      setError('Failed to fetch drivers: ' + err.message)
    } finally {
      setLoading(false)
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
      await apiService.createDriver(formData)
      setSuccess('Driver created successfully!')
      setError('')
      setFormData({
        username: '',
        first_name: '',
        last_name: '',
        email: '',
        license_number: '',
        password: 'defaultpass123'
      })
      fetchDrivers()
    } catch (err) {
      setError('Failed to create driver: ' + err.message)
      setSuccess('')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2>👥 Driver Management</h2>
      
      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}

      <div className="form-grid">
        <div className="form-section">
          <h3>Add New Driver</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Username *</label>
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleInputChange}
                required
                placeholder="Enter username"
              />
            </div>
            
            <div className="form-group">
              <label>First Name *</label>
              <input
                type="text"
                name="first_name"
                value={formData.first_name}
                onChange={handleInputChange}
                required
                placeholder="Enter first name"
              />
            </div>
            
            <div className="form-group">
              <label>Last Name *</label>
              <input
                type="text"
                name="last_name"
                value={formData.last_name}
                onChange={handleInputChange}
                required
                placeholder="Enter last name"
              />
            </div>
            
            <div className="form-group">
              <label>Email *</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                required
                placeholder="Enter email address"
              />
            </div>
            
            <div className="form-group">
              <label>License Number *</label>
              <input
                type="text"
                name="license_number"
                value={formData.license_number}
                onChange={handleInputChange}
                required
                placeholder="Enter license number"
              />
            </div>
            
            <button type="submit" className="btn" disabled={loading}>
              {loading ? 'Creating...' : 'Create Driver'}
            </button>
            <button type="button" className="btn btn-success" onClick={fetchDrivers}>
              Refresh List
            </button>
          </form>
        </div>

        <div className="response-section">
          <h3>Current Drivers</h3>
          {loading ? (
            <div className="loading">Loading drivers...</div>
          ) : (
            <div className="response-content">
              {drivers.length === 0 ? (
                <p>No drivers found. Create your first driver!</p>
              ) : (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Username</th>
                      <th>License</th>
                      <th>Email</th>
                    </tr>
                  </thead>
                  <tbody>
                    {drivers.map((driver) => (
                      <tr key={driver.id}>
                        <td>{driver.id}</td>
                        <td>{driver.first_name} {driver.last_name}</td>
                        <td>{driver.username}</td>
                        <td>{driver.license_number}</td>
                        <td>{driver.email}</td>
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

export default DriversSection
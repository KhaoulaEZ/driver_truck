import { useState, useEffect } from 'react'
import apiService from '../services/apiService'

function VehiclesSection() {
  const [vehicles, setVehicles] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [formData, setFormData] = useState({
    license_plate: '',
    make: '',
    model: '',
    year: '',
    vin: ''
  })

  useEffect(() => {
    fetchVehicles()
  }, [])

  const fetchVehicles = async () => {
    try {
      setLoading(true)
      const response = await apiService.getVehicles()
      setVehicles(response.results || response)
      setError('')
    } catch (err) {
      setError('Failed to fetch vehicles: ' + err.message)
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
      await apiService.createVehicle(formData)
      setSuccess('Vehicle added successfully!')
      setError('')
      setFormData({
        license_plate: '',
        make: '',
        model: '',
        year: '',
        vin: ''
      })
      fetchVehicles()
    } catch (err) {
      setError('Failed to add vehicle: ' + err.message)
      setSuccess('')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2>🚚 Vehicle Management</h2>
      
      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}

      <div className="form-grid">
        <div className="form-section">
          <h3>Add New Vehicle</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>License Plate *</label>
              <input
                type="text"
                name="license_plate"
                value={formData.license_plate}
                onChange={handleInputChange}
                required
                placeholder="e.g., ABC-123"
              />
            </div>
            
            <div className="form-group">
              <label>Make *</label>
              <input
                type="text"
                name="make"
                value={formData.make}
                onChange={handleInputChange}
                required
                placeholder="e.g., Freightliner"
              />
            </div>
            
            <div className="form-group">
              <label>Model *</label>
              <input
                type="text"
                name="model"
                value={formData.model}
                onChange={handleInputChange}
                required
                placeholder="e.g., Cascadia"
              />
            </div>
            
            <div className="form-group">
              <label>Year *</label>
              <input
                type="number"
                name="year"
                value={formData.year}
                onChange={handleInputChange}
                required
                min="1900"
                max="2030"
                placeholder="e.g., 2023"
              />
            </div>
            
            <div className="form-group">
              <label>VIN *</label>
              <input
                type="text"
                name="vin"
                value={formData.vin}
                onChange={handleInputChange}
                required
                placeholder="17-character VIN"
                maxLength="17"
              />
            </div>
            
            <button type="submit" className="btn" disabled={loading}>
              {loading ? 'Adding...' : 'Add Vehicle'}
            </button>
            <button type="button" className="btn btn-success" onClick={fetchVehicles}>
              Refresh List
            </button>
          </form>
        </div>

        <div className="response-section">
          <h3>Fleet Vehicles</h3>
          {loading ? (
            <div className="loading">Loading vehicles...</div>
          ) : (
            <div className="response-content">
              {vehicles.length === 0 ? (
                <p>No vehicles found. Add your first vehicle!</p>
              ) : (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>License Plate</th>
                      <th>Make & Model</th>
                      <th>Year</th>
                      <th>VIN</th>
                    </tr>
                  </thead>
                  <tbody>
                    {vehicles.map((vehicle) => (
                      <tr key={vehicle.id}>
                        <td>{vehicle.id}</td>
                        <td><strong>{vehicle.license_plate}</strong></td>
                        <td>{vehicle.make} {vehicle.model}</td>
                        <td>{vehicle.year}</td>
                        <td>{vehicle.vin}</td>
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

export default VehiclesSection
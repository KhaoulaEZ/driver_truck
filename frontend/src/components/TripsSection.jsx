import { useState, useEffect } from 'react'
import apiService from '../services/apiService'

function TripsSection() {
  const [trips, setTrips] = useState([])
  const [drivers, setDrivers] = useState([])
  const [vehicles, setVehicles] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [formData, setFormData] = useState({
    driver: '',
    vehicle: '',
    origin: '',
    destination: '',
    planned_distance: ''
  })

  useEffect(() => {
    fetchTrips()
    fetchDrivers()
    fetchVehicles()
  }, [])

  const fetchTrips = async () => {
    try {
      setLoading(true)
      const response = await apiService.getTrips()
      setTrips(response.results || response)
      setError('')
    } catch (err) {
      setError('Failed to fetch trips: ' + err.message)
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

  const fetchVehicles = async () => {
    try {
      const response = await apiService.getVehicles()
      setVehicles(response.results || response)
    } catch (err) {
      console.error('Failed to fetch vehicles:', err)
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
      await apiService.createTrip(formData)
      setSuccess('Trip created successfully!')
      setError('')
      setFormData({
        driver: '',
        vehicle: '',
        origin: '',
        destination: '',
        planned_distance: ''
      })
      fetchTrips()
    } catch (err) {
      setError('Failed to create trip: ' + err.message)
      setSuccess('')
    } finally {
      setLoading(false)
    }
  }

  const getStatusBadge = (status) => {
    const statusClasses = {
      'planned': 'status-badge',
      'in_progress': 'status-driving',
      'completed': 'status-online',
      'cancelled': 'status-offline'
    }
    return statusClasses[status] || 'status-badge'
  }

  return (
    <div>
      <h2>🛣️ Trip Management</h2>
      
      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}

      <div className="form-grid">
        <div className="form-section">
          <h3>Create New Trip</h3>
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
              <label>Vehicle *</label>
              <select
                name="vehicle"
                value={formData.vehicle}
                onChange={handleInputChange}
                required
              >
                <option value="">Select a vehicle</option>
                {vehicles.map((vehicle) => (
                  <option key={vehicle.id} value={vehicle.id}>
                    {vehicle.license_plate} - {vehicle.make} {vehicle.model}
                  </option>
                ))}
              </select>
            </div>
            
            <div className="form-group">
              <label>Origin *</label>
              <input
                type="text"
                name="origin"
                value={formData.origin}
                onChange={handleInputChange}
                required
                placeholder="e.g., New York, NY"
              />
            </div>
            
            <div className="form-group">
              <label>Destination *</label>
              <input
                type="text"
                name="destination"
                value={formData.destination}
                onChange={handleInputChange}
                required
                placeholder="e.g., Los Angeles, CA"
              />
            </div>
            
            <div className="form-group">
              <label>Planned Distance (miles) *</label>
              <input
                type="number"
                name="planned_distance"
                value={formData.planned_distance}
                onChange={handleInputChange}
                required
                step="0.1"
                min="0"
                placeholder="e.g., 2800.5"
              />
            </div>
            
            <button type="submit" className="btn" disabled={loading}>
              {loading ? 'Creating...' : 'Create Trip'}
            </button>
            <button type="button" className="btn btn-success" onClick={fetchTrips}>
              Refresh Trips
            </button>
          </form>
        </div>

        <div className="response-section">
          <h3>Active Trips</h3>
          {loading ? (
            <div className="loading">Loading trips...</div>
          ) : (
            <div className="response-content">
              {trips.length === 0 ? (
                <p>No trips found. Create your first trip!</p>
              ) : (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Trip ID</th>
                      <th>Driver</th>
                      <th>Vehicle</th>
                      <th>Route</th>
                      <th>Distance</th>
                      <th>Status</th>
                      <th>Created</th>
                    </tr>
                  </thead>
                  <tbody>
                    {trips.map((trip) => (
                      <tr key={trip.id}>
                        <td><strong>#{trip.id}</strong></td>
                        <td>{trip.driver_name || `Driver ${trip.driver}`}</td>
                        <td>{trip.vehicle_plate || `Vehicle ${trip.vehicle}`}</td>
                        <td>{trip.origin} → {trip.destination}</td>
                        <td>{trip.planned_distance} mi</td>
                        <td>
                          <span className={`status-badge ${getStatusBadge(trip.status)}`}>
                            {trip.status || 'Planned'}
                          </span>
                        </td>
                        <td>{new Date(trip.created_at).toLocaleDateString()}</td>
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

export default TripsSection
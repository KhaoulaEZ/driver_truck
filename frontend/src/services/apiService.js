// API base URL - will be proxied by Vite to Django backend
const API_BASE_URL = '/api'

// Helper function to get CSRF token from cookies
function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

// Get CSRF token from Django
async function getCSRFToken() {
  try {
    const response = await fetch('/api/csrf/', {
      credentials: 'include'
    })
    if (response.ok) {
      const data = await response.json()
      return data.csrfToken
    }
  } catch (error) {
    console.warn('Could not get CSRF token:', error)
  }
  return getCookie('csrftoken')
}

// Helper function to make API requests
async function apiRequest(url, options = {}) {
  // Get CSRF token
  const csrftoken = await getCSRFToken()
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
      ...(csrftoken && { 'X-CSRFToken': csrftoken }),
    },
    credentials: 'include', // Include cookies for session auth
  }

  const finalOptions = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers,
    },
  }

  try {
    const response = await fetch(`${API_BASE_URL}${url}`, finalOptions)
    
    if (!response.ok) {
      const errorText = await response.text()
      let errorMessage
      try {
        const errorJson = JSON.parse(errorText)
        errorMessage = errorJson.detail || errorJson.message || Object.values(errorJson).join(', ')
      } catch {
        errorMessage = errorText || `HTTP ${response.status}`
      }
      throw new Error(errorMessage)
    }

    const contentType = response.headers.get('content-type')
    if (contentType && contentType.includes('application/json')) {
      return await response.json()
    }
    return await response.text()
  } catch (error) {
    console.error('API Request failed:', error)
    throw error
  }
}

// Driver API endpoints
const driverAPI = {
  getDrivers: () => apiRequest('/drivers/drivers/'),
  createDriver: (data) => apiRequest('/drivers/drivers/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  updateDriver: (id, data) => apiRequest(`/drivers/drivers/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  deleteDriver: (id) => apiRequest(`/drivers/drivers/${id}/`, {
    method: 'DELETE',
  }),
}

// Vehicle API endpoints
const vehicleAPI = {
  getVehicles: () => apiRequest('/drivers/vehicles/'),
  createVehicle: (data) => apiRequest('/drivers/vehicles/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  updateVehicle: (id, data) => apiRequest(`/drivers/vehicles/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  deleteVehicle: (id) => apiRequest(`/drivers/vehicles/${id}/`, {
    method: 'DELETE',
  }),
}

// Duty Log API endpoints
const dutyLogAPI = {
  getDutyLogs: () => apiRequest('/logs/duty-logs/'),
  createDutyLog: (data) => apiRequest('/logs/duty-logs/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  updateDutyLog: (id, data) => apiRequest(`/logs/duty-logs/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  deleteDutyLog: (id) => apiRequest(`/logs/duty-logs/${id}/`, {
    method: 'DELETE',
  }),
}

// Trip API endpoints
const tripAPI = {
  getTrips: () => apiRequest('/trips/trips/'),
  createTrip: (data) => apiRequest('/trips/trips/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  updateTrip: (id, data) => apiRequest(`/trips/trips/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  deleteTrip: (id) => apiRequest(`/trips/trips/${id}/`, {
    method: 'DELETE',
  }),
  getTripStops: (tripId) => apiRequest(`/trips/trip-stops/?trip=${tripId}`),
  createTripStop: (data) => apiRequest('/trips/trip-stops/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  getTripEvents: (tripId) => apiRequest(`/trips/trip-events/?trip=${tripId}`),
  createTripEvent: (data) => apiRequest('/trips/trip-events/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
}

// Combined API service object
const apiService = {
  // Drivers
  getDrivers: driverAPI.getDrivers,
  createDriver: driverAPI.createDriver,
  updateDriver: driverAPI.updateDriver,
  deleteDriver: driverAPI.deleteDriver,

  // Vehicles
  getVehicles: vehicleAPI.getVehicles,
  createVehicle: vehicleAPI.createVehicle,
  updateVehicle: vehicleAPI.updateVehicle,
  deleteVehicle: vehicleAPI.deleteVehicle,

  // Duty Logs
  getDutyLogs: dutyLogAPI.getDutyLogs,
  createDutyLog: dutyLogAPI.createDutyLog,
  updateDutyLog: dutyLogAPI.updateDutyLog,
  deleteDutyLog: dutyLogAPI.deleteDutyLog,

  // Trips
  getTrips: tripAPI.getTrips,
  createTrip: tripAPI.createTrip,
  updateTrip: tripAPI.updateTrip,
  deleteTrip: tripAPI.deleteTrip,
  getTripStops: tripAPI.getTripStops,
  createTripStop: tripAPI.createTripStop,
  getTripEvents: tripAPI.getTripEvents,
  createTripEvent: tripAPI.createTripEvent,

  // Utility
  checkStatus: () => apiRequest('/status/'),
}

export default apiService
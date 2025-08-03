import axios from 'axios';

// Get API URL from environment or use proxy server for development
const API_URL = process.env.REACT_APP_API_URL || 
                (process.env.NODE_ENV === 'production' 
                  ? `${window.location.protocol}//${window.location.host}`
                  : 'http://localhost:3002');

console.log('API URL:', API_URL); // Debug log

// Create axios instance with updated configuration
const api = axios.create({
  baseURL: API_URL,
  timeout: 15000, // Increased timeout for production
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false, // Disable credentials for CORS
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log('Making request to:', config.url); // Debug log
    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log('Response received:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    console.error('Error details:', {
      status: error.response?.status,
      url: error.config?.url,
      method: error.config?.method
    });
    return Promise.reject(error);
  }
);

// API endpoints
export const dataQualityAPI = {
  getMetrics: () => api.get('/api/v1/data-quality/metrics'),
  uploadData: (data) => api.post('/api/v1/data-quality/upload', data),
  getIssues: () => api.get('/api/v1/data-quality/issues'),
  getHistory: () => api.get('/api/v1/data-quality/history'),
};

export const modelMonitoringAPI = {
  getModels: () => api.get('/api/v1/model-monitoring/models'),
  getPerformance: (modelId) => api.get(`/api/v1/model-monitoring/performance/${modelId}`),
  getDrift: (modelId) => api.get(`/api/v1/model-monitoring/drift/${modelId}`),
  deployModel: (modelData) => api.post('/api/v1/model-monitoring/deploy', modelData),
};

export const alertsAPI = {
  getAlerts: () => api.get('/api/v1/alerts'),
  createAlert: (alertData) => api.post('/api/v1/alerts', alertData),
  updateAlert: (alertId, alertData) => api.put(`/api/v1/alerts/${alertId}`, alertData),
  deleteAlert: (alertId) => api.delete(`/api/v1/alerts/${alertId}`),
};

export const dashboardAPI = {
  getOverview: () => api.get('/api/v1/dashboard/overview'),
  getMetrics: () => api.get('/api/v1/dashboard/metrics'),
  getRecentActivity: () => api.get('/api/v1/dashboard/recent-activity'),
  getTrends: () => api.get('/api/v1/dashboard/trends'),
  getSystemStatus: () => api.get('/api/v1/dashboard/system-status'),
};

export default api; 
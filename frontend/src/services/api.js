import axios from 'axios';

// Get API URL from environment or use default
const API_URL = process.env.REACT_APP_API_URL || 
                (process.env.NODE_ENV === 'production' 
                  ? `${window.location.origin}/api` 
                  : 'http://localhost:8000');

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// API endpoints
export const dataQualityAPI = {
  getMetrics: () => api.get('/v1/data-quality/metrics'),
  uploadData: (data) => api.post('/v1/data-quality/upload', data),
  getIssues: () => api.get('/v1/data-quality/issues'),
  getHistory: () => api.get('/v1/data-quality/history'),
};

export const modelMonitoringAPI = {
  getModels: () => api.get('/v1/model-monitoring/models'),
  getPerformance: (modelId) => api.get(`/v1/model-monitoring/performance/${modelId}`),
  getDrift: (modelId) => api.get(`/v1/model-monitoring/drift/${modelId}`),
  deployModel: (modelData) => api.post('/v1/model-monitoring/deploy', modelData),
};

export const alertsAPI = {
  getAlerts: () => api.get('/v1/alerts'),
  createAlert: (alertData) => api.post('/v1/alerts', alertData),
  updateAlert: (alertId, alertData) => api.put(`/v1/alerts/${alertId}`, alertData),
  deleteAlert: (alertId) => api.delete(`/v1/alerts/${alertId}`),
};

export const dashboardAPI = {
  getOverview: () => api.get('/v1/dashboard/overview'),
  getMetrics: () => api.get('/v1/dashboard/metrics'),
  getRecentActivity: () => api.get('/v1/dashboard/recent-activity'),
};

export default api; 
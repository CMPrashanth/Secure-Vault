import axios from 'axios';

// Reads the backend URL from an environment variable for production,
// but falls back to localhost for local development.
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

// This "interceptor" runs before every API call.
// It automatically adds the user's authentication token to the request headers.
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('accessToken'); // Using 'accessToken' as found in your AuthContext
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

export default apiClient;
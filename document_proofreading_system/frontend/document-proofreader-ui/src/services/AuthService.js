import axios from "axios";

const API_BASE_URL = process.env.VUE_APP_API_BASE_URL || "http://localhost:5000";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add a request interceptor to include the token if available
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});


export default {
  login(credentials) {
    // Backend endpoint is /auth/login
    return apiClient.post("/auth/login", credentials);
  },
  register(userData) {
    // Backend endpoint is /auth/register
    return apiClient.post("/auth/register", userData);
  },
  // Example of a protected route, if needed directly by a service
  // getProtectedData() {
  //   return apiClient.get("/auth/protected"); // Assuming backend has /auth/protected
  // }
};

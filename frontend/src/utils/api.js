/**
 * API utility functions for making HTTP requests
 * 
 * This module provides a centralized API client with error handling,
 * request/response interceptors, and retry logic.
 * 
 * @author AI Job Readiness Team
 * @version 1.0.0
 */

import axios from 'axios';
import { API_CONFIG, HTTP_STATUS, STORAGE_KEYS, ERROR_MESSAGES } from './constants';

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add authentication token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling and token refresh
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // Handle 401 errors (unauthorized)
    if (error.response?.status === HTTP_STATUS.UNAUTHORIZED && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
        if (refreshToken) {
          const response = await axios.post(`${API_CONFIG.BASE_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          });

          const { access_token, refresh_token: newRefreshToken } = response.data;
          localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, access_token);
          localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, newRefreshToken);

          // Retry the original request with new token
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return apiClient(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, redirect to login
        localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
        localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
        localStorage.removeItem(STORAGE_KEYS.USER_DATA);
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

/**
 * Generic API request function with retry logic
 * @param {Function} requestFn - The axios request function to execute
 * @param {number} retries - Number of retry attempts (default: 3)
 * @returns {Promise} - The API response
 */
const makeRequest = async (requestFn, retries = API_CONFIG.RETRY_ATTEMPTS) => {
  try {
    return await requestFn();
  } catch (error) {
    if (retries > 0 && shouldRetry(error)) {
      await new Promise(resolve => setTimeout(resolve, API_CONFIG.RETRY_DELAY));
      return makeRequest(requestFn, retries - 1);
    }
    throw error;
  }
};

/**
 * Check if an error should trigger a retry
 * @param {Error} error - The error to check
 * @returns {boolean} - Whether to retry the request
 */
const shouldRetry = (error) => {
  // Retry on network errors or 5xx server errors
  return !error.response || 
         error.response.status >= 500 || 
         error.code === 'NETWORK_ERROR' ||
         error.code === 'ECONNABORTED';
};

/**
 * Handle API errors and return user-friendly messages
 * @param {Error} error - The error to handle
 * @returns {string} - User-friendly error message
 */
const handleApiError = (error) => {
  if (error.response) {
    const { status, data } = error.response;
    
    switch (status) {
      case HTTP_STATUS.BAD_REQUEST:
        return data?.message || data?.detail || ERROR_MESSAGES.VALIDATION_ERROR;
      case HTTP_STATUS.UNAUTHORIZED:
        return ERROR_MESSAGES.UNAUTHORIZED;
      case HTTP_STATUS.FORBIDDEN:
        return ERROR_MESSAGES.FORBIDDEN;
      case HTTP_STATUS.NOT_FOUND:
        return ERROR_MESSAGES.NOT_FOUND;
      case HTTP_STATUS.TOO_MANY_REQUESTS:
        return 'Too many requests. Please try again later.';
      case HTTP_STATUS.INTERNAL_SERVER_ERROR:
      case HTTP_STATUS.SERVICE_UNAVAILABLE:
        return ERROR_MESSAGES.SERVER_ERROR;
      default:
        return data?.message || data?.detail || ERROR_MESSAGES.GENERIC;
    }
  } else if (error.request) {
    return ERROR_MESSAGES.NETWORK_ERROR;
  } else {
    return error.message || ERROR_MESSAGES.GENERIC;
  }
};

// Authentication API functions
export const authAPI = {
  /**
   * Login user
   * @param {Object} credentials - Login credentials
   * @returns {Promise<Object>} - Login response
   */
  login: async (credentials) => {
    return makeRequest(() => apiClient.post('/auth/login', credentials));
  },

  /**
   * Register new user
   * @param {Object} userData - User registration data
   * @returns {Promise<Object>} - Registration response
   */
  register: async (userData) => {
    return makeRequest(() => apiClient.post('/auth/register', userData));
  },

  /**
   * Logout user
   * @returns {Promise<Object>} - Logout response
   */
  logout: async () => {
    return makeRequest(() => apiClient.post('/auth/logout'));
  },

  /**
   * Get current user profile
   * @returns {Promise<Object>} - User profile data
   */
  getCurrentUser: async () => {
    return makeRequest(() => apiClient.get('/auth/me'));
  },

  /**
   * Forgot password
   * @param {string} email - User email
   * @returns {Promise<Object>} - Forgot password response
   */
  forgotPassword: async (email) => {
    return makeRequest(() => apiClient.post('/auth/forgot-password', { email }));
  },

  /**
   * Reset password
   * @param {Object} resetData - Password reset data
   * @returns {Promise<Object>} - Reset password response
   */
  resetPassword: async (resetData) => {
    return makeRequest(() => apiClient.post('/auth/reset-password', resetData));
  },

  /**
   * Verify email
   * @param {string} token - Email verification token
   * @returns {Promise<Object>} - Email verification response
   */
  verifyEmail: async (token) => {
    return makeRequest(() => apiClient.post('/auth/verify-email', { token }));
  },
};

// Users API functions
export const usersAPI = {
  /**
   * Get user profile
   * @param {string} userId - User ID
   * @returns {Promise<Object>} - User profile data
   */
  getProfile: async (userId) => {
    return makeRequest(() => apiClient.get(`/users/${userId}`));
  },

  /**
   * Update user profile
   * @param {string} userId - User ID
   * @param {Object} profileData - Profile update data
   * @returns {Promise<Object>} - Updated profile data
   */
  updateProfile: async (userId, profileData) => {
    return makeRequest(() => apiClient.put(`/users/${userId}`, profileData));
  },

  /**
   * Get users list (admin only)
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} - Users list
   */
  getUsers: async (params = {}) => {
    return makeRequest(() => apiClient.get('/users/list', { params }));
  },

  /**
   * Activate user account
   * @param {string} userId - User ID
   * @returns {Promise<Object>} - Activation response
   */
  activateUser: async (userId) => {
    return makeRequest(() => apiClient.post(`/users/${userId}/activate`));
  },

  /**
   * Deactivate user account
   * @param {string} userId - User ID
   * @returns {Promise<Object>} - Deactivation response
   */
  deactivateUser: async (userId) => {
    return makeRequest(() => apiClient.post(`/users/${userId}/deactivate`));
  },
};

// Resumes API functions
export const resumesAPI = {
  /**
   * Get user's resumes
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} - Resumes list
   */
  getResumes: async (params = {}) => {
    return makeRequest(() => apiClient.get('/resumes/', { params }));
  },

  /**
   * Get resume by ID
   * @param {string} resumeId - Resume ID
   * @returns {Promise<Object>} - Resume data
   */
  getResume: async (resumeId) => {
    return makeRequest(() => apiClient.get(`/resumes/${resumeId}`));
  },

  /**
   * Create new resume
   * @param {Object} resumeData - Resume data
   * @returns {Promise<Object>} - Created resume data
   */
  createResume: async (resumeData) => {
    return makeRequest(() => apiClient.post('/resumes/', resumeData));
  },

  /**
   * Update resume
   * @param {string} resumeId - Resume ID
   * @param {Object} resumeData - Resume update data
   * @returns {Promise<Object>} - Updated resume data
   */
  updateResume: async (resumeId, resumeData) => {
    return makeRequest(() => apiClient.put(`/resumes/${resumeId}`, resumeData));
  },

  /**
   * Delete resume
   * @param {string} resumeId - Resume ID
   * @returns {Promise<Object>} - Deletion response
   */
  deleteResume: async (resumeId) => {
    return makeRequest(() => apiClient.delete(`/resumes/${resumeId}`));
  },

  /**
   * Upload resume file
   * @param {string} resumeId - Resume ID
   * @param {File} file - File to upload
   * @param {Function} onProgress - Progress callback
   * @returns {Promise<Object>} - Upload response
   */
  uploadResumeFile: async (resumeId, file, onProgress) => {
    const formData = new FormData();
    formData.append('file', file);

    return makeRequest(() => 
      apiClient.post(`/resumes/${resumeId}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: onProgress,
      })
    );
  },

  /**
   * Download resume file
   * @param {string} resumeId - Resume ID
   * @returns {Promise<Blob>} - File blob
   */
  downloadResumeFile: async (resumeId) => {
    return makeRequest(() => 
      apiClient.get(`/resumes/${resumeId}/download`, {
        responseType: 'blob',
      })
    );
  },

  /**
   * Analyze resume
   * @param {string} resumeId - Resume ID
   * @param {Object} analysisParams - Analysis parameters
   * @returns {Promise<Object>} - Analysis response
   */
  analyzeResume: async (resumeId, analysisParams = {}) => {
    return makeRequest(() => 
      apiClient.post(`/resumes/${resumeId}/analyze`, analysisParams)
    );
  },

  /**
   * Get resume statistics
   * @returns {Promise<Object>} - Resume statistics
   */
  getResumeStats: async () => {
    return makeRequest(() => apiClient.get('/resumes/stats/summary'));
  },
};

// Roles API functions
export const rolesAPI = {
  /**
   * Get roles list
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} - Roles list
   */
  getRoles: async (params = {}) => {
    return makeRequest(() => apiClient.get('/roles/', { params }));
  },

  /**
   * Get role by ID
   * @param {string} roleId - Role ID
   * @returns {Promise<Object>} - Role data
   */
  getRole: async (roleId) => {
    return makeRequest(() => apiClient.get(`/roles/${roleId}`));
  },

  /**
   * Create new role
   * @param {Object} roleData - Role data
   * @returns {Promise<Object>} - Created role data
   */
  createRole: async (roleData) => {
    return makeRequest(() => apiClient.post('/roles/', roleData));
  },

  /**
   * Update role
   * @param {string} roleId - Role ID
   * @param {Object} roleData - Role update data
   * @returns {Promise<Object>} - Updated role data
   */
  updateRole: async (roleId, roleData) => {
    return makeRequest(() => apiClient.put(`/roles/${roleId}`, roleData));
  },

  /**
   * Delete role
   * @param {string} roleId - Role ID
   * @returns {Promise<Object>} - Deletion response
   */
  deleteRole: async (roleId) => {
    return makeRequest(() => apiClient.delete(`/roles/${roleId}`));
  },

  /**
   * Assign role to user
   * @param {string} userId - User ID
   * @param {string} roleId - Role ID
   * @returns {Promise<Object>} - Assignment response
   */
  assignRole: async (userId, roleId) => {
    return makeRequest(() => apiClient.post(`/roles/${roleId}/assign/${userId}`));
  },

  /**
   * Unassign role from user
   * @param {string} userId - User ID
   * @param {string} roleId - Role ID
   * @returns {Promise<Object>} - Unassignment response
   */
  unassignRole: async (userId, roleId) => {
    return makeRequest(() => apiClient.post(`/roles/${roleId}/unassign/${userId}`));
  },
};

// System API functions
export const systemAPI = {
  /**
   * Health check
   * @returns {Promise<Object>} - Health status
   */
  healthCheck: async () => {
    return makeRequest(() => apiClient.get('/health'));
  },

  /**
   * Get system info
   * @returns {Promise<Object>} - System information
   */
  getSystemInfo: async () => {
    return makeRequest(() => apiClient.get('/api/v1/info'));
  },

  /**
   * Get database status
   * @returns {Promise<Object>} - Database status
   */
  getDatabaseStatus: async () => {
    return makeRequest(() => apiClient.get('/database'));
  },

  /**
   * Get models status
   * @returns {Promise<Object>} - Models status
   */
  getModelsStatus: async () => {
    return makeRequest(() => apiClient.get('/models'));
  },
};

// Export the main API client and error handler
export { apiClient, handleApiError };

// Export all API functions as a single object
export const api = {
  auth: authAPI,
  users: usersAPI,
  resumes: resumesAPI,
  roles: rolesAPI,
  system: systemAPI,
};

/**
 * Custom React hooks
 * 
 * This module provides reusable custom hooks for common functionality
 * like API calls, form handling, and state management.
 * 
 * @author AI Job Readiness Team
 * @version 1.0.0
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { api, handleApiError } from './api';
import { authStorage } from './storage';
import { debounce } from './helpers';

/**
 * Custom hook for API calls with loading and error states
 * @param {Function} apiCall - API function to call
 * @param {Array} dependencies - Dependencies array for useEffect
 * @param {Object} options - Additional options
 * @returns {Object} - { data, loading, error, refetch }
 */
export const useApi = (apiCall, dependencies = [], options = {}) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    if (!apiCall) return;

    setLoading(true);
    setError(null);

    try {
      const result = await apiCall();
      setData(result.data);
    } catch (err) {
      const errorMessage = handleApiError(err);
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [apiCall]);

  useEffect(() => {
    if (options.autoFetch !== false) {
      fetchData();
    }
  }, dependencies);

  const refetch = useCallback(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch };
};

/**
 * Custom hook for form state management
 * @param {Object} initialValues - Initial form values
 * @param {Object} validationRules - Validation rules
 * @param {Function} onSubmit - Submit handler
 * @returns {Object} - Form state and handlers
 */
export const useForm = (initialValues = {}, validationRules = {}, onSubmit) => {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const setValue = useCallback((name, value) => {
    setValues(prev => ({ ...prev, [name]: value }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  }, [errors]);

  const setFieldTouched = useCallback((name) => {
    setTouched(prev => ({ ...prev, [name]: true }));
  }, []);

  const validateField = useCallback((name, value) => {
    const rules = validationRules[name];
    if (!rules) return { isValid: true, message: '' };

    // Required validation
    if (rules.required && (!value || value.toString().trim() === '')) {
      return { isValid: false, message: `${name} is required` };
    }

    // Skip other validations if field is empty and not required
    if (!value && !rules.required) {
      return { isValid: true, message: '' };
    }

    // Type-specific validations
    if (rules.type === 'email') {
      const emailRegex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i;
      if (!emailRegex.test(value)) {
        return { isValid: false, message: 'Please enter a valid email address' };
      }
    }

    if (rules.type === 'password') {
      if (value.length < 8) {
        return { isValid: false, message: 'Password must be at least 8 characters long' };
      }
    }

    if (rules.type === 'phone') {
      const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
      if (!phoneRegex.test(value)) {
        return { isValid: false, message: 'Please enter a valid phone number' };
      }
    }

    // Length validations
    if (rules.minLength && value.length < rules.minLength) {
      return { isValid: false, message: `${name} must be at least ${rules.minLength} characters long` };
    }

    if (rules.maxLength && value.length > rules.maxLength) {
      return { isValid: false, message: `${name} must be no more than ${rules.maxLength} characters long` };
    }

    // Custom validation
    if (rules.custom && typeof rules.custom === 'function') {
      return rules.custom(value, name);
    }

    return { isValid: true, message: '' };
  }, [validationRules]);

  const validateForm = useCallback(() => {
    const newErrors = {};
    let isValid = true;

    for (const [name, value] of Object.entries(values)) {
      const fieldError = validateField(name, value);
      if (!fieldError.isValid) {
        newErrors[name] = fieldError.message;
        isValid = false;
      }
    }

    setErrors(newErrors);
    return isValid;
  }, [values, validateField]);

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit(values);
    } catch (error) {
      console.error('Form submission error:', error);
    } finally {
      setIsSubmitting(false);
    }
  }, [values, validateForm, onSubmit]);

  const handleChange = useCallback((e) => {
    const { name, value, type, checked } = e.target;
    const newValue = type === 'checkbox' ? checked : value;
    setValue(name, newValue);
  }, [setValue]);

  const handleBlur = useCallback((e) => {
    const { name, value } = e.target;
    setFieldTouched(name);
    
    const fieldError = validateField(name, value);
    if (!fieldError.isValid) {
      setErrors(prev => ({ ...prev, [name]: fieldError.message }));
    }
  }, [setFieldTouched, validateField]);

  const resetForm = useCallback(() => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
    setIsSubmitting(false);
  }, [initialValues]);

  return {
    values,
    errors,
    touched,
    isSubmitting,
    setValue,
    setFieldTouched,
    handleChange,
    handleBlur,
    handleSubmit,
    resetForm,
    validateForm
  };
};

/**
 * Custom hook for authentication state
 * @returns {Object} - Authentication state and methods
 */
export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = authStorage.getToken();
        if (token) {
          const userData = authStorage.getUserData();
          if (userData) {
            setUser(userData);
            setIsAuthenticated(true);
          } else {
            // Try to fetch user data from API
            const response = await api.auth.getCurrentUser();
            setUser(response.data);
            setIsAuthenticated(true);
            authStorage.setUserData(response.data);
          }
        }
      } catch (error) {
        console.error('Auth check failed:', error);
        authStorage.clear();
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = useCallback(async (credentials) => {
    try {
      const response = await api.auth.login(credentials);
      const { access_token, refresh_token, user: userData } = response.data;
      
      authStorage.setToken(access_token);
      authStorage.setRefreshToken(refresh_token);
      authStorage.setUserData(userData);
      
      setUser(userData);
      setIsAuthenticated(true);
      
      return { success: true, data: userData };
    } catch (error) {
      const errorMessage = handleApiError(error);
      return { success: false, error: errorMessage };
    }
  }, []);

  const logout = useCallback(async () => {
    try {
      await api.auth.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      authStorage.clear();
      setUser(null);
      setIsAuthenticated(false);
    }
  }, []);

  const register = useCallback(async (userData) => {
    try {
      const response = await api.auth.register(userData);
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage = handleApiError(error);
      return { success: false, error: errorMessage };
    }
  }, []);

  return {
    user,
    isAuthenticated,
    loading,
    login,
    logout,
    register
  };
};

/**
 * Custom hook for pagination
 * @param {Function} fetchData - Function to fetch data
 * @param {Object} initialParams - Initial parameters
 * @returns {Object} - Pagination state and methods
 */
export const usePagination = (fetchData, initialParams = {}) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState({
    page: 1,
    pageSize: 10,
    total: 0,
    totalPages: 0
  });

  const fetchPage = useCallback(async (page, pageSize = pagination.pageSize) => {
    setLoading(true);
    setError(null);

    try {
      const params = { ...initialParams, page, page_size: pageSize };
      const response = await fetchData(params);
      
      setData(response.data);
      setPagination(prev => ({
        ...prev,
        page,
        pageSize,
        total: response.total || 0,
        totalPages: response.total_pages || 0
      }));
    } catch (err) {
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  }, [fetchData, initialParams, pagination.pageSize]);

  useEffect(() => {
    fetchPage(1);
  }, [fetchPage]);

  const goToPage = useCallback((page) => {
    if (page >= 1 && page <= pagination.totalPages) {
      fetchPage(page);
    }
  }, [fetchPage, pagination.totalPages]);

  const changePageSize = useCallback((newPageSize) => {
    fetchPage(1, newPageSize);
  }, [fetchPage]);

  return {
    data,
    loading,
    error,
    pagination,
    goToPage,
    changePageSize,
    refetch: () => fetchPage(pagination.page)
  };
};

/**
 * Custom hook for debounced search
 * @param {Function} searchFunction - Search function to call
 * @param {number} delay - Debounce delay in milliseconds
 * @returns {Object} - Search state and methods
 */
export const useDebouncedSearch = (searchFunction, delay = 300) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const debouncedSearch = useCallback(
    debounce(async (searchQuery) => {
      if (!searchQuery.trim()) {
        setResults([]);
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const response = await searchFunction(searchQuery);
        setResults(response.data || []);
      } catch (err) {
        setError(handleApiError(err));
        setResults([]);
      } finally {
        setLoading(false);
      }
    }, delay),
    [searchFunction, delay]
  );

  const handleSearch = useCallback((searchQuery) => {
    setQuery(searchQuery);
    debouncedSearch(searchQuery);
  }, [debouncedSearch]);

  const clearSearch = useCallback(() => {
    setQuery('');
    setResults([]);
    setError(null);
  }, []);

  return {
    query,
    results,
    loading,
    error,
    handleSearch,
    clearSearch
  };
};

/**
 * Custom hook for local storage
 * @param {string} key - Storage key
 * @param {any} defaultValue - Default value
 * @returns {Array} - [value, setValue, removeValue]
 */
export const useLocalStorage = (key, defaultValue) => {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : defaultValue;
    } catch (error) {
      console.warn(`Error reading localStorage key "${key}":`, error);
      return defaultValue;
    }
  });

  const setValue = useCallback((value) => {
    try {
      setStoredValue(value);
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.warn(`Error setting localStorage key "${key}":`, error);
    }
  }, [key]);

  const removeValue = useCallback(() => {
    try {
      setStoredValue(defaultValue);
      window.localStorage.removeItem(key);
    } catch (error) {
      console.warn(`Error removing localStorage key "${key}":`, error);
    }
  }, [key, defaultValue]);

  return [storedValue, setValue, removeValue];
};

/**
 * Custom hook for previous value
 * @param {any} value - Current value
 * @returns {any} - Previous value
 */
export const usePrevious = (value) => {
  const ref = useRef();
  
  useEffect(() => {
    ref.current = value;
  });
  
  return ref.current;
};

/**
 * Custom hook for window size
 * @returns {Object} - Window dimensions
 */
export const useWindowSize = () => {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  });

  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight
      });
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return windowSize;
};

/**
 * Custom hook for online status
 * @returns {boolean} - Online status
 */
export const useOnlineStatus = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return isOnline;
};

/**
 * Custom hook for click outside
 * @param {Function} handler - Handler function
 * @returns {Object} - Ref to attach to element
 */
export const useClickOutside = (handler) => {
  const ref = useRef();

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (ref.current && !ref.current.contains(event.target)) {
        handler();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [handler]);

  return ref;
};

/**
 * Custom hook for async operation
 * @param {Function} asyncFunction - Async function to execute
 * @param {Array} dependencies - Dependencies array
 * @returns {Object} - { data, loading, error, execute }
 */
export const useAsync = (asyncFunction, dependencies = []) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = useCallback(async (...args) => {
    setLoading(true);
    setError(null);

    try {
      const result = await asyncFunction(...args);
      setData(result);
      return result;
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, dependencies);

  return { data, loading, error, execute };
};

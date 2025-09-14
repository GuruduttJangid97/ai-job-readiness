/**
 * Local storage utility functions
 * 
 * This module provides utilities for managing local storage,
 * session storage, and other client-side storage operations.
 * 
 * @author AI Job Readiness Team
 * @version 1.0.0
 */

import { STORAGE_KEYS } from './constants';

/**
 * Check if localStorage is available
 * @returns {boolean} - True if localStorage is available
 */
export const isLocalStorageAvailable = () => {
  try {
    const test = '__localStorage_test__';
    localStorage.setItem(test, test);
    localStorage.removeItem(test);
    return true;
  } catch (e) {
    return false;
  }
};

/**
 * Check if sessionStorage is available
 * @returns {boolean} - True if sessionStorage is available
 */
export const isSessionStorageAvailable = () => {
  try {
    const test = '__sessionStorage_test__';
    sessionStorage.setItem(test, test);
    sessionStorage.removeItem(test);
    return true;
  } catch (e) {
    return false;
  }
};

/**
 * Get item from localStorage
 * @param {string} key - Storage key
 * @param {any} defaultValue - Default value if key doesn't exist
 * @returns {any} - Stored value or default
 */
export const getLocalStorageItem = (key, defaultValue = null) => {
  if (!isLocalStorageAvailable()) {
    return defaultValue;
  }

  try {
    const item = localStorage.getItem(key);
    if (item === null) {
      return defaultValue;
    }
    return JSON.parse(item);
  } catch (error) {
    console.warn(`Error reading localStorage key "${key}":`, error);
    return defaultValue;
  }
};

/**
 * Set item in localStorage
 * @param {string} key - Storage key
 * @param {any} value - Value to store
 * @returns {boolean} - True if successful
 */
export const setLocalStorageItem = (key, value) => {
  if (!isLocalStorageAvailable()) {
    return false;
  }

  try {
    localStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch (error) {
    console.warn(`Error writing localStorage key "${key}":`, error);
    return false;
  }
};

/**
 * Remove item from localStorage
 * @param {string} key - Storage key
 * @returns {boolean} - True if successful
 */
export const removeLocalStorageItem = (key) => {
  if (!isLocalStorageAvailable()) {
    return false;
  }

  try {
    localStorage.removeItem(key);
    return true;
  } catch (error) {
    console.warn(`Error removing localStorage key "${key}":`, error);
    return false;
  }
};

/**
 * Clear all localStorage
 * @returns {boolean} - True if successful
 */
export const clearLocalStorage = () => {
  if (!isLocalStorageAvailable()) {
    return false;
  }

  try {
    localStorage.clear();
    return true;
  } catch (error) {
    console.warn('Error clearing localStorage:', error);
    return false;
  }
};

/**
 * Get item from sessionStorage
 * @param {string} key - Storage key
 * @param {any} defaultValue - Default value if key doesn't exist
 * @returns {any} - Stored value or default
 */
export const getSessionStorageItem = (key, defaultValue = null) => {
  if (!isSessionStorageAvailable()) {
    return defaultValue;
  }

  try {
    const item = sessionStorage.getItem(key);
    if (item === null) {
      return defaultValue;
    }
    return JSON.parse(item);
  } catch (error) {
    console.warn(`Error reading sessionStorage key "${key}":`, error);
    return defaultValue;
  }
};

/**
 * Set item in sessionStorage
 * @param {string} key - Storage key
 * @param {any} value - Value to store
 * @returns {boolean} - True if successful
 */
export const setSessionStorageItem = (key, value) => {
  if (!isSessionStorageAvailable()) {
    return false;
  }

  try {
    sessionStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch (error) {
    console.warn(`Error writing sessionStorage key "${key}":`, error);
    return false;
  }
};

/**
 * Remove item from sessionStorage
 * @param {string} key - Storage key
 * @returns {boolean} - True if successful
 */
export const removeSessionStorageItem = (key) => {
  if (!isSessionStorageAvailable()) {
    return false;
  }

  try {
    sessionStorage.removeItem(key);
    return true;
  } catch (error) {
    console.warn(`Error removing sessionStorage key "${key}":`, error);
    return false;
  }
};

/**
 * Clear all sessionStorage
 * @returns {boolean} - True if successful
 */
export const clearSessionStorage = () => {
  if (!isSessionStorageAvailable()) {
    return false;
  }

  try {
    sessionStorage.clear();
    return true;
  } catch (error) {
    console.warn('Error clearing sessionStorage:', error);
    return false;
  }
};

/**
 * Get all localStorage keys
 * @returns {string[]} - Array of keys
 */
export const getLocalStorageKeys = () => {
  if (!isLocalStorageAvailable()) {
    return [];
  }

  try {
    return Object.keys(localStorage);
  } catch (error) {
    console.warn('Error getting localStorage keys:', error);
    return [];
  }
};

/**
 * Get all sessionStorage keys
 * @returns {string[]} - Array of keys
 */
export const getSessionStorageKeys = () => {
  if (!isSessionStorageAvailable()) {
    return [];
  }

  try {
    return Object.keys(sessionStorage);
  } catch (error) {
    console.warn('Error getting sessionStorage keys:', error);
    return [];
  }
};

/**
 * Check if key exists in localStorage
 * @param {string} key - Storage key
 * @returns {boolean} - True if key exists
 */
export const hasLocalStorageKey = (key) => {
  if (!isLocalStorageAvailable()) {
    return false;
  }

  try {
    return localStorage.getItem(key) !== null;
  } catch (error) {
    console.warn(`Error checking localStorage key "${key}":`, error);
    return false;
  }
};

/**
 * Check if key exists in sessionStorage
 * @param {string} key - Storage key
 * @returns {boolean} - True if key exists
 */
export const hasSessionStorageKey = (key) => {
  if (!isSessionStorageAvailable()) {
    return false;
  }

  try {
    return sessionStorage.getItem(key) !== null;
  } catch (error) {
    console.warn(`Error checking sessionStorage key "${key}":`, error);
    return false;
  }
};

/**
 * Get storage size in bytes
 * @param {Storage} storage - Storage object (localStorage or sessionStorage)
 * @returns {number} - Storage size in bytes
 */
export const getStorageSize = (storage) => {
  if (!storage) {
    return 0;
  }

  try {
    let total = 0;
    for (const key in storage) {
      if (storage.hasOwnProperty(key)) {
        total += storage[key].length + key.length;
      }
    }
    return total;
  } catch (error) {
    console.warn('Error calculating storage size:', error);
    return 0;
  }
};

/**
 * Get localStorage size in bytes
 * @returns {number} - localStorage size in bytes
 */
export const getLocalStorageSize = () => {
  return getStorageSize(localStorage);
};

/**
 * Get sessionStorage size in bytes
 * @returns {number} - sessionStorage size in bytes
 */
export const getSessionStorageSize = () => {
  return getStorageSize(sessionStorage);
};

/**
 * Get total storage size in bytes
 * @returns {number} - Total storage size in bytes
 */
export const getTotalStorageSize = () => {
  return getLocalStorageSize() + getSessionStorageSize();
};

/**
 * Storage quota estimation (approximate)
 * @returns {Object} - Storage quota information
 */
export const getStorageQuota = () => {
  if (!isLocalStorageAvailable()) {
    return { used: 0, available: 0, total: 0 };
  }

  try {
    const used = getTotalStorageSize();
    // Most browsers have a 5-10MB limit for localStorage
    const estimatedTotal = 5 * 1024 * 1024; // 5MB
    const available = Math.max(0, estimatedTotal - used);

    return {
      used,
      available,
      total: estimatedTotal,
      percentage: (used / estimatedTotal) * 100
    };
  } catch (error) {
    console.warn('Error calculating storage quota:', error);
    return { used: 0, available: 0, total: 0, percentage: 0 };
  }
};

/**
 * Clean up expired items from storage
 * @param {Storage} storage - Storage object
 * @param {string} prefix - Prefix for timestamp keys
 * @param {number} maxAge - Maximum age in milliseconds
 * @returns {number} - Number of items cleaned
 */
export const cleanupExpiredItems = (storage, prefix = 'exp_', maxAge = 24 * 60 * 60 * 1000) => {
  if (!storage) {
    return 0;
  }

  let cleaned = 0;
  const now = Date.now();

  try {
    for (const key in storage) {
      if (storage.hasOwnProperty(key) && key.startsWith(prefix)) {
        const timestamp = parseInt(key.substring(prefix.length), 10);
        if (!isNaN(timestamp) && now - timestamp > maxAge) {
          storage.removeItem(key);
          cleaned++;
        }
      }
    }
  } catch (error) {
    console.warn('Error cleaning up expired items:', error);
  }

  return cleaned;
};

/**
 * Set item with expiration
 * @param {string} key - Storage key
 * @param {any} value - Value to store
 * @param {number} ttl - Time to live in milliseconds
 * @returns {boolean} - True if successful
 */
export const setLocalStorageItemWithTTL = (key, value, ttl) => {
  const now = Date.now();
  const item = {
    value,
    expires: now + ttl
  };

  return setLocalStorageItem(key, item);
};

/**
 * Get item with expiration check
 * @param {string} key - Storage key
 * @param {any} defaultValue - Default value if expired or not found
 * @returns {any} - Stored value or default
 */
export const getLocalStorageItemWithTTL = (key, defaultValue = null) => {
  const item = getLocalStorageItem(key, null);
  
  if (!item || typeof item !== 'object' || !item.hasOwnProperty('value') || !item.hasOwnProperty('expires')) {
    return defaultValue;
  }

  if (Date.now() > item.expires) {
    removeLocalStorageItem(key);
    return defaultValue;
  }

  return item.value;
};

/**
 * Authentication storage helpers
 */
export const authStorage = {
  /**
   * Get authentication token
   * @returns {string|null} - Auth token or null
   */
  getToken: () => getLocalStorageItem(STORAGE_KEYS.AUTH_TOKEN, null),

  /**
   * Set authentication token
   * @param {string} token - Auth token
   * @returns {boolean} - True if successful
   */
  setToken: (token) => setLocalStorageItem(STORAGE_KEYS.AUTH_TOKEN, token),

  /**
   * Remove authentication token
   * @returns {boolean} - True if successful
   */
  removeToken: () => removeLocalStorageItem(STORAGE_KEYS.AUTH_TOKEN),

  /**
   * Get refresh token
   * @returns {string|null} - Refresh token or null
   */
  getRefreshToken: () => getLocalStorageItem(STORAGE_KEYS.REFRESH_TOKEN, null),

  /**
   * Set refresh token
   * @param {string} token - Refresh token
   * @returns {boolean} - True if successful
   */
  setRefreshToken: (token) => setLocalStorageItem(STORAGE_KEYS.REFRESH_TOKEN, token),

  /**
   * Remove refresh token
   * @returns {boolean} - True if successful
   */
  removeRefreshToken: () => removeLocalStorageItem(STORAGE_KEYS.REFRESH_TOKEN),

  /**
   * Get user data
   * @returns {Object|null} - User data or null
   */
  getUserData: () => getLocalStorageItem(STORAGE_KEYS.USER_DATA, null),

  /**
   * Set user data
   * @param {Object} userData - User data
   * @returns {boolean} - True if successful
   */
  setUserData: (userData) => setLocalStorageItem(STORAGE_KEYS.USER_DATA, userData),

  /**
   * Remove user data
   * @returns {boolean} - True if successful
   */
  removeUserData: () => removeLocalStorageItem(STORAGE_KEYS.USER_DATA),

  /**
   * Clear all authentication data
   * @returns {boolean} - True if successful
   */
  clear: () => {
    const results = [
      removeLocalStorageItem(STORAGE_KEYS.AUTH_TOKEN),
      removeLocalStorageItem(STORAGE_KEYS.REFRESH_TOKEN),
      removeLocalStorageItem(STORAGE_KEYS.USER_DATA)
    ];
    return results.every(result => result);
  },

  /**
   * Check if user is authenticated
   * @returns {boolean} - True if authenticated
   */
  isAuthenticated: () => {
    const token = getLocalStorageItem(STORAGE_KEYS.AUTH_TOKEN, null);
    return token !== null && token !== '';
  }
};

/**
 * Settings storage helpers
 */
export const settingsStorage = {
  /**
   * Get theme setting
   * @returns {string} - Theme setting
   */
  getTheme: () => getLocalStorageItem(STORAGE_KEYS.THEME, 'light'),

  /**
   * Set theme setting
   * @param {string} theme - Theme setting
   * @returns {boolean} - True if successful
   */
  setTheme: (theme) => setLocalStorageItem(STORAGE_KEYS.THEME, theme),

  /**
   * Get language setting
   * @returns {string} - Language setting
   */
  getLanguage: () => getLocalStorageItem(STORAGE_KEYS.LANGUAGE, 'en'),

  /**
   * Set language setting
   * @param {string} language - Language setting
   * @returns {boolean} - True if successful
   */
  setLanguage: (language) => setLocalStorageItem(STORAGE_KEYS.LANGUAGE, language),

  /**
   * Get app settings
   * @returns {Object} - App settings
   */
  getSettings: () => getLocalStorageItem(STORAGE_KEYS.SETTINGS, {}),

  /**
   * Set app settings
   * @param {Object} settings - App settings
   * @returns {boolean} - True if successful
   */
  setSettings: (settings) => setLocalStorageItem(STORAGE_KEYS.SETTINGS, settings),

  /**
   * Update app settings
   * @param {Object} updates - Settings updates
   * @returns {boolean} - True if successful
   */
  updateSettings: (updates) => {
    const currentSettings = getLocalStorageItem(STORAGE_KEYS.SETTINGS, {});
    const newSettings = { ...currentSettings, ...updates };
    return setLocalStorageItem(STORAGE_KEYS.SETTINGS, newSettings);
  }
};

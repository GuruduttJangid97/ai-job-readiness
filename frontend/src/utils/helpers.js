/**
 * General utility helper functions
 * 
 * This module provides common utility functions for data manipulation,
 * formatting, calculations, and other helper operations.
 * 
 * @author AI Job Readiness Team
 * @version 1.0.0
 */

import { SCORE_CONFIG, ANALYSIS_TYPES, USER_ROLES, THEME_CONFIG, LANGUAGE_CONFIG } from './constants';

/**
 * Format file size in human-readable format
 * @param {number} bytes - File size in bytes
 * @param {number} decimals - Number of decimal places
 * @returns {string} - Formatted file size
 */
export const formatFileSize = (bytes, decimals = 2) => {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
};

/**
 * Format date in a readable format
 * @param {Date|string} date - Date to format
 * @param {Object} options - Formatting options
 * @returns {string} - Formatted date
 */
export const formatDate = (date, options = {}) => {
  const {
    format = 'long',
    timezone = 'UTC',
    locale = 'en-US'
  } = options;

  const dateObj = new Date(date);
  if (isNaN(dateObj.getTime())) {
    return 'Invalid Date';
  }

  const formatOptions = {
    long: {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      timeZone: timezone
    },
    short: {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      timeZone: timezone
    },
    time: {
      hour: '2-digit',
      minute: '2-digit',
      timeZone: timezone
    },
    date: {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      timeZone: timezone
    }
  };

  return dateObj.toLocaleDateString(locale, formatOptions[format] || formatOptions.long);
};

/**
 * Format relative time (e.g., "2 hours ago")
 * @param {Date|string} date - Date to format
 * @returns {string} - Relative time string
 */
export const formatRelativeTime = (date) => {
  const dateObj = new Date(date);
  if (isNaN(dateObj.getTime())) {
    return 'Invalid Date';
  }

  const now = new Date();
  const diffInSeconds = Math.floor((now - dateObj) / 1000);

  if (diffInSeconds < 60) {
    return 'Just now';
  }

  const diffInMinutes = Math.floor(diffInSeconds / 60);
  if (diffInMinutes < 60) {
    return `${diffInMinutes} minute${diffInMinutes !== 1 ? 's' : ''} ago`;
  }

  const diffInHours = Math.floor(diffInMinutes / 60);
  if (diffInHours < 24) {
    return `${diffInHours} hour${diffInHours !== 1 ? 's' : ''} ago`;
  }

  const diffInDays = Math.floor(diffInHours / 24);
  if (diffInDays < 30) {
    return `${diffInDays} day${diffInDays !== 1 ? 's' : ''} ago`;
  }

  const diffInMonths = Math.floor(diffInDays / 30);
  if (diffInMonths < 12) {
    return `${diffInMonths} month${diffInMonths !== 1 ? 's' : ''} ago`;
  }

  const diffInYears = Math.floor(diffInMonths / 12);
  return `${diffInYears} year${diffInYears !== 1 ? 's' : ''} ago`;
};

/**
 * Get score grade based on score value
 * @param {number} score - Score value (0-100)
 * @returns {Object} - Grade information
 */
export const getScoreGrade = (score) => {
  if (score < 0 || score > 100) {
    return { grade: 'N/A', color: '#6b7280', label: 'Invalid Score' };
  }

  for (const [grade, config] of Object.entries(SCORE_CONFIG.GRADES)) {
    if (score >= config.min && score <= config.max) {
      return { grade, color: config.color, label: grade };
    }
  }

  return { grade: 'F', color: '#ef4444', label: 'F' };
};

/**
 * Get score range information
 * @param {number} score - Score value (0-100)
 * @returns {Object} - Range information
 */
export const getScoreRange = (score) => {
  if (score < 0 || score > 100) {
    return { range: 'Invalid', color: '#6b7280', label: 'Invalid Score' };
  }

  for (const [range, config] of Object.entries(SCORE_CONFIG.RANGES)) {
    if (score >= config.min && score <= config.max) {
      return { range, color: config.color, label: config.label };
    }
  }

  return { range: 'Poor', color: '#ef4444', label: 'Poor' };
};

/**
 * Calculate percentage
 * @param {number} value - Value
 * @param {number} total - Total value
 * @param {number} decimals - Number of decimal places
 * @returns {number} - Percentage
 */
export const calculatePercentage = (value, total, decimals = 2) => {
  if (total === 0) return 0;
  return parseFloat(((value / total) * 100).toFixed(decimals));
};

/**
 * Generate random string
 * @param {number} length - String length
 * @param {string} charset - Character set to use
 * @returns {string} - Random string
 */
export const generateRandomString = (length = 8, charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') => {
  let result = '';
  for (let i = 0; i < length; i++) {
    result += charset.charAt(Math.floor(Math.random() * charset.length));
  }
  return result;
};

/**
 * Generate UUID v4
 * @returns {string} - UUID v4 string
 */
export const generateUUID = () => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
};

/**
 * Debounce function
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @param {boolean} immediate - Execute immediately
 * @returns {Function} - Debounced function
 */
export const debounce = (func, wait, immediate = false) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      timeout = null;
      if (!immediate) func(...args);
    };
    const callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func(...args);
  };
};

/**
 * Throttle function
 * @param {Function} func - Function to throttle
 * @param {number} limit - Time limit in milliseconds
 * @returns {Function} - Throttled function
 */
export const throttle = (func, limit) => {
  let inThrottle;
  return function executedFunction(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
};

/**
 * Deep clone object
 * @param {any} obj - Object to clone
 * @returns {any} - Cloned object
 */
export const deepClone = (obj) => {
  if (obj === null || typeof obj !== 'object') return obj;
  if (obj instanceof Date) return new Date(obj.getTime());
  if (obj instanceof Array) return obj.map(item => deepClone(item));
  if (typeof obj === 'object') {
    const clonedObj = {};
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        clonedObj[key] = deepClone(obj[key]);
      }
    }
    return clonedObj;
  }
  return obj;
};

/**
 * Merge objects deeply
 * @param {Object} target - Target object
 * @param {...Object} sources - Source objects
 * @returns {Object} - Merged object
 */
export const deepMerge = (target, ...sources) => {
  if (!sources.length) return target;
  const source = sources.shift();

  if (isObject(target) && isObject(source)) {
    for (const key in source) {
      if (isObject(source[key])) {
        if (!target[key]) Object.assign(target, { [key]: {} });
        deepMerge(target[key], source[key]);
      } else {
        Object.assign(target, { [key]: source[key] });
      }
    }
  }

  return deepMerge(target, ...sources);
};

/**
 * Check if value is an object
 * @param {any} item - Value to check
 * @returns {boolean} - True if object
 */
export const isObject = (item) => {
  return item && typeof item === 'object' && !Array.isArray(item);
};

/**
 * Get nested object property safely
 * @param {Object} obj - Object to access
 * @param {string} path - Property path (e.g., 'user.profile.name')
 * @param {any} defaultValue - Default value if property doesn't exist
 * @returns {any} - Property value or default
 */
export const getNestedProperty = (obj, path, defaultValue = undefined) => {
  const keys = path.split('.');
  let result = obj;

  for (const key of keys) {
    if (result === null || result === undefined || !result.hasOwnProperty(key)) {
      return defaultValue;
    }
    result = result[key];
  }

  return result;
};

/**
 * Set nested object property safely
 * @param {Object} obj - Object to modify
 * @param {string} path - Property path (e.g., 'user.profile.name')
 * @param {any} value - Value to set
 * @returns {Object} - Modified object
 */
export const setNestedProperty = (obj, path, value) => {
  const keys = path.split('.');
  const lastKey = keys.pop();
  let current = obj;

  for (const key of keys) {
    if (!current[key] || typeof current[key] !== 'object') {
      current[key] = {};
    }
    current = current[key];
  }

  current[lastKey] = value;
  return obj;
};

/**
 * Remove falsy values from object
 * @param {Object} obj - Object to clean
 * @returns {Object} - Cleaned object
 */
export const removeFalsyValues = (obj) => {
  const cleaned = {};
  for (const [key, value] of Object.entries(obj)) {
    if (value !== null && value !== undefined && value !== '') {
      cleaned[key] = value;
    }
  }
  return cleaned;
};

/**
 * Group array by key
 * @param {Array} array - Array to group
 * @param {string|Function} key - Key to group by
 * @returns {Object} - Grouped object
 */
export const groupBy = (array, key) => {
  return array.reduce((groups, item) => {
    const groupKey = typeof key === 'function' ? key(item) : item[key];
    if (!groups[groupKey]) {
      groups[groupKey] = [];
    }
    groups[groupKey].push(item);
    return groups;
  }, {});
};

/**
 * Sort array by key
 * @param {Array} array - Array to sort
 * @param {string} key - Key to sort by
 * @param {string} order - Sort order ('asc' or 'desc')
 * @returns {Array} - Sorted array
 */
export const sortBy = (array, key, order = 'asc') => {
  return [...array].sort((a, b) => {
    const aVal = getNestedProperty(a, key);
    const bVal = getNestedProperty(b, key);
    
    if (aVal < bVal) return order === 'asc' ? -1 : 1;
    if (aVal > bVal) return order === 'asc' ? 1 : -1;
    return 0;
  });
};

/**
 * Get unique values from array
 * @param {Array} array - Array to process
 * @param {string} key - Key to get unique values by (optional)
 * @returns {Array} - Array of unique values
 */
export const getUniqueValues = (array, key = null) => {
  if (key) {
    return [...new Set(array.map(item => getNestedProperty(item, key)))];
  }
  return [...new Set(array)];
};

/**
 * Capitalize first letter of string
 * @param {string} str - String to capitalize
 * @returns {string} - Capitalized string
 */
export const capitalize = (str) => {
  if (!str || typeof str !== 'string') return '';
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
};

/**
 * Convert string to title case
 * @param {string} str - String to convert
 * @returns {string} - Title case string
 */
export const toTitleCase = (str) => {
  if (!str || typeof str !== 'string') return '';
  return str.replace(/\w\S*/g, (txt) => 
    txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
  );
};

/**
 * Convert string to kebab case
 * @param {string} str - String to convert
 * @returns {string} - Kebab case string
 */
export const toKebabCase = (str) => {
  if (!str || typeof str !== 'string') return '';
  return str
    .replace(/([a-z])([A-Z])/g, '$1-$2')
    .replace(/[\s_]+/g, '-')
    .toLowerCase();
};

/**
 * Convert string to camel case
 * @param {string} str - String to convert
 * @returns {string} - Camel case string
 */
export const toCamelCase = (str) => {
  if (!str || typeof str !== 'string') return '';
  return str
    .replace(/(?:^\w|[A-Z]|\b\w)/g, (word, index) => 
      index === 0 ? word.toLowerCase() : word.toUpperCase()
    )
    .replace(/\s+/g, '');
};

/**
 * Truncate string to specified length
 * @param {string} str - String to truncate
 * @param {number} length - Maximum length
 * @param {string} suffix - Suffix to add
 * @returns {string} - Truncated string
 */
export const truncateString = (str, length = 100, suffix = '...') => {
  if (!str || typeof str !== 'string') return '';
  if (str.length <= length) return str;
  return str.substring(0, length - suffix.length) + suffix;
};

/**
 * Check if value is empty
 * @param {any} value - Value to check
 * @returns {boolean} - True if empty
 */
export const isEmpty = (value) => {
  if (value === null || value === undefined) return true;
  if (typeof value === 'string') return value.trim().length === 0;
  if (Array.isArray(value)) return value.length === 0;
  if (typeof value === 'object') return Object.keys(value).length === 0;
  return false;
};

/**
 * Check if value is not empty
 * @param {any} value - Value to check
 * @returns {boolean} - True if not empty
 */
export const isNotEmpty = (value) => {
  return !isEmpty(value);
};

/**
 * Get user role display name
 * @param {string} role - Role key
 * @returns {string} - Display name
 */
export const getRoleDisplayName = (role) => {
  const roleMap = {
    [USER_ROLES.ADMIN]: 'Administrator',
    [USER_ROLES.USER]: 'User',
    [USER_ROLES.ANALYST]: 'Analyst',
    [USER_ROLES.MODERATOR]: 'Moderator',
  };
  return roleMap[role] || capitalize(role);
};

/**
 * Get analysis type display name
 * @param {string} type - Analysis type key
 * @returns {string} - Display name
 */
export const getAnalysisTypeDisplayName = (type) => {
  const typeMap = {
    [ANALYSIS_TYPES.OVERALL]: 'Overall Analysis',
    [ANALYSIS_TYPES.JOB_MATCH]: 'Job Match Analysis',
    [ANALYSIS_TYPES.SKILL_ANALYSIS]: 'Skill Analysis',
    [ANALYSIS_TYPES.EXPERIENCE_ANALYSIS]: 'Experience Analysis',
    [ANALYSIS_TYPES.EDUCATION_ANALYSIS]: 'Education Analysis',
  };
  return typeMap[type] || capitalize(type);
};

/**
 * Get theme display name
 * @param {string} theme - Theme key
 * @returns {string} - Display name
 */
export const getThemeDisplayName = (theme) => {
  const themeMap = {
    [THEME_CONFIG.LIGHT]: 'Light',
    [THEME_CONFIG.DARK]: 'Dark',
    [THEME_CONFIG.SYSTEM]: 'System',
  };
  return themeMap[theme] || capitalize(theme);
};

/**
 * Get language display name
 * @param {string} language - Language key
 * @returns {string} - Display name
 */
export const getLanguageDisplayName = (language) => {
  const languageMap = {
    [LANGUAGE_CONFIG.EN]: 'English',
    [LANGUAGE_CONFIG.ES]: 'Español',
    [LANGUAGE_CONFIG.FR]: 'Français',
    [LANGUAGE_CONFIG.DE]: 'Deutsch',
  };
  return languageMap[language] || capitalize(language);
};

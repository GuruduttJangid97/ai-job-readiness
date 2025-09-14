/**
 * Formatting utility functions
 * 
 * This module provides functions for formatting data, text, numbers,
 * dates, and other content for display purposes.
 * 
 * @author AI Job Readiness Team
 * @version 1.0.0
 */

import { SCORE_CONFIG, ANALYSIS_TYPES, USER_ROLES } from './constants';

/**
 * Format currency
 * @param {number} amount - Amount to format
 * @param {string} currency - Currency code (default: 'USD')
 * @param {string} locale - Locale code (default: 'en-US')
 * @returns {string} - Formatted currency
 */
export const formatCurrency = (amount, currency = 'USD', locale = 'en-US') => {
  if (typeof amount !== 'number' || isNaN(amount)) {
    return '$0.00';
  }

  try {
    return new Intl.NumberFormat(locale, {
      style: 'currency',
      currency: currency,
    }).format(amount);
  } catch (error) {
    console.warn('Error formatting currency:', error);
    return `$${amount.toFixed(2)}`;
  }
};

/**
 * Format number with thousands separator
 * @param {number} number - Number to format
 * @param {number} decimals - Number of decimal places
 * @param {string} locale - Locale code (default: 'en-US')
 * @returns {string} - Formatted number
 */
export const formatNumber = (number, decimals = 0, locale = 'en-US') => {
  if (typeof number !== 'number' || isNaN(number)) {
    return '0';
  }

  try {
    return new Intl.NumberFormat(locale, {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    }).format(number);
  } catch (error) {
    console.warn('Error formatting number:', error);
    return number.toFixed(decimals);
  }
};

/**
 * Format percentage
 * @param {number} value - Value to format as percentage
 * @param {number} decimals - Number of decimal places
 * @param {string} locale - Locale code (default: 'en-US')
 * @returns {string} - Formatted percentage
 */
export const formatPercentage = (value, decimals = 1, locale = 'en-US') => {
  if (typeof value !== 'number' || isNaN(value)) {
    return '0%';
  }

  try {
    return new Intl.NumberFormat(locale, {
      style: 'percent',
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    }).format(value / 100);
  } catch (error) {
    console.warn('Error formatting percentage:', error);
    return `${value.toFixed(decimals)}%`;
  }
};

/**
 * Format file size
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
 * Format date
 * @param {Date|string|number} date - Date to format
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
    short: {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      timeZone: timezone
    },
    long: {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      timeZone: timezone
    },
    time: {
      hour: '2-digit',
      minute: '2-digit',
      timeZone: timezone
    },
    datetime: {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      timeZone: timezone
    },
    full: {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      timeZone: timezone
    }
  };

  try {
    return dateObj.toLocaleDateString(locale, formatOptions[format] || formatOptions.long);
  } catch (error) {
    console.warn('Error formatting date:', error);
    return dateObj.toISOString();
  }
};

/**
 * Format relative time (e.g., "2 hours ago")
 * @param {Date|string|number} date - Date to format
 * @param {string} locale - Locale code (default: 'en-US')
 * @returns {string} - Relative time string
 */
export const formatRelativeTime = (date, locale = 'en-US') => {
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
 * Format duration in human-readable format
 * @param {number} milliseconds - Duration in milliseconds
 * @returns {string} - Formatted duration
 */
export const formatDuration = (milliseconds) => {
  if (typeof milliseconds !== 'number' || isNaN(milliseconds)) {
    return '0s';
  }

  const seconds = Math.floor(milliseconds / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (days > 0) {
    return `${days}d ${hours % 24}h ${minutes % 60}m`;
  } else if (hours > 0) {
    return `${hours}h ${minutes % 60}m ${seconds % 60}s`;
  } else if (minutes > 0) {
    return `${minutes}m ${seconds % 60}s`;
  } else {
    return `${seconds}s`;
  }
};

/**
 * Format score with grade
 * @param {number} score - Score value (0-100)
 * @param {boolean} showGrade - Whether to show grade
 * @returns {Object} - Formatted score information
 */
export const formatScore = (score, showGrade = true) => {
  if (typeof score !== 'number' || isNaN(score) || score < 0 || score > 100) {
    return {
      score: 'N/A',
      grade: 'N/A',
      color: '#6b7280',
      label: 'Invalid Score'
    };
  }

  const roundedScore = Math.round(score);
  const range = getScoreRange(score);
  const grade = showGrade ? getScoreGrade(score) : null;

  return {
    score: roundedScore,
    grade: grade?.grade || null,
    color: range.color,
    label: range.label,
    percentage: `${roundedScore}%`
  };
};

/**
 * Get score range information
 * @param {number} score - Score value (0-100)
 * @returns {Object} - Range information
 */
const getScoreRange = (score) => {
  for (const [range, config] of Object.entries(SCORE_CONFIG.RANGES)) {
    if (score >= config.min && score <= config.max) {
      return { range, color: config.color, label: config.label };
    }
  }
  return { range: 'Poor', color: '#ef4444', label: 'Poor' };
};

/**
 * Get score grade information
 * @param {number} score - Score value (0-100)
 * @returns {Object} - Grade information
 */
const getScoreGrade = (score) => {
  for (const [grade, config] of Object.entries(SCORE_CONFIG.GRADES)) {
    if (score >= config.min && score <= config.max) {
      return { grade, color: config.color, label: grade };
    }
  }
  return { grade: 'F', color: '#ef4444', label: 'F' };
};

/**
 * Format phone number
 * @param {string} phone - Phone number to format
 * @param {string} locale - Locale code (default: 'en-US')
 * @returns {string} - Formatted phone number
 */
export const formatPhoneNumber = (phone, locale = 'en-US') => {
  if (!phone || typeof phone !== 'string') {
    return '';
  }

  // Remove all non-digit characters
  const digits = phone.replace(/\D/g, '');

  if (digits.length === 10) {
    // US format: (123) 456-7890
    return `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6)}`;
  } else if (digits.length === 11 && digits[0] === '1') {
    // US format with country code: +1 (123) 456-7890
    return `+1 (${digits.slice(1, 4)}) ${digits.slice(4, 7)}-${digits.slice(7)}`;
  } else {
    // Return original if not standard US format
    return phone;
  }
};

/**
 * Format email address
 * @param {string} email - Email to format
 * @returns {string} - Formatted email
 */
export const formatEmail = (email) => {
  if (!email || typeof email !== 'string') {
    return '';
  }

  return email.toLowerCase().trim();
};

/**
 * Format name (first name, last name)
 * @param {string} firstName - First name
 * @param {string} lastName - Last name
 * @param {string} format - Format type ('full', 'initials', 'first', 'last')
 * @returns {string} - Formatted name
 */
export const formatName = (firstName, lastName, format = 'full') => {
  const first = firstName?.trim() || '';
  const last = lastName?.trim() || '';

  switch (format) {
    case 'full':
      return `${first} ${last}`.trim();
    case 'initials':
      const firstInitial = first.charAt(0).toUpperCase();
      const lastInitial = last.charAt(0).toUpperCase();
      return `${firstInitial}${lastInitial}`;
    case 'first':
      return first;
    case 'last':
      return last;
    default:
      return `${first} ${last}`.trim();
  }
};

/**
 * Format role display name
 * @param {string} role - Role key
 * @returns {string} - Display name
 */
export const formatRole = (role) => {
  const roleMap = {
    [USER_ROLES.ADMIN]: 'Administrator',
    [USER_ROLES.USER]: 'User',
    [USER_ROLES.ANALYST]: 'Analyst',
    [USER_ROLES.MODERATOR]: 'Moderator',
  };
  return roleMap[role] || capitalize(role);
};

/**
 * Format analysis type display name
 * @param {string} type - Analysis type key
 * @returns {string} - Display name
 */
export const formatAnalysisType = (type) => {
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
 * Format text with line breaks
 * @param {string} text - Text to format
 * @param {number} maxLength - Maximum line length
 * @returns {string} - Formatted text with line breaks
 */
export const formatTextWithLineBreaks = (text, maxLength = 80) => {
  if (!text || typeof text !== 'string') {
    return '';
  }

  const words = text.split(' ');
  const lines = [];
  let currentLine = '';

  for (const word of words) {
    if (currentLine.length + word.length + 1 <= maxLength) {
      currentLine += (currentLine ? ' ' : '') + word;
    } else {
      if (currentLine) {
        lines.push(currentLine);
      }
      currentLine = word;
    }
  }

  if (currentLine) {
    lines.push(currentLine);
  }

  return lines.join('\n');
};

/**
 * Format JSON for display
 * @param {any} data - Data to format
 * @param {number} indent - Indentation level
 * @returns {string} - Formatted JSON string
 */
export const formatJSON = (data, indent = 2) => {
  try {
    return JSON.stringify(data, null, indent);
  } catch (error) {
    console.warn('Error formatting JSON:', error);
    return String(data);
  }
};

/**
 * Format URL for display
 * @param {string} url - URL to format
 * @param {number} maxLength - Maximum length
 * @returns {string} - Formatted URL
 */
export const formatURL = (url, maxLength = 50) => {
  if (!url || typeof url !== 'string') {
    return '';
  }

  if (url.length <= maxLength) {
    return url;
  }

  const start = url.substring(0, maxLength - 3);
  return `${start}...`;
};

/**
 * Format list items
 * @param {Array} items - Items to format
 * @param {string} separator - Separator (default: ', ')
 * @param {number} maxItems - Maximum number of items to show
 * @returns {string} - Formatted list
 */
export const formatList = (items, separator = ', ', maxItems = 5) => {
  if (!Array.isArray(items) || items.length === 0) {
    return '';
  }

  const displayItems = items.slice(0, maxItems);
  const remaining = items.length - maxItems;

  let result = displayItems.join(separator);
  if (remaining > 0) {
    result += ` and ${remaining} more`;
  }

  return result;
};

/**
 * Format address
 * @param {Object} address - Address object
 * @returns {string} - Formatted address
 */
export const formatAddress = (address) => {
  if (!address || typeof address !== 'object') {
    return '';
  }

  const parts = [
    address.street,
    address.city,
    address.state,
    address.zipCode,
    address.country
  ].filter(Boolean);

  return parts.join(', ');
};

/**
 * Format social security number
 * @param {string} ssn - SSN to format
 * @param {boolean} mask - Whether to mask the SSN
 * @returns {string} - Formatted SSN
 */
export const formatSSN = (ssn, mask = true) => {
  if (!ssn || typeof ssn !== 'string') {
    return '';
  }

  const digits = ssn.replace(/\D/g, '');
  
  if (digits.length !== 9) {
    return ssn;
  }

  if (mask) {
    return `XXX-XX-${digits.slice(-4)}`;
  } else {
    return `${digits.slice(0, 3)}-${digits.slice(3, 5)}-${digits.slice(5)}`;
  }
};

/**
 * Format credit card number
 * @param {string} cardNumber - Card number to format
 * @param {boolean} mask - Whether to mask the card number
 * @returns {string} - Formatted card number
 */
export const formatCreditCard = (cardNumber, mask = true) => {
  if (!cardNumber || typeof cardNumber !== 'string') {
    return '';
  }

  const digits = cardNumber.replace(/\D/g, '');
  
  if (digits.length < 13 || digits.length > 19) {
    return cardNumber;
  }

  if (mask) {
    const lastFour = digits.slice(-4);
    return `****-****-****-${lastFour}`;
  } else {
    // Format with spaces every 4 digits
    return digits.replace(/(.{4})/g, '$1-').replace(/-$/, '');
  }
};

/**
 * Capitalize first letter of string
 * @param {string} str - String to capitalize
 * @returns {string} - Capitalized string
 */
const capitalize = (str) => {
  if (!str || typeof str !== 'string') return '';
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
};

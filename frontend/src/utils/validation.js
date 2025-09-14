/**
 * Validation utility functions
 * 
 * This module provides client-side validation functions for forms,
 * data validation, and input sanitization.
 * 
 * @author AI Job Readiness Team
 * @version 1.0.0
 */

import { VALIDATION_RULES, FILE_CONFIG } from './constants';

/**
 * Validate email format
 * @param {string} email - Email to validate
 * @returns {Object} - Validation result with isValid and message
 */
export const validateEmail = (email) => {
  if (!email) {
    return { isValid: false, message: 'Email is required' };
  }

  if (!VALIDATION_RULES.EMAIL.PATTERN.test(email)) {
    return { isValid: false, message: VALIDATION_RULES.EMAIL.MESSAGE };
  }

  return { isValid: true, message: '' };
};

/**
 * Validate password strength
 * @param {string} password - Password to validate
 * @returns {Object} - Validation result with isValid, message, and strength
 */
export const validatePassword = (password) => {
  if (!password) {
    return { isValid: false, message: 'Password is required', strength: 0 };
  }

  if (password.length < VALIDATION_RULES.PASSWORD.MIN_LENGTH) {
    return { 
      isValid: false, 
      message: `Password must be at least ${VALIDATION_RULES.PASSWORD.MIN_LENGTH} characters long`,
      strength: 0
    };
  }

  let strength = 0;
  const checks = {
    length: password.length >= VALIDATION_RULES.PASSWORD.MIN_LENGTH,
    uppercase: VALIDATION_RULES.PASSWORD.REQUIRE_UPPERCASE ? /[A-Z]/.test(password) : true,
    lowercase: VALIDATION_RULES.PASSWORD.REQUIRE_LOWERCASE ? /[a-z]/.test(password) : true,
    digits: VALIDATION_RULES.PASSWORD.REQUIRE_DIGITS ? /\d/.test(password) : true,
    special: VALIDATION_RULES.PASSWORD.REQUIRE_SPECIAL_CHARS ? /[!@#$%^&*(),.?":{}|<>]/.test(password) : true,
  };

  strength = Object.values(checks).filter(Boolean).length;

  if (!checks.uppercase || !checks.lowercase || !checks.digits) {
    return { 
      isValid: false, 
      message: VALIDATION_RULES.PASSWORD.MESSAGE,
      strength
    };
  }

  return { isValid: true, message: '', strength };
};

/**
 * Validate phone number format
 * @param {string} phone - Phone number to validate
 * @returns {Object} - Validation result with isValid and message
 */
export const validatePhone = (phone) => {
  if (!phone) {
    return { isValid: true, message: '' }; // Phone is optional
  }

  if (!VALIDATION_RULES.PHONE.PATTERN.test(phone)) {
    return { isValid: false, message: VALIDATION_RULES.PHONE.MESSAGE };
  }

  return { isValid: true, message: '' };
};

/**
 * Validate name format
 * @param {string} name - Name to validate
 * @param {string} fieldName - Field name for error message
 * @returns {Object} - Validation result with isValid and message
 */
export const validateName = (name, fieldName = 'Name') => {
  if (!name) {
    return { isValid: false, message: `${fieldName} is required` };
  }

  if (name.length < VALIDATION_RULES.NAME.MIN_LENGTH) {
    return { 
      isValid: false, 
      message: `${fieldName} must be at least ${VALIDATION_RULES.NAME.MIN_LENGTH} characters long` 
    };
  }

  if (name.length > VALIDATION_RULES.NAME.MAX_LENGTH) {
    return { 
      isValid: false, 
      message: `${fieldName} must be no more than ${VALIDATION_RULES.NAME.MAX_LENGTH} characters long` 
    };
  }

  if (!VALIDATION_RULES.NAME.PATTERN.test(name)) {
    return { isValid: false, message: VALIDATION_RULES.NAME.MESSAGE };
  }

  return { isValid: true, message: '' };
};

/**
 * Validate file upload
 * @param {File} file - File to validate
 * @returns {Object} - Validation result with isValid and message
 */
export const validateFile = (file) => {
  if (!file) {
    return { isValid: false, message: 'File is required' };
  }

  // Check file size
  if (file.size > FILE_CONFIG.MAX_SIZE) {
    return { 
      isValid: false, 
      message: `File size must be less than ${FILE_CONFIG.MAX_SIZE / (1024 * 1024)}MB` 
    };
  }

  // Check file type
  const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
  if (!FILE_CONFIG.ALLOWED_TYPES.includes(fileExtension)) {
    return { 
      isValid: false, 
      message: `File type must be one of: ${FILE_CONFIG.ALLOWED_TYPES.join(', ')}` 
    };
  }

  // Check MIME type
  if (!FILE_CONFIG.ALLOWED_MIME_TYPES.includes(file.type)) {
    return { 
      isValid: false, 
      message: 'Invalid file type. Please upload a valid document.' 
    };
  }

  return { isValid: true, message: '' };
};

/**
 * Validate URL format
 * @param {string} url - URL to validate
 * @returns {Object} - Validation result with isValid and message
 */
export const validateUrl = (url) => {
  if (!url) {
    return { isValid: true, message: '' }; // URL is optional
  }

  try {
    new URL(url);
    return { isValid: true, message: '' };
  } catch {
    return { isValid: false, message: 'Please enter a valid URL' };
  }
};

/**
 * Validate required field
 * @param {any} value - Value to validate
 * @param {string} fieldName - Field name for error message
 * @returns {Object} - Validation result with isValid and message
 */
export const validateRequired = (value, fieldName) => {
  if (value === null || value === undefined || value === '') {
    return { isValid: false, message: `${fieldName} is required` };
  }

  return { isValid: true, message: '' };
};

/**
 * Validate minimum length
 * @param {string} value - Value to validate
 * @param {number} minLength - Minimum length required
 * @param {string} fieldName - Field name for error message
 * @returns {Object} - Validation result with isValid and message
 */
export const validateMinLength = (value, minLength, fieldName) => {
  if (!value || value.length < minLength) {
    return { 
      isValid: false, 
      message: `${fieldName} must be at least ${minLength} characters long` 
    };
  }

  return { isValid: true, message: '' };
};

/**
 * Validate maximum length
 * @param {string} value - Value to validate
 * @param {number} maxLength - Maximum length allowed
 * @param {string} fieldName - Field name for error message
 * @returns {Object} - Validation result with isValid and message
 */
export const validateMaxLength = (value, maxLength, fieldName) => {
  if (value && value.length > maxLength) {
    return { 
      isValid: false, 
      message: `${fieldName} must be no more than ${maxLength} characters long` 
    };
  }

  return { isValid: true, message: '' };
};

/**
 * Validate numeric value
 * @param {any} value - Value to validate
 * @param {string} fieldName - Field name for error message
 * @param {Object} options - Validation options
 * @returns {Object} - Validation result with isValid and message
 */
export const validateNumber = (value, fieldName, options = {}) => {
  const { min, max, integer = false } = options;

  if (value === null || value === undefined || value === '') {
    return { isValid: false, message: `${fieldName} is required` };
  }

  const num = Number(value);
  if (isNaN(num)) {
    return { isValid: false, message: `${fieldName} must be a valid number` };
  }

  if (integer && !Number.isInteger(num)) {
    return { isValid: false, message: `${fieldName} must be a whole number` };
  }

  if (min !== undefined && num < min) {
    return { isValid: false, message: `${fieldName} must be at least ${min}` };
  }

  if (max !== undefined && num > max) {
    return { isValid: false, message: `${fieldName} must be no more than ${max}` };
  }

  return { isValid: true, message: '' };
};

/**
 * Validate date
 * @param {any} value - Value to validate
 * @param {string} fieldName - Field name for error message
 * @param {Object} options - Validation options
 * @returns {Object} - Validation result with isValid and message
 */
export const validateDate = (value, fieldName, options = {}) => {
  const { min, max, future = false, past = false } = options;

  if (!value) {
    return { isValid: false, message: `${fieldName} is required` };
  }

  const date = new Date(value);
  if (isNaN(date.getTime())) {
    return { isValid: false, message: `${fieldName} must be a valid date` };
  }

  const now = new Date();
  if (future && date <= now) {
    return { isValid: false, message: `${fieldName} must be in the future` };
  }

  if (past && date >= now) {
    return { isValid: false, message: `${fieldName} must be in the past` };
  }

  if (min && date < new Date(min)) {
    return { isValid: false, message: `${fieldName} must be after ${min}` };
  }

  if (max && date > new Date(max)) {
    return { isValid: false, message: `${fieldName} must be before ${max}` };
  }

  return { isValid: true, message: '' };
};

/**
 * Validate form data
 * @param {Object} data - Form data to validate
 * @param {Object} rules - Validation rules
 * @returns {Object} - Validation result with isValid, errors, and data
 */
export const validateForm = (data, rules) => {
  const errors = {};
  let isValid = true;

  for (const [field, fieldRules] of Object.entries(rules)) {
    const value = data[field];
    const fieldError = validateField(value, fieldRules, field);
    
    if (!fieldError.isValid) {
      errors[field] = fieldError.message;
      isValid = false;
    }
  }

  return { isValid, errors, data };
};

/**
 * Validate individual field based on rules
 * @param {any} value - Field value
 * @param {Object} rules - Field validation rules
 * @param {string} fieldName - Field name
 * @returns {Object} - Validation result with isValid and message
 */
export const validateField = (value, rules, fieldName) => {
  // Required validation
  if (rules.required) {
    const requiredResult = validateRequired(value, fieldName);
    if (!requiredResult.isValid) {
      return requiredResult;
    }
  }

  // Skip other validations if field is empty and not required
  if (!value && !rules.required) {
    return { isValid: true, message: '' };
  }

  // Type-specific validations
  if (rules.type === 'email') {
    return validateEmail(value);
  }

  if (rules.type === 'password') {
    return validatePassword(value);
  }

  if (rules.type === 'phone') {
    return validatePhone(value);
  }

  if (rules.type === 'name') {
    return validateName(value, fieldName);
  }

  if (rules.type === 'url') {
    return validateUrl(value);
  }

  if (rules.type === 'number') {
    return validateNumber(value, fieldName, rules);
  }

  if (rules.type === 'date') {
    return validateDate(value, fieldName, rules);
  }

  // Length validations
  if (rules.minLength) {
    const minLengthResult = validateMinLength(value, rules.minLength, fieldName);
    if (!minLengthResult.isValid) {
      return minLengthResult;
    }
  }

  if (rules.maxLength) {
    const maxLengthResult = validateMaxLength(value, rules.maxLength, fieldName);
    if (!maxLengthResult.isValid) {
      return maxLengthResult;
    }
  }

  // Custom validation function
  if (rules.custom && typeof rules.custom === 'function') {
    return rules.custom(value, fieldName);
  }

  return { isValid: true, message: '' };
};

/**
 * Sanitize string input
 * @param {string} input - Input to sanitize
 * @returns {string} - Sanitized input
 */
export const sanitizeString = (input) => {
  if (typeof input !== 'string') {
    return '';
  }

  return input
    .trim()
    .replace(/[<>]/g, '') // Remove potential HTML tags
    .replace(/[&<>"']/g, (match) => {
      const escapeMap = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#x27;',
      };
      return escapeMap[match];
    });
};

/**
 * Sanitize HTML input
 * @param {string} input - HTML input to sanitize
 * @returns {string} - Sanitized HTML
 */
export const sanitizeHtml = (input) => {
  if (typeof input !== 'string') {
    return '';
  }

  // Basic HTML sanitization - remove script tags and dangerous attributes
  return input
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
    .replace(/on\w+="[^"]*"/gi, '')
    .replace(/javascript:/gi, '');
};

/**
 * Validate and sanitize form data
 * @param {Object} data - Form data
 * @param {Object} rules - Validation rules
 * @returns {Object} - Sanitized and validated data
 */
export const validateAndSanitizeForm = (data, rules) => {
  const sanitizedData = {};
  const errors = {};
  let isValid = true;

  for (const [field, value] of Object.entries(data)) {
    // Sanitize string values
    if (typeof value === 'string') {
      sanitizedData[field] = sanitizeString(value);
    } else {
      sanitizedData[field] = value;
    }

    // Validate field if rules exist
    if (rules[field]) {
      const fieldError = validateField(sanitizedData[field], rules[field], field);
      if (!fieldError.isValid) {
        errors[field] = fieldError.message;
        isValid = false;
      }
    }
  }

  return { isValid, errors, data: sanitizedData };
};

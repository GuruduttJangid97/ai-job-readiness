/**
 * Application constants and configuration
 * 
 * This module contains all application constants, configuration values,
 * and static data used throughout the frontend application.
 * 
 * @author AI Job Readiness Team
 * @version 1.0.0
 */

// API Configuration
export const API_CONFIG = {
  BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  TIMEOUT: 10000,
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000,
};

// API Endpoints
export const API_ENDPOINTS = {
  // Authentication
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    LOGOUT: '/auth/logout',
    REFRESH: '/auth/refresh',
    ME: '/auth/me',
    FORGOT_PASSWORD: '/auth/forgot-password',
    RESET_PASSWORD: '/auth/reset-password',
    VERIFY_EMAIL: '/auth/verify-email',
  },
  
  // Users
  USERS: {
    PROFILE: '/users/profile',
    LIST: '/users/list',
    BY_ID: (id) => `/users/${id}`,
    ACTIVATE: (id) => `/users/${id}/activate`,
    DEACTIVATE: (id) => `/users/${id}/deactivate`,
  },
  
  // Resumes
  RESUMES: {
    LIST: '/resumes/',
    CREATE: '/resumes/',
    BY_ID: (id) => `/resumes/${id}`,
    UPLOAD: (id) => `/resumes/${id}/upload`,
    DOWNLOAD: (id) => `/resumes/${id}/download`,
    ANALYZE: (id) => `/resumes/${id}/analyze`,
    PUBLIC: (id) => `/resumes/public/${id}`,
    STATS: '/resumes/stats/summary',
  },
  
  // Roles
  ROLES: {
    LIST: '/roles/',
    CREATE: '/roles/',
    BY_ID: (id) => `/roles/${id}`,
    ASSIGN: (userId, roleId) => `/roles/${roleId}/assign/${userId}`,
    UNASSIGN: (userId, roleId) => `/roles/${roleId}/unassign/${userId}`,
  },
  
  // System
  SYSTEM: {
    HEALTH: '/health',
    MODELS: '/models',
    DATABASE: '/database',
    INFO: '/api/v1/info',
  },
};

// HTTP Status Codes
export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  CONFLICT: 409,
  UNPROCESSABLE_ENTITY: 422,
  TOO_MANY_REQUESTS: 429,
  INTERNAL_SERVER_ERROR: 500,
  SERVICE_UNAVAILABLE: 503,
};

// Local Storage Keys
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  REFRESH_TOKEN: 'refresh_token',
  USER_DATA: 'user_data',
  THEME: 'theme',
  LANGUAGE: 'language',
  SETTINGS: 'app_settings',
};

// File Upload Configuration
export const FILE_CONFIG = {
  MAX_SIZE: 10 * 1024 * 1024, // 10MB
  ALLOWED_TYPES: ['.pdf', '.doc', '.docx', '.txt'],
  ALLOWED_MIME_TYPES: [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain',
  ],
};

// Pagination Configuration
export const PAGINATION = {
  DEFAULT_PAGE: 1,
  DEFAULT_PAGE_SIZE: 10,
  MAX_PAGE_SIZE: 100,
  PAGE_SIZE_OPTIONS: [5, 10, 25, 50, 100],
};

// Form Validation Rules
export const VALIDATION_RULES = {
  EMAIL: {
    PATTERN: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
    MESSAGE: 'Please enter a valid email address',
  },
  PASSWORD: {
    MIN_LENGTH: 8,
    REQUIRE_UPPERCASE: true,
    REQUIRE_LOWERCASE: true,
    REQUIRE_DIGITS: true,
    REQUIRE_SPECIAL_CHARS: false,
    MESSAGE: 'Password must be at least 8 characters long and contain uppercase, lowercase, and digits',
  },
  PHONE: {
    PATTERN: /^[\+]?[1-9][\d]{0,15}$/,
    MESSAGE: 'Please enter a valid phone number',
  },
  NAME: {
    MIN_LENGTH: 2,
    MAX_LENGTH: 100,
    PATTERN: /^[a-zA-Z\s'-]+$/,
    MESSAGE: 'Name must be 2-100 characters and contain only letters, spaces, hyphens, and apostrophes',
  },
};

// Score Ranges and Grades
export const SCORE_CONFIG = {
  RANGES: {
    EXCELLENT: { min: 85, max: 100, label: 'Excellent', color: '#10b981' },
    GOOD: { min: 70, max: 84, label: 'Good', color: '#3b82f6' },
    FAIR: { min: 55, max: 69, label: 'Fair', color: '#f59e0b' },
    POOR: { min: 0, max: 54, label: 'Poor', color: '#ef4444' },
  },
  GRADES: {
    'A+': { min: 97, max: 100, color: '#10b981' },
    'A': { min: 93, max: 96, color: '#10b981' },
    'A-': { min: 90, max: 92, color: '#10b981' },
    'B+': { min: 87, max: 89, color: '#3b82f6' },
    'B': { min: 83, max: 86, color: '#3b82f6' },
    'B-': { min: 80, max: 82, color: '#3b82f6' },
    'C+': { min: 77, max: 79, color: '#f59e0b' },
    'C': { min: 73, max: 76, color: '#f59e0b' },
    'C-': { min: 70, max: 72, color: '#f59e0b' },
    'D+': { min: 67, max: 69, color: '#ef4444' },
    'D': { min: 65, max: 66, color: '#ef4444' },
    'F': { min: 0, max: 64, color: '#ef4444' },
  },
};

// Analysis Types
export const ANALYSIS_TYPES = {
  OVERALL: 'overall',
  JOB_MATCH: 'job_match',
  SKILL_ANALYSIS: 'skill_analysis',
  EXPERIENCE_ANALYSIS: 'experience_analysis',
  EDUCATION_ANALYSIS: 'education_analysis',
};

// User Roles
export const USER_ROLES = {
  ADMIN: 'admin',
  USER: 'user',
  ANALYST: 'analyst',
  MODERATOR: 'moderator',
};

// Theme Configuration
export const THEME_CONFIG = {
  LIGHT: 'light',
  DARK: 'dark',
  SYSTEM: 'system',
};

// Language Configuration
export const LANGUAGE_CONFIG = {
  EN: 'en',
  ES: 'es',
  FR: 'fr',
  DE: 'de',
};

// Animation Durations (in milliseconds)
export const ANIMATION_DURATION = {
  FAST: 150,
  NORMAL: 250,
  SLOW: 350,
  VERY_SLOW: 500,
};

// Breakpoints for responsive design
export const BREAKPOINTS = {
  XS: '480px',
  SM: '640px',
  MD: '768px',
  LG: '1024px',
  XL: '1280px',
  '2XL': '1536px',
};

// Error Messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error. Please check your connection and try again.',
  SERVER_ERROR: 'Server error. Please try again later.',
  UNAUTHORIZED: 'You are not authorized to perform this action.',
  FORBIDDEN: 'Access denied. You do not have permission to access this resource.',
  NOT_FOUND: 'The requested resource was not found.',
  VALIDATION_ERROR: 'Please check your input and try again.',
  FILE_TOO_LARGE: 'File is too large. Maximum size is 10MB.',
  INVALID_FILE_TYPE: 'Invalid file type. Please upload a PDF, DOC, DOCX, or TXT file.',
  GENERIC: 'An unexpected error occurred. Please try again.',
};

// Success Messages
export const SUCCESS_MESSAGES = {
  LOGIN: 'Login successful!',
  LOGOUT: 'Logout successful!',
  REGISTER: 'Registration successful! Please check your email to verify your account.',
  PROFILE_UPDATE: 'Profile updated successfully!',
  PASSWORD_CHANGE: 'Password changed successfully!',
  RESUME_UPLOAD: 'Resume uploaded successfully!',
  RESUME_DELETE: 'Resume deleted successfully!',
  RESUME_ANALYZE: 'Resume analysis completed!',
  GENERIC: 'Operation completed successfully!',
};

// Loading States
export const LOADING_STATES = {
  IDLE: 'idle',
  LOADING: 'loading',
  SUCCESS: 'success',
  ERROR: 'error',
};

// Default Values
export const DEFAULTS = {
  PAGE_SIZE: 10,
  SORT_ORDER: 'desc',
  SORT_FIELD: 'created_at',
  THEME: THEME_CONFIG.LIGHT,
  LANGUAGE: LANGUAGE_CONFIG.EN,
  DEBOUNCE_DELAY: 300,
  TOAST_DURATION: 5000,
};

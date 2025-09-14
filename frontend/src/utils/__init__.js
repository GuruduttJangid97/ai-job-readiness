/**
 * Utility modules for AI Job Readiness Platform Frontend
 * 
 * This package contains utility functions and classes that are used
 * across the frontend application to reduce code duplication and improve maintainability.
 * 
 * Modules:
 * - api: API service functions and HTTP client configuration
 * - auth: Authentication utilities and token management
 * - validation: Form validation and data validation utilities
 * - storage: Local storage and session storage utilities
 * - formatting: Data formatting and display utilities
 * - constants: Application constants and configuration
 * - helpers: General helper functions
 * 
 * @author AI Job Readiness Team
 * @version 1.0.0
 */

export { default as apiClient } from './api';
export { default as authUtils } from './auth';
export { default as validationUtils } from './validation';
export { default as storageUtils } from './storage';
export { default as formattingUtils } from './formatting';
export { default as constants } from './constants';
export { default as helpers } from './helpers';

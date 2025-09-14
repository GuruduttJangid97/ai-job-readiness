/**
 * AI Job Readiness Platform - Main Application Component
 * 
 * This is the main React component for the AI Job Readiness Platform frontend.
 * It provides the primary user interface for job readiness assessment and analysis.
 * 
 * Features:
 * - User authentication and profile management
 * - Resume upload and analysis
 * - Job readiness scoring and insights
 * - Skills assessment and gap analysis
 * - Personalized recommendations
 * 
 * @component
 * @returns {JSX.Element} The main application component
 * 
 * @author AI Job Readiness Team
 * @version 1.0.0
 */

import React, { useState, useEffect } from 'react';
import './App.css';

// Import utilities
import { useAuth } from './utils/hooks';
import { formatName, formatDate } from './utils/formatting';
import { SUCCESS_MESSAGES, ERROR_MESSAGES } from './utils/constants';

// Import components (to be created)
// import Header from './components/Header';
// import Navigation from './components/Navigation';
// import Dashboard from './components/Dashboard';
// import AuthModal from './components/AuthModal';
// import ResumeUpload from './components/ResumeUpload';
// import ScoreDisplay from './components/ScoreDisplay';

/**
 * Main App component that renders the AI Job Readiness Platform
 * 
 * This component manages the overall application state and routing.
 * It provides a clean, modern interface for users to assess their
 * job readiness and improve their career prospects.
 */
function App() {
  // Use custom authentication hook
  const { user, isAuthenticated, loading: authLoading, login, logout } = useAuth();
  
  // Application state management
  const [activeTab, setActiveTab] = useState('dashboard');
  const [notifications, setNotifications] = useState([]);

  /**
   * Handle user logout with cleanup
   */
  const handleLogout = async () => {
    try {
      await logout();
      setActiveTab('dashboard');
      addNotification(SUCCESS_MESSAGES.LOGOUT, 'success');
    } catch (error) {
      console.error('Logout error:', error);
      addNotification(ERROR_MESSAGES.GENERIC, 'error');
    }
  };

  /**
   * Handle tab navigation
   * @param {string} tabName - Name of the tab to activate
   */
  const handleTabChange = (tabName) => {
    setActiveTab(tabName);
  };

  /**
   * Add notification to the notification list
   * @param {string} message - Notification message
   * @param {string} type - Notification type (success, error, info, warning)
   */
  const addNotification = (message, type = 'info') => {
    const notification = {
      id: Date.now(),
      message,
      type,
      timestamp: new Date()
    };
    
    setNotifications(prev => [...prev, notification]);
    
    // Auto-remove notification after 5 seconds
    setTimeout(() => {
      removeNotification(notification.id);
    }, 5000);
  };

  /**
   * Remove notification from the notification list
   * @param {number} id - Notification ID
   */
  const removeNotification = (id) => {
    setNotifications(prev => prev.filter(notification => notification.id !== id));
  };

  /**
   * Get user display name
   * @returns {string} - User display name
   */
  const getUserDisplayName = () => {
    if (!user) return 'User';
    return formatName(user.first_name, user.last_name, 'full') || user.email || 'User';
  };

  // Show loading spinner during authentication check
  if (authLoading) {
    return (
      <div className="App">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading AI Job Readiness Platform...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      {/* Application Header */}
      <header className="App-header">
        <div className="header-content">
          <div className="logo-section">
            <h1 className="app-title">AI Job Readiness</h1>
            <p className="app-subtitle">Empowering Your Career Journey</p>
          </div>
          
          {/* Navigation will be added here */}
          <nav className="main-navigation">
            <button 
              className={`nav-button ${activeTab === 'dashboard' ? 'active' : ''}`}
              onClick={() => handleTabChange('dashboard')}
            >
              Dashboard
            </button>
            <button 
              className={`nav-button ${activeTab === 'resume' ? 'active' : ''}`}
              onClick={() => handleTabChange('resume')}
            >
              Resume Analysis
            </button>
            <button 
              className={`nav-button ${activeTab === 'scores' ? 'active' : ''}`}
              onClick={() => handleTabChange('scores')}
            >
              My Scores
            </button>
            <button 
              className={`nav-button ${activeTab === 'recommendations' ? 'active' : ''}`}
              onClick={() => handleTabChange('recommendations')}
            >
              Recommendations
            </button>
          </nav>

          {/* Authentication Section */}
          <div className="auth-section">
            {isAuthenticated ? (
              <div className="user-menu">
                <span className="user-greeting">
                  Welcome, {getUserDisplayName()}!
                </span>
                <button className="logout-button" onClick={handleLogout}>
                  Logout
                </button>
              </div>
            ) : (
              <div className="auth-buttons">
                <button className="login-button">Login</button>
                <button className="register-button">Register</button>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="App-main">
        {!isAuthenticated ? (
          // Landing page for unauthenticated users
          <div className="landing-page">
            <div className="hero-section">
              <h2>Transform Your Job Search with AI</h2>
              <p>
                Get personalized insights, skill assessments, and recommendations 
                to improve your job readiness and land your dream job.
              </p>
              <div className="cta-buttons">
                <button className="cta-primary">Get Started</button>
                <button className="cta-secondary">Learn More</button>
              </div>
            </div>
            
            <div className="features-section">
              <div className="feature-card">
                <h3>Resume Analysis</h3>
                <p>AI-powered resume analysis with detailed feedback and improvement suggestions.</p>
              </div>
              <div className="feature-card">
                <h3>Skill Assessment</h3>
                <p>Comprehensive skill evaluation and gap analysis for your target roles.</p>
              </div>
              <div className="feature-card">
                <h3>Job Matching</h3>
                <p>Smart job matching based on your profile and career goals.</p>
              </div>
            </div>
          </div>
        ) : (
          // Authenticated user dashboard
          <div className="dashboard">
            <div className="dashboard-header">
              <h2>Welcome back, {getUserDisplayName()}!</h2>
              <p>Here's your job readiness overview</p>
            </div>
            
            <div className="dashboard-content">
              <div className="stats-grid">
                <div className="stat-card">
                  <h3>Overall Score</h3>
                  <div className="score-display">85/100</div>
                  <p>Good job readiness</p>
                </div>
                <div className="stat-card">
                  <h3>Resumes Analyzed</h3>
                  <div className="score-display">3</div>
                  <p>Keep improving</p>
                </div>
                <div className="stat-card">
                  <h3>Skills Assessed</h3>
                  <div className="score-display">12</div>
                  <p>Strong foundation</p>
                </div>
              </div>
              
              <div className="quick-actions">
                <h3>Quick Actions</h3>
                <div className="action-buttons">
                  <button className="action-button">Upload Resume</button>
                  <button className="action-button">Take Skill Test</button>
                  <button className="action-button">View Recommendations</button>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Application Footer */}
      <footer className="App-footer">
        <div className="footer-content">
          <p>&copy; 2024 AI Job Readiness Platform. All rights reserved.</p>
          <div className="footer-links">
            <a href="/privacy">Privacy Policy</a>
            <a href="/terms">Terms of Service</a>
            <a href="/contact">Contact Us</a>
          </div>
        </div>
      </footer>

      {/* Notification System */}
      {notifications.length > 0 && (
        <div className="notification-container">
          {notifications.map(notification => (
            <div 
              key={notification.id} 
              className={`notification notification-${notification.type}`}
              onClick={() => removeNotification(notification.id)}
            >
              <span className="notification-message">{notification.message}</span>
              <button className="notification-close">&times;</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;

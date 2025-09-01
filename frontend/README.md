# 🎨 AI Job Readiness Frontend

A modern React frontend application for the AI Job Readiness platform, providing an intuitive user interface for resume analysis, job readiness assessment, and progress tracking.

## 🎯 Overview

The AI Job Readiness Frontend is a modern React application that provides:

- **User Interface**: Clean, responsive design for all user interactions
- **File Upload**: Drag-and-drop resume upload with progress tracking
- **Dashboard**: Comprehensive analytics and progress visualization
- **Real-time Updates**: Live data updates and notifications
- **Mobile Support**: Fully responsive design for all devices

## ✨ Features

### 🔐 User Management
- User registration and login
- Profile management
- Password reset functionality
- Session management

### 📄 Resume Management
- Drag-and-drop file upload
- Multiple file format support (PDF, DOC, DOCX)
- Resume preview and editing
- Version history and management

### 📊 Analytics Dashboard
- Job readiness scoring visualization
- Progress tracking over time
- Skills gap analysis
- Detailed reports and insights

## 🛠️ Tech Stack

- **Framework**: React 18
- **Build Tool**: Create React App
- **Styling**: CSS3 with modern features
- **HTTP Client**: Axios
- **State Management**: React Hooks
- **Routing**: React Router
- **Icons**: React Icons
- **Charts**: Chart.js / Recharts
- **File Upload**: React Dropzone
- **Notifications**: React Toastify

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- Backend API running (see backend README)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/ai-job-readiness.git
   cd ai-job-readiness/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```

4. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 💻 Development

### Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App (one-way operation)

### Development Workflow

1. Create a feature branch
2. Make your changes following existing patterns
3. Test your changes with `npm test`
4. Build and test production build
5. Commit and push your changes

## 🧩 Components

The application is built with reusable components:

- **Common Components**: Button, Input, Modal, Loading
- **Layout Components**: Header, Sidebar, Footer
- **Form Components**: LoginForm, RegisterForm, ProfileForm
- **Page Components**: Dashboard, Login, Register, Profile, Resumes, Analysis

## 🔌 API Integration

The frontend integrates with the backend API using:

- **Axios**: HTTP client for API requests
- **Interceptors**: Automatic token handling and error management
- **Custom Hooks**: useAuth, useApi for state management
- **Context Providers**: AuthContext, ThemeContext

## 🎨 Styling

- **CSS Architecture**: Modular approach with global, component, and theme styles
- **Theme System**: Light/dark theme support with CSS variables
- **Responsive Design**: Mobile-first approach with breakpoints
- **Component Styles**: Scoped styles for individual components

## 🧪 Testing

- **Unit Tests**: Test individual components and functions
- **Integration Tests**: Test component interactions
- **Testing Library**: React Testing Library for component testing
- **Coverage Reports**: Generate test coverage reports

## 🚀 Build & Deployment

### Production Build
```bash
npm run build
```

### Environment Variables
- `REACT_APP_API_URL`: Backend API URL
- `REACT_APP_ENVIRONMENT`: Environment (dev/staging/prod)
- `REACT_APP_VERSION`: App version

### Deployment Options
- Static hosting (Netlify, Vercel)
- Docker deployment
- Nginx deployment

## 📱 Progressive Web App (PWA)

The application includes PWA capabilities:
- Service Worker for offline functionality
- Web App Manifest for app-like experience
- Responsive design for all devices
- Fast loading with optimized performance

## 🤝 Contributing

1. Follow existing code structure and patterns
2. Use functional components with hooks
3. Add tests for new functionality
4. Ensure responsive design
5. Follow accessibility guidelines
6. Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

**Built with ❤️ using React**

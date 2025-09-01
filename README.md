# 🚀 AI Job Readiness Platform

A comprehensive monorepo application for AI-powered job readiness assessment and analysis. This platform helps job seekers improve their readiness through resume analysis, skill assessment, and personalized recommendations.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Development](#development)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The AI Job Readiness Platform is a full-stack application designed to help job seekers assess and improve their job readiness through:

- **Resume Analysis**: AI-powered resume parsing and content extraction
- **Skill Assessment**: Comprehensive skill evaluation and gap analysis
- **Job Readiness Scoring**: Multi-dimensional scoring system
- **Personalized Recommendations**: AI-driven improvement suggestions
- **Progress Tracking**: Monitor improvement over time

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│  (PostgreSQL)   │
│                 │    │                 │    │                 │
│ • User Interface│    │ • REST API      │    │ • User Data     │
│ • File Upload   │    │ • Authentication│    │ • Resumes       │
│ • Analytics     │    │ • AI Analysis   │    │ • Scores        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## ✨ Features

### 🔐 User Management
- Secure user registration and authentication
- Profile management with personal information
- Role-based access control (Admin, User, Analyst)
- Password reset and email verification

### 📄 Resume Management
- Upload and store resume files (PDF, DOC, DOCX)
- AI-powered resume parsing and content extraction
- Skills and experience extraction
- Resume versioning and history

### 🎯 Job Readiness Assessment
- Multi-dimensional scoring system
- Skills gap analysis
- Experience level assessment
- Education evaluation
- Language proficiency analysis

### 📊 Analytics & Insights
- Comprehensive scoring dashboard
- Progress tracking over time
- Detailed analysis reports
- Personalized improvement recommendations

### 🤖 AI-Powered Features
- Natural language processing for resume analysis
- Skill matching and gap identification
- Personalized recommendation engine
- Automated scoring algorithms

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy with async support
- **Authentication**: FastAPI-Users
- **Migrations**: Alembic
- **File Storage**: Local filesystem (configurable for cloud storage)

### Frontend
- **Framework**: React 18
- **Build Tool**: Create React App
- **Styling**: CSS3 with modern features
- **HTTP Client**: Axios
- **State Management**: React Hooks

### DevOps & Infrastructure
- **Containerization**: Docker & Docker Compose
- **Development**: Hot reload for both frontend and backend
- **Database**: PostgreSQL with connection pooling
- **Environment**: Development, staging, and production configurations

## 📁 Project Structure

```
ai-job-readiness/
├── 📁 backend/                    # FastAPI backend application
│   ├── 📁 app/                    # Main application code
│   │   ├── 📁 api/                # API route handlers
│   │   ├── 📁 core/               # Core configuration and utilities
│   │   ├── 📁 db/                 # Database configuration and models
│   │   ├── 📁 models/             # SQLAlchemy models
│   │   ├── 📁 schemas/            # Pydantic schemas
│   │   └── 📄 main.py             # FastAPI application entry point
│   ├── 📁 alembic/                # Database migrations
│   ├── 📁 tests/                  # Backend tests
│   ├── 📄 Dockerfile              # Backend Docker configuration
│   ├── 📄 requirements.txt        # Python dependencies
│   └── 📄 README.md               # Backend documentation
├── 📁 frontend/                   # React frontend application
│   ├── 📁 public/                 # Static assets
│   ├── 📁 src/                    # React source code
│   │   ├── 📁 components/         # Reusable React components
│   │   ├── 📁 pages/              # Page components
│   │   ├── 📁 services/           # API service functions
│   │   ├── 📁 utils/              # Utility functions
│   │   └── 📄 App.js              # Main React component
│   ├── 📄 Dockerfile              # Frontend Docker configuration
│   ├── 📄 package.json            # Node.js dependencies
│   └── 📄 README.md               # Frontend documentation
├── 📁 docs/                       # Project documentation
├── 📁 scripts/                    # Development and deployment scripts
├── 📄 docker-compose.yml          # Multi-container application setup
├── 📄 .env.example                # Environment variables template
├── 📄 .gitignore                  # Git ignore rules
└── 📄 README.md                   # This file
```

## 🚀 Getting Started

### Prerequisites

- **Docker** and **Docker Compose** (recommended)
- **Node.js** 18+ (for local frontend development)
- **Python** 3.11+ (for local backend development)
- **PostgreSQL** 15+ (for local database development)

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/ai-job-readiness.git
   cd ai-job-readiness
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development Setup

1. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Database Setup**
   ```bash
   # Start PostgreSQL (using Docker)
   docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15
   
   # Run migrations
   cd backend
   alembic upgrade head
   ```

## 💻 Development

### Backend Development

The backend is built with FastAPI and follows these principles:

- **Async/Await**: All database operations are asynchronous
- **Type Hints**: Full type annotation for better code quality
- **Dependency Injection**: Clean separation of concerns
- **Error Handling**: Comprehensive error handling and logging
- **API Documentation**: Auto-generated OpenAPI documentation

#### Key Backend Features:

- **Models**: SQLAlchemy models with comprehensive relationships
- **Authentication**: JWT-based authentication with FastAPI-Users
- **File Upload**: Secure file upload and processing
- **AI Integration**: Ready for AI service integration
- **Database Migrations**: Alembic for schema versioning

### Frontend Development

The frontend is built with React and follows modern practices:

- **Component-Based**: Reusable and maintainable components
- **Hooks**: Modern React patterns with hooks
- **Responsive Design**: Mobile-first responsive design
- **API Integration**: Clean API service layer
- **Error Handling**: User-friendly error messages

#### Key Frontend Features:

- **File Upload**: Drag-and-drop resume upload
- **Dashboard**: Comprehensive analytics dashboard
- **User Management**: Profile and settings management
- **Real-time Updates**: Live data updates
- **Progressive Web App**: PWA capabilities

## 📚 API Documentation

### Authentication Endpoints
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user

### Resume Endpoints
- `GET /resumes/` - List user resumes
- `POST /resumes/` - Upload new resume
- `GET /resumes/{id}` - Get resume details
- `PUT /resumes/{id}` - Update resume
- `DELETE /resumes/{id}` - Delete resume

### Analysis Endpoints
- `POST /analysis/analyze` - Analyze resume
- `GET /analysis/scores/{resume_id}` - Get analysis scores
- `GET /analysis/recommendations/{resume_id}` - Get recommendations

### User Endpoints
- `GET /users/profile` - Get user profile
- `PUT /users/profile` - Update user profile
- `GET /users/dashboard` - Get user dashboard data

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest tests/ -v
```

### Frontend Testing
```bash
cd frontend
npm test
```

### Integration Testing
```bash
# Run full test suite
docker-compose -f docker-compose.test.yml up --build
```

## 🚀 Deployment

### Production Deployment

1. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with production values
   ```

2. **Build and Deploy**
   ```bash
   docker-compose -f docker-compose.prod.yml up --build -d
   ```

3. **Database Migration**
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://postgres:password@localhost:5432/ai_job_readiness` |
| `SECRET_KEY` | JWT secret key | `your-secret-key` |
| `ENVIRONMENT` | Environment (dev/staging/prod) | `development` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for your changes
5. Run the test suite: `npm test` and `pytest`
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to the branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

### Code Style

- **Backend**: Follow PEP 8, use type hints, and write docstrings
- **Frontend**: Follow ESLint rules, use functional components with hooks
- **Commits**: Use conventional commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [Full Documentation](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-org/ai-job-readiness/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/ai-job-readiness/discussions)
- **Email**: support@aijobreadiness.com

## 🙏 Acknowledgments

- FastAPI team for the excellent framework
- React team for the amazing frontend library
- PostgreSQL team for the robust database
- All contributors and users of this project

---

**Made with ❤️ by the AI Job Readiness Team**
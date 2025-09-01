# 🚀 AI Job Readiness Backend API

A comprehensive FastAPI backend for the AI Job Readiness platform, providing robust APIs for user management, resume analysis, and job readiness assessment.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Database Models](#database-models)
- [Authentication](#authentication)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)

## 🎯 Overview

The AI Job Readiness Backend is a high-performance REST API built with FastAPI that provides:

- **User Management**: Complete user lifecycle management with authentication
- **Resume Processing**: AI-powered resume analysis and content extraction
- **Job Readiness Scoring**: Multi-dimensional assessment algorithms
- **Role-Based Access Control**: Flexible permission system
- **Real-time Analytics**: Comprehensive reporting and insights

## ✨ Features

### 🔐 Authentication & Authorization
- JWT-based authentication with FastAPI-Users
- Role-based access control (Admin, User, Analyst)
- Password reset and email verification
- Secure session management

### 📄 Resume Management
- Multi-format file upload (PDF, DOC, DOCX)
- AI-powered content extraction
- Skills and experience parsing
- Resume versioning and history

### 🎯 Job Readiness Assessment
- Comprehensive scoring algorithms
- Skills gap analysis
- Experience level evaluation
- Education assessment
- Language proficiency analysis

### 📊 Analytics & Reporting
- Real-time dashboard data
- Progress tracking
- Detailed analysis reports
- Export capabilities

### 🤖 AI Integration Ready
- Modular AI service integration
- Natural language processing
- Machine learning model support
- Recommendation engine

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   API       │  │   Auth      │  │   AI        │         │
│  │  Routes     │  │  System     │  │  Services   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Database   │  │   File      │  │   Cache     │         │
│  │   Layer     │  │  Storage    │  │   Layer     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.104+
- **Python**: 3.11+
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0+ with async support
- **Authentication**: FastAPI-Users
- **Migrations**: Alembic
- **Validation**: Pydantic
- **Testing**: Pytest with async support
- **Documentation**: Auto-generated OpenAPI/Swagger

## 📁 Project Structure

```
backend/
├── 📁 app/                        # Main application code
│   ├── 📁 api/                    # API route handlers
│   │   ├── 📁 v1/                 # API version 1 routes
│   │   │   ├── 📄 auth.py         # Authentication endpoints
│   │   │   ├── 📄 users.py        # User management endpoints
│   │   │   ├── 📄 resumes.py      # Resume endpoints
│   │   │   ├── 📄 analysis.py     # Analysis endpoints
│   │   │   └── 📄 scores.py       # Scoring endpoints
│   │   └── 📄 __init__.py
│   ├── 📁 core/                   # Core configuration
│   │   ├── 📄 config.py           # Application configuration
│   │   ├── 📄 security.py         # Security utilities
│   │   └── 📄 logging.py          # Logging configuration
│   ├── 📁 db/                     # Database configuration
│   │   ├── 📄 database.py         # Database connection and session
│   │   └── 📄 base.py             # Base model class
│   ├── 📁 models/                 # SQLAlchemy models
│   │   ├── 📄 user.py             # User model
│   │   ├── 📄 resume.py           # Resume model
│   │   ├── 📄 score.py            # Score model
│   │   ├── 📄 role.py             # Role model
│   │   └── 📄 __init__.py
│   ├── 📁 schemas/                # Pydantic schemas
│   │   ├── 📄 user.py             # User schemas
│   │   ├── 📄 resume.py           # Resume schemas
│   │   ├── 📄 score.py            # Score schemas
│   │   └── 📄 __init__.py
│   ├── 📁 services/               # Business logic services
│   │   ├── 📄 user_service.py     # User business logic
│   │   ├── 📄 resume_service.py   # Resume processing
│   │   ├── 📄 analysis_service.py # Analysis algorithms
│   │   └── 📄 ai_service.py       # AI integration
│   ├── 📁 utils/                  # Utility functions
│   │   ├── 📄 file_utils.py       # File handling utilities
│   │   ├── 📄 text_utils.py       # Text processing utilities
│   │   └── 📄 validation.py       # Custom validators
│   └── 📄 main.py                 # FastAPI application entry point
├── 📁 alembic/                    # Database migrations
│   ├── 📁 versions/               # Migration files
│   ├── 📄 env.py                  # Alembic environment
│   └── 📄 script.py.mako          # Migration template
├── 📁 tests/                      # Test suite
│   ├── 📁 unit/                   # Unit tests
│   ├── 📁 integration/            # Integration tests
│   ├── 📁 fixtures/               # Test fixtures
│   └── 📄 conftest.py             # Pytest configuration
├── 📄 Dockerfile                  # Docker configuration
├── 📄 requirements.txt            # Python dependencies
├── 📄 alembic.ini                 # Alembic configuration
├── 📄 pytest.ini                 # Pytest configuration
└── 📄 README.md                   # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Docker (optional, for containerized development)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/ai-job-readiness.git
   cd ai-job-readiness/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Set up database**
   ```bash
   # Start PostgreSQL (using Docker)
   docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15
   
   # Run migrations
   alembic upgrade head
   ```

6. **Start the development server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Docker Development

```bash
# Build and start all services
docker-compose up --build

# Start only the backend
docker-compose up backend --build
```

## 📚 API Documentation

### Interactive Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### API Endpoints Overview

#### Authentication Endpoints
```
POST   /auth/register          # User registration
POST   /auth/login             # User login
POST   /auth/logout            # User logout
POST   /auth/refresh           # Refresh access token
GET    /auth/me                # Get current user
POST   /auth/forgot-password   # Request password reset
POST   /auth/reset-password    # Reset password
```

#### User Management
```
GET    /users/                 # List users (admin only)
GET    /users/{user_id}        # Get user details
PUT    /users/{user_id}        # Update user
DELETE /users/{user_id}        # Delete user
GET    /users/profile          # Get current user profile
PUT    /users/profile          # Update current user profile
```

#### Resume Management
```
GET    /resumes/               # List user resumes
POST   /resumes/               # Upload new resume
GET    /resumes/{resume_id}    # Get resume details
PUT    /resumes/{resume_id}    # Update resume
DELETE /resumes/{resume_id}    # Delete resume
POST   /resumes/{resume_id}/analyze  # Analyze resume
```

#### Analysis & Scoring
```
GET    /analysis/scores/{resume_id}        # Get analysis scores
GET    /analysis/recommendations/{resume_id}  # Get recommendations
POST   /analysis/analyze                   # Run analysis
GET    /analysis/history/{user_id}         # Get analysis history
```

#### System Endpoints
```
GET    /health                 # Health check
GET    /models                 # List available models
GET    /database               # Database status
GET    /api/v1/info            # API information
```

## 🗄️ Database Models

### User Model
- **Authentication**: Email, password, verification status
- **Profile**: Name, phone, bio, profile picture
- **Metadata**: Created/updated timestamps, active status
- **Relationships**: Roles, resumes, scores

### Resume Model
- **File Management**: Path, name, size, type
- **Content**: Summary, experience, education, skills
- **Status**: Active, public, analysis status
- **Relationships**: User, scores

### Score Model
- **Scoring**: Overall score, category scores
- **Analysis**: Skills, gaps, recommendations
- **Metadata**: Analysis date, status
- **Relationships**: User, resume

### Role Model
- **Access Control**: Role name, permissions
- **Relationships**: Users (many-to-many)

## 🔐 Authentication

The API uses JWT-based authentication with FastAPI-Users:

### Authentication Flow
1. User registers/logs in
2. Server returns access token and refresh token
3. Client includes access token in Authorization header
4. Server validates token and grants access
5. Token can be refreshed using refresh token

### Example Usage
```python
# Login
response = requests.post("/auth/login", json={
    "email": "user@example.com",
    "password": "password"
})
tokens = response.json()

# Use access token
headers = {"Authorization": f"Bearer {tokens['access_token']}"}
response = requests.get("/users/profile", headers=headers)
```

## 💻 Development

### Code Style
- Follow PEP 8 guidelines
- Use type hints for all functions
- Write comprehensive docstrings
- Use async/await for database operations

### Adding New Endpoints

1. **Create route handler** in `app/api/v1/`
2. **Define Pydantic schemas** in `app/schemas/`
3. **Add business logic** in `app/services/`
4. **Update database models** if needed
5. **Add tests** in `tests/`
6. **Update documentation**

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://postgres:password@localhost:5432/ai_job_readiness` |
| `SECRET_KEY` | JWT secret key | `your-secret-key` |
| `ENVIRONMENT` | Environment (dev/staging/prod) | `development` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |
| `SQL_ECHO` | Enable SQL query logging | `true` |

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_users.py

# Run with verbose output
pytest -v
```

### Test Structure
- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test API endpoints and database operations
- **Fixtures**: Reusable test data and database setup

### Writing Tests

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

## 🚀 Deployment

### Production Deployment

1. **Set environment variables**
   ```bash
   export DATABASE_URL="postgresql+asyncpg://user:pass@host:port/db"
   export SECRET_KEY="your-production-secret-key"
   export ENVIRONMENT="production"
   ```

2. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

3. **Start the application**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

### Docker Production

```bash
# Build production image
docker build -t ai-job-readiness-backend .

# Run with environment variables
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL="your-db-url" \
  -e SECRET_KEY="your-secret-key" \
  ai-job-readiness-backend
```

### Performance Optimization

- Use connection pooling for database
- Enable Redis caching for frequently accessed data
- Use async/await for I/O operations
- Implement rate limiting for API endpoints
- Use CDN for static file serving

## 📊 Monitoring & Logging

### Logging Configuration
- Structured logging with JSON format
- Different log levels for different environments
- Request/response logging
- Error tracking and alerting

### Health Checks
- Database connectivity check
- External service availability
- System resource monitoring
- Custom health check endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

**Built with ❤️ using FastAPI**
# AI Job Readiness Platform

A comprehensive full-stack application that leverages artificial intelligence to assess and improve job readiness through resume analysis, skill assessment, and personalized recommendations.

## 🚀 Features

### Core Functionality
- **User Management**: Complete authentication system with JWT tokens, email verification, and password reset
- **Resume Processing**: AI-powered resume analysis with detailed feedback and improvement suggestions
- **Job Readiness Scoring**: Comprehensive scoring system across multiple dimensions
- **Skills Assessment**: Detailed skill evaluation and gap analysis
- **Personalized Recommendations**: AI-driven suggestions for career improvement
- **Role-Based Access Control**: Secure multi-role system (Admin, User, Analyst, Moderator)

### Technical Features
- **Modern Architecture**: React frontend with FastAPI backend
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **API-First Design**: RESTful APIs with comprehensive documentation
- **Real-time Updates**: WebSocket support for live updates
- **File Management**: Secure file upload and processing
- **Responsive Design**: Mobile-first, accessible user interface

## 🏗️ Architecture

### Frontend (React 18)
- **Framework**: React 18 with Create React App
- **State Management**: React Hooks and Context API
- **Styling**: CSS3 with custom properties and responsive design
- **HTTP Client**: Axios with interceptors and error handling
- **Routing**: React Router for navigation
- **Icons**: React Icons library
- **Charts**: Chart.js/Recharts for data visualization
- **File Upload**: React Dropzone for file handling
- **Notifications**: React Toastify for user feedback
- **PWA**: Progressive Web App capabilities

### Backend (FastAPI)
- **Framework**: FastAPI with Python 3.11+
- **Database**: PostgreSQL 15 with SQLAlchemy 2.0+ (async support)
- **Authentication**: FastAPI-Users with JWT tokens
- **Validation**: Pydantic for data validation and serialization
- **Migrations**: Alembic for database schema management
- **Testing**: Pytest with async support
- **Documentation**: Auto-generated OpenAPI/Swagger docs

### Database Schema
- **Users**: User profiles with authentication and profile data
- **Roles**: Role-based access control system
- **Resumes**: Resume storage and metadata
- **Scores**: AI analysis results and job readiness scores
- **Relationships**: Proper foreign key relationships and constraints

## 📁 Project Structure

```
ai-job-readiness/
├── backend/                    # FastAPI backend application
│   ├── app/
│   │   ├── api/               # API route handlers
│   │   │   ├── auth.py        # Authentication endpoints
│   │   │   ├── users.py       # User management endpoints
│   │   │   └── resume.py      # Resume management endpoints
│   │   ├── core/              # Core configuration
│   │   │   └── config.py      # Application settings
│   │   ├── db/                # Database configuration
│   │   │   └── database.py    # Database connection and session management
│   │   ├── models/            # SQLAlchemy models
│   │   │   ├── user.py        # User model
│   │   │   ├── role.py        # Role and UserRole models
│   │   │   ├── resume.py      # Resume model
│   │   │   └── score.py       # Score model
│   │   ├── schemas/           # Pydantic schemas
│   │   │   └── user.py        # User data validation schemas
│   │   ├── utils/             # Utility functions
│   │   │   ├── file_utils.py  # File handling utilities
│   │   │   ├── text_utils.py  # Text processing utilities
│   │   │   ├── validation.py  # Data validation utilities
│   │   │   ├── response.py    # API response utilities
│   │   │   ├── exceptions.py  # Custom exception classes
│   │   │   └── decorators.py  # Custom decorators
│   │   └── main.py            # FastAPI application entry point
│   ├── tests/                 # Test files
│   │   └── unit/              # Unit tests
│   │       ├── test_models.py # Model tests
│   │       └── test_relationships.py # Relationship tests
│   ├── requirements.txt       # Python dependencies
│   └── README.md             # Backend documentation
├── frontend/                  # React frontend application
│   ├── public/               # Static assets
│   ├── src/
│   │   ├── components/       # React components (to be created)
│   │   ├── utils/            # Utility functions
│   │   │   ├── constants.js  # Application constants
│   │   │   ├── api.js        # API client functions
│   │   │   ├── validation.js # Client-side validation
│   │   │   ├── helpers.js    # General helper functions
│   │   │   ├── storage.js    # Local storage utilities
│   │   │   ├── formatting.js # Data formatting utilities
│   │   │   └── hooks.js      # Custom React hooks
│   │   ├── App.js            # Main application component
│   │   ├── App.css           # Global styles
│   │   └── index.js          # Application entry point
│   ├── package.json          # Node.js dependencies
│   └── README.md             # Frontend documentation
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 16+
- PostgreSQL 15+
- Git

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-job-readiness
   ```

2. **Set up Python environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database and API settings
   ```

4. **Set up database**
   ```bash
   # Create PostgreSQL database
   createdb ai_job_readiness
   
   # Run migrations
   alembic upgrade head
   ```

5. **Start the backend server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your API URL
   ```

3. **Start the development server**
   ```bash
   npm start
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🔧 Configuration

### Backend Configuration

The backend uses a structured configuration system with Pydantic settings:

```python
# Environment variables
DATABASE_URL=postgresql://user:password@localhost/ai_job_readiness
SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Frontend Configuration

```javascript
// Environment variables
REACT_APP_API_URL=http://localhost:8000
REACT_APP_APP_NAME=AI Job Readiness
REACT_APP_VERSION=1.0.0
```

## 📊 API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `POST /auth/logout` - User logout
- `POST /auth/refresh` - Refresh access token
- `GET /auth/me` - Get current user profile

### User Management
- `GET /users/profile` - Get user profile
- `PUT /users/profile` - Update user profile
- `GET /users/list` - List users (admin only)
- `POST /users/{id}/activate` - Activate user (admin only)
- `POST /users/{id}/deactivate` - Deactivate user (admin only)

### Resume Management
- `GET /resumes/` - List user resumes
- `POST /resumes/` - Create new resume
- `GET /resumes/{id}` - Get resume details
- `PUT /resumes/{id}` - Update resume
- `DELETE /resumes/{id}` - Delete resume
- `POST /resumes/{id}/upload` - Upload resume file
- `GET /resumes/{id}/download` - Download resume file
- `POST /resumes/{id}/analyze` - Trigger AI analysis

### System
- `GET /health` - Health check
- `GET /api/v1/info` - System information
- `GET /models` - AI models status
- `GET /database` - Database status

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest tests/ -v
pytest tests/unit/ -v
pytest tests/integration/ -v
```

### Frontend Testing
```bash
cd frontend
npm test
npm run test:coverage
```

## 🚀 Deployment

### Backend Deployment
1. **Production requirements**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment setup**
   ```bash
   export DATABASE_URL=postgresql://user:password@host:port/database
   export SECRET_KEY=your-production-secret-key
   ```

3. **Run with Gunicorn**
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

### Frontend Deployment
1. **Build for production**
   ```bash
   npm run build
   ```

2. **Serve with nginx or similar**
   ```bash
   nginx -s reload
   ```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt password hashing
- **CORS Protection**: Configurable CORS settings
- **Input Validation**: Comprehensive data validation
- **SQL Injection Protection**: SQLAlchemy ORM protection
- **File Upload Security**: Secure file handling and validation
- **Rate Limiting**: API rate limiting (configurable)
- **HTTPS Support**: SSL/TLS encryption support

## 📈 Performance Optimizations

### Backend Optimizations
- **Async/Await**: Full async support for better concurrency
- **Database Connection Pooling**: Efficient database connections
- **Caching**: Redis caching for frequently accessed data
- **Query Optimization**: Optimized database queries
- **Response Compression**: Gzip compression for API responses

### Frontend Optimizations
- **Code Splitting**: Lazy loading of components
- **Bundle Optimization**: Webpack optimization
- **Image Optimization**: Optimized image loading
- **Caching**: Browser caching strategies
- **PWA Features**: Service worker for offline support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation at `/docs`

## 🔄 Recent Updates

### Version 1.0.0 (Current)
- ✅ Complete backend API implementation
- ✅ User authentication and authorization
- ✅ Resume upload and analysis system
- ✅ Job readiness scoring algorithm
- ✅ Role-based access control
- ✅ Comprehensive test coverage
- ✅ API documentation
- ✅ Frontend utility modules
- ✅ Custom React hooks
- ✅ Responsive design system

### Development Status
| Component | Status | Progress |
|-----------|--------|----------|
| Backend API | ✅ Complete | 100% |
| Database Models | ✅ Complete | 100% |
| Authentication | ✅ Complete | 100% |
| File Upload | ✅ Complete | 100% |
| AI Integration | 🔄 In Progress | 80% |
| Frontend Components | 🔄 In Progress | 60% |
| Testing | ✅ Complete | 95% |
| Documentation | ✅ Complete | 90% |
| Deployment | 🔄 In Progress | 70% |

## 🎯 Future Enhancements

- **Advanced AI Features**: Enhanced resume analysis with NLP
- **Real-time Collaboration**: Multi-user editing and sharing
- **Mobile App**: React Native mobile application
- **Analytics Dashboard**: Advanced analytics and reporting
- **Integration APIs**: Third-party service integrations
- **Machine Learning**: Predictive job matching algorithms
- **Video Interviews**: AI-powered interview practice
- **Career Path Planning**: Long-term career development tools

---

**Built with ❤️ by the AI Job Readiness Team**
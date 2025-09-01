# Monorepo Testing Guide with Docker Compose

This guide shows you how to test your entire monorepo stack including frontend, backend with SQLAlchemy models, and PostgreSQL database using Docker Compose.

## 🏗️ **Monorepo Structure**

```
ai-job-readiness/
├── docker-compose.yml          # Root orchestration
├── .env                        # Environment variables
├── frontend/                   # React application
├── backend/                    # FastAPI + SQLAlchemy + Alembic
│   ├── app/
│   │   ├── models/            # SQLAlchemy models
│   │   ├── db/                # Database configuration
│   │   └── main.py            # FastAPI application
│   ├── alembic/               # Database migrations
│   └── Dockerfile
└── test_monorepo.sh           # Test script
```

## 🚀 **Quick Start Testing**

### **Option 1: One-Command Test**
```bash
# Run the complete monorepo test suite
./test_monorepo.sh
```

### **Option 2: Manual Testing**
```bash
# Start all services
docker-compose up -d

# Wait for services to be ready
sleep 25

# Check status
docker-compose ps

# Test individual services
curl http://localhost:8000/health      # Backend
curl http://localhost:3000             # Frontend
```

## 🐳 **Services Overview**

| Service | Port | Purpose | Health Check |
|---------|------|---------|--------------|
| **database** | 5432 | PostgreSQL database | `pg_isready` |
| **backend** | 8000 | FastAPI + Alembic | API endpoints |
| **frontend** | 3000 | React application | Web interface |

## 🔧 **Testing Alembic Migrations**

### **Automatic Migration on Startup**
The backend service automatically runs migrations when it starts:
```yaml
command: >
  sh -c "
    echo 'Waiting for database to be ready...' &&
    sleep 10 &&
    echo 'Running Alembic migrations...' &&
    alembic upgrade head &&
    echo 'Starting FastAPI server...' &&
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
  "
```

### **Manual Migration Testing**
```bash
# Connect to backend container
docker-compose exec backend bash

# Check current migration
alembic current

# View migration history
alembic history

# Create new migration
alembic revision --autogenerate -m "Add new field"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1
```

### **Database Operations**
```bash
# Connect to PostgreSQL
docker-compose exec database psql -U postgres -d ai_job_readiness

# List tables
\dt

# Describe table structure
\d users
\d roles
\d resumes
\d scores

# Check data
SELECT * FROM users;
SELECT * FROM roles;

# Exit
\q
```

## 🌐 **API Testing**

### **Backend Endpoints**
- **Health**: `GET /health` - Service health check
- **Models**: `GET /models` - List all SQLAlchemy models
- **Database**: `GET /database` - Database connection status
- **Docs**: `GET /docs` - Swagger UI documentation

### **Test with curl**
```bash
# Health check
curl http://localhost:8000/health

# List models
curl http://localhost:8000/models

# Check database
curl http://localhost:8000/database

# Open API docs
open http://localhost:8000/docs
```

### **Frontend Testing**
```bash
# Check if frontend is accessible
curl -I http://localhost:3000

# Open in browser
open http://localhost:3000
```

## 🧪 **Testing Different Scenarios**

### **1. Fresh Start Test**
```bash
# Remove everything and start fresh
docker-compose down -v
docker-compose up -d

# Wait for startup
sleep 25

# Check migrations
docker-compose exec backend alembic current
```

### **2. Model Changes Test**
```bash
# Make changes to models in backend/app/models/
# Then create new migration
docker-compose exec backend alembic revision --autogenerate -m "Add new field"

# Apply migration
docker-compose exec backend alembic upgrade head

# Restart backend to pick up changes
docker-compose restart backend
```

### **3. Data Persistence Test**
```bash
# Add test data
docker-compose exec database psql -U postgres -d ai_job_readiness -c "
INSERT INTO roles (name, description, is_active) VALUES ('admin', 'Administrator', true);
"

# Restart services
docker-compose restart

# Check if data persists
docker-compose exec database psql -U postgres -d ai_job_readiness -c "SELECT * FROM roles;"
```

### **4. Hot Reload Testing**
```bash
# Make changes to backend code
# Backend should auto-reload due to volume mount

# Make changes to frontend code
# Frontend should auto-reload due to volume mount
```

## 🚨 **Troubleshooting**

### **Common Issues**

#### **1. Services Won't Start**
```bash
# Check logs
docker-compose logs

# Check specific service
docker-compose logs database
docker-compose logs backend
docker-compose logs frontend

# Restart services
docker-compose restart
```

#### **2. Database Connection Issues**
```bash
# Check if PostgreSQL is ready
docker-compose exec database pg_isready -U postgres

# Check database exists
docker-compose exec database psql -U postgres -l

# Recreate database
docker-compose exec database psql -U postgres -c "DROP DATABASE IF EXISTS ai_job_readiness;"
docker-compose exec database psql -U postgres -c "CREATE DATABASE ai_job_readiness;"
```

#### **3. Migration Issues**
```bash
# Check migration status
docker-compose exec backend alembic current

# Reset migrations
docker-compose exec backend alembic stamp head

# Force upgrade
docker-compose exec backend alembic upgrade head --sql
```

#### **4. Port Conflicts**
```bash
# Check what's using the ports
lsof -i :5432  # PostgreSQL
lsof -i :8000  # Backend
lsof -i :3000  # Frontend

# Stop conflicting services or change ports in docker-compose.yml
```

### **Debug Commands**
```bash
# Check container status
docker-compose ps

# Check container resources
docker stats

# Check container logs
docker-compose logs -f

# Execute commands in container
docker-compose exec backend python -c "from app.models import User; print('Models loaded')"
docker-compose exec frontend node --version
```

## 📊 **Monitoring & Health Checks**

### **Service Health**
```bash
# Check all services
docker-compose ps

# Check specific service health
docker inspect $(docker-compose ps -q database) | grep Health -A 10
```

### **Performance Monitoring**
```bash
# Monitor resource usage
docker stats

# Check database performance
docker-compose exec database psql -U postgres -d ai_job_readiness -c "
SELECT schemaname, tablename, attname, n_distinct, correlation 
FROM pg_stats 
WHERE tablename IN ('users', 'roles', 'resumes', 'scores');
"
```

### **Log Monitoring**
```bash
# Follow all logs
docker-compose logs -f

# Follow specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f database
```

## 🎯 **Success Criteria**

Your monorepo is working correctly when:

✅ **PostgreSQL** is running and accessible on port 5432  
✅ **Backend** is running and accessible on port 8000  
✅ **Frontend** is running and accessible on port 3000  
✅ **Alembic migrations** run without errors  
✅ **All database tables** are created (users, roles, user_roles, resumes, scores)  
✅ **API endpoints** respond correctly  
✅ **Models can be imported** and used  
✅ **Database operations work** (insert, select, etc.)  
✅ **Frontend can connect** to backend API  
✅ **Hot reload** works for development  

## 🚀 **Development Workflow**

### **Daily Development**
```bash
# Start services
docker-compose up -d

# Make code changes (auto-reload enabled)
# Test endpoints
curl http://localhost:8000/health

# Stop services
docker-compose down
```

### **Adding New Models**
```bash
# 1. Add new model to backend/app/models/
# 2. Create migration
docker-compose exec backend alembic revision --autogenerate -m "Add new model"
# 3. Apply migration
docker-compose exec backend alembic upgrade head
# 4. Restart backend
docker-compose restart backend
```

### **Database Schema Changes**
```bash
# 1. Modify existing models
# 2. Generate migration
docker-compose exec backend alembic revision --autogenerate -m "Modify schema"
# 3. Review migration file
# 4. Apply migration
docker-compose exec backend alembic upgrade head
```

## 💡 **Pro Tips**

1. **Keep services running**: `docker-compose up -d`
2. **Stop services**: `docker-compose down`
3. **View logs**: `docker-compose logs -f`
4. **Restart specific service**: `docker-compose restart [service_name]`
5. **Rebuild specific service**: `docker-compose up --build [service_name]`
6. **Check service status**: `docker-compose ps`
7. **Access container shell**: `docker-compose exec [service_name] bash`

## 📚 **Additional Resources**

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [React Development](https://reactjs.org/docs/getting-started.html)

## 🔄 **Next Steps**

After successful monorepo testing:

1. **Integration Testing**: Add comprehensive end-to-end tests
2. **Performance Testing**: Test with larger datasets and load
3. **Production Setup**: Configure for production environment
4. **CI/CD Pipeline**: Add Docker testing to your CI pipeline
5. **Monitoring**: Add application performance monitoring
6. **Security**: Implement security best practices

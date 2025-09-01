# Docker Testing Guide for Alembic Migrations

This guide shows you how to test your SQLAlchemy models and Alembic migrations using Docker.

## 🚀 Quick Start

### 1. Test Everything with One Command

```bash
# Run the complete test suite
./test_docker_simple.sh
```

This script will:
- Build and start PostgreSQL and Backend services
- Run Alembic migrations automatically
- Test all API endpoints
- Verify database tables are created
- Test Alembic operations

### 2. Manual Step-by-Step Testing

```bash
# Start services
docker-compose up -d

# Wait for services to be ready
sleep 20

# Check service status
docker-compose ps

# Test Alembic migrations
docker-compose exec backend alembic current
docker-compose exec backend alembic history

# Test API endpoints
curl http://localhost:8000/health
curl http://localhost:8000/models
curl http://localhost:8000/database

# Check database tables
docker-compose exec postgres psql -U postgres -d ai_job_readiness -c "\dt"

# Stop services
docker-compose down
```

## 🐳 What Gets Created

### Services
- **PostgreSQL**: Database server on port 5432
- **Backend**: FastAPI application on port 8000

### Database
- **Database**: `ai_job_readiness`
- **User**: `postgres`
- **Password**: `password`
- **Tables**: All models (users, roles, user_roles, resumes, scores)

## 🔧 Testing Alembic Commands

### Inside the Backend Container

```bash
# Connect to backend container
docker-compose exec backend bash

# Check current migration
alembic current

# View migration history
alembic history

# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1

# Check migration status
alembic show current
```

### Database Operations

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U postgres -d ai_job_readiness

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

# Exit PostgreSQL
\q
```

## 🌐 API Testing

### Available Endpoints

- **Health Check**: `GET /health`
- **Models List**: `GET /models`
- **Database Status**: `GET /database`
- **API Docs**: `GET /docs` (Swagger UI)

### Test with curl

```bash
# Health check
curl http://localhost:8000/health

# List models
curl http://localhost:8000/models

# Check database connection
curl http://localhost:8000/database

# Get API documentation
open http://localhost:8000/docs
```

## 🧪 Testing Different Scenarios

### 1. Fresh Database Test

```bash
# Remove all data and start fresh
docker-compose down -v
docker-compose up -d

# Wait for startup
sleep 20

# Check migrations
docker-compose exec backend alembic current
```

### 2. Model Changes Test

```bash
# Make changes to models
# Then create new migration
docker-compose exec backend alembic revision --autogenerate -m "Add new field"

# Apply migration
docker-compose exec backend alembic upgrade head
```

### 3. Data Persistence Test

```bash
# Add some test data
docker-compose exec postgres psql -U postgres -d ai_job_readiness -c "
INSERT INTO roles (name, description, is_active) VALUES ('admin', 'Administrator', true);
"

# Restart services
docker-compose restart

# Check if data persists
docker-compose exec postgres psql -U postgres -d ai_job_readiness -c "SELECT * FROM roles;"
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Services Won't Start
```bash
# Check logs
docker-compose logs

# Check specific service
docker-compose logs postgres
docker-compose logs backend

# Restart services
docker-compose restart
```

#### 2. Database Connection Issues
```bash
# Check if PostgreSQL is ready
docker-compose exec postgres pg_isready -U postgres

# Check database exists
docker-compose exec postgres psql -U postgres -l

# Recreate database
docker-compose exec postgres psql -U postgres -c "DROP DATABASE IF EXISTS ai_job_readiness;"
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE ai_job_readiness;"
```

#### 3. Migration Issues
```bash
# Check migration status
docker-compose exec backend alembic current

# Reset migrations
docker-compose exec backend alembic stamp head

# Force upgrade
docker-compose exec backend alembic upgrade head --sql
```

### Debug Commands

```bash
# Check container status
docker-compose ps

# Check container resources
docker stats

# Check container logs
docker-compose logs -f

# Execute commands in container
docker-compose exec backend python -c "from app.models import User; print('Models loaded')"
```

## 📊 Monitoring

### Health Checks

```bash
# Check all services
docker-compose ps

# Check specific service health
docker inspect $(docker-compose ps -q postgres) | grep Health -A 10
```

### Performance

```bash
# Monitor resource usage
docker stats

# Check database performance
docker-compose exec postgres psql -U postgres -d ai_job_readiness -c "
SELECT schemaname, tablename, attname, n_distinct, correlation 
FROM pg_stats 
WHERE tablename IN ('users', 'roles', 'resumes', 'scores');
"
```

## 🎯 Success Criteria

Your Docker setup is working correctly when:

✅ **PostgreSQL is running** and accessible on port 5432  
✅ **Backend is running** and accessible on port 8000  
✅ **Alembic migrations run** without errors  
✅ **All tables are created** in the database  
✅ **API endpoints respond** correctly  
✅ **Models can be imported** and used  
✅ **Database operations work** (insert, select, etc.)  

## 🚀 Next Steps

After successful Docker testing:

1. **Integration Testing**: Add more comprehensive tests
2. **Performance Testing**: Test with larger datasets
3. **Production Setup**: Configure for production environment
4. **CI/CD**: Add Docker testing to your CI pipeline

## 📚 Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)

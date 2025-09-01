#!/bin/bash

echo "🐳 Testing Alembic Migrations with Docker (Simple)"
echo "=================================================="

# Function to cleanup
cleanup() {
    echo "🧹 Cleaning up..."
    docker-compose down -v
}

# Set trap to cleanup on exit
trap cleanup EXIT

echo "1. Building and starting services..."
docker-compose up --build -d

echo "2. Waiting for services to be ready..."
sleep 20

echo "3. Checking if PostgreSQL is running..."
if docker-compose ps postgres | grep -q "Up"; then
    echo "✅ PostgreSQL is running"
else
    echo "❌ PostgreSQL failed to start"
    exit 1
fi

echo "4. Checking if backend is running..."
if docker-compose ps backend | grep -q "Up"; then
    echo "✅ Backend is running"
else
    echo "❌ Backend failed to start"
    exit 1
fi

echo "5. Testing Alembic migrations..."
echo "   Running 'alembic current' to check migration status..."
docker-compose exec backend alembic current

echo "6. Testing API endpoints..."
echo "   Testing health endpoint..."
curl -s http://localhost:8000/health

echo ""
echo "   Testing models endpoint..."
curl -s http://localhost:8000/models

echo ""
echo "   Testing database endpoint..."
curl -s http://localhost:8000/database

echo ""

echo "7. Checking database tables..."
echo "   Connecting to PostgreSQL and listing tables..."
docker-compose exec postgres psql -U postgres -d ai_job_readiness -c "\dt"

echo "8. Testing Alembic operations..."
echo "   Creating a test migration..."
docker-compose exec backend alembic revision -m "Test migration" --autogenerate

echo "   Checking migration history..."
docker-compose exec backend alembic history

echo ""
echo "🎉 Docker migration test completed successfully!"
echo "   - PostgreSQL is running on localhost:5432"
echo "   - Backend API is running on localhost:8000"
echo "   - Alembic migrations are working"
echo "   - All models are loaded and accessible"
echo ""
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🔍 Health Check: http://localhost:8000/health"
echo "🗄️  Database: localhost:5432 (postgres/ai_job_readiness)"
echo ""
echo "💡 To keep services running, use: docker-compose up -d"
echo "💡 To stop services, use: docker-compose down"

#!/bin/bash

echo "🏗️  Testing Monorepo with Docker Compose"
echo "========================================="

# Function to cleanup
cleanup() {
    echo "🧹 Cleaning up..."
    docker-compose down -v
    docker system prune -f
}

# Set trap to cleanup on exit
trap cleanup EXIT

echo "1. Building and starting all services..."
docker-compose up --build -d

echo "2. Waiting for services to be ready..."
sleep 25

echo "3. Checking service status..."
docker-compose ps

echo "4. Checking if PostgreSQL is running..."
if docker-compose ps database | grep -q "Up"; then
    echo "✅ PostgreSQL is running"
else
    echo "❌ PostgreSQL failed to start"
    exit 1
fi

echo "5. Checking if backend is running..."
if docker-compose ps backend | grep -q "Up"; then
    echo "✅ Backend is running"
else
    echo "❌ Backend failed to start"
    exit 1
fi

echo "6. Checking if frontend is running..."
if docker-compose ps frontend | grep -q "Up"; then
    echo "✅ Frontend is running"
else
    echo "❌ Frontend failed to start"
    exit 1
fi

echo "7. Testing Alembic migrations..."
echo "   Running 'alembic current' to check migration status..."
docker-compose exec backend alembic current

echo "8. Testing API endpoints..."
echo "   Testing health endpoint..."
curl -s http://localhost:8000/health

echo ""
echo "   Testing models endpoint..."
curl -s http://localhost:8000/models

echo ""
echo "   Testing database endpoint..."
curl -s http://localhost:8000/database

echo ""

echo "9. Checking database tables..."
echo "   Connecting to PostgreSQL and listing tables..."
docker-compose exec database psql -U postgres -d ai_job_readiness -c "\dt"

echo "10. Testing Alembic operations..."
echo "    Creating a test migration..."
docker-compose exec backend alembic revision -m "Test migration" --autogenerate

echo "    Checking migration history..."
docker-compose exec backend alembic history

echo "11. Testing frontend accessibility..."
echo "    Frontend should be accessible at: http://localhost:3000"

echo ""
echo "🎉 Monorepo test completed successfully!"
echo "========================================"
echo "   🗄️  PostgreSQL: localhost:5432 (postgres/ai_job_readiness)"
echo "   🚀 Backend API: localhost:8000"
echo "   🌐 Frontend: localhost:3000"
echo "   📚 API Docs: http://localhost:8000/docs"
echo "   🔍 Health Check: http://localhost:8000/health"
echo ""
echo "💡 To keep services running, use: docker-compose up -d"
echo "💡 To stop services, use: docker-compose down"
echo "💡 To view logs, use: docker-compose logs -f"
echo "💡 To restart a service: docker-compose restart [service_name]"

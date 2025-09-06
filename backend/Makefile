# Makefile for Role System Testing
# This Makefile provides convenient commands for testing the Role and User models

.PHONY: help install test test-python test-api seed-data clean start-server check-deps

# Default target
help:
	@echo "Role System Testing Makefile"
	@echo "============================"
	@echo ""
	@echo "Available commands:"
	@echo "  install      - Install dependencies"
	@echo "  check-deps   - Check if dependencies are installed"
	@echo "  start-server - Start the FastAPI server"
	@echo "  seed-data    - Seed database with test data"
	@echo "  test         - Run all tests (Python + API)"
	@echo "  test-python  - Run Python comprehensive tests"
	@echo "  test-api     - Run API endpoint tests"
	@echo "  clean        - Clean up test data and temporary files"
	@echo "  help         - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make install && make seed-data && make test"
	@echo "  make start-server  # In one terminal"
	@echo "  make test-api      # In another terminal"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

# Check if dependencies are installed
check-deps:
	@echo "🔍 Checking dependencies..."
	@python -c "import fastapi, sqlalchemy, alembic, pydantic" || (echo "❌ Missing dependencies. Run 'make install'" && exit 1)
	@echo "✅ All dependencies are installed"

# Start the FastAPI server
start-server:
	@echo "🚀 Starting FastAPI server..."
	@echo "Server will be available at: http://localhost:8000"
	@echo "API docs: http://localhost:8000/docs"
	@echo "Press Ctrl+C to stop the server"
	python -m uvicorn app.main:app --reload

# Seed database with test data
seed-data:
	@echo "🌱 Seeding database with test data..."
	python seed_test_data.py
	@echo "✅ Database seeded successfully"

# Run all tests
test: check-deps
	@echo "🧪 Running all tests..."
	@echo "======================"
	@echo ""
	@echo "1. Running Python comprehensive tests..."
	python test_role_system.py
	@echo ""
	@echo "2. Running API endpoint tests..."
	@echo "   (Make sure server is running: make start-server)"
	./test_api.sh
	@echo ""
	@echo "✅ All tests completed!"

# Run Python comprehensive tests only
test-python: check-deps
	@echo "🐍 Running Python comprehensive tests..."
	python test_role_system.py
	@echo "✅ Python tests completed!"

# Run API endpoint tests only
test-api:
	@echo "🌐 Running API endpoint tests..."
	@echo "Make sure the server is running (make start-server)"
	./test_api.sh
	@echo "✅ API tests completed!"

# Clean up test data and temporary files
clean:
	@echo "🧹 Cleaning up..."
	@echo "This will remove test data from the database."
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ]
	@echo "Cleaning up test data..."
	@echo "⚠️  Note: This is a placeholder. Implement cleanup logic as needed."
	@echo "✅ Cleanup completed"

# Development setup
dev-setup: install seed-data
	@echo "🎯 Development setup completed!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Start the server: make start-server"
	@echo "2. Run tests: make test"
	@echo "3. View API docs: http://localhost:8000/docs"

# Quick test (assumes server is running)
quick-test:
	@echo "⚡ Running quick API test..."
	./test_api.sh --server
	@echo "✅ Quick test completed!"

# Show test data info
show-data:
	@echo "📊 Test Data Information"
	@echo "======================="
	@echo ""
	@echo "Users created by seed script:"
	@echo "  - superadmin@test.com (Super Admin)"
	@echo "  - admin@test.com (Admin)"
	@echo "  - moderator@test.com (Moderator)"
	@echo "  - john.doe@test.com (Regular User)"
	@echo "  - jane.smith@test.com (Regular User)"
	@echo "  - bob.wilson@test.com (Regular User)"
	@echo "  - alice.brown@test.com (Regular User)"
	@echo "  - guest@test.com (Guest User)"
	@echo "  - hr.manager@test.com (HR Manager)"
	@echo "  - analyst@test.com (Data Analyst)"
	@echo "  - inactive@test.com (Inactive User)"
	@echo ""
	@echo "Roles created:"
	@echo "  - super_admin (Full system access)"
	@echo "  - admin (Management privileges)"
	@echo "  - moderator (Content moderation)"
	@echo "  - user (Basic user access)"
	@echo "  - guest (Limited access)"
	@echo "  - hr_manager (Recruitment access)"
	@echo "  - analyst (Data analysis access)"
	@echo "  - inactive_role (Inactive role)"
	@echo ""
	@echo "All users have password: [Role]123!"
	@echo "Example: admin@test.com / Admin123!"

# Database operations
db-migrate:
	@echo "🗄️ Running database migrations..."
	alembic upgrade head
	@echo "✅ Database migrations completed"

db-reset:
	@echo "🔄 Resetting database..."
	@echo "This will drop and recreate all tables."
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ]
	alembic downgrade base
	alembic upgrade head
	@echo "✅ Database reset completed"

# Show server status
status:
	@echo "📊 Server Status"
	@echo "==============="
	@curl -s http://localhost:8000/health 2>/dev/null && echo "✅ Server is running" || echo "❌ Server is not running"
	@echo ""
	@echo "Available endpoints:"
	@echo "  - Health: http://localhost:8000/health"
	@echo "  - API Docs: http://localhost:8000/docs"
	@echo "  - ReDoc: http://localhost:8000/redoc"
	@echo "  - Models: http://localhost:8000/models"
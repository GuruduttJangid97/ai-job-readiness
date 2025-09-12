# AI Job Readiness Backend - Production Makefile

.PHONY: help test test-unit test-integration test-all test-coverage clean install dev-setup lint format

# Default target
help:
	@echo "AI Job Readiness Backend - Production Commands"
	@echo "=============================================="
	@echo ""
	@echo "Testing Commands:"
	@echo "  test            - Run all tests (default)"
	@echo "  test-unit       - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  test-coverage   - Run tests with coverage report"
	@echo ""
	@echo "Development Commands:"
	@echo "  install         - Install dependencies"
	@echo "  dev-setup       - Setup development environment"
	@echo "  reset-db        - Reset database (WARNING: deletes all data)"
	@echo "  clean           - Clean up artifacts"
	@echo "  lint            - Lint code"
	@echo "  format          - Format code"
	@echo ""
	@echo "Production Commands:"
	@echo "  test-all        - Run all tests with full reporting"
	@echo "  help            - Show this help message"

# Default: run all tests
test: test-all

# Run all tests with comprehensive reporting
test-all:
	@echo "🚀 Running All Tests..."
	python tests/run_tests.py --all

# Run unit tests only
test-unit:
	@echo "🧪 Running Unit Tests..."
	python tests/run_tests.py --unit

# Run integration tests only
test-integration:
	@echo "🔗 Running Integration Tests..."
	python tests/run_tests.py --integration

# Run tests with coverage
test-coverage:
	@echo "📊 Running Tests with Coverage..."
	python tests/run_tests.py --all --coverage

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

# Setup development environment
dev-setup: install
	@echo "🔧 Setting up development environment..."
	python -c "from app.db.database import init_db; import asyncio; asyncio.run(init_db())"
	@echo "✅ Development environment ready!"

# Reset database (WARNING: deletes all data)
reset-db:
	@echo "🔄 Resetting database..."
	python reset_database.py

# Clean up artifacts
clean:
	@echo "🧹 Cleaning up artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	rm -f .coverage 2>/dev/null || true
	rm -rf htmlcov/ 2>/dev/null || true
	rm -rf .pytest_cache/ 2>/dev/null || true

# Lint code
lint:
	@echo "🔍 Linting code..."
	python -m flake8 app/models/ tests/ --max-line-length=100 --ignore=E203,W503

# Format code
format:
	@echo "🎨 Formatting code..."
	python -m black app/models/ tests/ --line-length=100

# CI/CD pipeline command
ci-test: clean test-coverage
	@echo "✅ CI/CD pipeline completed successfully"

# Production deployment check
prod-check: clean test-all lint
	@echo "✅ Production readiness check completed"
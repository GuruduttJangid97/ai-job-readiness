# AI Job Readiness Platform - Testing Guide

## Overview

This document provides comprehensive testing instructions for the AI Job Readiness platform models and database operations.

## Quick Start

```bash
# Run all tests
make test

# Run specific test types
make test-unit
make test-integration
make test-coverage
```

## Test Structure

```
tests/
├── conftest.py              # Test configuration and fixtures
├── run_tests.py             # Production test runner
└── unit/
    ├── test_model_simple.py     # Unit tests (13 tests)
    ├── test_model_creation.py   # Model creation tests (33 tests)
    ├── test_model_relationships.py  # Relationship tests (13 tests)
    └── test_model_constraints.py    # Constraint tests (28 tests)
```

## Available Commands

### Makefile Commands

| Command | Description |
|---------|-------------|
| `make test` | Run all tests (default) |
| `make test-unit` | Run unit tests only |
| `make test-integration` | Run integration tests only |
| `make test-coverage` | Run tests with coverage report |
| `make clean` | Clean up test artifacts |
| `make lint` | Lint code |
| `make format` | Format code |
| `make dev-setup` | Setup development environment |
| `make prod-check` | Production readiness check |

### Python Commands

```bash
# Run specific test files
python -m pytest tests/unit/test_model_simple.py -v
python -m pytest tests/unit/test_model_creation.py -v

# Run with coverage
python -m pytest tests/unit/ --cov=app.models --cov-report=html

# Run production test runner
python tests/run_tests.py --all
python tests/run_tests.py --unit
python tests/run_tests.py --integration --coverage
```

## Test Categories

### Unit Tests (46 tests)
- **Model Creation**: Tests model instantiation and field validation
- **Model Methods**: Tests business logic and utility methods
- **Model Serialization**: Tests JSON serialization/deserialization
- **Model Properties**: Tests computed properties and getters

### Integration Tests (41 tests)
- **Database Operations**: Tests model persistence and queries
- **Relationships**: Tests foreign key relationships and cascades
- **Constraints**: Tests database constraints and validation
- **Cascade Deletion**: Tests data integrity on deletion

## Test Coverage

Current test coverage includes:
- ✅ User model (100%)
- ✅ Role model (100%)
- ✅ UserRole model (100%)
- ✅ Resume model (100%)
- ✅ Score model (100%)
- ✅ Database relationships (100%)
- ✅ Constraint validation (100%)

## Running Tests

### Development

```bash
# Setup environment
make dev-setup

# Run tests
make test

# Run with coverage
make test-coverage
```

### CI/CD Pipeline

```bash
# Full CI pipeline
make ci-test

# Production check
make prod-check
```

### Production

```bash
# Run all tests with reporting
python tests/run_tests.py --all

# Run with coverage
python tests/run_tests.py --all --coverage
```

## Test Configuration

### Pytest Configuration
- Async mode enabled for database tests
- Strict markers and configuration
- Coverage reporting enabled
- Warning filters configured

### Database Configuration
- SQLite in-memory database for tests
- Automatic cleanup between tests
- Foreign key constraints enabled
- Cascade deletion tested

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   ```bash
   # Initialize database
   make dev-setup
   ```

2. **Import Errors**
   ```bash
   # Ensure you're in the backend directory
   cd backend
   ```

3. **Permission Errors**
   ```bash
   # Make scripts executable
   chmod +x tests/run_tests.py
   ```

### Debug Mode

```bash
# Run with verbose output
python -m pytest tests/unit/test_model_simple.py -v -s

# Run specific test
python -m pytest tests/unit/test_model_simple.py::TestSimpleModelCreation::test_user_creation -v
```

## Performance

- **Unit Tests**: ~2-3 seconds
- **Integration Tests**: ~5-10 seconds
- **Full Test Suite**: ~10-15 seconds
- **Memory Usage**: Minimal (SQLite in-memory)

## Best Practices

1. **Run tests before committing**
   ```bash
   make test
   ```

2. **Check coverage regularly**
   ```bash
   make test-coverage
   ```

3. **Clean up artifacts**
   ```bash
   make clean
   ```

4. **Use production test runner for CI/CD**
   ```bash
   python tests/run_tests.py --all
   ```

## Contributing

When adding new tests:
1. Follow existing test patterns
2. Add appropriate markers (`@pytest.mark.unit`, `@pytest.mark.integration`)
3. Include docstrings explaining test purpose
4. Ensure tests are isolated and can run independently
5. Update this documentation if adding new test categories

## Support

For testing issues or questions:
1. Check this documentation
2. Run `make help` for available commands
3. Check test output for specific error messages
4. Ensure all dependencies are installed with `make install`

# 🧪 Test Suite Documentation

This directory contains all test files for the AI Job Readiness Backend, organized by test type for better maintainability and clarity.

## 📁 Directory Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # Shared test configuration and fixtures
├── run_tests.py               # Master test runner
├── README.md                  # This documentation
├── unit/                      # Unit tests
│   ├── __init__.py
│   └── test_roles_simple.py   # Basic functionality tests
├── integration/               # Integration tests
│   ├── __init__.py
│   └── test_role_integration.py # End-to-end workflow tests
├── performance/               # Performance tests
│   ├── __init__.py
│   └── test_role_performance.py # Load and performance tests
├── security/                  # Security tests
│   ├── __init__.py
│   └── test_role_security.py  # Security and validation tests
└── api/                       # API tests
    ├── __init__.py
    └── test_role_api.py       # API endpoint tests
```

## 🚀 Running Tests

### Using the Master Test Runner

```bash
# Run all tests
python tests/run_tests.py

# Run specific test categories
python tests/run_tests.py --only-unit
python tests/run_tests.py --only-performance
python tests/run_tests.py --only-security
python tests/run_tests.py --only-integration
python tests/run_tests.py --only-api

# Skip specific test categories
python tests/run_tests.py --skip-api --skip-performance
python tests/run_tests.py --skip-integration
```

### Using pytest

```bash
# Run all tests
pytest

# Run specific test categories
pytest -m unit
pytest -m performance
pytest -m security
pytest -m integration
pytest -m api

# Run specific test files
pytest tests/unit/test_roles_simple.py
pytest tests/performance/test_role_performance.py
pytest tests/security/test_role_security.py
pytest tests/integration/test_role_integration.py
pytest tests/api/test_role_api.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app
```

## 📋 Test Categories

### 🔧 Unit Tests (`tests/unit/`)
- **Purpose**: Test individual components in isolation
- **Files**: `test_roles_simple.py`
- **Duration**: ~0.05 seconds
- **What it tests**:
  - Role creation and management
  - User creation and management
  - Role assignment to users
  - Permission checking and manipulation
  - Basic CRUD operations

### 🔗 Integration Tests (`tests/integration/`)
- **Purpose**: Test complete workflows and component interactions
- **Files**: `test_role_integration.py`
- **Duration**: ~5-10 seconds
- **What it tests**:
  - End-to-end role management workflows
  - Cross-component interactions
  - Error handling and edge cases
  - Complete user journeys

### ⚡ Performance Tests (`tests/performance/`)
- **Purpose**: Test system performance under load
- **Files**: `test_role_performance.py`
- **Duration**: ~30 seconds
- **What it tests**:
  - Large dataset creation (1000+ roles, 5000+ users)
  - Query performance benchmarks
  - Concurrent operations (50+ simultaneous operations)
  - Memory usage monitoring
  - Scalability validation

### 🔒 Security Tests (`tests/security/`)
- **Purpose**: Test security aspects and data integrity
- **Files**: `test_role_security.py`
- **Duration**: ~0.08 seconds
- **What it tests**:
  - Permission validation and access control
  - SQL injection protection
  - Data integrity constraints
  - Inactive role handling
  - Concurrent access safety
  - Input validation

### 🌐 API Tests (`tests/api/`)
- **Purpose**: Test REST API endpoints
- **Files**: `test_role_api.py`
- **Duration**: ~2-3 seconds
- **What it tests**:
  - CRUD operations via HTTP requests
  - Authentication and authorization
  - Request/response validation
  - Error handling
  - API contract compliance

## 🛠️ Test Configuration

### Shared Fixtures (`conftest.py`)
- `clear_test_data()`: Clear all test data from database
- `create_test_user()`: Create a test user
- `create_test_role()`: Create a test role
- `create_test_user_role()`: Create a user-role assignment

### Pytest Configuration (`pytest.ini`)
- Test discovery patterns
- Markers for test categorization
- Async test support
- Output formatting options

## 📊 Test Results

### Expected Performance
- **Unit Tests**: 100% pass rate, <0.1s
- **Integration Tests**: 100% pass rate, <10s
- **Performance Tests**: 100% pass rate, <30s
- **Security Tests**: 100% pass rate, <0.1s
- **API Tests**: 100% pass rate, <5s

### Success Criteria
- All tests must pass before deployment
- Performance tests must meet benchmark thresholds
- Security tests must validate all security measures
- Integration tests must validate complete workflows

## 🔧 Development Workflow

### Adding New Tests
1. Choose the appropriate test category
2. Create test file in the correct directory
3. Use shared fixtures from `conftest.py`
4. Add appropriate markers for test categorization
5. Update this documentation if needed

### Test Naming Convention
- Test files: `test_*.py`
- Test functions: `test_*`
- Test classes: `Test*`
- Use descriptive names that explain what is being tested

### Best Practices
- Keep tests independent and isolated
- Use meaningful assertions
- Clean up test data after each test
- Use fixtures for common setup/teardown
- Write tests that are easy to understand and maintain

## 🐛 Troubleshooting

### Common Issues
1. **Database Connection Errors**: Ensure database is running and accessible
2. **Import Errors**: Check Python path and module structure
3. **Async Test Issues**: Ensure proper async/await usage
4. **Permission Errors**: Check file permissions and database access

### Debug Mode
```bash
# Run tests with debug output
pytest -v -s --tb=long

# Run specific test with debug
pytest -v -s tests/unit/test_roles_simple.py::test_role_system
```

## 📈 Continuous Integration

These tests are designed to run in CI/CD pipelines:
- Fast execution for quick feedback
- Comprehensive coverage of all functionality
- Clear pass/fail indicators
- Detailed reporting for debugging

## 🤝 Contributing

When adding new features:
1. Write tests first (TDD approach)
2. Ensure all tests pass
3. Update documentation
4. Follow established patterns and conventions

# 🤝 Contributing to AI Job Readiness Platform

Thank you for your interest in contributing to the AI Job Readiness Platform! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)
- [Feature Requests](#feature-requests)

## 📜 Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow. Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## 🚀 Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Git** installed and configured
- **Docker** and **Docker Compose** (recommended)
- **Node.js** 18+ (for frontend development)
- **Python** 3.11+ (for backend development)
- **PostgreSQL** 15+ (for local database development)

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/ai-job-readiness.git
   cd ai-job-readiness
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/original-org/ai-job-readiness.git
   ```

## 💻 Development Setup

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/your-username/ai-job-readiness.git
cd ai-job-readiness

# Start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Local Development Setup

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

#### Database Setup
```bash
# Start PostgreSQL
docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15

# Run migrations
cd backend
alembic upgrade head
```

## 📝 Contributing Guidelines

### Types of Contributions

We welcome various types of contributions:

- **Bug Fixes**: Fix existing issues
- **Feature Development**: Add new functionality
- **Documentation**: Improve or add documentation
- **Testing**: Add or improve tests
- **Performance**: Optimize existing code
- **UI/UX**: Improve user interface and experience

### Workflow

1. **Check existing issues** and pull requests
2. **Create an issue** if you're planning a significant change
3. **Create a feature branch** from `main`
4. **Make your changes** following our guidelines
5. **Test your changes** thoroughly
6. **Submit a pull request**

### Branch Naming

Use descriptive branch names:

- `feature/user-authentication`
- `bugfix/resume-upload-error`
- `docs/api-documentation`
- `refactor/database-models`
- `test/user-service-tests`

## 🔄 Pull Request Process

### Before Submitting

1. **Update your fork**:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes** and commit:
   ```bash
   git add .
   git commit -m "Add: descriptive commit message"
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

### Pull Request Template

When creating a pull request, please include:

- **Description**: What changes were made and why
- **Type**: Bug fix, feature, documentation, etc.
- **Testing**: How the changes were tested
- **Screenshots**: For UI changes
- **Breaking Changes**: Any breaking changes
- **Related Issues**: Link to related issues

### Review Process

1. **Automated Checks**: CI/CD pipeline runs tests
2. **Code Review**: Maintainers review the code
3. **Testing**: Changes are tested in staging
4. **Approval**: Maintainers approve the PR
5. **Merge**: PR is merged into main branch

## 🎨 Code Style

### Backend (Python)

- **PEP 8**: Follow Python PEP 8 style guide
- **Type Hints**: Use type hints for all functions
- **Docstrings**: Write comprehensive docstrings
- **Async/Await**: Use async/await for database operations
- **Error Handling**: Implement proper error handling

#### Example:
```python
async def get_user_by_id(user_id: uuid.UUID) -> Optional[User]:
    """
    Retrieve a user by their ID.
    
    Args:
        user_id: The UUID of the user to retrieve
        
    Returns:
        User object if found, None otherwise
        
    Raises:
        DatabaseError: If database operation fails
    """
    try:
        async with get_db_session() as db:
            result = await db.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()
    except Exception as e:
        logger.error(f"Error retrieving user {user_id}: {e}")
        raise DatabaseError(f"Failed to retrieve user: {e}")
```

### Frontend (React)

- **Functional Components**: Use functional components with hooks
- **TypeScript**: Use TypeScript for type safety
- **ESLint**: Follow ESLint rules
- **Component Structure**: Follow established patterns
- **Error Boundaries**: Implement error boundaries

#### Example:
```jsx
import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';

interface UserProfileProps {
  userId: string;
  onUpdate?: (user: User) => void;
}

const UserProfile: React.FC<UserProfileProps> = ({ userId, onUpdate }) => {
  const { user, loading, error } = useAuth();
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    // Component logic
  }, [userId]);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <div className="user-profile">
      {/* Component JSX */}
    </div>
  );
};

export default UserProfile;
```

### Commit Messages

Use conventional commit messages:

- `feat: add user authentication system`
- `fix: resolve resume upload timeout issue`
- `docs: update API documentation`
- `test: add unit tests for user service`
- `refactor: improve database connection handling`
- `style: format code according to linting rules`

## 🧪 Testing

### Backend Testing

```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=app --cov-report=html
```

#### Test Structure:
- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test API endpoints and database operations
- **Fixtures**: Reusable test data and database setup

#### Example Test:
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_user():
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
        "first_name": "Test",
        "last_name": "User"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]
```

### Frontend Testing

```bash
cd frontend
npm test
npm test -- --coverage
```

#### Example Test:
```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import LoginForm from './LoginForm';

const renderWithRouter = (component) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('LoginForm', () => {
  test('renders login form', () => {
    renderWithRouter(<LoginForm />);
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  });

  test('submits form with valid data', async () => {
    const mockOnSubmit = jest.fn();
    renderWithRouter(<LoginForm onSubmit={mockOnSubmit} />);
    
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'test@example.com' }
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password123' }
    });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));
    
    expect(mockOnSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123'
    });
  });
});
```

## 📚 Documentation

### Code Documentation

- **Docstrings**: Write comprehensive docstrings for all functions
- **Comments**: Add inline comments for complex logic
- **README**: Keep README files updated
- **API Docs**: Document all API endpoints

### Documentation Updates

When making changes that affect documentation:

1. **Update relevant README files**
2. **Update API documentation**
3. **Add or update code comments**
4. **Update inline documentation**

## 🐛 Issue Reporting

### Bug Reports

When reporting bugs, please include:

- **Description**: Clear description of the bug
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: OS, browser, version information
- **Screenshots**: If applicable
- **Logs**: Relevant error logs

### Issue Template

```markdown
## Bug Description
Brief description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Environment
- OS: [e.g., Windows 10, macOS 12, Ubuntu 20.04]
- Browser: [e.g., Chrome 95, Firefox 94, Safari 15]
- Version: [e.g., 1.0.0]

## Additional Context
Any other context about the problem
```

## 💡 Feature Requests

### Feature Request Template

```markdown
## Feature Description
Brief description of the feature

## Problem Statement
What problem does this feature solve?

## Proposed Solution
How should this feature work?

## Alternatives Considered
What other solutions have you considered?

## Additional Context
Any other context or screenshots
```

## 🏷️ Labels and Milestones

We use labels to categorize issues and pull requests:

- **bug**: Something isn't working
- **enhancement**: New feature or request
- **documentation**: Improvements or additions to documentation
- **good first issue**: Good for newcomers
- **help wanted**: Extra attention is needed
- **priority: high**: High priority
- **priority: low**: Low priority
- **status: in progress**: Currently being worked on
- **status: needs review**: Needs code review

## 🎯 Getting Help

### Communication Channels

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Pull Requests**: For code-related discussions

### Asking Questions

When asking questions:

1. **Search existing issues** first
2. **Provide context** about your environment
3. **Include relevant code** snippets
4. **Be specific** about what you're trying to achieve

## 🏆 Recognition

Contributors will be recognized in:

- **CONTRIBUTORS.md**: List of all contributors
- **Release Notes**: Mentioned in release notes
- **GitHub**: Listed as contributors on the repository

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You

Thank you for contributing to the AI Job Readiness Platform! Your contributions help make this project better for everyone.

---

**Happy Contributing! 🚀**

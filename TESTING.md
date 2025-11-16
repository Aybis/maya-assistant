# Maya Assistant - Testing Guide

This guide provides instructions for running tests in the Maya Assistant project.

## 📋 Quick Start

### Run All Tests (Backend + Frontend)

```bash
./run_all_tests.sh
```

This master script will:
- ✅ Run backend tests with pytest
- ✅ Run frontend tests with vitest
- 📊 Generate coverage reports for both
- 📈 Display a summary of all test results

---

## 🐍 Backend Tests (Python/FastAPI)

### Prerequisites

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running Backend Tests

#### Run all tests
```bash
cd backend
pytest
```

#### Run with coverage
```bash
pytest --cov=app --cov-report=html
```

#### Run specific test file
```bash
pytest tests/test_main.py
```

#### Run specific test function
```bash
pytest tests/test_main.py::test_root_endpoint
```

#### Run with markers
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

#### Watch mode (re-run on file changes)
```bash
pytest-watch
```

### Backend Test Structure

```
backend/tests/
├── __init__.py
├── conftest.py              # Pytest fixtures and configuration
├── test_main.py             # Main app tests
├── test_dependencies.py     # Authentication tests
├── api/
│   ├── test_conversations.py
│   └── test_messages.py
├── services/
│   ├── test_ai_service.py
│   ├── test_supabase_service.py
│   └── test_*_service.py
└── utils/
    └── test_streaming.py
```

### Coverage Report

After running tests with coverage, open:
```bash
open backend/htmlcov/index.html
```

---

## 🎨 Frontend Tests (Next.js/TypeScript)

### Prerequisites

```bash
cd frontend
npm install
```

### Running Frontend Tests

#### Run all tests
```bash
npm test
```

#### Run with coverage
```bash
npm run test:coverage
```

#### Watch mode (interactive)
```bash
npm run test:watch
```

#### UI mode (visual test runner)
```bash
npm run test:ui
```

#### Run specific test file
```bash
npm test -- Button.test.tsx
```

#### Run tests matching pattern
```bash
npm test -- --grep "Chat Store"
```

### Frontend Test Structure

```
frontend/__tests__/
├── components/
│   ├── atoms/
│   │   ├── Button.test.tsx
│   │   ├── Input.test.tsx
│   │   └── ...
│   ├── molecules/
│   │   ├── ChatInput.test.tsx
│   │   ├── MessageBubble.test.tsx
│   │   └── ...
│   └── organisms/
│       ├── ChatArea.test.tsx
│       └── Sidebar.test.tsx
├── lib/
│   ├── api.test.ts
│   └── utils.test.ts
└── store/
    ├── chatStore.test.ts
    ├── conversationStore.test.ts
    └── authStore.test.ts
```

### Coverage Report

After running tests with coverage, open:
```bash
open frontend/coverage/index.html
```

---

## 🧪 Test Coverage Goals

### Current Coverage

Run tests to see current coverage:
```bash
./run_all_tests.sh
```

### Target Coverage

| Component | Target | Priority |
|-----------|--------|----------|
| Authentication | 90%+ | 🔴 Critical |
| API Endpoints | 85%+ | 🔴 Critical |
| AI Services | 80%+ | 🔴 Critical |
| Database Layer | 75%+ | 🟡 High |
| UI Components | 70%+ | 🟢 Medium |
| Utilities | 80%+ | 🟢 Medium |

---

## 📝 Writing Tests

### Backend Test Example

```python
# tests/api/test_example.py
import pytest
from fastapi.testclient import TestClient

@pytest.mark.asyncio
async def test_example_endpoint(authenticated_client, mock_supabase_service):
    """Test example endpoint"""
    # Arrange
    mock_supabase_service.some_method.return_value = {"data": "test"}

    # Act
    response = authenticated_client.get("/api/example")

    # Assert
    assert response.status_code == 200
    assert response.json()["data"] == "test"
```

### Frontend Test Example

```typescript
// __tests__/components/Example.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Example } from '@/components/Example';

describe('Example Component', () => {
  it('should render and handle click', () => {
    // Arrange
    const handleClick = vi.fn();

    // Act
    render(<Example onClick={handleClick} />);
    fireEvent.click(screen.getByRole('button'));

    // Assert
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

---

## 🛠️ Testing Utilities

### Backend Fixtures (conftest.py)

Available fixtures:
- `client`: FastAPI TestClient
- `mock_user`: Authenticated user data
- `mock_supabase_service`: Mocked database service
- `authenticated_client`: Client with auth bypass
- `sample_conversation`: Sample conversation data
- `sample_message`: Sample message data

### Frontend Test Utilities

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';

// Mock Next.js router
vi.mock('next/navigation', () => ({
  useRouter: () => ({ push: vi.fn(), ... })
}));

// Mock API calls
vi.mock('@/lib/api', () => ({
  conversationsApi: {
    getAll: vi.fn(() => Promise.resolve([]))
  }
}));
```

---

## 🔍 Debugging Tests

### Backend Debugging

```bash
# Run with verbose output
pytest -vv

# Run with print statements visible
pytest -s

# Run with detailed traceback
pytest --tb=long

# Drop into debugger on failure
pytest --pdb
```

### Frontend Debugging

```bash
# Run in UI mode for visual debugging
npm run test:ui

# Run with debug output
DEBUG=true npm test

# Run single test file in watch mode
npm test -- Button.test.tsx --watch
```

---

## 🚀 CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: cd backend && pip install -r requirements.txt
      - run: cd backend && pytest --cov --cov-report=xml
      - uses: codecov/codecov-action@v3

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: cd frontend && npm ci
      - run: cd frontend && npm test -- --coverage
      - uses: codecov/codecov-action@v3
```

---

## 📊 Test Reports

### Generate Combined Report

```bash
# Run all tests with coverage
./run_all_tests.sh

# View reports
echo "Backend:  file://$(pwd)/backend/htmlcov/index.html"
echo "Frontend: file://$(pwd)/frontend/coverage/index.html"
```

### Coverage Badges

Add to README.md:
```markdown
![Backend Coverage](https://img.shields.io/badge/backend%20coverage-XX%25-green)
![Frontend Coverage](https://img.shields.io/badge/frontend%20coverage-XX%25-green)
```

---

## 🐛 Common Issues

### Backend

**Issue:** ImportError: No module named 'app'
```bash
# Solution: Ensure you're in backend directory
cd backend
pytest
```

**Issue:** Database connection errors in tests
```bash
# Solution: Tests use mocked services, check conftest.py
# Ensure mock_supabase_service fixture is used
```

### Frontend

**Issue:** "Cannot find module '@/...'"
```bash
# Solution: Check vitest.config.ts has correct alias
resolve: {
  alias: {
    '@': path.resolve(__dirname, './src'),
  },
}
```

**Issue:** "ReferenceError: vi is not defined"
```bash
# Solution: Add to vitest.setup.ts
import { vi } from 'vitest';
```

---

## 📚 Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Vitest Documentation](https://vitest.dev/)
- [Testing Library](https://testing-library.com/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Next.js Testing](https://nextjs.org/docs/testing)

---

## ✅ Testing Checklist

Before committing code:

- [ ] All tests pass locally
- [ ] New features have tests
- [ ] Bug fixes have regression tests
- [ ] Coverage didn't decrease
- [ ] No console errors in tests
- [ ] Tests are well-documented
- [ ] Mocks are properly configured
- [ ] Edge cases are covered

---

**Happy Testing!** 🧪✨

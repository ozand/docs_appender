# Backend E2E Authentication Tests

This directory contains End-to-End (E2E) tests for the backend authentication system. These tests validate the complete authentication flow from API endpoints to database operations.

## Test Coverage

### Authentication Endpoints
- **User Registration** (`POST /auth/register`)
  - Valid user data registration
  - Duplicate email handling
  - Invalid email format validation
  - Weak password rejection

- **User Login** (`POST /auth/login`)
  - Valid credential authentication
  - Invalid email handling
  - Wrong password handling
  - Empty credential validation

- **Token Validation** (`GET /auth/validate`)
  - Valid token acceptance
  - Invalid token rejection
  - Expired token handling

- **Token Refresh** (`POST /auth/refresh`)
  - Valid refresh token exchange
  - Invalid refresh token rejection
  - New token generation

- **User Logout** (`POST /auth/logout`)
  - Successful logout processing
  - Invalid token handling

### Protected Endpoints
- **Protected Files** (`GET /protected/files`)
  - Access with valid token
  - Access denied with invalid token
  - Access denied without token

### Error Scenarios
- SQL injection attempt handling
- Malformed request processing
- Concurrent login handling
- Invalid input validation

## Test Structure

```
backend/tests/e2e/
├── test_authentication.py      # Main authentication test suite
├── data/
│   └── users.json             # Test data and scenarios
└── README.md                  # This file
```

## Prerequisites

1. **Backend Server**: The backend server must be running on `http://localhost:8000`
2. **Dependencies**: Install test dependencies:
   ```bash
   cd backend
   uv sync
   ```

## Running Tests

### Run All E2E Tests
```bash
cd backend
uv run pytest tests/e2e/
```

### Run Specific Test Classes
```bash
# Run only registration tests
uv run pytest tests/e2e/test_authentication.py::TestUserRegistration

# Run only login tests
uv run pytest tests/e2e/test_authentication.py::TestUserLogin

# Run only token tests
uv run pytest tests/e2e/test_authentication.py::TestTokenValidation
```

### Run with Coverage
```bash
uv run pytest tests/e2e/ --cov=src --cov-report=html
```

### Run with Verbose Output
```bash
uv run pytest tests/e2e/ -v
```

## Test Data

Test data is stored in `data/users.json` and includes:
- Predefined test users with known credentials
- Test scenarios with expected outcomes
- Edge cases and error conditions

### Test User Accounts

| Email | Password | Status | Purpose |
|-------|----------|--------|---------|
| test@example.com | testpassword123 | Active | General testing |
| admin@example.com | admin123 | Active | Admin testing |
| inactive@example.com | inactive123 | Inactive | Inactive user testing |

## Configuration

Tests use the following default configuration:
- **Base URL**: `http://localhost:8000`
- **Auth Base URL**: `http://localhost:8000/auth`
- **Timeout**: 5000ms for API requests
- **Max Concurrent Requests**: 5 for concurrent testing

## Test Isolation

Each test uses isolated data to prevent interference:
- Unique email addresses with timestamps
- Automatic cleanup of test data
- Independent test scenarios
- No shared state between tests

## Best Practices

### Writing New Tests
1. Follow the naming convention: `test_action_with_expected_outcome()`
2. Use the `AuthTestHelper` class for common operations
3. Create unique test data for each test
4. Include both positive and negative test cases
5. Add appropriate assertions for all scenarios

### Test Data Management
1. Use the `data/users.json` file for predefined test data
2. Generate unique data for tests that modify state
3. Clean up test data after tests complete
4. Avoid hardcoded values in tests

### Debugging Failed Tests
1. Check the backend server logs for errors
2. Use verbose output to see detailed test execution
3. Check if test data conflicts with existing data
4. Verify API endpoints are accessible

## CI/CD Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run Backend E2E Tests
  run: |
    cd backend
    uv run pytest tests/e2e/ --cov=src --cov-report=xml
```

## Troubleshooting

### Common Issues

1. **Connection Refused**: Ensure backend server is running on port 8000
2. **Authentication Failed**: Check if test users exist in the database
3. **Timeout Errors**: Increase timeout values for slower systems
4. **Data Conflicts**: Use unique test data to avoid conflicts

### Debug Commands
```bash
# Check if backend is running
curl http://localhost:8000/docs

# Check test user exists
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpassword123"}'

# Run tests with debug output
uv run pytest tests/e2e/ -v -s
```

## Extending Tests

To add new authentication tests:

1. **Add to existing classes** for related functionality
2. **Create new test classes** for new features
3. **Update test data** in `data/users.json`
4. **Add helper methods** to `AuthTestHelper` for reusable operations
5. **Update this README** with new test coverage information
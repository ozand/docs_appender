# Frontend E2E Authentication Tests

This directory contains End-to-End (E2E) tests for the frontend authentication system. These tests validate the complete user interface authentication flow using Playwright browser automation.

## Test Coverage

### Login Form Functionality
- **Form Accessibility**: Login form accessibility and proper labeling
- **Input Validation**: Real-time form validation and error handling
- **Authentication Flow**: Complete login/logout user journeys
- **Error Handling**: Error message display and user feedback

### User Interface Tests
- **Login Form Display**: Proper rendering of login form elements
- **Input Fields**: Email and password field functionality
- **Button States**: Sign-in button loading states and disabled states
- **Form Submission**: Form submission with Enter key and button click
- **Error Messages**: Display of validation and authentication errors

### Session Management
- **Session Persistence**: Session persistence across page navigation
- **Session Persistence**: Session persistence across page refreshes
- **Logout Functionality**: Proper logout and session cleanup
- **Authentication Status**: Correct display of authentication status

### Error Scenarios
- **Invalid Credentials**: Handling of wrong email/password combinations
- **Empty Fields**: Validation of empty required fields
- **Invalid Email Format**: Email format validation
- **Network Errors**: Handling of connection failures
- **Concurrent Sessions**: Multiple login attempt handling

## Test Structure

```
frontend/tests/e2e/
├── test_login_logout.py        # Main login/logout test suite
├── pages/
│   └── login_page.py          # Page Object Model for login page
├── data/
│   └── users.json             # Test data and scenarios
└── README.md                  # This file
```

## Prerequisites

1. **Frontend Server**: The Streamlit frontend must be running on `http://localhost:8501`
2. **Backend Server**: The backend API must be running on `http://localhost:8000`
3. **Dependencies**: Install test dependencies:
   ```bash
   cd frontend
   uv add --dev pytest pytest-playwright
   uv run playwright install
   ```

## Running Tests

### Run All E2E Tests
```bash
cd frontend
uv run pytest tests/e2e/
```

### Run Specific Test Classes
```bash
# Run only login flow tests
uv run pytest tests/e2e/test_login_logout.py::TestLoginLogoutFlows

# Run only error scenario tests
uv run pytest tests/e2e/test_login_logout.py::TestAuthenticationErrorScenarios

# Run only session management tests
uv run pytest tests/e2e/test_login_logout.py::TestSessionManagement
```

### Run with Screenshots on Failure
```bash
uv run pytest tests/e2e/ --screenshot on --video on
```

### Run with Tracing
```bash
uv run pytest tests/e2e/ --tracing on
```

### Run Across Multiple Browsers
```bash
uv run pytest tests/e2e/ --browser chromium --browser firefox --browser webkit
```

## Page Object Model

The tests use a Page Object Model pattern implemented in `pages/login_page.py`:

### Key Features
- **Robust Selectors**: Uses `data-testid` attributes and semantic selectors
- **Method Chaining**: Fluent interface for test readability
- **Wait Strategies**: Proper waiting with Playwright's auto-waiting mechanisms
- **Error Handling**: Comprehensive error handling and reporting

### Usage Example
```python
login_page = LoginPage(page)
login_page.navigate_to_login()
login_page.fill_email("test@example.com")
login_page.fill_password("password123")
login_page.click_sign_in()
```

## Test Data

Test data is stored in `data/users.json` and includes:
- Predefined test user credentials
- Test scenarios with expected outcomes
- Form validation test cases
- UI viewport configurations

### Test User Accounts

| Email | Password | Status | Purpose |
|-------|----------|--------|---------|
| test@example.com | testpassword123 | Active | General testing |
| admin@example.com | admin123 | Active | Admin testing |
| inactive@example.com | inactive123 | Inactive | Inactive user testing |

## Configuration

### Playwright Configuration
Tests use the following Playwright configuration:
- **Base URL**: `http://localhost:8501`
- **Browser**: Chromium (default), Firefox, WebKit available
- **Viewport**: 1280x720 (default), responsive testing available
- **Timeout**: 30 seconds for navigation, 10 seconds for assertions

### Environment Variables
```bash
# Frontend URL (optional, defaults to localhost:8501)
FRONTEND_URL=http://localhost:8501

# Backend URL (optional, defaults to localhost:8000)
BACKEND_URL=http://localhost:8000
```

## Test Isolation

Each test ensures isolation through:
- **Unique Test Data**: Each test uses unique identifiers
- **Clean State**: Tests start from a clean browser state
- **No Shared Sessions**: Each test runs in isolation
- **Data Cleanup**: Automatic cleanup of test artifacts

## Best Practices

### Writing New Tests
1. **Follow POM Pattern**: Use the LoginPage class for all interactions
2. **Descriptive Names**: Use clear, descriptive test method names
3. **Wait Strategies**: Use Playwright's auto-waiting instead of `time.sleep()`
4. **Robust Selectors**: Prefer semantic selectors over brittle CSS/XPath
5. **Error Assertions**: Include both positive and negative test cases

### Test Data Management
1. **Use Test Data Files**: Store test data in `data/users.json`
2. **Dynamic Data**: Generate unique data for tests that create state
3. **Cleanup**: Ensure tests clean up after themselves
4. **Isolation**: Avoid dependencies between tests

### Debugging Failed Tests
1. **Screenshots**: Use `--screenshot on` to capture failure screenshots
2. **Videos**: Use `--video on` to record test execution
3. **Traces**: Use `--tracing on` and view traces with `playwright show-trace`
4. **Step-by-step**: Add `page.pause()` for interactive debugging

## CI/CD Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Install Playwright
  run: |
    cd frontend
    uv run playwright install

- name: Run Frontend E2E Tests
  run: |
    cd frontend
    uv run pytest tests/e2e/ --browser chromium --screenshot on
```

## Troubleshooting

### Common Issues

1. **Connection Refused**: Ensure both frontend and backend servers are running
2. **Element Not Found**: Check if selectors match the current UI structure
3. **Timeout Errors**: Increase timeout values or check for slow loading
4. **Authentication Failed**: Verify test user accounts exist in backend

### Debug Commands
```bash
# Check if servers are running
curl http://localhost:8501  # Frontend
curl http://localhost:8000  # Backend

# Run single test with debug output
uv run pytest tests/e2e/test_login_logout.py::TestLoginLogoutFlows::test_login_with_valid_credentials_succeeds_chromium -v -s

# Capture screenshots on failure
uv run pytest tests/e2e/ --screenshot on --screenshot-path screenshots/

# Generate test trace
uv run pytest tests/e2e/ --tracing on
uv run playwright show-trace trace.zip
```

## Browser Support

Tests are designed to work across multiple browsers:

### Chromium (Primary)
- Fastest execution
- Most compatible with modern web features
- Best debugging tools

### Firefox
- Alternative rendering engine
- Good for cross-browser compatibility testing

### WebKit
- Safari compatibility testing
- Mobile Safari simulation

## Performance Considerations

1. **Parallel Execution**: Tests can run in parallel for faster execution
2. **Resource Cleanup**: Proper browser context cleanup between tests
3. **Minimal Waits**: Use efficient waiting strategies
4. **Headless Mode**: Run in headless mode for CI/CD environments

## Extending Tests

To add new frontend E2E tests:

1. **Add to existing classes** for related functionality
2. **Create new Page Objects** for new UI components
3. **Update test data** in `data/users.json`
4. **Add new test methods** following naming conventions
5. **Update this README** with new test coverage information

## Related Documentation

- [Playwright Documentation](https://playwright.dev/docs/intro)
- [Pytest Documentation](https://docs.pytest.org/)
- [Page Object Model Pattern](https://playwright.dev/docs/pom)
- [E2E Testing Guidelines](../rules/03-e2e-tests-guideline.md)
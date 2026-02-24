# FastAPI Backend Tests

Comprehensive test suite for the Mergington High School API backend using pytest with AAA (Arrange-Act-Assert) pattern.

## Test Structure

The tests follow the **AAA (Arrange-Act-Assert)** pattern for clarity and maintainability:

- **Arrange**: Set up test data, fixtures, and preconditions
- **Act**: Execute the code being tested
- **Assert**: Verify the expected outcomes

### Example

```python
def test_signup_success(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={new_email}")
    
    # Assert
    assert response.status_code == 200
    assert new_email in response.json()["message"]
```

## Test Files

- **`conftest.py`**: Shared fixtures including `client` (TestClient) and `reset_activities` (data reset)
- **`test_activities.py`**: Tests for `GET /activities` endpoint
- **`test_signup.py`**: Tests for `POST /activities/{activity_name}/signup` endpoint
- **`test_deletion.py`**: Tests for `DELETE /activities/{activity_name}/participants/{email}` endpoint
- **`test_root.py`**: Tests for `GET /` (root redirect) endpoint

## Running Tests

### Prerequisites

Install dependencies:

```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Specific Test File

```bash
pytest tests/test_signup.py
```

### Run Specific Test Function

```bash
pytest tests/test_signup.py::test_signup_success
```

### Run Tests by Keyword

```bash
# Run all tests with "signup" in the name
pytest -k signup

# Run all tests with "error" or "404" in the name
pytest -k "error or 404"
```

## Coverage Reports

### Generate Coverage Report (Terminal)

```bash
pytest --cov=src --cov-report=term-missing
```

This shows:
- Overall coverage percentage
- Lines covered per file
- Missing line numbers

### Generate HTML Coverage Report

```bash
pytest --cov=src --cov-report=html
```

Open `htmlcov/index.html` in your browser to see an interactive coverage report.

### Generate Both Terminal and HTML Reports

```bash
pytest --cov=src --cov-report=term-missing --cov-report=html
```

### Coverage Targets

- **Current Target**: >90% code coverage
- **Ideal Target**: >95% code coverage

## Test Coverage Summary

### Endpoints Tested

| Endpoint | Method | Test Coverage |
|----------|--------|---------------|
| `/` | GET | ✅ Redirect functionality |
| `/activities` | GET | ✅ List all, structure validation |
| `/activities/{activity_name}/signup` | POST | ✅ Success, errors (404, 400), edge cases |
| `/activities/{activity_name}/participants/{email}` | DELETE | ✅ Success, errors (404), edge cases |

### Test Scenarios Covered

#### GET /activities
- ✅ Returns all 9 activities
- ✅ Correct structure with all required fields
- ✅ Initial participants present
- ✅ Valid max_participants values

#### POST /activities/{activity_name}/signup
- ✅ Successful signup
- ✅ Error: Non-existent activity (404)
- ✅ Error: Duplicate signup (400)
- ✅ Participant count increases
- ✅ Multiple signups to different activities
- ✅ Same email to multiple activities
- ✅ Special characters in email

#### DELETE /activities/{activity_name}/participants/{email}
- ✅ Successful deletion
- ✅ Error: Non-existent activity (404)
- ✅ Error: Non-existent participant (404)
- ✅ Participant count decreases
- ✅ Delete then re-signup
- ✅ Delete all participants
- ✅ Delete from multiple activities
- ✅ URL-encoded emails

#### GET /
- ✅ Redirects to /static/index.html
- ✅ Redirect can be followed
- ✅ Correct redirect status code

## Fixtures

### `client` Fixture

Provides a FastAPI `TestClient` for making HTTP requests to the API.

**Usage:**
```python
def test_example(client):
    response = client.get("/activities")
    assert response.status_code == 200
```

### `reset_activities` Fixture (Auto-used)

Automatically resets the in-memory activities database before and after each test to ensure test isolation. No need to explicitly use this fixture - it runs automatically.

## Writing New Tests

When adding new tests, follow these guidelines:

### 1. Use AAA Pattern

Structure your test with clear sections:

```python
def test_new_feature(client):
    # Arrange
    # Set up test data here
    
    # Act
    # Execute the functionality being tested
    
    # Assert
    # Verify expected outcomes
```

### 2. Descriptive Test Names

Use clear, descriptive names that explain what is being tested:

```python
# Good
def test_signup_with_invalid_email_format()

# Bad
def test_signup_2()
```

### 3. Test One Thing

Each test should verify one specific behavior or scenario.

### 4. Use Assertions Effectively

```python
# Assert status codes
assert response.status_code == 200

# Assert response structure
assert "key" in response.json()

# Assert values
assert response.json()["count"] == 5
```

### 5. Add Docstrings

Include a docstring explaining the test's purpose and AAA structure:

```python
def test_example(client):
    """
    Test that feature X behaves correctly under condition Y.
    
    Following AAA pattern:
    - Arrange: Set up test data
    - Act: Call the endpoint
    - Assert: Verify expected behavior
    """
```

## Continuous Integration

To integrate these tests into CI/CD:

```yaml
# Example GitHub Actions workflow
- name: Install dependencies
  run: pip install -r requirements.txt

- name: Run tests with coverage
  run: pytest --cov=src --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Troubleshooting

### Tests Failing Due to State Issues

If tests are failing due to data from previous tests:
- Verify the `reset_activities` fixture is working
- Check that tests aren't modifying global state without cleanup
- Run tests in isolation: `pytest tests/test_signup.py::test_signup_success`

### Import Errors

If you see import errors:
- Ensure you're running pytest from the project root directory
- Check that `pythonpath = .` is set in `pytest.ini`
- Verify the `src` directory is accessible

### Coverage Not Showing Source Files

If coverage report is empty:
- Ensure `source = src` is set in `pytest.ini`
- Run with explicit source: `pytest --cov=src`
- Check file paths in the coverage report

## Best Practices

1. **Run tests frequently** during development
2. **Maintain high coverage** (aim for >90%)
3. **Keep tests independent** - each test should work in isolation
4. **Use meaningful assertions** - make failures easy to debug
5. **Follow AAA pattern** consistently across all tests
6. **Document complex test scenarios** with clear comments
7. **Test both success and failure cases**
8. **Test edge cases** and boundary conditions

## Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [AAA Pattern](https://wiki.c2.com/?ArrangeActAssert)

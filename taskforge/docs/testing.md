# Testing Guide

## Testing Strategy

TaskForge employs a comprehensive testing strategy with multiple layers of testing to ensure code quality and reliability.

## Test Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── unit/                    # Unit tests for individual components
│   ├── test_user_service.py
│   ├── test_project_service.py
│   ├── test_task_service.py
│   ├── test_tag_service.py
│   ├── test_note_service.py
│   ├── test_reminder_service.py
│   ├── test_report_service.py
│   ├── test_search_service.py
│   ├── test_date_utils.py
│   └── test_file_utils.py
├── integration/             # Integration tests
│   └── test_database.py
├── api/                     # API endpoint tests
│   ├── test_users_api.py
│   ├── test_projects_api.py
│   ├── test_tasks_api.py
│   └── test_reports_api.py
└── cli/                     # CLI command tests
    ├── test_user_commands.py
    ├── test_project_commands.py
    ├── test_task_commands.py
    └── test_report_commands.py
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# API tests only
pytest tests/api/

# CLI tests only
pytest tests/cli/
```

### Run Single Test File
```bash
pytest tests/unit/test_user_service.py
```

### Run Single Test
```bash
pytest tests/unit/test_user_service.py::test_create_user -v
```

### Run Tests with Coverage
```bash
pytest --cov=taskforge --cov-report=html
```

### Run Tests in Verbose Mode
```bash
pytest -v
```

### Run Tests with Debug Output
```bash
pytest -s --pdb
```

## Test Configuration

### pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
markers =
    unit: Unit tests
    integration: Integration tests
    api: API tests
    cli: CLI tests
```

### Coverage Configuration
```ini
[coverage:run]
source = taskforge
omit =
    */tests/*
    */venv/*
    */__pycache__/*

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

## Test Fixtures

### Database Fixtures
```python
@pytest.fixture
def db_session():
    """Create a test database session."""
    # Setup test database
    # Yield session for test
    # Cleanup after test
```

### API Test Client
```python
@pytest.fixture
def client():
    """Create a test client for API testing."""
    from fastapi.testclient import TestClient
    from taskforge.api.main import app
    return TestClient(app)
```

### CLI Runner
```python
@pytest.fixture
def runner():
    """Create a CLI runner for command testing."""
    from typer.testing import CliRunner
    return CliRunner()
```

## Writing Tests

### Unit Test Example
```python
def test_create_user():
    """Test creating a user."""
    service = UserService()
    user_data = UserCreate(name="John Doe", email="john@example.com")

    user = service.create_user(user_data)

    assert user.name == "John Doe"
    assert user.email == "john@example.com"
    assert user.id is not None
```

### API Test Example
```python
def test_create_user_api(client):
    """Test creating a user via API."""
    response = client.post(
        "/users/",
        json={"name": "John Doe", "email": "john@example.com"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
```

### CLI Test Example
```python
def test_create_user_cli(runner):
    """Test creating a user via CLI."""
    result = runner.invoke(app, ["user", "create", "John Doe", "john@example.com"])

    assert result.exit_code == 0
    assert "User created successfully" in result.output
```

## Test Categories

### Unit Tests
- Test individual functions and methods
- Mock external dependencies
- Focus on business logic
- Fast execution

### Integration Tests
- Test component interactions
- Use real database connections
- Test data persistence
- Medium execution speed

### API Tests
- Test REST endpoints
- Verify request/response formats
- Test error handling
- Use FastAPI TestClient

### CLI Tests
- Test command-line interfaces
- Verify command outputs
- Test argument parsing
- Use Typer CliRunner

## Mocking and Fixtures

### Mocking External Dependencies
```python
from unittest.mock import Mock, patch

def test_service_with_mock():
    """Test service with mocked repository."""
    mock_repo = Mock()
    mock_repo.create.return_value = User(id=1, name="Test")

    service = UserService(repository=mock_repo)
    result = service.create_user(UserCreate(name="Test"))

    assert result.id == 1
    mock_repo.create.assert_called_once()
```

### Database Fixtures
```python
@pytest.fixture
def test_user(db_session):
    """Create a test user in database."""
    user = User(name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    return user
```

## Test Data Management

### Test Database Setup
```python
@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine."""
    engine = create_engine("sqlite:///./test_taskforge.db")
    Base.metadata.create_all(bind=engine)
    yield engine
    # Cleanup after all tests
    os.remove("./test_taskforge.db")
```

### Data Cleanup
```python
@pytest.fixture(autouse=True)
def clean_database(db_session):
    """Clean database before each test."""
    # Delete all data
    db_session.query(Reminder).delete()
    db_session.query(Note).delete()
    db_session.query(TaskTag).delete()
    db_session.query(Tag).delete()
    db_session.query(Task).delete()
    db_session.query(Project).delete()
    db_session.query(User).delete()
    db_session.commit()
```

## Continuous Integration

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[dev]
    - name: Run tests
      run: pytest --cov=taskforge --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## Test Coverage Goals

### Coverage Metrics
- **Unit Tests**: 90%+ coverage
- **Integration Tests**: Key workflows covered
- **API Tests**: All endpoints tested
- **CLI Tests**: All commands tested

### Coverage Report
```bash
pytest --cov=taskforge --cov-report=html
# Open htmlcov/index.html in browser
```

## Performance Testing

### Benchmark Tests
```python
import pytest_benchmark

def test_create_many_tasks(benchmark, db_session):
    """Benchmark creating many tasks."""
    def create_tasks():
        for i in range(100):
            task = Task(title=f"Task {i}")
            db_session.add(task)
        db_session.commit()

    benchmark(create_tasks)
```

## Test Organization Best Practices

### Test Naming
- `test_function_name`: Unit test for function
- `test_method_name`: Unit test for method
- `test_feature_scenario`: Integration test
- `test_api_endpoint`: API test
- `test_cli_command`: CLI test

### Test Structure
```python
def test_feature_under_test():
    """Test description."""
    # Arrange
    setup_data()

    # Act
    result = perform_action()

    # Assert
    verify_result(result)
```

### Test Isolation
- Each test should be independent
- No shared state between tests
- Use fixtures for setup/cleanup

## Debugging Tests

### Debug Failed Tests
```bash
pytest -v --tb=long --pdb
```

### Inspect Test Data
```python
def test_debug_example(db_session):
    """Example test with debugging."""
    # Add debug prints
    print(f"Database: {db_session}")

    # Use debugger
    import pdb; pdb.set_trace()

    # Your test code here
```

## Test Maintenance

### Keeping Tests Updated
- Update tests when changing functionality
- Remove obsolete tests
- Add tests for new features

### Test Code Quality
- Tests should be readable and maintainable
- Use descriptive names and docstrings
- Follow DRY principle
- Avoid test duplication

## Advanced Testing

### Property-Based Testing
```python
from hypothesis import given, strategies as st

@given(name=st.text(min_size=1, max_size=100))
def test_user_name_validation(name):
    """Test user name validation with various inputs."""
    # Test with generated data
```

### Async Testing
```python
@pytest.mark.asyncio
async def test_async_function():
    """Test async functions."""
    result = await async_function()
    assert result == expected
```

### Load Testing
```python
def test_concurrent_users(client):
    """Test API under concurrent load."""
    import concurrent.futures

    def make_request():
        return client.get("/users/")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(100)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    assert all(r.status_code == 200 for r in results)
```

## Troubleshooting

### Common Issues
- **Database locked**: Use separate test database
- **Fixture conflicts**: Ensure proper fixture scoping
- **Import errors**: Check Python path and dependencies
- **Slow tests**: Profile and optimize database operations

### Test Debugging Tips
- Use `-s` flag to see print statements
- Use `--pdb` to debug failures
- Check database state between tests
- Verify fixture setup and teardown
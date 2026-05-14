# AI Task 002: Add Task Due Date Validation

## Objective
Implement validation for task due dates to ensure they are reasonable and prevent invalid dates.

## Requirements
1. Validate due dates are not in the past (with configurable grace period)
2. Validate due dates are not too far in the future (configurable limit)
3. Add custom validation error messages
4. Update both CLI and API validation

## Technical Details
- Grace period for past dates: 1 day (configurable)
- Future limit: 1 year (configurable)
- Use Pydantic validators for API
- Custom exceptions for CLI
- Update schemas and services

## Files to Modify
- `src/taskforge/schemas/task_schema.py`
- `src/taskforge/services/task_service.py`
- `src/taskforge/exceptions.py`
- `tests/unit/test_task_service.py`
- `tests/api/test_tasks_api.py`

## Expected Behavior
```bash
# Should fail: past date
taskforge task create "Past Task" --due-date 2020-01-01

# Should succeed: future date
taskforge task create "Future Task" --due-date 2024-12-31
```

## Acceptance Criteria
- Past dates are rejected with clear error messages
- Future dates beyond limit are rejected
- Configuration is easily changeable
- Both CLI and API validation work consistently
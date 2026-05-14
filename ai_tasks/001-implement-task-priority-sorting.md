# AI Task 001: Implement Task Priority Sorting

## Objective
Implement a priority-based sorting system for tasks that allows users to view and manage tasks by their priority levels.

## Requirements
1. Add priority sorting to the task listing functionality
2. Support sorting by priority (high → medium → low)
3. Update both CLI and API interfaces
4. Add tests for the new functionality

## Technical Details
- Priority levels: high, medium, low
- Default priority: medium
- Sorting should be stable (maintain order for same priority)
- Update existing task list commands and endpoints

## Files to Modify
- `src/taskforge/services/task_service.py`
- `src/taskforge/cli/task_commands.py`
- `src/taskforge/api/routes/tasks.py`
- `tests/unit/test_task_service.py`
- `tests/cli/test_task_commands.py`
- `tests/api/test_tasks_api.py`

## Expected Behavior
```bash
# CLI: List tasks sorted by priority
taskforge task list --sort priority

# API: Get tasks with priority sorting
GET /tasks/?sort=priority
```

## Acceptance Criteria
- Tasks are sorted by priority (high first, then medium, then low)
- Sorting is applied to both CLI and API
- Tests pass for all new functionality
- No breaking changes to existing functionality
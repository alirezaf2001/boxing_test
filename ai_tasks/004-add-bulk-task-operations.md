# AI Task 004: Add Bulk Task Operations

## Objective
Implement bulk operations for tasks to allow users to perform actions on multiple tasks simultaneously.

## Requirements
1. Bulk complete tasks
2. Bulk update priority
3. Bulk add/remove tags
4. Bulk move to different project
5. Bulk delete tasks

## Technical Details
- Accept task IDs as comma-separated list or range
- Validate all tasks exist before performing operations
- Use database transactions for consistency
- Provide progress feedback for large operations

## Files to Modify
- `src/taskforge/services/task_service.py`
- `src/taskforge/cli/task_commands.py`
- `src/taskforge/api/routes/tasks.py`
- `tests/unit/test_task_service.py`
- `tests/cli/test_task_commands.py`

## Expected Behavior
```bash
# Complete multiple tasks
taskforge task complete 1,2,3,5

# Update priority for multiple tasks
taskforge task update-priority 1-10 --priority high

# Move tasks to different project
taskforge task move 1,2,3 --project 2
```

## Acceptance Criteria
- All operations support bulk actions
- Error handling for invalid task IDs
- Transactions ensure data consistency
- Progress feedback for large operations
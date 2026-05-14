# AI Task 010: Add Task Dependencies

## Objective
Implement task dependency management to allow tasks to be linked and ensure proper execution order.

## Requirements
1. Define prerequisite tasks
2. Prevent completion of tasks with unfinished dependencies
3. Visualize dependency chains
4. Detect circular dependencies
5. Dependency reports

## Technical Details
- Self-referencing many-to-many relationship
- Dependency validation
- Graph algorithms for cycle detection
- UI indicators for blocked tasks

## Files to Modify
- `src/taskforge/models/task_dependency.py`
- `src/taskforge/services/task_service.py`
- `src/taskforge/cli/task_commands.py`
- `src/taskforge/api/routes/tasks.py`

## Expected Behavior
```bash
# Add dependency
taskforge task add-dependency 2 --depends-on 1

# Try to complete task with dependencies
taskforge task complete 2  # Should fail if 1 is not complete

# View dependency graph
taskforge task dependencies 1
```

## Acceptance Criteria
- Dependencies prevent invalid completions
- Circular dependencies are detected
- Dependency chains are visualized
- Performance impact is minimal
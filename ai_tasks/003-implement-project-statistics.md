# AI Task 003: Implement Project Statistics

## Objective
Add comprehensive statistics and metrics for projects to help users track progress and productivity.

## Requirements
1. Calculate project completion rates
2. Track task counts by status and priority
3. Add time-based metrics (created this week/month)
4. Include team member contributions (future multi-user)
5. Generate project health scores

## Technical Details
- Statistics should be computed on-demand
- Cache results for performance
- Include both summary and detailed views
- Add to existing project service

## Files to Modify
- `src/taskforge/services/project_service.py`
- `src/taskforge/schemas/project_schema.py`
- `src/taskforge/cli/project_commands.py`
- `src/taskforge/api/routes/projects.py`
- `tests/unit/test_project_service.py`

## Expected Behavior
```bash
# CLI: Show project statistics
taskforge project stats 1

# Output:
# Project: My Project
# Total Tasks: 15
# Completed: 10 (67%)
# In Progress: 3
# Pending: 2
# High Priority: 5
# Health Score: 85/100
```

## Acceptance Criteria
- Statistics are accurate and up-to-date
- Performance is acceptable for large projects
- Both CLI and API provide statistics
- Health scoring algorithm is documented
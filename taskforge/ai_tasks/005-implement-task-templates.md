# AI Task 005: Implement Task Templates

## Objective
Create a system for task templates to allow users to quickly create common task types with predefined settings.

## Requirements
1. Create and manage task templates
2. Apply templates when creating tasks
3. Template includes: title, description, priority, tags, due date offset
4. Built-in templates for common task types

## Technical Details
- Templates stored in database
- Due date offsets (e.g., "in 3 days", "end of week")
- Template inheritance and customization
- CLI and API support

## Files to Modify
- `src/taskforge/models/task_template.py`
- `src/taskforge/services/task_template_service.py`
- `src/taskforge/cli/task_commands.py`
- `src/taskforge/api/routes/tasks.py`
- Database migration for new table

## Expected Behavior
```bash
# Create template
taskforge task create-template "Code Review" --description "Review pull request" --priority high --tags code-review --due-offset "1 day"

# Use template
taskforge task create-from-template "Code Review" --title "Review auth PR"

# List templates
taskforge task list-templates
```

## Acceptance Criteria
- Templates can be created, listed, and used
- Due date offsets work correctly
- Templates include all relevant task properties
- Built-in templates are available
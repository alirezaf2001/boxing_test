# CLI Guide

## Command Line Interface

TaskForge provides a comprehensive CLI for managing your productivity data directly from the terminal.

## Getting Started

```bash
# Install TaskForge
pip install -e .

# View help
taskforge --help

# Create your first user
taskforge user create "John Doe" john@example.com

# Create a project
taskforge project create "My Project" --description "A sample project"

# Add tasks
taskforge task create "Write documentation" --project 1 --priority high
taskforge task create "Review code" --due-date 2024-01-15

# View your tasks
taskforge task list

# Complete a task
taskforge task complete 1

# Generate reports
taskforge report productivity
```

## User Management

### Create User
```bash
taskforge user create "Full Name" email@example.com [--timezone UTC]
```

### Get Current User
```bash
taskforge user get
```

### Update User
```bash
taskforge user update [--name "New Name"] [--email new@example.com] [--timezone EST]
```

### Delete User
```bash
taskforge user delete
```

## Project Management

### Create Project
```bash
taskforge project create "Project Name" [--description "Description"]
```

### List Projects
```bash
taskforge project list
```

### Get Project
```bash
taskforge project get PROJECT_ID
```

### Update Project
```bash
taskforge project update PROJECT_ID [--name "New Name"] [--description "New Description"]
```

### Archive Project
```bash
taskforge project archive PROJECT_ID
```

### Delete Project
```bash
taskforge project delete PROJECT_ID
```

## Task Management

### Create Task
```bash
taskforge task create "Task Title" [--description "Description"] [--project PROJECT_ID] [--priority low|medium|high] [--due-date YYYY-MM-DD]
```

### List Tasks
```bash
taskforge task list [--project PROJECT_ID] [--status pending|completed] [--priority low|medium|high]
```

### Get Task
```bash
taskforge task get TASK_ID
```

### Update Task
```bash
taskforge task update TASK_ID [--title "New Title"] [--description "New Description"] [--priority low|medium|high] [--due-date YYYY-MM-DD]
```

### Complete Task
```bash
taskforge task complete TASK_ID
```

### Search Tasks
```bash
taskforge task search "search term"
```

### Delete Task
```bash
taskforge task delete TASK_ID
```

## Tag Management

### Create Tag
```bash
taskforge tag create "Tag Name" [--color "#FF0000"]
```

### List Tags
```bash
taskforge tag list
```

### Add Tag to Task
```bash
taskforge tag add TASK_ID TAG_ID
```

### Remove Tag from Task
```bash
taskforge tag remove TASK_ID TAG_ID
```

## Note Management

### Create Note
```bash
taskforge note create "Note Title" "Note Content" [--task TASK_ID] [--project PROJECT_ID]
```

### List Notes
```bash
taskforge note list [--task TASK_ID] [--project PROJECT_ID]
```

### Get Note
```bash
taskforge note get NOTE_ID
```

### Update Note
```bash
taskforge note update NOTE_ID [--title "New Title"] [--content "New Content"]
```

### Delete Note
```bash
taskforge note delete NOTE_ID
```

## Reminder Management

### Create Reminder
```bash
taskforge reminder create "Reminder Title" "YYYY-MM-DD HH:MM" [--task TASK_ID] [--note "Additional note"]
```

### List Reminders
```bash
taskforge reminder list [--upcoming] [--overdue]
```

### Get Reminder
```bash
taskforge reminder get REMINDER_ID
```

### Update Reminder
```bash
taskforge reminder update REMINDER_ID [--title "New Title"] [--datetime "YYYY-MM-DD HH:MM"]
```

### Complete Reminder
```bash
taskforge reminder complete REMINDER_ID
```

### Delete Reminder
```bash
taskforge reminder delete REMINDER_ID
```

## Reporting

### Productivity Report
```bash
taskforge report productivity [--start-date YYYY-MM-DD] [--end-date YYYY-MM-DD]
```

### Project Report
```bash
taskforge report projects [--archived]
```

### Task Report
```bash
taskforge report tasks [--status pending|completed] [--priority low|medium|high]
```

### Export Reports
```bash
# Export productivity report
taskforge report export-productivity --format json|csv [--output-file report.json]

# Export project report
taskforge report export-projects --format json|csv [--output-file projects.json]
```

## Advanced Usage

### Filtering and Searching
```bash
# List high priority tasks
taskforge task list --priority high

# Search for tasks containing "urgent"
taskforge task search urgent

# List upcoming reminders
taskforge reminder list --upcoming
```

### Batch Operations
```bash
# Complete multiple tasks (requires scripting)
for id in 1 2 3; do taskforge task complete $id; done
```

### Configuration
```bash
# Set environment variables
export TASKFORGE_DATABASE_URL="sqlite:///custom.db"
export TASKFORGE_TIMEZONE="America/New_York"
```

## Exit Codes

- `0`: Success
- `1`: General error
- `2`: Validation error
- `3`: Not found error

## Tips

- Use `--help` with any command to see detailed options
- Commands support tab completion in supported shells
- All dates should be in YYYY-MM-DD format
- All datetimes should be in YYYY-MM-DD HH:MM format
- IDs are auto-incrementing integers starting from 1
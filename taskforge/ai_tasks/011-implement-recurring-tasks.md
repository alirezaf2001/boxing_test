# AI Task 011: Implement Recurring Tasks

## Objective
Add support for recurring tasks that automatically create new instances based on schedules.

## Requirements
1. Define recurrence patterns (daily, weekly, monthly)
2. Automatic task creation
3. Completion tracking for recurring tasks
4. Recurrence customization
5. Skip/next occurrence management

## Technical Details
- Recurrence rules (RRULE-like syntax)
- Background job processing
- Instance vs template distinction
- Completion affects future instances

## Files to Modify
- `src/taskforge/models/recurring_task.py`
- `src/taskforge/services/recurring_service.py`
- `src/taskforge/cli/task_commands.py`
- Background job system

## Expected Behavior
```bash
# Create recurring task
taskforge task create-recurring "Daily standup" --schedule "daily" --time "09:00"

# Complete instance (creates next)
taskforge task complete 1

# Skip next occurrence
taskforge task skip-next 1
```

## Acceptance Criteria
- Tasks are created automatically
- Recurrence patterns work correctly
- Users can manage recurring tasks
- System handles edge cases (weekends, holidays)
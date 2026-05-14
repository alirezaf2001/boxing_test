# AI Task 006: Add Time Tracking

## Objective
Implement time tracking functionality to allow users to log time spent on tasks and projects.

## Requirements
1. Start/stop time tracking on tasks
2. Log time entries with descriptions
3. View time reports by task/project
4. Calculate total time spent
5. Export time tracking data

## Technical Details
- Time entries stored in separate table
- Support for ongoing timers
- Time calculations in hours/minutes
- Integration with existing reporting

## Files to Modify
- `src/taskforge/models/time_entry.py`
- `src/taskforge/services/time_service.py`
- `src/taskforge/cli/task_commands.py`
- `src/taskforge/api/routes/tasks.py`
- `src/taskforge/api/routes/reports.py`

## Expected Behavior
```bash
# Start tracking time
taskforge task start-timer 1

# Stop tracking
taskforge task stop-timer 1 --description "Fixed login bug"

# View time spent
taskforge task time-report 1

# Project time report
taskforge report project-time 1
```

## Acceptance Criteria
- Time tracking works accurately
- Multiple timers can run (future enhancement)
- Time reports are detailed and accurate
- Data can be exported
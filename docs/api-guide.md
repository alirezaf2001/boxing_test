# API Guide

## REST API Documentation

TaskForge provides a RESTful API for programmatic access to all features.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required. This is suitable for local development.

## API Endpoints

### Users

#### Create User
```http
POST /users/
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "timezone": "UTC"
}
```

#### Get User
```http
GET /users/
```

#### Update User
```http
PUT /users/
Content-Type: application/json

{
  "name": "Jane Doe",
  "timezone": "EST"
}
```

#### Delete User
```http
DELETE /users/
```

### Projects

#### Create Project
```http
POST /projects/
Content-Type: application/json

{
  "name": "My Project",
  "description": "Project description"
}
```

#### List Projects
```http
GET /projects/
```

#### Get Project
```http
GET /projects/{project_id}
```

#### Update Project
```http
PUT /projects/{project_id}
Content-Type: application/json

{
  "name": "Updated Name",
  "description": "Updated description"
}
```

#### Archive Project
```http
PUT /projects/{project_id}/archive
```

#### Delete Project
```http
DELETE /projects/{project_id}
```

### Tasks

#### Create Task
```http
POST /tasks/
Content-Type: application/json

{
  "title": "Task Title",
  "description": "Task description",
  "project_id": 1,
  "priority": "high",
  "due_date": "2024-01-15"
}
```

#### List Tasks
```http
GET /tasks/?project_id=1&status=pending&priority=high
```

#### Get Task
```http
GET /tasks/{task_id}
```

#### Update Task
```http
PUT /tasks/{task_id}
Content-Type: application/json

{
  "title": "Updated Title",
  "priority": "medium"
}
```

#### Complete Task
```http
PUT /tasks/{task_id}/complete
```

#### Search Tasks
```http
GET /tasks/search/{query}
```

#### Delete Task
```http
DELETE /tasks/{task_id}
```

### Tags

#### Create Tag
```http
POST /tags/
Content-Type: application/json

{
  "name": "urgent",
  "color": "#FF0000"
}
```

#### List Tags
```http
GET /tags/
```

#### Get Tag
```http
GET /tags/{tag_id}
```

#### Update Tag
```http
PUT /tags/{tag_id}
Content-Type: application/json

{
  "name": "important",
  "color": "#00FF00"
}
```

#### Delete Tag
```http
DELETE /tags/{tag_id}
```

#### Add Tag to Task
```http
POST /tasks/{task_id}/tags/{tag_id}
```

#### Remove Tag from Task
```http
DELETE /tasks/{task_id}/tags/{tag_id}
```

### Notes

#### Create Note
```http
POST /notes/
Content-Type: application/json

{
  "title": "Meeting Notes",
  "content": "Discussion points...",
  "task_id": 1,
  "project_id": 1
}
```

#### List Notes
```http
GET /notes/?task_id=1&project_id=1
```

#### Get Note
```http
GET /notes/{note_id}
```

#### Update Note
```http
PUT /notes/{note_id}
Content-Type: application/json

{
  "title": "Updated Notes",
  "content": "Updated content..."
}
```

#### Delete Note
```http
DELETE /notes/{note_id}
```

### Reminders

#### Create Reminder
```http
POST /reminders/
Content-Type: application/json

{
  "title": "Call client",
  "reminder_datetime": "2024-01-15T10:00:00",
  "task_id": 1,
  "note": "Discuss project status"
}
```

#### List Reminders
```http
GET /reminders/?upcoming=true&overdue=false
```

#### Get Reminder
```http
GET /reminders/{reminder_id}
```

#### Update Reminder
```http
PUT /reminders/{reminder_id}
Content-Type: application/json

{
  "title": "Updated reminder",
  "reminder_datetime": "2024-01-15T11:00:00"
}
```

#### Complete Reminder
```http
PUT /reminders/{reminder_id}/complete
```

#### Delete Reminder
```http
DELETE /reminders/{reminder_id}
```

### Reports

#### Productivity Report
```http
GET /reports/productivity?start_date=2024-01-01&end_date=2024-01-31
```

#### Project Report
```http
GET /reports/projects?archived=false
```

#### Task Report
```http
GET /reports/tasks?status=completed&priority=high
```

#### Export Productivity Report
```http
GET /reports/productivity/export?format=json&start_date=2024-01-01&end_date=2024-01-31
```

#### Export Project Report
```http
GET /reports/projects/export?format=csv&archived=false
```

## Response Formats

### Success Response
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Error Response
```json
{
  "detail": "User not found"
}
```

### List Response
```json
[
  {
    "id": 1,
    "name": "Project 1",
    "description": "Description",
    "archived": false
  },
  {
    "id": 2,
    "name": "Project 2",
    "description": "Description",
    "archived": false
  }
]
```

## HTTP Status Codes

- `200`: Success
- `201`: Created
- `400`: Bad Request
- `404`: Not Found
- `422`: Validation Error
- `500`: Internal Server Error

## Data Types

### Priority
- `low`
- `medium`
- `high`

### Status
- `pending`
- `completed`

### Date Format
- `YYYY-MM-DD`

### DateTime Format
- `YYYY-MM-DDTHH:MM:SS` (ISO 8601)

### Export Formats
- `json`
- `csv`

## Pagination

List endpoints support pagination:

```http
GET /tasks/?skip=0&limit=10
```

Parameters:
- `skip`: Number of items to skip (default: 0)
- `limit`: Maximum number of items to return (default: 100)

## Filtering

Most list endpoints support filtering:

```http
GET /tasks/?project_id=1&status=pending&priority=high
```

## Validation

The API uses Pydantic for request validation. Invalid requests will return a 422 status code with detailed error information.

## Rate Limiting

Currently, no rate limiting is implemented.

## CORS

CORS is enabled for local development. In production, configure appropriate origins.

## OpenAPI Documentation

When running the API server, visit `/docs` for interactive API documentation powered by Swagger UI.

## Examples

### Python Client
```python
import requests

# Create a task
response = requests.post("http://localhost:8000/tasks/", json={
    "title": "New Task",
    "description": "Task description"
})
task = response.json()

# Get all tasks
response = requests.get("http://localhost:8000/tasks/")
tasks = response.json()

# Complete a task
requests.put(f"http://localhost:8000/tasks/{task['id']}/complete")
```

### cURL Examples
```bash
# Create user
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "email": "john@example.com"}'

# List tasks
curl "http://localhost:8000/tasks/"

# Get productivity report
curl "http://localhost:8000/reports/productivity"
```
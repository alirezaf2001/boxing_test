# TaskForge

A local productivity and workflow management application built with Python. TaskForge helps you manage tasks, projects, notes, reminders, and more through both a command-line interface and a lightweight web API.

## Features

- **User Profile Management**: Create and manage local user profiles with settings
- **Project Management**: Organize tasks into projects
- **Task Management**: Create, edit, prioritize, and track tasks
- **Tag System**: Categorize tasks with custom tags
- **Notes System**: Attach notes to projects and tasks
- **Reminder System**: Set and manage reminders for tasks
- **Reporting**: Generate productivity reports and summaries
- **CLI Interface**: Full command-line interface using Typer
- **Web API**: RESTful API built with FastAPI
- **Local Storage**: SQLite database for all data

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

### Install from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/taskforge.git
   cd taskforge
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```

3. (Optional) Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Usage

### Command Line Interface

TaskForge provides a comprehensive CLI for all operations:

```bash
# Initialize user profile
taskforge user create --name "John Doe" --email "john@example.com"

# Create a project
taskforge project create "Work Project"

# Add a task
taskforge task create "Finish report" --project "Work Project" --priority high --due-date 2024-01-15

# List tasks
taskforge task list --status active

# Generate a weekly report
taskforge report weekly
```

### Web API

Start the web server:

```bash
uvicorn taskforge.api.main:app --reload
```

The API will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for interactive API documentation.

### API Examples

```bash
# Get all tasks
curl http://localhost:8000/tasks/

# Create a new task
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "New Task", "description": "Task description", "priority": "medium"}'
```

## Project Structure

```
taskforge/
├── src/taskforge/
│   ├── cli/           # Command-line interface commands
│   ├── api/           # FastAPI application and routes
│   ├── models/        # SQLAlchemy database models
│   ├── schemas/       # Pydantic schemas for validation
│   ├── repositories/  # Data access layer
│   ├── services/      # Business logic layer
│   ├── exporters/     # Data export utilities
│   └── utils/         # Utility functions
├── tests/             # Test suite
├── docs/              # Documentation
├── scripts/           # Utility scripts
└── ai_tasks/          # Tasks for AI coding agent testing
```

## Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type checking
mypy src/
```

### Database

TaskForge uses SQLite for local storage. The database file is created automatically in the user's data directory.

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.
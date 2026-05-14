# Database Design

## Database Schema

TaskForge uses SQLite as its database engine with SQLAlchemy ORM for data persistence.

## Core Tables

### users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    timezone VARCHAR(50) DEFAULT 'UTC',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### projects
```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    archived BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### tasks
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    project_id INTEGER,
    priority VARCHAR(10) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high')),
    status VARCHAR(10) DEFAULT 'pending' CHECK (status IN ('pending', 'completed')),
    due_date DATE,
    completed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
);
```

### tags
```sql
CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    color VARCHAR(7) DEFAULT '#808080',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### task_tags
```sql
CREATE TABLE task_tags (
    task_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (task_id, tag_id),
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);
```

### notes
```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    task_id INTEGER,
    project_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);
```

### reminders
```sql
CREATE TABLE reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    reminder_datetime DATETIME NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    completed_at DATETIME,
    task_id INTEGER,
    note TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);
```

## Relationships

### Entity Relationship Diagram

```
users (1) ──── (0..*) tasks
projects (1) ──── (0..*) tasks
projects (1) ──── (0..*) notes
tasks (1) ──── (0..*) notes
tasks (1) ──── (0..*) task_tags (0..*) ──── (1) tags
tasks (1) ──── (0..*) reminders
```

## Indexes

### Performance Indexes
```sql
-- Task queries by project
CREATE INDEX idx_tasks_project_id ON tasks(project_id);

-- Task queries by status
CREATE INDEX idx_tasks_status ON tasks(status);

-- Task queries by priority
CREATE INDEX idx_tasks_priority ON tasks(priority);

-- Task queries by due date
CREATE INDEX idx_tasks_due_date ON tasks(due_date);

-- Notes by task
CREATE INDEX idx_notes_task_id ON notes(task_id);

-- Notes by project
CREATE INDEX idx_notes_project_id ON notes(project_id);

-- Reminders by datetime
CREATE INDEX idx_reminders_datetime ON reminders(reminder_datetime);

-- Reminders by task
CREATE INDEX idx_reminders_task_id ON reminders(task_id);

-- Task-tag relationships
CREATE INDEX idx_task_tags_task_id ON task_tags(task_id);
CREATE INDEX idx_task_tags_tag_id ON task_tags(tag_id);
```

## Constraints

### Check Constraints
- `tasks.priority`: Must be 'low', 'medium', or 'high'
- `tasks.status`: Must be 'pending' or 'completed'

### Foreign Key Constraints
- Tasks reference projects (nullable)
- Notes reference tasks and projects (nullable)
- Reminders reference tasks (nullable)
- Task-tags reference both tasks and tags

### Unique Constraints
- User emails must be unique
- Tag names must be unique

## Data Types

### SQLite Data Types Used
- `INTEGER`: Auto-incrementing primary keys, foreign keys, boolean flags
- `VARCHAR(n)`: Fixed-length strings (names, emails, priorities)
- `TEXT`: Unlimited text (descriptions, content, notes)
- `DATE`: Date-only fields (due dates)
- `DATETIME`: Timestamp fields (creation, updates, reminders)
- `BOOLEAN`: True/false flags (archived, completed)

## Migration Strategy

### Current State
- No migration system implemented yet
- Schema changes require manual database recreation
- Suitable for development and single-user applications

### Future Enhancements
- Implement Alembic for schema migrations
- Version control database schema changes
- Support for production deployments

## Database Configuration

### Connection Settings
```python
# Default SQLite database
DATABASE_URL = "sqlite:///./taskforge.db"

# Alternative configurations
# PostgreSQL: "postgresql://user:password@localhost/taskforge"
# MySQL: "mysql://user:password@localhost/taskforge"
```

### Connection Pooling
- SQLite uses file-based locking (no pooling needed)
- Future database engines will use SQLAlchemy connection pooling

## Backup and Recovery

### Backup Strategy
```bash
# Simple file copy for SQLite
cp taskforge.db taskforge.db.backup

# With timestamp
cp taskforge.db "taskforge_$(date +%Y%m%d_%H%M%S).db"
```

### Recovery
```bash
# Restore from backup
cp taskforge.db.backup taskforge.db
```

## Performance Considerations

### Query Optimization
- Use indexes for frequently queried columns
- Avoid N+1 queries with eager loading
- Use pagination for large result sets

### Database Size
- SQLite databases can grow to several GB
- Regular cleanup of old data may be needed
- Consider archiving completed tasks after a period

## Security

### Data Protection
- SQLite files should be properly secured
- Database files contain sensitive user data
- Implement proper file permissions

### SQL Injection
- All queries use SQLAlchemy ORM or parameterized queries
- No direct SQL string concatenation

## Monitoring

### Database Metrics
- File size monitoring
- Query performance logging
- Connection status monitoring

### Health Checks
```python
# Basic connectivity check
def check_database_health():
    try:
        db.execute("SELECT 1")
        return True
    except Exception:
        return False
```

## Development Tools

### Database Browser
- Use DB Browser for SQLite for schema inspection
- SQLite command-line client for advanced queries

### Schema Visualization
- Generate ER diagrams from SQLAlchemy models
- Use tools like ERwin or draw.io for documentation

## Testing

### Test Database
- Separate test database file
- Automatic cleanup between tests
- Use pytest fixtures for database setup

### Database Fixtures
```python
@pytest.fixture
def test_db():
    # Create test database
    # Yield for test execution
    # Cleanup after test
```

## Future Improvements

### Planned Enhancements
- Database migrations with Alembic
- Support for PostgreSQL/MySQL
- Database encryption
- Automated backups
- Query performance monitoring
- Database sharding (if needed)
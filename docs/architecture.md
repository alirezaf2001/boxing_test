# Architecture Overview

## System Architecture

TaskForge is built using a modular, layered architecture that separates concerns and promotes maintainability and testability.

### Core Components

#### 1. **Models Layer** (`src/taskforge/models/`)
- SQLAlchemy ORM models for database entities
- Defines relationships between entities
- Handles data persistence

#### 2. **Schemas Layer** (`src/taskforge/schemas/`)
- Pydantic models for data validation and serialization
- API request/response schemas
- Data transfer objects

#### 3. **Repositories Layer** (`src/taskforge/repositories/`)
- Data access layer
- CRUD operations for each entity
- Database query abstractions

#### 4. **Services Layer** (`src/taskforge/services/`)
- Business logic layer
- Validation and business rules
- Orchestrates repository operations

#### 5. **API Layer** (`src/taskforge/api/`)
- FastAPI REST endpoints
- Request routing and response handling
- Dependency injection

#### 6. **CLI Layer** (`src/taskforge/cli/`)
- Typer command-line interface
- User interaction commands
- Service orchestration

### Data Flow

```
CLI/API Request → Service → Repository → Database
                      ↓
                Validation & Business Logic
```

### Key Design Patterns

- **Repository Pattern**: Abstracts data access operations
- **Service Layer**: Contains business logic and validation
- **Dependency Injection**: Services receive dependencies
- **Factory Pattern**: Object creation through services

### Database Design

- **SQLite**: Local file-based database
- **SQLAlchemy ORM**: Object-relational mapping
- **Migrations**: Schema versioning (future enhancement)

### Configuration Management

- **Pydantic Settings**: Environment-based configuration
- **Environment Variables**: Runtime configuration
- **Default Values**: Sensible defaults for development

### Error Handling

- **Custom Exceptions**: Domain-specific error types
- **HTTP Status Codes**: RESTful API responses
- **CLI Exit Codes**: Command-line error reporting

### Testing Strategy

- **Unit Tests**: Individual component testing
- **Integration Tests**: Database and service integration
- **API Tests**: Endpoint testing
- **CLI Tests**: Command testing

### Dependencies

- **FastAPI**: Web framework
- **Typer**: CLI framework
- **SQLAlchemy**: ORM
- **Pydantic**: Data validation
- **pytest**: Testing framework
- **ruff**: Linting and formatting
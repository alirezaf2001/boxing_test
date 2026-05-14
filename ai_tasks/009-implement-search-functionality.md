# AI Task 009: Implement Advanced Search

## Objective
Add powerful search functionality to find tasks, projects, notes, and other content across the application.

## Requirements
1. Full-text search across all content
2. Search filters (date range, status, priority)
3. Search suggestions and autocomplete
4. Saved searches
5. Search result highlighting

## Technical Details
- Use SQLite FTS (Full-Text Search)
- Search across multiple tables
- Weighted search results
- Search query parsing

## Files to Modify
- `src/taskforge/services/search_service.py` (enhance existing)
- `src/taskforge/cli/search_commands.py`
- `src/taskforge/api/routes/search.py`
- Database schema for FTS tables

## Expected Behavior
```bash
# Search all content
taskforge search "urgent project"

# Search with filters
taskforge search "bug" --status pending --priority high

# Save search
taskforge search save "my search" "important tasks"
```

## Acceptance Criteria
- Search finds relevant results quickly
- Filters work correctly
- Search syntax is intuitive
- Performance is good for large datasets
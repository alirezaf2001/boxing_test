"""FastAPI application setup."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from taskforge.api.routes import (
    users,
    projects,
    tasks,
    tags,
    notes,
    reminders,
    reports,
)
from taskforge.database import create_tables

# Create database tables
create_tables()

app = FastAPI(
    title="TaskForge API",
    description="A REST API for TaskForge productivity management",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(tags.router, prefix="/tags", tags=["tags"])
app.include_router(notes.router, prefix="/notes", tags=["notes"])
app.include_router(reminders.router, prefix="/reminders", tags=["reminders"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to TaskForge API", "version": "0.1.0"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
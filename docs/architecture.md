# BookCircle Architecture

## High-Level Architecture

```text
Browser UI (HTML/CSS/JS + Jinja2)
        |
        v
FastAPI Routers (Presentation Layer)
        |
        v
Service Layer (Business Logic)
        |
        v
SQLAlchemy ORM / Database Access Layer
        |
        v
SQLite Database
```

## Layer Responsibilities

- Presentation: route handlers, templates, forms, rendering.
- Business: book lending rules, request approval rules, loan lifecycle.
- Data access: SQLAlchemy models and session management.
- Persistence: SQLite database.

## Feature Decomposition

- Authentication
- Book management
- Borrow request workflow
- Loan management
- Admin moderation

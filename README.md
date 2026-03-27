# BookCircle

BookCircle is a neighborhood book-lending web application built with FastAPI, Jinja2, SQLAlchemy, and SQLite for the **Software Architectures** course project.

## Features

1. User registration and login
2. Add and browse books
3. Borrow request workflow
4. Loan approval and return handling
5. Admin moderation

## User Roles

- Member
- Admin

## Architecture

- **Presentation layer:** FastAPI routers + Jinja2 templates
- **Business layer:** service modules
- **Data layer:** SQLAlchemy ORM
- **Persistence layer:** SQLite

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python -m app.seed
uvicorn app.main:app --reload
```

## Demo Accounts

- Admin: `admin@bookcircle.local` / `admin123`
- Member: `member@bookcircle.local` / `member123`

## OpenAPI

FastAPI automatically provides:
- `/docs`
- `/openapi.json`

A generated API contract is also included at `docs/openapi.json`.

## Project Documents

- `docs/architecture.md`
- `docs/error-taxonomy.md`
- `docs/threat-model.md`
- `docs/adr/`
- `docs/prompt-log.md`

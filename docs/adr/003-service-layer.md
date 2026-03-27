# ADR 003: Use a Dedicated Service Layer

## Status
Accepted

## Context
Business rules such as borrow approvals and returns should not be embedded directly in route handlers.

## Decision
Put core business logic in service modules.

## Consequences
- Cleaner routers
- Better separation of concerns
- Easier testing and maintenance

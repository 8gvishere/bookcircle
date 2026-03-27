# Threat Model

## Main Threats

1. Unauthorized access to protected pages
2. User modifying resources they do not own
3. Bad input in forms
4. Weak password handling
5. Data inconsistency in request/loan state changes

## Mitigations

- JWT stored in HTTP-only cookie
- role and ownership checks
- Pydantic and form validation
- bcrypt password hashing
- service-layer business rules

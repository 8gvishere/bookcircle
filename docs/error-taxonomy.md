# Error Taxonomy

## Categories

- Validation Error (400)
- Authentication Error (401)
- Permission Error (403)
- Not Found Error (404)
- Conflict Error (409)
- Internal Server Error (500)

## Strategy

All application errors return:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message"
  }
}
```

## Examples

- invalid login credentials -> AUTH_ERROR
- deleting another user's book -> PERMISSION_ERROR
- duplicate borrow request -> CONFLICT

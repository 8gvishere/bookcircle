from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    def __init__(self, status_code: int, code: str, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(message)


class ValidationAppError(AppError):
    def __init__(self, message: str = "Validation failed"):
        super().__init__(400, "VALIDATION_ERROR", message)


class AuthAppError(AppError):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(401, "AUTH_ERROR", message)


class PermissionAppError(AppError):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(403, "PERMISSION_ERROR", message)


class NotFoundAppError(AppError):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(404, "NOT_FOUND", message)


class ConflictAppError(AppError):
    def __init__(self, message: str = "Conflict"):
        super().__init__(409, "CONFLICT", message)


async def app_error_handler(_: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )

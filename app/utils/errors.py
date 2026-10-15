"""Custom exception classes for the application."""


class AppError(Exception):
    """Base application error."""

    code = "APP_ERROR"
    message = "An application error occurred"
    status_code = 500

    def __init__(self, message=None, details=None, code=None, status_code=None):
        super().__init__(message or self.message)
        if message:
            self.message = message
        if code:
            self.code = code
        if status_code:
            self.status_code = status_code
        self.details = details


class ValidationError(AppError):
    """Request validation error."""

    code = "VALIDATION_ERROR"
    message = "Invalid request parameters"
    status_code = 400


class NotFoundError(AppError):
    """Resource not found."""

    code = "NOT_FOUND"
    message = "Resource not found"
    status_code = 404


class ConflictError(AppError):
    """Resource conflict (e.g., duplicate, illegal state transition)."""

    code = "CONFLICT"
    message = "Resource conflict"
    status_code = 409


class ForbiddenError(AppError):
    """Operation not allowed."""

    code = "FORBIDDEN"
    message = "Operation not allowed"
    status_code = 403


class UnauthorizedError(AppError):
    """Authentication required."""

    code = "UNAUTHORIZED"
    message = "Authentication required"
    status_code = 401


class ExternalServiceError(AppError):
    """External service error (RSS feed, AI provider, platform API)."""

    code = "EXTERNAL_SERVICE_ERROR"
    message = "External service error"
    status_code = 502


class ProviderNotConfiguredError(AppError):
    """AI provider not configured."""

    code = "PROVIDER_NOT_CONFIGURED"
    message = "AI provider is not configured"
    status_code = 503

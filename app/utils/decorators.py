"""Decorators for API authentication."""
from functools import wraps

from flask import request, g

from app.services.auth_service import AuthService
from app.utils.responses import error_response


def auth_required(f):
    """Decorator that requires a valid JWT token in Authorization header.

    Extracts Bearer token from the Authorization header, verifies it,
    and stores the user in flask.g.current_user.

    Returns:
        401 error response if token is missing, invalid, or expired.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return error_response(
                code="UNAUTHORIZED",
                message="Missing or invalid Authorization header. Use 'Bearer <token>'.",
                status_code=401,
            )

        token = auth_header[7:]  # Strip "Bearer "
        try:
            user = AuthService.verify_token(token)
        except Exception as e:
            return error_response(
                code="UNAUTHORIZED",
                message=str(e.message) if hasattr(e, "message") else str(e),
                status_code=401,
            )

        g.current_user = user
        return f(*args, **kwargs)

    return decorated

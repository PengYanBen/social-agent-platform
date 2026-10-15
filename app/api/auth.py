"""Authentication blueprint - register, login, me."""
from flask import Blueprint, request, g

from app.services.auth_service import AuthService
from app.utils.decorators import auth_required
from app.utils.responses import success_response, error_response
from app.utils.errors import ValidationError, ConflictError, UnauthorizedError

bp = Blueprint("auth", __name__)


@bp.route("/api/v1/auth/register", methods=["POST"])
def register():
    """Register a new user.

    Request body:
        username: Desired username.
        email: User email.
        password: Plaintext password (min 6 chars).

    Returns:
        201 with user data, or 400/409 on error.
    """
    data = request.get_json(silent=True) or {}
    try:
        user = AuthService.register(
            username=data.get("username", ""),
            email=data.get("email", ""),
            password=data.get("password", ""),
        )
    except ConflictError as e:
        return error_response(
            code=e.code, message=e.message, status_code=e.status_code
        )
    except ValidationError as e:
        return error_response(
            code=e.code, message=e.message, status_code=e.status_code
        )
    return success_response(data=user.to_dict(), status_code=201)


@bp.route("/api/v1/auth/login", methods=["POST"])
def login():
    """Login and receive JWT token.

    Request body:
        username: Username or email.
        password: Plaintext password.

    Returns:
        200 with token and user data, or 401 on error.
    """
    data = request.get_json(silent=True) or {}
    try:
        result = AuthService.login(
            username_or_email=data.get("username", ""),
            password=data.get("password", ""),
        )
    except UnauthorizedError as e:
        return error_response(
            code=e.code, message=e.message, status_code=e.status_code
        )
    return success_response(data=result)


@bp.route("/api/v1/auth/me", methods=["GET"])
@auth_required
def me():
    """Get current authenticated user info.

    Requires:
        Authorization: Bearer <token>

    Returns:
        200 with user data, or 401 if not authenticated.
    """
    return success_response(data=g.current_user.to_dict())
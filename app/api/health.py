"""Health check blueprint."""
from flask import Blueprint

from app.utils.responses import success_response

bp = Blueprint("health", __name__)


@bp.route("/api/v1/health", methods=["GET"])
def health_check():
    """Health check endpoint.

    Returns:
        JSON with service status.
    """
    return success_response(
        data={"status": "ok", "service": "social-agent-platform"},
        status_code=200,
    )
"""Utility functions for consistent API responses."""
from flask import jsonify


def success_response(data=None, meta=None, status_code=200):
    """Return a unified success JSON response.

    Args:
        data: The response data payload.
        meta: Optional metadata (pagination, etc.).
        status_code: HTTP status code.

    Returns:
        Flask Response with JSON body.
    """
    body = {"success": True, "data": data if data is not None else {}}
    if meta is not None:
        body["meta"] = meta
    return jsonify(body), status_code


def error_response(code, message, details=None, status_code=400):
    """Return a unified error JSON response.

    Args:
        code: Machine-readable error code string.
        message: Human-readable error message.
        details: Optional additional error details.
        status_code: HTTP status code.

    Returns:
        Flask Response with JSON body.
    """
    body = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        },
    }
    if details is not None:
        body["error"]["details"] = details
    return jsonify(body), status_code


def paginated_response(items, total, page, per_page):
    """Return a paginated success response.

    Args:
        items: List of serialized items.
        total: Total number of items.
        page: Current page number.
        per_page: Items per page.

    Returns:
        Flask Response with JSON body.
    """
    return success_response(
        data=items,
        meta={
            "pagination": {
                "total": total,
                "page": page,
                "per_page": per_page,
                "pages": (total + per_page - 1) // per_page if per_page > 0 else 0,
            }
        },
    )

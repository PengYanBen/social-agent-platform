"""Projects blueprint - CRUD for operational projects."""
from flask import Blueprint, request

from app.extensions import db
from app.models.project import Project
from app.utils.responses import success_response, paginated_response
from app.utils.errors import NotFoundError, ValidationError

bp = Blueprint("projects", __name__)


@bp.route("/api/v1/projects", methods=["GET"])
def list_projects():
    """List projects with pagination."""
    page = int(request.args.get("page", 1))
    per_page = min(int(request.args.get("per_page", 20)), 100)

    query = Project.query.filter_by(is_active=True)
    total = query.count()
    projects = query.offset((page - 1) * per_page).limit(per_page).all()

    return paginated_response(
        [serialize_project(p) for p in projects], total, page, per_page
    )


@bp.route("/api/v1/projects", methods=["POST"])
def create_project():
    """Create a new project."""
    data = request.get_json()
    if not data or not data.get("name"):
        raise ValidationError(message="Project name is required")

    project = Project(
        name=data["name"],
        niche=data.get("niche"),
        audience=data.get("audience"),
        language=data.get("language", "zh"),
        timezone=data.get("timezone", "UTC"),
        settings_json=data.get("settings_json"),
    )
    db.session.add(project)
    db.session.commit()

    return success_response(serialize_project(project), status_code=201)


@bp.route("/api/v1/projects/<project_id>", methods=["GET"])
def get_project(project_id):
    """Get project details."""
    project = Project.query.get(project_id)
    if not project or not project.is_active:
        raise NotFoundError(message="Project not found")
    return success_response(serialize_project(project))


@bp.route("/api/v1/projects/<project_id>", methods=["PATCH"])
def update_project(project_id):
    """Update a project."""
    project = Project.query.get(project_id)
    if not project or not project.is_active:
        raise NotFoundError(message="Project not found")

    data = request.get_json()
    if not data:
        raise ValidationError(message="No data provided")

    for field in ["name", "niche", "audience", "language", "timezone", "settings_json"]:
        if field in data:
            setattr(project, field, data[field])

    db.session.commit()
    return success_response(serialize_project(project))


@bp.route("/api/v1/projects/<project_id>", methods=["DELETE"])
def delete_project(project_id):
    """Soft-delete a project."""
    project = Project.query.get(project_id)
    if not project or not project.is_active:
        raise NotFoundError(message="Project not found")

    project.is_active = False
    db.session.commit()
    return success_response(data={"id": project_id, "deleted": True})


def serialize_project(p):
    """Serialize a project to dict."""
    return {
        "id": p.id,
        "name": p.name,
        "niche": p.niche,
        "audience": p.audience,
        "language": p.language,
        "timezone": p.timezone,
        "is_active": p.is_active,
        "created_at": p.created_at.isoformat() if p.created_at else None,
        "updated_at": p.updated_at.isoformat() if p.updated_at else None,
    }
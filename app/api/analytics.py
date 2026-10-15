"""Analytics blueprint - metrics overview, per-post metrics, and review reports."""
from flask import Blueprint, request

from app.extensions import db
from app.models.post import PublishedPost, ScheduledPost
from app.models.metric_snapshot import MetricSnapshot
from app.utils.responses import success_response, paginated_response
from app.utils.errors import NotFoundError, ValidationError
from app.services.analytics_service import AnalyticsService

bp = Blueprint("analytics", __name__)


@bp.route("/api/v1/analytics/overview", methods=["GET"])
def overview():
    """Get analytics overview across posts."""
    account_id = request.args.get("account_id")
    result = AnalyticsService.get_overview(account_id=account_id)
    return success_response(data=result)


@bp.route("/api/v1/analytics/posts/<post_id>", methods=["GET"])
def post_metrics(post_id):
    """Get metrics for a specific post."""
    post = PublishedPost.query.get(post_id)
    if not post:
        raise NotFoundError(message="Published post not found")

    snapshots = MetricSnapshot.query.filter_by(published_post_id=post_id).order_by(
        MetricSnapshot.captured_at.desc()
    ).all()

    return success_response(
        {
            "post_id": post_id,
            "platform_post_id": post.platform_post_id,
            "post_url": post.post_url,
            "status": post.status,
            "is_mock": post.is_mock,
            "snapshots": [
                {
                    "id": s.id,
                    "captured_at": s.captured_at.isoformat() if s.captured_at else None,
                    "metrics_json": s.metrics_json,
                    "source": s.source,
                    "is_mock": s.is_mock,
                    "engagement_rate": s.engagement_rate,
                    "click_rate": s.click_rate,
                }
                for s in snapshots
            ],
        }
    )


@bp.route("/api/v1/analytics/review", methods=["POST"])
def generate_review():
    """Generate a review report."""
    data = request.get_json() or {}
    account_id = data.get("account_id")
    project_id = data.get("project_id")

    if not project_id:
        raise ValidationError(message="project_id is required")

    result = AnalyticsService.generate_review(project_id=project_id, account_id=account_id)
    return success_response(data=result)
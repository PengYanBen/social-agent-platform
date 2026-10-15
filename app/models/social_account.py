"""Social account model."""
from sqlalchemy import Column, String, Text, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, TimestampMixin


class SocialAccount(BaseModel, TimestampMixin):
    """Social media account linked to a project."""

    __tablename__ = "social_accounts"

    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    platform = Column(String(50), nullable=False)  # e.g. 'x', 'mock'
    platform_user_id = Column(String(255))
    display_name = Column(String(255))
    auth_status = Column(String(50), default="disconnected")  # connected, disconnected, expired
    credential_ref = Column(String(255))  # Reference to secure credential store
    account_timezone = Column(String(50), default="UTC")
    settings_json = Column(Text)
    is_active = Column(Boolean, default=True)

    # Relationships
    project = relationship("Project", back_populates="accounts")
    scheduled_posts = relationship(
        "ScheduledPost", back_populates="account", cascade="all, delete-orphan"
    )
    published_posts = relationship(
        "PublishedPost", back_populates="account", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_accounts_project_platform", "project_id", "platform"),
    )

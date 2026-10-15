"""Collectors package — multi-platform data source aggregation.

Supported collector types:
  - NewsNowCollector: 40+ platforms via NewsNow API (baidu, douyin, bilibili, etc.)
  - RSSCollector: Traditional RSS/Atom feeds

Auto-registers all NewsNow platform collectors on import.
"""
from app.collectors.base import (
    BaseCollector,
    CollectedEntry,
    CollectorRegistry,
)
from app.collectors.newsnow_collector import (
    NewsNowCollector,
    NEWSNOW_PLATFORMS,
    register_all_collectors,
)
from app.collectors.rss_collector import RSSCollector

__all__ = [
    "BaseCollector",
    "CollectedEntry",
    "CollectorRegistry",
    "NewsNowCollector",
    "RSSCollector",
    "NEWSNOW_PLATFORMS",
    "register_all_collectors",
]
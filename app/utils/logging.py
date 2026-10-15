"""Logging configuration."""
import logging
import sys


def configure_logging(app):
    """Configure structured logging for the application.

    Args:
        app: Flask application instance.
    """
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    handler.setFormatter(formatter)

    log_level = logging.DEBUG if app.config.get("DEBUG") else logging.INFO
    handler.setLevel(log_level)

    app.logger.setLevel(log_level)
    app.logger.handlers.clear()
    app.logger.addHandler(handler)

    # Also configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    if not root_logger.handlers:
        root_logger.addHandler(handler)

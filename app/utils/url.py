"""URL normalization utilities."""
from urllib.parse import urlparse, urlunparse
import re


def normalize_url(url):
    """Normalize a URL for deduplication.

    - Lowercase scheme and host
    - Remove default ports
    - Remove trailing slashes
    - Sort query parameters
    - Remove fragments

    Args:
        url: The URL string to normalize.

    Returns:
        Normalized URL string, or the original if parsing fails.
    """
    if not url:
        return url

    try:
        parsed = urlparse(url.strip())

        scheme = parsed.scheme.lower()
        host = parsed.hostname.lower() if parsed.hostname else ""
        port = parsed.port

        # Remove default ports
        if (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
            netloc = host
        else:
            netloc = host
            if port:
                netloc = f"{host}:{port}"

        path = parsed.path.rstrip("/") if parsed.path != "/" else ""

        # Sort query params
        query = parsed.query
        if query:
            pairs = sorted(query.split("&"))
            query = "&".join(pairs)

        return urlunparse((scheme, netloc, path, parsed.params, query, ""))
    except Exception:
        return url


def is_valid_url(url):
    """Check if a URL is valid and uses http/https scheme.

    Args:
        url: The URL string to check.

    Returns:
        True if valid http/https URL.
    """
    if not url:
        return False
    try:
        parsed = urlparse(url.strip())
        return parsed.scheme in ("http", "https") and bool(parsed.hostname)
    except Exception:
        return False

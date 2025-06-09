import logging
from .constants import LOG_LEVEL


def setup_logging():
    """Configure root logging based on LOG_LEVEL env variable."""
    logging.basicConfig(level=getattr(logging, LOG_LEVEL.upper(), logging.INFO))


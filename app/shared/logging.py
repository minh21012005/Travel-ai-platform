import logging
import sys

from app.shared.config import get_settings


def setup_logging() -> None:
    """
    Configures logging for the application.
    """

    settings = get_settings()

    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )

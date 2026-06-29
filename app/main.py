import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.exception_handlers import register_exception_handlers
from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.core.middleware import process_time_middleware

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Executed once when the application starts
    and once when the application shuts down.
    """

    setup_logging()

    settings = get_settings()

    logger.info(
        "Starting %s...",
        settings.app_name,
    )

    yield

    logger.info("Application stopped.")


def create_app() -> FastAPI:

    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
    )

    app.middleware("http")(process_time_middleware)

    register_exception_handlers(app)

    app.include_router(api_router)

    return app


app = create_app()

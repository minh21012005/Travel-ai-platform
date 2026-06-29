from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import ApplicationException, InvalidDestinationException


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApplicationException)
    async def application_exception_handler(
        request: Request, exc: ApplicationException
    ):
        return JSONResponse(
            status_code=400,
            content={"message": exc.message},
        )

    @app.exception_handler(InvalidDestinationException)
    async def invalid_destination_exception_handler(
        request: Request, exc: InvalidDestinationException
    ):
        return JSONResponse(
            status_code=400,
            content={"message": exc.message},
        )

from http import HTTPStatus


class ApplicationException(Exception):
    """
    Base exception for the application.
    """

    def __init__(
        self,
        code: str,
        message: str,
        status_code: HTTPStatus,
    ) -> None:

        self.code = code
        self.message = message
        self.status_code = status_code

        super().__init__(message)


class InvalidDestinationException(ApplicationException):
    def __init__(self) -> None:
        super().__init__(
            code="INVALID_DESTINATION",
            message="Destination is invalid.",
            status_code=HTTPStatus.BAD_REQUEST,
        )

class ApplicationException(Exception):
    """
    Base exception for the application.
    """

    def __init__(
        self,
        message: str,
    ) -> None:
        self.message = message
        super().__init__(message)


class InvalidDestinationException(ApplicationException):
    def __init__(self) -> None:
        super().__init__("Destination is invalid.")

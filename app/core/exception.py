class CustomException(Exception):
    status_code = 500
    message = "Internal server error"

    def __init__(self, message: str | None = None):
        self.message = message or self.message
        super().__init__(self.message)


class ValidationError(CustomException):
    status_code = 400
    message = "Email and password are required"


class InvalidCredentialsError(CustomException):
    status_code = 401
    message = "Invalid login credentials"


class MissingTokenError(CustomException):
    status_code = 401
    message = "Access token required"


class InvalidTokenError(CustomException):
    status_code = 401
    message = "Invalid or expired token"
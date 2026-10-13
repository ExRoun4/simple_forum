from fastapi import HTTPException, status

class AuthBaseException(HTTPException):
    error_code: str = "AUTHENTICATION_ERROR"
    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(self.status_code, detail)

class UserAlreadyExistsException(AuthBaseException):
    error_code: str = "USER_ALREADY_EXISTS"

class InvalidCredentialsException(AuthBaseException):
    error_code: str = "INVALID_CREDENTIALS"

class InvalidTokenException(AuthBaseException):
    error_code: str = "INVALID_TOKEN"

class InvalidSessionException(AuthBaseException):
    error_code: str = "INVALID_SESSION"

class TokenExpiredException(AuthBaseException):
    error_code: str = "TOKEN_EXPIRED"

class SessionExpiredException(AuthBaseException):
    error_code: str = "SESSION_EXPIRED"

class SessionInvalidatedException(AuthBaseException):
    error_code: str = "SESSION_INVALIDATED"


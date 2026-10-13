from enums import Enum

MAX_SESSIONS: int = 5
PASSWORD_ENCODING: str = "utf-8"

class JWTTypes(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"

class TokensData:
    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token
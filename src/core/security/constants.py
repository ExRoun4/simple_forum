from enums import Enum

class JWTTypes(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"

class TokensData:
    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token
from aredis_om import HashModel

class UserSession(HashModel):
    session_key: str
    user_agent: str
    ip_address: str
from pydantic import BaseModel, ConfigDict


class AuthRegisterSchema(BaseModel):
    username: str
    email: str
    password: str

class AuthRegisterResponseSchema(BaseModel):
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)

class AuthLoginSchema(BaseModel):
    login: str
    password: str

class AuthLoginResponseSchema(BaseModel):
    access_token: str

class AuthLogoutResponseSchema(BaseModel):
    status: str = "success"

class AuthRefreshResponseSchema(BaseModel):
    access_token: str
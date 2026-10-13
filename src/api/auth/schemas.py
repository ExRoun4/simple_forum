from pydantic import BaseModel

class AuthRegisterSchema(BaseModel):
    username: str
    email: str
    password: str

class AuthRegisterResponseSchema(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True

class AuthLoginSchema(BaseModel):
    login: str
    password: str

class AuthLoginResponseSchema(BaseModel):
    access_token: str

class AuthLogoutResponseSchema(BaseModel):
    ...

class AuthRefreshResponseSchema(BaseModel):
    access_token: str
import datetime
import bcrypt
import jwt

from src.core.security.constants import TokensData, JWTTypes
from src.core.security.settings import settings, jwt_settings
from src.core.security import constants
from datetime import timezone

from fastapi import Depends, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.api.auth.constants import Routes
from src.api.auth.exceptions import TokenExpiredException, InvalidTokenException

bearer_scheme = HTTPBearer(auto_error=False)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode(settings.PASSWORD_ENCODING),
        bcrypt.gensalt()
    ).decode(settings.PASSWORD_ENCODING)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode(settings.PASSWORD_ENCODING),
        hashed_password.encode(settings.PASSWORD_ENCODING)
    )

def create_jwt_token(user_id: int, token_type: constants.JWTTypes, session_key: str) -> str:
    is_refresh = token_type == constants.JWTTypes.REFRESH

    now = datetime.datetime.now(timezone.utc)
    expire = now + datetime.timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_IN_MINUTES)
    if is_refresh:
        expire = now + datetime.timedelta(days=jwt_settings.REFRESH_TOKEN_EXPIRE_IN_DAYS)

    payload = {
        "sub": str(user_id),
        "exp": expire,
        "iat": now,
        "type": token_type,
        "session_key": session_key
    }

    return jwt.encode(
        payload,
        jwt_settings.JWT_REFRESH_SECRET_KEY if is_refresh else jwt_settings.JWT_SECRET_KEY,
        algorithm=jwt_settings.JWT_ALGORITHM
    )

def create_jwt_tokens_pair(user_id: int, session_key: str) -> TokensData:
    return TokensData(
        access_token=create_jwt_token(user_id, JWTTypes.ACCESS, session_key),
        refresh_token=create_jwt_token(user_id, JWTTypes.REFRESH, session_key)
    )

def update_refresh_token_in_response(response: Response, token: str | None):
    response.set_cookie(
        key=jwt_settings.JWT_REFRESH_TOKEN_NAME,
        value=token,
        max_age=jwt_settings.get_refresh_token_expire_in_seconds() if token else 0,
        path=Routes.get_refresh_full_route(),
        httponly=True,
        secure=jwt_settings.COOKIE_SECURE,
        samesite=jwt_settings.COOKIE_SAME_SITE,
    )

def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)) -> int | None:
    if not credentials:
        return None

    try:
        payload = jwt.decode(credentials.credentials, jwt_settings.JWT_SECRET_KEY, algorithms=[jwt_settings.JWT_ALGORITHM])

        if payload.get("type") != constants.JWTTypes.ACCESS.value:
            raise TokenExpiredException("Некорректный тип токена доступа")

        user_id = payload.get("sub")
        if not user_id:
            raise TokenExpiredException("Токен не содержит идентификатор пользователя")

        return int(user_id)

    except jwt.ExpiredSignatureError:
        raise TokenExpiredException("Сессия истекла. Войдите заново")
    except jwt.InvalidTokenError:
        raise InvalidTokenException("Невалидный сессионный токен")
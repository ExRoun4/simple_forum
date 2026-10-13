import datetime
import uuid
import jwt

from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth import schemas
from src.api.auth.db import repository
from src.core.security import security, settings
from src.api.auth import exceptions

async def register_user(
    payload: schemas.AuthRegisterSchema,
    db: AsyncSession
) -> schemas.AuthRegisterResponseSchema:
    existing_by_username = await repository.get_user_by_username(payload.username, db)
    if existing_by_username:
        raise exceptions.UserAlreadyExistsException("Пользователь с таким никнеймом уже зарегистрирован")

    existing_by_email = await repository.get_user_by_email(payload.email, db)
    if existing_by_email:
        raise exceptions.UserAlreadyExistsException("Пользователь с таким email уже зарегистрирован")

    new_user = await repository.create_user(payload, db)
    return schemas.AuthRegisterResponseSchema.model_validate(new_user)

async def login_user(
    payload: schemas.AuthLoginSchema,
    request: Request,
    response: Response,
    db: AsyncSession,
) -> schemas.AuthLoginResponseSchema:
    user = await repository.get_user_by_username_or_email(payload.login, payload.login, db)
    if not user or not security.verify_password(payload.password, user.hashed_password):
        raise exceptions.InvalidCredentialsException(f"Неверный логин или пароль!")

    await repository.update_sessions(user.id, db)
    session = await repository.create_user_session(
        user.id,
        request.headers.get("user-agent"),
        request.headers.get("x-forwarded-for") or request.client.host,
        db
    )
    tokens = security.create_jwt_tokens_pair(user.id, session.session_key)
    security.update_refresh_token_in_response(response, tokens.refresh_token)

    return schemas.AuthLoginResponseSchema(access_token=tokens.access_token)

async def logout_user(
    response: Response,
    refresh_token: str | None,
    db: AsyncSession
) -> schemas.AuthLogoutResponseSchema:
    try:
        payload = jwt.decode(
            refresh_token,
            security.jwt_settings.JWT_REFRESH_SECRET_KEY,
            algorithms=[security.jwt_settings.JWT_ALGORITHM],
            options={"verify_exp": False}
        )
        session_key = payload.get("session_key")
        if session_key:
            await repository.delete_session_by_key(session_key, db)
    except jwt.InvalidTokenError:
        ...
    finally:
        security.update_refresh_token_in_response(response, None)
        return schemas.AuthLogoutResponseSchema()

async def refresh_user_session(
    refresh_token: str | None,
    request: Request,
    response: Response,
    db: AsyncSession
) -> schemas.AuthRefreshResponseSchema:
    if not refresh_token:
        raise exceptions.InvalidTokenException("Сессионный токен отсутствует")
    try:
        payload = jwt.decode(
            refresh_token,
            settings.jwt_settings.JWT_REFRESH_SECRET_KEY,
            algorithms=[security.jwt_settings.JWT_ALGORITHM]
        )
    except jwt.ExpiredSignatureError:
        raise exceptions.TokenExpiredException("Сессионный токен истёк")
    except jwt.InvalidTokenError:
        raise exceptions.InvalidTokenException("Невалидный сессионный токен")

    user_id: int = int(payload.get("sub"))
    session_key: str = payload.get("session_key")
    user_agent: str = request.headers.get("user-agent")
    ip: str = request.headers.get("x-forwarded-for") or request.client.host
    now = datetime.datetime.now(datetime.UTC)
    session = await repository.get_session_by_key(session_key, db)

    if not session:
        raise exceptions.SessionInvalidatedException("Сессия аннулирована")

    if session.expires_at.replace(tzinfo=datetime.UTC) < now:
        await db.delete(session)
        await db.commit()

        raise exceptions.SessionExpiredException("Срок действия сессии истек")

    if user_agent != session.user_agent or ip != session.ip_address:
        raise exceptions.InvalidSessionException("Невалидная сессия")

    new_session_key = str(uuid.uuid4())
    session.session_key = new_session_key
    session.expires_at = now + datetime.timedelta(days=settings.jwt_settings.REFRESH_TOKEN_EXPIRE_IN_DAYS)
    await db.commit()

    new_tokens = security.create_jwt_tokens_pair(user_id, new_session_key)
    security.update_refresh_token_in_response(response, new_tokens.refresh_token)

    return schemas.AuthRefreshResponseSchema(access_token=new_tokens.access_token)
from sqlalchemy.ext.asyncio import AsyncSession

import src.core.security.security as security

from redis.asyncio import Redis
from fastapi import APIRouter, status, Depends, Response, Cookie, Request
from src.api.auth import constants, schemas, service
from src.core.database import create_session
from src.core.redis_db import get_redis

router = APIRouter(
    prefix=constants.Routes.PREFIX,
    tags=constants.tags
)

@router.post(constants.Routes.REGISTER, status_code=status.HTTP_201_CREATED, response_model=schemas.AuthRegisterResponseSchema)
async def register_user(
    payload: schemas.AuthRegisterSchema,
    db: AsyncSession = Depends(create_session)
) -> schemas.AuthRegisterResponseSchema:
    register_response = await service.register_user(payload, db)
    return register_response

@router.post(constants.Routes.LOGIN, response_model=schemas.AuthLoginResponseSchema)
async def login_user(
    payload: schemas.AuthLoginSchema,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(create_session),
    redis: Redis = Depends(get_redis)
) -> schemas.AuthLoginResponseSchema:
    auth_response = await service.login_user(payload, request, response, db, redis)
    return auth_response

@router.post(constants.Routes.LOGOUT, response_model=schemas.AuthLogoutResponseSchema)
async def logout_user(
    response: Response,
    refresh_token: str | None = Cookie(default=None, alias=security.jwt_settings.REFRESH_TOKEN_NAME),
    redis: Redis = Depends(get_redis)
) -> schemas.AuthLogoutResponseSchema:
    logout_response = await service.logout_user(response, refresh_token, redis)
    return logout_response

@router.post(constants.Routes.REFRESH, response_model=schemas.AuthRefreshResponseSchema)
async def refresh_user_tokens(
    request: Request,
    response: Response,
    refresh_token: str | None = Cookie(default=None, alias=security.jwt_settings.REFRESH_TOKEN_NAME),
    redis: Redis = Depends(get_redis)
) -> schemas.AuthRefreshResponseSchema:
    refresh_response = await service.refresh_user_session(refresh_token, request, response, redis)
    return refresh_response
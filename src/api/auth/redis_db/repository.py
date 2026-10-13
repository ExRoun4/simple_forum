import time
import uuid

from redis.asyncio import Redis
from src.core.security.settings import jwt_settings
from src.core.security.constants import MAX_SESSIONS
from src.api.auth.redis_db.models import UserSession

async def create_user_session(
    user_id: int,
    user_agent: str | None,
    ip: str | None,
    redis: Redis
) -> UserSession:
    session_data = UserSession(
        session_key=str(uuid.uuid4()),
        user_agent=user_agent or "unknown",
        ip_address=ip
    )

    s_key = get_session_key(session_data.session_key)
    u_sessions_key = get_user_sessions_key(user_id)
    expire_seconds = jwt_settings.get_refresh_token_expire_in_seconds()

    await redis.hset(s_key, mapping=session_data.model_dump(mode="json"))
    await redis.expire(s_key, expire_seconds)

    await redis.zadd(u_sessions_key, {session_data.session_key: time.time()})
    await redis.expire(u_sessions_key, expire_seconds)

    return session_data

async def enforce_max_sessions(user_id: int, redis: Redis, max_sessions: int = MAX_SESSIONS) -> None:
    u_sessions_key = get_user_sessions_key(user_id)

    count = await redis.zcard(u_sessions_key)
    if count < max_sessions:
        return

    old_session_keys = await redis.zrange(u_sessions_key, 0, count - max_sessions - 1)

    if old_session_keys:
        for old_key in old_session_keys:
            await redis.delete(get_session_key(old_key))
        await redis.zrem(u_sessions_key, *old_session_keys)

async def get_session_by_key(session_key: str, redis: Redis) -> UserSession | None:
    data = await redis.hgetall(get_session_key(session_key))
    if not data:
        return None

    return UserSession.model_validate(data)

async def delete_session_by_key(user_id: int, session_key: str, redis: Redis) -> None:
    await redis.delete(get_session_key(session_key))
    await redis.zrem(get_user_sessions_key(user_id), session_key)

def get_session_key(session_key: str) -> str:
    return f"session:{session_key}"

def get_user_sessions_key(user_id: int) -> str:
    return f"user_sessions:{user_id}"
from redis.asyncio import ConnectionPool, Redis
from src.core.settings import settings

REDIS_URL = "redis://{0}:{1}/{2}".format(
    settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_NAME
)
redis_pool: ConnectionPool | None = None

def init_redis() -> Redis:
    global redis_pool
    redis_pool = ConnectionPool.from_url(
        REDIS_URL,
        decode_responses=True,
        max_connections=100
    )
    return Redis(connection_pool=redis_pool)

async def close_redis() -> None:
    if redis_pool:
        await redis_pool.disconnect()

async def get_redis() -> Redis:
    return Redis(connection_pool=redis_pool)
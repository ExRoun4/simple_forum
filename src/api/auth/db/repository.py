import datetime
import uuid

from sqlalchemy import select, or_, func, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.db.models import User, UserSession
from src.api.auth.exceptions import UserAlreadyExistsException
from src.api.auth.schemas import AuthRegisterSchema
from src.core.security import security, settings

async def create_user(
    payload: AuthRegisterSchema,
    db: AsyncSession
) -> User:
    new_user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=security.hash_password(payload.password)
    )

    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user
    except IntegrityError:
        await db.rollback()
        raise UserAlreadyExistsException("Пользователь уже существует")

async def get_user_by_id(user_id: int, db: AsyncSession) -> User | None:
    return await db.get(User, user_id)

async def get_user_by_username(username: str, db: AsyncSession) -> User | None:
    result = await db.execute(
        select(User).where(User.username == username)
    )
    return result.scalar_one_or_none()

async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()

async def get_user_by_username_or_email(username: str, email: str, db: AsyncSession) -> User | None:
    result = await db.execute(
        select(User).where(or_(
            User.username == username,
            User.email == email
        ))
    )
    return result.scalar_one_or_none()

async def create_user_session(
    user_id: int,
    user_agent: str | None,
    ip: str | None,
    db: AsyncSession
) -> UserSession:
    expires_at = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=settings.jwt_settings.REFRESH_TOKEN_EXPIRE_IN_DAYS)
    db_session = UserSession(
        user_id=user_id,
        session_key=str(uuid.uuid4()),
        user_agent=user_agent,
        ip_address=ip,
        expires_at=expires_at.replace(tzinfo=None)
    )
    db.add(db_session)
    await db.commit()
    await db.refresh(db_session)

    return db_session

async def delete_session_by_key(session_key: str, db: AsyncSession) -> bool:
    session = await get_session_by_key(session_key, db)
    if not session:
        return False

    await db.delete(session)
    await db.commit()
    return True

async def update_sessions(user_id: int, db: AsyncSession, max_sessions: int = settings.settings.MAX_SESSIONS):
    current_sessions = await db.execute(
        select(func.count()).where(UserSession.user_id == user_id)
    )
    current_sessions_count = current_sessions.scalar() or 0
    if current_sessions_count < max_sessions:
        return

    old_sessions = await db.execute(
        select(UserSession.id) \
        .where(UserSession.user_id == user_id) \
        .order_by(UserSession.created_at.asc()) \
        .limit(current_sessions_count - max_sessions + 1)
    )
    old_sessions_ids = old_sessions.scalars().all()
    if old_sessions_ids:
        await db.execute(delete(UserSession).where(UserSession.id.in_(old_sessions_ids)))

async def get_session_by_key(session_key: str, db: AsyncSession) -> UserSession | None:
    result = await db.execute(
        select(UserSession).where(
            UserSession.session_key == session_key,
            UserSession.expires_at > datetime.datetime.now(datetime.UTC)
        )
    )
    return result.scalar_one_or_none()
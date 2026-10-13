from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.db.models import User
from src.api.auth.exceptions import UserAlreadyExistsException
from src.api.auth.schemas import AuthRegisterSchema
from src.core.security import security

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
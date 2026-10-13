from datetime import datetime
from pydantic import EmailStr
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey, String

from src.core.database import Base
from src.api.threads.db.models import Thread
from src.api.posts.db.models import Post

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    threads: Mapped[list[Thread]] = relationship(back_populates="creator")
    posts: Mapped[list[Post]] = relationship(back_populates="creator")

class UserSession(Base):
    __tablename__ = "users_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_key: Mapped[str] = mapped_column(String(36), unique=True, nullable=False)
    user_agent: Mapped[str] = mapped_column(String(500), nullable=True)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user: Mapped[User] = relationship()
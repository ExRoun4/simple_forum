from datetime import datetime

from sqlalchemy import ForeignKey, func

from src.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Thread(Base):
    __tablename__ = "threads"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)

    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    creator_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))

    creator: Mapped["User"] = relationship(back_populates="threads")
    posts: Mapped[list["Post"]] = relationship(back_populates="thread", cascade="all, delete-orphan")

from datetime import datetime
from sqlalchemy import ForeignKey, func

from src.core.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    creator_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    thread_id: Mapped[int] = mapped_column(ForeignKey("threads.id", ondelete="CASCADE"), nullable=False)

    creator: Mapped["User"] = relationship(back_populates="posts")
    thread: Mapped["Thread"] = relationship(back_populates="posts")
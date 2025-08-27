from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(sa.String(200), nullable=False)
    content: Mapped[str] = mapped_column(sa.Text, nullable=False)
    image_url: Mapped[str | None] = mapped_column(sa.String(500))
    likes_count: Mapped[int] = mapped_column(sa.Integer, server_default="0", nullable=False)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now())

    author = relationship("User", back_populates="posts")

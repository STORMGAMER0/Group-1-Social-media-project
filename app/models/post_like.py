# app/models/post_like.py
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class PostLike(Base):
    __tablename__ = "post_likes"

    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id: Mapped[int] = mapped_column(sa.ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)

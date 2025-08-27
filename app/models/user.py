from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(sa.String(32), unique=True, index=True, nullable=False)
    email: Mapped[str | None] = mapped_column(sa.String(255), unique=True)
    full_name: Mapped[str | None] = mapped_column(sa.String(255))
    hashed_password: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now())

    posts = relationship("Post", back_populates="author", cascade="all, delete", passive_deletes=True)

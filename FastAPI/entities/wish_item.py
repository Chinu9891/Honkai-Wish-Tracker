# app/models/wish.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Enum as SqlEnum, DateTime
from database.core import Base
from datetime import datetime, timezone
from enum import Enum

class ItemType(str, Enum):
    CHARACTER = "character"
    LIGHTCONE = "lightcone"

class WishItem(Base):
    __tablename__ = "wishes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_name: Mapped[str] = mapped_column(String(32), nullable=False)
    item_type: Mapped[ItemType] = mapped_column(SqlEnum(ItemType), nullable=False)
    item_rarity: Mapped[int] = mapped_column(Integer, nullable=False)
    item_path: Mapped[str] = mapped_column(String(32), nullable=False)
    item_element: Mapped[str] = mapped_column(String(32), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="wishes")

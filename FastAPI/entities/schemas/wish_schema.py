from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class ItemType(str, Enum):
    CHARACTER = "character"
    LIGHTCONE = "lightcone"

class WishCreate(BaseModel):
    item_name: str  # What the client sends

class WishSchema(BaseModel):
    id: int
    item_name: str
    # rarity: int
    # item_type: ItemType
    created_at: datetime

    class Config:
        from_attributes = True
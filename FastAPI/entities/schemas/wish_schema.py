from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class ItemType(str, Enum):
    CHARACTER = "character"
    LIGHTCONE = "lightcone"

# What the client sends
class WishCreate(BaseModel):
    name: str
    rarity: int
    item_type: str
    element: Optional[str] = None
    path: str 

class WishSchema(BaseModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
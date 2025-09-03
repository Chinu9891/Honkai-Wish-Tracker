from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends

from entities.schemas.wish_schema import WishCreate, WishSchema
from entities.wish_item import WishItem

from typing import List
from sqlalchemy.orm import Session

def create_wishes(db: Session, wishes: List[WishCreate], user_id: int):

    for wish in wishes:
        item = WishItem(
            item_name=wish.item_name,
            user_id=user_id
        )
        db.add(item)
        db.commit() 
        db.refresh(item)

def get_wishes(db: Session, user_id: int):
    
    wish_list =  db.query(WishItem).filter(WishItem.user_id == user_id).order_by(WishItem.created_at.desc()).limit(10).all()

    wishes_to_return: List[WishSchema] = []
    
    for wish in wish_list:
        wish_schema = WishSchema(id=wish.id, item_name=wish.item_name, created_at=wish.created_at)
        
        wishes_to_return.append(wish_schema)
        
    return wishes_to_return
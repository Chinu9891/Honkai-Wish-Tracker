from fastapi import APIRouter, Depends, HTTPException
from typing import List, Union
from sqlalchemy.orm import Session

from entities.user import User
from auth.services.auth_service import get_current_active_user
from database.core import get_db
from entities.schemas.wish_schema import WishSchema, WishCreate
from entities.services.wish_service import create_wishes, get_wishes


wish_router = APIRouter(
    prefix='/wishes',
    tags=['Wishes']
)

@wish_router.get('/', response_model=list[WishSchema])
def wish_list(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    wish_items = get_wishes(db, current_user.id)

    return wish_items

@wish_router.post('/')
def wish_post(wish: Union[WishCreate, List[WishCreate]], db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    
    wishes_to_create = wish if isinstance(wish, List) else [wish]
    
    create_wishes(db, wishes_to_create, current_user.id)
    
    return {"status": "success", "message": f"{len(wishes_to_create)} wish(es) created."}
    
    
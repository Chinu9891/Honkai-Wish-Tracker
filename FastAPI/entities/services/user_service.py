from sqlalchemy.orm import Session

from entities.user import User
from entities.schemas.user_schema import UserCreate
from auth.utils.auth_utils import get_password_hash

def get_users(db: Session):
    return db.query(User).all()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(user_id==User.id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(
        email = str(user.email),
        username = user.username,
        password = get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user
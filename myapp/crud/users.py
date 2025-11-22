from sqlalchemy.orm import Session
from myapp.models.user import User
from myapp.models.role import Role
from myapp.schemas.add_users import UserCreate, UserUpdate
from myapp.backend.auth.hashing import hash_password

# ---------------- Create User ----------------
def create_user(db: Session, user_in: UserCreate) -> User:
    db_user = User(
        name=user_in.name,
        email=user_in.email,
        password=hash_password(user_in.password),
        roll_no=user_in.roll_no,
        phone_number=user_in.phone_number
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ---------------- Get User by ID ----------------
def get_user(db: Session, user_id: int) -> User :
    return db.query(User).filter(User.id == user_id).first()


# ---------------- Get User by Email ----------------
def get_user_by_email(db: Session, email: str) -> User :
    return db.query(User).filter(User.email == email).first()


# ---------------- List All Users ----------------
# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     user =  db.query(User).offset(skip).limit(limit).all()
#     for user in user:
#         if user.is_active is None:
#             user.is_active = False
#     return user

from typing import List

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    users = db.query(User).offset(skip).limit(limit).all()
    
    # ensure all boolean fields are True/False
    for u in users:
        if u.is_active is None:
            u.is_active = False
    
    return users


# ---------------- Update User ----------------
def update_user(db: Session, user_id: int, user_in: UserUpdate) -> User :
    user = get_user(db, user_id)
    if not user:
        return None

    if user_in.name is not None:
        user.name = user_in.name
    if user_in.roll_no is not None:
        user.roll_no = user_in.roll_no
    if user_in.phone_number is not None:
        user.phone_number = user_in.phone_number
    if user_in.password:
        user.password = hash_password(user_in.password)

    db.commit()
    db.refresh(user)
    return user


# ---------------- Delete User ----------------
def delete_user(db: Session, user_id: int) -> bool:
    user = get_user(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True


def fetch_role(db, id: int):
    return db.query(Role).filter(Role.id ==id).first()
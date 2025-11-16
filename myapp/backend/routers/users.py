from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from myapp.database.connect_db import get_db
from myapp.schemas.add_users import UserCreate, UserResponse, UserUpdate
from myapp.crud.users import create_user, get_user, get_users, update_user, delete_user, get_user_by_email
from myapp.backend.auth.dependencies import get_current_user
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

# ---------------- Create User ----------------
@router.post("/create", response_model=UserResponse)
def create_new_user(user_in: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user_in)


# ---------------- Get Current User ----------------
@router.get("/me", response_model=UserResponse)
def read_current_user(current_user=Depends(get_current_user)):
    return current_user


# ---------------- Get User by ID ----------------
@router.get("/user/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ---------------- List All Users ----------------
@router.get("/list", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    print(current_user.__dict__,'-----------cur')
    # user_rec = get_user(db, int(current_user.sub))
    if current_user:
        return get_users(db, skip=skip, limit=limit)
    else:
        print("ro record found")

# ---------------- Update User ----------------
@router.put("/{user_id}", response_model=UserResponse)
def update_existing_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    updated_user = update_user(db, user_id, user_in)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


# ---------------- Delete User ----------------
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return

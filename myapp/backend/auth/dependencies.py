# app/auth/dependencies.py

# python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
# from app.config import SECRET_KEY, ALGORITHM
from myapp.database.connect_db import SessionLocal
from myapp.models.user import User
SECRET_KEY = "your_secret_key_here"        # 🔒 Use environment variable in production
ALGORITHM = "HS256"
REFRESH_TOKEN_EXPIRE_DAYS = 7 
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(401, "Invalid token")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(404, "User not found")
        return user

    except JWTError:
        raise HTTPException(401, "Token expired or invalid")


 # 🔐 5. AUTH – JWT Access & Refresh Tokens

# app/auth/jwt_handler.py

# python
from datetime import datetime, timedelta
from jose import jwt
# from myapp.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
SECRET_KEY = "your_secret_key_here"        # 🔒 Use environment variable in production
ALGORITHM = "HS256"
REFRESH_TOKEN_EXPIRE_DAYS = 7 
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

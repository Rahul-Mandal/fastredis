from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
 
from myapp.database.connect_db import get_db, engine, Base
from myapp.crud.test import fetch_data
from myapp.models.user import User

from fastapi.responses import HTMLResponse
import redis
import time 
import random

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="My API", version="1.0.0")

Base.metadata.create_all(bind = engine)


origins = [
    "http://localhost:5173",   # React/Vue/Next.js local dev server
    "https://yourfrontend.com", # Your production frontend domain
    "http://127.0.0.1:5173",  # sometimes needed too
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    # allow_origins=["*"],          # List of allowed origins
    allow_credentials=True,         # Allow cookies / authentication headers
    allow_methods=["*"],            # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],            # Allow all headers
)

# connect to redis

r = redis.Redis(host = "localhost", port=6379, db = 0, decode_responses = True)

# simulate expensive db call

def get_dashboard_data_from_db():
    print(" simulating  expensive db calls")
    time.sleep(3) # simulate delay (eg.. slow query)
    data = {
        "total_user" : random.randint(1000,2000),
        "total_sales" : random.randint(500, 1000),
        "conversion_rate": round(random.uniform(1.2, 2.5),2)
    }
    return data

# endpoint using redis cache

@app.get("/dashboard", response_class = HTMLResponse)
def get_dashboard():
    start = time.time()
    cache_key = "dashboarg_page_v1"
    cached_html = r.get(cache_key)

    if cached_html:
        duration = time.time() -start
        print(f"cache hit - returning cache dashboard in {duration: .3f}s ")
        return cached_html

    print("cache miss - fetching fresh data")
    data = get_dashboard_data_from_db()
     
    html = f"""
     <html>
     <head>
     <title>Dashboard</title>
     </head>
     <body>
     <h1> Business dashboard</h1>
     <p><b> Total users: </b> {data['total_user']}</p>

     <p><b> Total sales: </b> {data['total_sales']}</p>

     <p><b> Conversion rate : </b> {data['conversion_rate']}</p>
     <p style='color':gray;'> Generated at {time.strftime("%H:%M:%S")}</p>
     </body>
     </html>

     """

     # cache for 120 sec

    r.setex(cache_key, 120, html)
    duration = time.time() -start
    print(f"cache miss - returning non cache dashboard in {duration: .3f}s ")
    return html

@app.get('/details')
def get_data(db: Session = Depends(get_db)):
    data = db.query(User).all()  # simple query
    print(data)
    return data


from fastapi import FastAPI, Depends, HTTPException, status,Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel

class LoginInput(BaseModel):
    username: str
    password: str


# === Configuration ===
SECRET_KEY = "your_secret_key_here"        # 🔒 Use environment variable in production
ALGORITHM = "HS256"
REFRESH_TOKEN_EXPIRE_DAYS = 7 
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# === Password hashing ===
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# === OAuth2 setup ===
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# app = FastAPI()

# === Mock user (simulate DB) ===
fake_user_db = {
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderland",
        "hashed_password": pwd_context.hash("password123"),
    }
}

# === Helper functions ===
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    return fake_user_db.get(username)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# === Routes ===

@app.post("/token")
async def login(form_data:LoginInput,response: Response): # OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    # --- Create refresh token ---
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_access_token(
        data={"sub": user["username"], "type": "refresh"},
        expires_delta=refresh_token_expires
    )

    # --- Optional: Set HttpOnly cookie for refresh token ---
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # True in production (HTTPS)
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )
    return {"access_token": access_token, "refresh_token": refresh_token,"token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


from fastapi import Cookie

@app.post("/refresh")
async def refresh_token(refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Create new access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)

    return {"access_token": new_access_token, "token_type": "bearer"}




# Example with simple hardcoded users:


# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# from auth_utils import create_access_token

app = FastAPI()

fake_users = {
    "admin@example.com": {"password": "admin123", "role": "admin"},
    "user@example.com": {"password": "user123", "role": "user"}
}

class LoginModel(BaseModel):
    email: str
    password: str

@app.post("/login")
def login(data: LoginModel):
    user = fake_users.get(data.email)
    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(
        {"sub": data.email, "role": user["role"]}
    )
    return {"access_token": token, "token_type": "bearer"}



# ✅ 5. Dependency to Extract Current User + Role


# dependencies.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
# from auth_config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")

        if username is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {"email": username, "role": role}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")




# ✅ 6. Role-Based Access Dependency (RBAC)

def role_required(*allowed_roles):
    def dependency(current_user=Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=403, 
                detail=f"Requires role: {allowed_roles}"
            )
        return current_user
    return dependency




# ✅ 7. Protect Routes by Role


@app.get("/admin")
def admin_panel(current_user=Depends(role_required("admin"))):
    return {"message": "Welcome admin!"}

@app.get("/user")
def user_panel(current_user=Depends(role_required("admin", "user"))):
    return {"message": "Welcome user!"}

@app.get("/super-secret")
def super_secret(current_user=Depends(role_required("superadmin"))):
    return {"message": "Super secret area!"}




from fastapi import FastAPI
from myapp.database.connect_db import Base, engine
from myapp.backend.routers import auth_router, user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router.router)
app.include_router(user_router.router)




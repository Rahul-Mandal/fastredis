from sqlalchemy import Column, Integer, String
from myapp.database.connect_db import Base

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)





### *Role-Permission Mapping*

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
# from app.database import Base

class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    permission_id = Column(Integer, ForeignKey("permissions.id"))

    role = relationship("Role", back_populates="permissions")




# ---

# # 🔐 4. AUTH – Password Hashing

# app/auth/hashing.py

# python
# from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)

# def verify_password(plain: str, hashed: str) -> bool:
#     return pwd_context.verify(plain, hashed)


# ---

# # 🔐 5. AUTH – JWT Access & Refresh Tokens

# app/auth/jwt_handler.py

# python
# from datetime import datetime, timedelta
# from jose import jwt
# from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

# def create_access_token(data: dict):
#     to_encode = data.copy()
#     to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# def create_refresh_token(data: dict):
#     to_encode = data.copy()
#     to_encode.update({"exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ---

# # 🧬 6. AUTH – Extract Current User & Check Roles/Permissions

# app/auth/dependencies.py

# python
# from fastapi import Depends, HTTPException
# from fastapi.security import OAuth2PasswordBearer
# from jose import jwt, JWTError
# from app.config import SECRET_KEY, ALGORITHM
# from app.database import SessionLocal
# from app.models.user import User

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id = payload.get("sub")
#         if user_id is None:
#             raise HTTPException(401, "Invalid token")

#         user = db.query(User).filter(User.id == user_id).first()
#         if not user:
#             raise HTTPException(404, "User not found")
#         return user

#     except JWTError:
#         raise HTTPException(401, "Token expired or invalid")


# ---

# # 🛡️ 7. AUTH – Role & Permission Checker

# app/auth/role_checker.py

# python
# from fastapi import Depends, HTTPException
# from app.auth.dependencies import get_current_user

# def role_required(*roles):
#     def wrapper(user=Depends(get_current_user)):
#         user_roles = [r.role.name for r in user.roles]
#         if not any(r in roles for r in user_roles):
#             raise HTTPException(403, f"Requires roles: {roles}")
#         return user
#     return wrapper

# def permission_required(*permissions):
#     def wrapper(user=Depends(get_current_user)):
#         user_permissions = set()
#         for user_role in user.roles:
#             for role_permission in user_role.role.permissions:
#                 user_permissions.add(role_permission.permission.name)

#         if not any(p in user_permissions for p in permissions):
#             raise HTTPException(403, f"Requires permissions: {permissions}")
#         return user
#     return wrapper


# ---

# # 📜 8. SCHEMAS

# ### Auth Schemas

# app/schemas/auth.py

# python
# from pydantic import BaseModel

# class LoginRequest(BaseModel):
#     email: str
#     password: str

# class TokenResponse(BaseModel):
#     access_token: str
#     refresh_token: str
#     token_type: str = "bearer"


# ### User Schema

# app/schemas/user.py

# python
# from pydantic import BaseModel

# class UserCreate(BaseModel):
#     email: str
#     password: str


# ---

# # 🔐 9. AUTH ROUTER

# app/routers/auth_router.py

# python
# from fastapi import APIRouter, Depends, HTTPException
# from app.schemas.auth import LoginRequest, TokenResponse
# from app.auth.hashing import verify_password
# from app.auth.jwt_handler import create_access_token, create_refresh_token
# from app.database import SessionLocal
# from app.models.user import User

# router = APIRouter(prefix="/auth", tags=["Auth"])

# @router.post("/login", response_model=TokenResponse)
# def login(data: LoginRequest):
#     db = SessionLocal()
#     user = db.query(User).filter(User.email == data.email).first()

#     if not user or not verify_password(data.password, user.password):
#         raise HTTPException(401, "Invalid credentials")

#     payload = {"sub": user.id}

#     return TokenResponse(
#         access_token=create_access_token(payload),
#         refresh_token=create_refresh_token(payload)
#     )


# ---

# # 👥 10. USER ROUTER

# app/routers/user_router.py

# python
# from fastapi import APIRouter, Depends
# from app.auth.role_checker import role_required, permission_required
# from app.auth.dependencies import get_current_user

# router = APIRouter(prefix="/users", tags=["Users"])

# @router.get("/admin-only")
# def admin_data(user=Depends(role_required("admin"))):
#     return {"msg": "Welcome admin"}

# @router.get("/update")
# def update_data(user=Depends(permission_required("edit_profile"))):
#     return {"msg": "You can edit profile!"}


# ---

# # 🚀 MAIN APP

# app/main.py

# python
# from fastapi import FastAPI
# from app.database import Base, engine
# from app.routers import auth_router, user_router

# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# app.include_router(auth_router.router)
# app.include_router(user_router.router)


# ---

# # 🎉 You Now Have:

# ### ✔ JWT Access Token

# ### ✔ JWT Refresh Token

# ### ✔ SQLAlchemy database

# ### ✔ bcrypt password hashing

# ### ✔ RBAC (roles + multiple roles per user)

# ### ✔ Permission-based access

# ### ✔ Role hierarchy (via permissions)

# ### ✔ Clean project structure

# ---

# # Next Step

# If you want, I can also generate:

# * 🧪 automatic tests (pytest)
# * 📄 OpenAPI documentation
# * 🔐 OAuth2 login with cookies instead of headers
# * 🧱 Dockerfile + docker-compose
# * 📡 Swagger UI with bearer auth pre-filled
# * 📂 Pre-filled database with roles + users

# Just tell me:
# *"Add tests"* or *"Add Docker"* or *"Add sample data"* etc.
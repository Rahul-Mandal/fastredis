# 🔐 9. AUTH ROUTER

# app/routers/auth_router.py

# python
from fastapi import APIRouter, Depends, HTTPException
from myapp.schemas.auth import LoginRequest, TokenResponse
from myapp.backend.auth.hashing import verify_password
from myapp.backend.auth.jwt_handler import create_access_token, create_refresh_token
from myapp.database.connect_db import SessionLocal
from myapp.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])

# @router.post("/login", response_model=TokenResponse)
# def login(data: LoginRequest):
#     db = SessionLocal()
#     user = db.query(User).filter(User.email == data.email).first()

#     if not user or not verify_password(data.password, user.password):
#         raise HTTPException(401, "Invalid credentials")

#     payload = {"sub": str(user.id)}

#     return TokenResponse(
#         access_token=create_access_token(payload),
#         refresh_token=create_refresh_token(payload)
#     )


@router.post('/login', response_model=TokenResponse)
def login(data: LoginRequest):
    db = SessionLocal()
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        return HTTPException(401, "Invalid credentails")
    payload = {"sub": str(user.id)}

    return TokenResponse(
        access_token = create_access_token(payload),
        refresh_token = create_refresh_token(payload)
    )

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(refresh_token: str):
    """
    Validate refresh token and return new access token.
    """
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        new_access = create_access_token({"sub": user_id})
        new_refresh = create_refresh_token({"sub": user_id})

        return TokenResponse(access_token=new_access, refresh_token=new_refresh)

    except JWTError:
        raise HTTPException(401, "Refresh token expired or invalid.")

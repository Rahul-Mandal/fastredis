from fastapi import Depends, HTTPException, Request, status
from jose import jwt, JWTError
from myapp.database.connect_db import SessionLocal
from myapp.models.user import User
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

print("SECRET_KEY =", repr(SECRET_KEY))
print("ALGORITHM =", repr(ALGORITHM))

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_bearer_token(request: Request) -> str:
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
        )
    return auth.split(" ")[1]

# def get_current_user(token: str = Depends(get_bearer_token), db=Depends(get_db)):
#     print(token, 'token')
#     try:
#         payload = jwt.decode("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsImV4cCI6MTc2MzIwNTMyMX0.gwCZM2ksUNd6D953EQczYmsg2ImzPC_wiBviUa0c9_Q", "supersecret12345", algorithms=["HS256"], options={"verify_exp": False})
#         print(payload)
#         user_id = payload.get("sub")
#         if user_id is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

#         user = db.query(User).filter(User.id == user_id).first()
#         if user is None:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#         return user

#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired or invalid")


from jose import jwt, ExpiredSignatureError, JWTError

def get_current_user(token: str = Depends(get_bearer_token), db=Depends(get_db)):
    print("RAW TOKEN:", token)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("DECODED PAYLOAD:", payload)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(401, "Invalid token payload")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(404, "User not found")

        return user

    except ExpiredSignatureError:
        raise HTTPException(401, "Token expired")

    except JWTError as e:
        print(f"JWT ERROR: {e}")
        raise HTTPException(401, f"Invalid token: {e}")

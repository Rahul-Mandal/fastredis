### User Schema

# app/schemas/user.py

# python
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

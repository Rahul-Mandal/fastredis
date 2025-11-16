from pydantic import BaseModel

class Adduser(BaseModel):
    email: str
    password: str

from pydantic import BaseModel, EmailStr
from typing import Optional, List

# ------------ Base User Schema ------------
class UserBase(BaseModel):
    name: str
    email: EmailStr
    roll_no: Optional[int] = None
    phone_number: Optional[str] = None

    class Config:
        orm_mode = True


# ------------ Schema for Creating User ------------
class UserCreate(UserBase):
    password: str   # required only on create


# ------------ Schema for Updating User ------------
class UserUpdate(BaseModel):
    name: Optional[str] = None
    roll_no: Optional[int] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None


# ------------ Response Schema (no password) ------------
class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


# ------------ User with Roles (Optional) ------------
class Role(BaseModel):
    id: int
    role_name: str

    class Config:
        orm_mode = True


class UserWithRoles(UserResponse):
    roles: List[Role] = []


















from pydantic import BaseModel, EmailStr
from typing import Optional, List


class UserBase(BaseModel):
    name: str
    email: EmailStr
    roll_no: Optional[int] = None
    phone_number: Optional[str] = None
    is_active: bool

    class Config:
        orm_mode = True


# ------------ Response Schema: return everything except password ------------
class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


# ------------ Create Schema (password required only here) ------------
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    roll_no: Optional[int] = None
    phone_number: Optional[str] = None


# ------------ Update Schema (all optional) ------------
class UserUpdate(BaseModel):
    name: Optional[str] = None
    roll_no: Optional[int] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None

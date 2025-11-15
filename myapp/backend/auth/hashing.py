# # 🔐 4. AUTH – Password Hashing

# app/auth/hashing.py

# python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    print(pwd_context.hash("rahul@123"))
    return pwd_context.verify(plain, hashed)

'''
(env) rahul@rahul-Vostro-3400:~/FastProject$ python3
Python 3.8.10 (default, Mar 18 2025, 20:04:55) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from passlib.context import CryptContext
>>> pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
>>> print(pwd.hash("rahul@123"))
$2b$12$cmGED2fixUhxO7mfVswb1ue/XnMHzgIVDXPi9kZ7OMlwCvAwbqrFO
>>> '''
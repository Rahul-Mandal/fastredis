from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from myapp.models.user_role_mapper import UserRoleMapper


from myapp.database.connect_db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    roll_no = Column(Integer)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    phone_number = Column(String, nullable=True)

    roles = relationship("UserRoleMapper", back_populates="user")


#alembic upgrade head
#alembic revision --autogenerate -m "create users and roles"
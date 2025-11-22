
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from myapp.database.connect_db import Base

from myapp.models.permission import RolePermission

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    permissions = relationship("RolePermission", back_populates="role")

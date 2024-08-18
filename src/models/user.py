from typing import Dict

from sqlalchemy import ForeignKey, String, Column, Integer
from sqlalchemy.orm import relationship

from .base import Base
from src.core.types import RoleEnum


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(256), unique=True, nullable=False)
    email = Column(String(128), unique=True, index=True, nullable=False)
    hashed_password = Column(String(1024), nullable=False)
    salt = Column(String(1024), nullable=False, unique=True, index=True)
    role_id = Column(Integer, ForeignKey('role.id'), default=RoleEnum.USER.value)

    role = relationship("Role", back_populates="users")
    snippets = relationship("CodeSnippet", back_populates="creator")

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "email": self.email,
            "role": self.role.to_dict() if self.role else None
        }

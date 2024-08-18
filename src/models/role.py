from typing import Dict

from sqlalchemy import Column, Integer, Enum
from sqlalchemy.orm import relationship

from src.core.types import RoleEnum
from .base import Base


class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(Enum(RoleEnum), unique=True, nullable=False)

    users = relationship("User", back_populates="role")

    def to_dict(self) -> Dict:
        return {
            "name": self.name.name
        }

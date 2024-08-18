import uuid

from sqlalchemy import String, Column, Integer, ForeignKey, UUID
from sqlalchemy.orm import relationship

from .base import Base


class CodeSnippet(Base):
    __tablename__ = "code_snippet"
    id = Column(UUID, primary_key=True, index=True, default=str(uuid.uuid4()))
    programming_language = Column(String(32), nullable=False)
    code = Column(String(16384), nullable=False)
    creator_id = Column(Integer, ForeignKey('user.id'))

    creator = relationship("User", back_populates="snippets")

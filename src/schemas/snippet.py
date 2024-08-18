import uuid

from pydantic import BaseModel, ConfigDict

from typing import Optional


class CodeSnippetBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    programming_language: str
    code: str


class CodeSnippetCreate(CodeSnippetBase):
    creator_id: int


class CodeSnippetUpdate(CodeSnippetBase):
    programming_language: Optional[str] = None
    code: Optional[str] = None


class CodeSnippetSchema(CodeSnippetBase):
    id: uuid.UUID
    creator_id: int


class CodeSnippetResponse(CodeSnippetSchema):
    pass

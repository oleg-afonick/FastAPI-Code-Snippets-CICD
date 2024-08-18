import uuid
from typing import Optional

from sqlalchemy.future import select

from src.db.db import db_dependency
from src.models import CodeSnippet
from src.schemas.snippet import CodeSnippetCreate, CodeSnippetUpdate, CodeSnippetSchema


async def get_code_snippet_by_uuid(db: db_dependency, uuid: str):
    result: Optional[CodeSnippet] = await db.execute(select(CodeSnippet).filter(CodeSnippet.id == uuid))
    if result:
        return result.scalars().first()
    return None


async def create_code_snippet(db: db_dependency, code_snippet: CodeSnippetCreate) -> CodeSnippetSchema:
    statement = CodeSnippet(id=str(uuid.uuid4()),
                            programming_language=code_snippet.programming_language,
                            code=code_snippet.code,
                            creator_id=code_snippet.creator_id)
    db.add(statement)
    await db.commit()
    await db.refresh(statement)
    return CodeSnippetSchema.from_orm(statement)


async def update_code_snippet(db: db_dependency, uuid: str,
                              code_snippet: CodeSnippetUpdate) -> CodeSnippetSchema | None:
    db_code_snippet: Optional[CodeSnippet] = await get_code_snippet_by_uuid(db, uuid)
    if db_code_snippet:
        db_code_snippet.programming_language = code_snippet.programming_language
        db_code_snippet.code = code_snippet.code
        await db.commit()
        await db.refresh(db_code_snippet)
    return db_code_snippet


async def delete_code_snippet(db: db_dependency, uuid: str):
    db_code_snippet: Optional[CodeSnippet] = await get_code_snippet_by_uuid(db, uuid)
    if db_code_snippet:
        await db.delete(db_code_snippet)
        await db.commit()
    return True

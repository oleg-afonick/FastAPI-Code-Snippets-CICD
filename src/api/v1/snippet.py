import logging
from typing import Optional

from fastapi import HTTPException, APIRouter, Depends

from auth.auth import has_role
from core.types import RoleEnum
from db.db import db_dependency
from models import CodeSnippet
from schemas.snippet import CodeSnippetCreate, CodeSnippetUpdate, CodeSnippetResponse
from services.snippet import get_code_snippet_by_uuid, create_code_snippet, update_code_snippet, delete_code_snippet
snippets_router = APIRouter(prefix="/snippets", tags=['snippets'])

logger = logging.getLogger("snippets_logger")


# Получить код по UUID
@snippets_router.get("/{uuid}", responses={
    200: {"model": CodeSnippetResponse, "description": "Success"},
    400: {"description": "Incorrect request"},
    404: {"description": "Not found"},
    500: {"description": "Eternal error"}
})
async def read_code_snippet(uuid: str, db: db_dependency):
    snippet: Optional[CodeSnippet] = await get_code_snippet_by_uuid(db, uuid)
    if not snippet:
        logger.error(f"Сниппет с UUID {uuid} не найден")
        raise HTTPException(status_code=404, detail="Snippet not found")
    logger.info(f"Сниппет с UUID {uuid} найден")
    return CodeSnippetResponse.from_orm(snippet)


# Создать новый кодовый сниппет
@snippets_router.post("/", dependencies=[Depends(has_role([RoleEnum.USER]))],
                      responses={
                          201: {"model": CodeSnippetResponse, "description": "Success"},
                          400: {"description": "Incorrect request"},
                          404: {"description": "Not found"},
                          500: {"description": "Eternal error"}
                      })
async def create_snippet(snippet: CodeSnippetCreate, db: db_dependency):
    created_snippet = await create_code_snippet(db, snippet)
    logger.info(f"Сниппет создан: {created_snippet.id}")

    return created_snippet


# Обновить кодовый сниппет
@snippets_router.put("/{uuid}", dependencies=[Depends(has_role([RoleEnum.USER]))],
                     responses={
                         200: {"model": CodeSnippetResponse, "description": "Success"},
                         400: {"description": "Incorrect request"},
                         404: {"description": "Not found"},
                         500: {"description": "Eternal error"}
                     })
async def update_snippet(uuid: str, snippet: CodeSnippetUpdate, db: db_dependency):
    updated_snippet = await update_code_snippet(db, uuid, snippet)
    if not updated_snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    logger.info(f"Сниппет с UUID {uuid} обновлён: {updated_snippet.code} |"
                f"{updated_snippet.programming_language}|")
    return updated_snippet


# Удалить кодовый сниппет
@snippets_router.delete("/{uuid}", dependencies=[Depends(has_role([RoleEnum.USER]))],
                        responses={
                            400: {"description": "Incorrect request"},
                            404: {"description": "Not found"},
                            500: {"description": "Eternal error"}
                        })
async def delete_snippet(uuid: str, db: db_dependency):
    success = await delete_code_snippet(db, uuid)
    if not success:
        logger.error(f"Сниппет с UUID {uuid} не найден")
        raise HTTPException(status_code=404, detail="Snippet not found")
    logger.info(f"Сниппет с UUID {uuid} успешно удалён")
    return {"status": "success"}

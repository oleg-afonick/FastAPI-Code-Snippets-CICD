from unittest.mock import AsyncMock, patch
from uuid import uuid4

from src.models import CodeSnippet
from src.schemas.snippet import CodeSnippetCreate, CodeSnippetUpdate, CodeSnippetSchema
from src.services.snippet import create_code_snippet, update_code_snippet, delete_code_snippet


async def test_create_code_snippet(mock_db):
    snippet_data = CodeSnippetCreate(
        programming_language="Python",
        code="print('Hello, world!')",
        creator_id=1
    )

    mock_snippet = CodeSnippet(
        id=str(uuid4()),
        programming_language=snippet_data.programming_language,
        code=snippet_data.code,
        creator_id=snippet_data.creator_id
    )

    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    with patch('services.snippet.create_code_snippet', new=AsyncMock(return_value=CodeSnippetSchema.from_orm(mock_snippet))):
        result = await create_code_snippet(mock_db, snippet_data)

    assert result.programming_language == "Python"
    assert result.code == "print('Hello, world!')"
    assert result.creator_id == 1


async def test_update_code_snippet(mock_db):
    snippet_id = str(uuid4())
    snippet_update = CodeSnippetUpdate(
        programming_language="JavaScript",
        code="console.log('Hello, world!')"
    )

    mock_snippet = CodeSnippet(
        id=snippet_id,
        programming_language="Python",
        code="print('Hello, world!')",
        creator_id=1
    )

    CodeSnippet(
        id=snippet_id,
        programming_language=snippet_update.programming_language,
        code=snippet_update.code,
        creator_id=1
    )

    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    with patch('services.snippet.get_code_snippet_by_uuid', new=AsyncMock(return_value=mock_snippet)):
        result = await update_code_snippet(mock_db, snippet_id, snippet_update)
        assert result.programming_language == "JavaScript"
        assert result.code == "console.log('Hello, world!')"


async def test_delete_code_snippet(mock_db):
    snippet_id = str(uuid4())

    mock_snippet = CodeSnippet(
        id=snippet_id,
        programming_language="Python",
        code="print('Hello, world!')",
        creator_id=1  # исправлено на число
    )

    mock_db.commit = AsyncMock()
    mock_db.delete = AsyncMock()

    with patch('services.snippet.get_code_snippet_by_uuid', new=AsyncMock(return_value=mock_snippet)):
        result = await delete_code_snippet(mock_db, snippet_id)
        assert result is True

from unittest.mock import AsyncMock

import pytest_asyncio


@pytest_asyncio.fixture
def mock_db():
    return AsyncMock()

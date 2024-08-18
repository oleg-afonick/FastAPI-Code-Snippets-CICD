import logging.config
import logging.handlers
import atexit
from contextlib import asynccontextmanager
from typing import AsyncContextManager

import uvicorn
from fastapi import FastAPI

from api import api_router
from core.config import uvicorn_options

from core.logger import LOGGING_CONFIG

logger = logging.getLogger("my_app")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncContextManager[None]:
    logging.config.dictConfig(LOGGING_CONFIG)
    queue_handler = logging.getHandlerByName("queue_handler")
    try:
        if queue_handler is not None:
            queue_handler.listener.start()
            atexit.register(queue_handler.listener.stop)
        yield
    except Exception as e:
        logger.error(f"Exception in lifespan: {e}")
        raise
    finally:
        if queue_handler is not None:
            queue_handler.listener.stop()

app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/openapi"
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"msg": "test"}

if __name__ == '__main__':
    # print для отображения настроек в терминале при локальной разработке
    print(uvicorn_options)
    uvicorn.run(
        'main:app',
        **uvicorn_options
    )

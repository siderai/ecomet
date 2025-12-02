from contextlib import asynccontextmanager
from typing import AsyncGenerator

import asyncpg
import uvicorn
from fastapi import FastAPI

from config import Settings
from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    settings = Settings() # type: ignore
    app.state.settings = settings

    pool = await asyncpg.create_pool(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name,
        min_size=settings.db_pool_min_size,
        max_size=settings.db_pool_max_size,
        timeout=settings.db_timeout,
        command_timeout=settings.db_command_timeout,
    )
    app.state.pool = pool

    yield

    await app.state.pool.close()


def create_app() -> FastAPI:
    app = FastAPI(title="e-Comet", lifespan=lifespan)
    app.include_router(router)
    return app


if __name__ == "__main__":
    uvicorn.run(
        "main:create_app",
        factory=True,
    )

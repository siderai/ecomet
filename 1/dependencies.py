from typing import AsyncGenerator

import asyncpg
from fastapi import HTTPException, Request


async def get_pg_connection(request: Request) -> AsyncGenerator[asyncpg.Connection, None]:
    pool: asyncpg.Pool = request.app.state.pool

    try:
        async with pool.acquire() as connection:
            yield connection
    except Exception:
        raise HTTPException(status_code=500, detail="Database connection error")

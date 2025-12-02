from typing import Annotated, cast

import asyncpg
from fastapi import APIRouter, Depends, HTTPException, Request

from dependencies import get_pg_connection
from models import DBVersionResponse, HealthResponse

router = APIRouter(prefix="/api")


@router.get("/health", response_model=HealthResponse)
async def health_check(request: Request) -> HealthResponse:
    try:
        pool: asyncpg.Pool = request.app.state.pool
        async with pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        return HealthResponse(status="healthy", database="connected")
    except Exception:
        raise HTTPException(status_code=503, detail="Service unavailable")


@router.get("/db_version", response_model=DBVersionResponse)
async def get_db_version(
    conn: Annotated[asyncpg.Connection, Depends(get_pg_connection)]
) -> DBVersionResponse:
    try:
        version = await conn.fetchval("SELECT version()")
        return DBVersionResponse(version=cast(str, version))
    except asyncpg.PostgresError:
        raise HTTPException(status_code=500, detail="Database query error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

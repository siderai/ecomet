from pydantic import BaseModel


class DBVersionResponse(BaseModel):
    version: str


class HealthResponse(BaseModel):
    status: str
    database: str

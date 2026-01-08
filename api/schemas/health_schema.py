# api/schemas/health_schema.py
from pydantic import BaseModel
from typing import Dict, Optional

class SystemStatus(BaseModel):
    cpu_usage: float
    memory_usage: float

class HealthResponse(BaseModel):
    status: str          # "ok" ou "error"
    database: str        # "online" ou "offline"
    system: SystemStatus
    version: str = "1.0.0"
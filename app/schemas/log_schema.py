# app/schemas/log_schema.py
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from app.core.database import Base

class LogBase(BaseModel):
    log_source: str
    severity: Optional[str] = None
    message: str
    timestamp: Optional[datetime] = None

class AwsQuery(BaseModel):
    log_group: str
    start_time: str
    end_time: str
    secret_key: str
    access_key: str
    

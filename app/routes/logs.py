import json
import platform
from fastapi import APIRouter,Depends, Query
from sqlalchemy.testing import db
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.crud.logs_crud import save_log
from app.services.logs_service import  fetch_platform_logs
import typing

router=APIRouter()

@router.get("/")
async def fetch_and_save_logs(
    log_types:Optional[typing.List[str]] = Query(None, description="List of log types to fetch")):
    print(log_types)
    try:
        current_platform = platform.system()
        if not log_types:
            if current_platform == "Windows":
                log_types = ["Application"]
            elif current_platform == "Linux":
                log_types = ["syslog"]
            else:
                return {"error": "Unsupported platform"}
            
        logs= await fetch_platform_logs(log_types)
    
        return {"status": "success", "logs_saved": logs}
    except Exception as e:
        return [f"Error fetching  logs: {str(e)}"]
    
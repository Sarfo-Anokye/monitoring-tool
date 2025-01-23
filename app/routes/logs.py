import datetime
import datetime
import json
import platform
from fastapi import APIRouter,Depends, HTTPException, Query
from sqlalchemy.testing import db
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.crud.logs_crud import save_log
from app.services.aws_service import convert_to_timestamp, retrieve_aws_logs
from app.services.logs_service import  fetch_platform_logs
import typing
from app.schemas.log_schema import AwsQuery

router=APIRouter()

@router.get("/")
async def get_local_logs(
    log_types:Optional[typing.List[str]] = Query(None, description="List of log types to fetch")):
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


@router.post("/aws")
def get_aws_logs(
    query:AwsQuery
):
    try:
        start_timestamp,end_timestamp=convert_to_timestamp(query.start_time,query.end_time)

        if start_timestamp >= end_timestamp:
            raise HTTPException(status_code=400, detail="Start time must be before end time.")
        
        credentials={
            "aws_access_key":query.access_key,
            "aws_secret_key":query.secret_key
            
        }

        return retrieve_aws_logs(query.log_group, start_timestamp, end_timestamp,credentials)

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid time format. Use 'YYYY-MM-DDTHH:MM:SS'.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
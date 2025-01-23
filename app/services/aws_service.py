import datetime
from app.core.aws_client_config import initialize_boto3_client
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import HTTPException
def retrieve_aws_logs(log_group: str, start_time: int, end_time: int,credentials):
    try:
        client =initialize_boto3_client("logs",credentials)
        
        # Filter log events
        response = client.filter_log_events(
            logGroupName=log_group,
            startTime=start_time,
            endTime=end_time
        )

        logs = []
        for event in response.get('events', []):
            logs.append({
                "timestamp": event.get("timestamp"),
                "message": event.get("message")
            })

        return logs

    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=str(e))

def convert_to_timestamp(start_time,end_time):
    start_time_clean = start_time.rstrip('Z')
    end_time_clean = end_time.rstrip('Z')
    # Convert start_time and end_time from string to milliseconds
    start_timestamp = int(datetime.datetime.strptime(start_time_clean, "%Y-%m-%dT%H:%M:%S").timestamp() * 1000)
    end_timestamp = int(datetime.datetime.strptime(end_time_clean, "%Y-%m-%dT%H:%M:%S").timestamp() * 1000)
    
    return start_timestamp,end_timestamp
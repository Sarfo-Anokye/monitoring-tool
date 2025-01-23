import boto3

def initialize_boto3_client(service,credentials):

    client= boto3.client(
        service,
        region_name="us-east-1",
        aws_access_key_id=credentials["aws_access_key"],
        aws_secret_access_key=credentials["aws_secret_key"],
    )
    return client

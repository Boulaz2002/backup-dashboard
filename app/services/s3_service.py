import boto3
import os
from app.config import AWS_BUCKET, AWS_REGION

s3 = boto3.client("s3", region_name=AWS_REGION)

def upload_to_s3(file_path: str, s3_key: str):
    s3.upload_file(
        file_path,
        AWS_BUCKET,
        s3_key,
        ExtraArgs={"StorageClass": "GLACIER"}  # Glacier deep archive
    )
    return f"s3://{AWS_BUCKET}/{s3_key}"

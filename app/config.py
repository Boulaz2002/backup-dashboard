import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# AWS Config
AWS_BUCKET = os.getenv("AWS_S3_BUCKET")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Database Config
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/backupdb")

ESXI_HOST=os.getenv("ESXI_HOST")
ESXI_USER=os.getenv("ESXI_USER")
ESXI_PASS=os.getenv("ESXI_PASS")
ESXI_DATASTORE=os.getenv("ESXI_DATASTORE")
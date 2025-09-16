from sqlalchemy import Column, Integer, String, DateTime, func
from app.db import Base

class BackupJob(Base):
    __tablename__ = "backup_jobs"

    id = Column(Integer, primary_key=True, index=True)
    vm_name = Column(String, index=True)
    status = Column(String, default="Pending")
    s3_key = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import BackupJob
from app.services import scheduler
from app.services.s3_service import upload_to_s3
from app.services.esxi_service import backup_vm_esxi
from app.services.scheduler import schedule_backup

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Trigger a new backup job
@router.post("/now")
def trigger_backup(vm_name: str, db: Session = Depends(get_db)):
    # 1. Create local backup file
    backup_file = f"/tmp/{vm_name}_backup.txt"
    with open(backup_file, "w") as f:
        f.write(f"Backup data for {vm_name}")

    # 2. Upload to S3 Glacier
    s3_key = f"backups/{vm_name}/{vm_name}_backup.txt"
    s3_uri = upload_to_s3(backup_file, s3_key)

    # 3. Save job in DB
    job = BackupJob(vm_name=vm_name, status="Success", s3_key=s3_uri)
    db.add(job)
    db.commit()
    db.refresh(job)

    return {"message": f"Backup uploaded to {s3_uri}", "job_id": job.id}

@router.post("/now1")
def trigger_backup(vm_name: str, db: Session = Depends(get_db)):
    # 1. Run ESXi backup
    backup_file = backup_vm_esxi(vm_name)

    # 2. Upload to S3 Glacier
    s3_key = f"backups/{vm_name}/{os.path.basename(backup_file)}"
    s3_uri = upload_to_s3(backup_file, s3_key)

    # 3. Save DB record
    job = BackupJob(vm_name=vm_name, status="Success", s3_key=s3_uri)
    db.add(job)
    db.commit()
    db.refresh(job)

    return {"message": f"Backup uploaded to {s3_uri}", "job_id": job.id}

@router.get("/jobs")
def list_jobs():
    jobs = scheduler.get_jobs()
    return [{"id": job.id, "next_run": str(job.next_run_time)} for job in jobs]


@router.post("/schedule")
def schedule_vm_backup(vm_name: str, hour: int, minute: int = 0, day_of_week: str = "*"):
    """
    Schedule automated backup for a VM.
    Example: {"vm_name": "fake_disk", "hour": 2, "minute": 30, "day_of_week": "0"}
    → Every Sunday at 2:30 AM
    """
    schedule_backup(vm_name, hour=hour, minute=minute, day_of_week=day_of_week)
    return {"message": f"Backup for {vm_name} scheduled at {hour:02d}:{minute:02d}, day {day_of_week}"}


# Get backup history
@router.get("/history")
def get_backups(db: Session = Depends(get_db)):
    jobs = db.query(BackupJob).all()
    return jobs

# Update status manually
@router.put("/{job_id}/status")
def update_status(job_id: int, status: str, db: Session = Depends(get_db)):
    job = db.query(BackupJob).filter(BackupJob.id == job_id).first()
    if not job:
        return {"error": "Job not found"}
    job.status = status
    db.commit()
    return {"message": f"Job {job_id} updated to {status}"}


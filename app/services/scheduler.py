from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.services.esxi_service import backup_vm_esxi
from app.services.s3_service import upload_to_s3
from app.db import SessionLocal
from app.models import BackupJob
import os



scheduler = BackgroundScheduler()
scheduler.start()

def schedule_backup(vm_name: str, hour: int = 2, minute: int = 0, day_of_week: str = "*"):
    """
    Schedule automatic backup of a VM at a given time.
    - hour: 0–23
    - minute: 0–59
    - day_of_week: "0-6" (0=Sunday) or "*" for daily
    """
    def job():
        db = SessionLocal()
        try:
            backup_file = backup_vm_esxi(vm_name)
            s3_key = f"backups/{vm_name}/{os.path.basename(backup_file)}"
            s3_uri = upload_to_s3(backup_file, s3_key)

            job = BackupJob(vm_name=vm_name, status="Success", s3_key=s3_uri)
            db.add(job)
            db.commit()
        except Exception as e:
            job = BackupJob(vm_name=vm_name, status="Fail", s3_key=str(e))
            db.add(job)
            db.commit()
        finally:
            db.close()

    scheduler.add_job(
        job,
        CronTrigger(hour=hour, minute=minute, day_of_week=day_of_week),
        id=f"backup_{vm_name}",
        replace_existing=True
    )

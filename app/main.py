from fastapi import FastAPI
from app.db import Base, engine
from app.routers import backup

# Auto-create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Backup Dashboard API")

# Register routes
app.include_router(backup.router, prefix="/backup", tags=["backup"])

@app.get("/")
def root():
    return {"message": "Backup Dashboard API Running"}

from fastapi import FastAPI, Depends, UploadFile, File
from database import init_db
from database import get_db
from sqlalchemy.orm import Session
from crud import calculateMetrics, getMetricsByUsername, getAllMetrics

app = FastAPI(
    title="Post and Profile Metrics API",
    description="API for exxploring post and profile metrics",
    version="1.0.0",
    contact={
        "name": "Farooq Memon",
    }
)

init_db()

@app.get("/")
async def root():
    return {"message": "Welcome to the Post and Profile Metrics API"}

@app.post("/metrics")
async def metrics(profileFile: UploadFile = File(...), postFile: UploadFile = File(...), db: Session = Depends(get_db)):
    return await calculateMetrics(profileFile, postFile, db)

@app.get("/metrics")
async def get_all_metrics(db: Session = Depends(get_db)):
    return await getAllMetrics(db)

@app.get("/metrics/{username}")
async def get_metrics(username: str, db: Session = Depends(get_db)):
    return await getMetricsByUsername(username, db)
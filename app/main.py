from fastapi import FastAPI
from database import init_db

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
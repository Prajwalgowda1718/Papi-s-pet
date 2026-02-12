from fastapi import FastAPI
from app.config import settings
from app.db.database import init_db



app=FastAPI(title="Papi's pet API")

@app.get("/")
def root():
    return {
        "message": "Papi's Pet is running",
        "environment": settings.APP_ENV,
        "debug": settings.DEBUG,
        
    }


@app.get("/health")
def health_check():
    return {"Status": "OK"}

@app.on_event("startup")
def startup_event():
    init_db()

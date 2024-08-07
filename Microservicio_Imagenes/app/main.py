import sys
import os

# Añade el directorio padre al Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from app.routes import images
from app.database import init_db

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    init_db()

app.include_router(images.router, tags=["images"])

@app.get("/")
async def root():
    return {"message": "Hola Mundo"}
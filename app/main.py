import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
from app.routers import video_processing

app = FastAPI()

# Incluir el router de procesamiento de video
app.include_router(video_processing.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de procesamiento de videos para evaluación de rúbricas."}

from fastapi import FastAPI, UploadFile, File, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
import sys
import shutil
import asyncio
from src.models.transcript_model import model_execution
from src.data.preprocess import split_transcript_audio
from src.models.gpt_model import process_video

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Ajusta esta ruta para apuntar al directorio externo de videos
VIDEO_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data/raw'))

# Almacena conexiones de WebSocket
connections = []

@app.websocket("/ws/progress")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            await asyncio.sleep(1)  # Mantiene la conexión abierta
    except WebSocketDisconnect:
        connections.remove(websocket)

async def notify_progress(message: str):
    for connection in connections:
        await connection.send_text(message)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    videos = [f for f in os.listdir(VIDEO_DIRECTORY) if f.endswith(".mp4")]
    return templates.TemplateResponse("index.html", {"request": request, "videos": videos})

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    file_location = os.path.join(VIDEO_DIRECTORY, file.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return {"info": f"Archivo {file.filename} subido correctamente"}

@app.post("/process-video/")
async def process_video_endpoint(request: Request, video_file: str = Form(...)):
    video_path = os.path.join(VIDEO_DIRECTORY, video_file)
    interval_seconds = 60  # Puedes ajustar este valor según sea necesario

    # Notificación inicial de procesamiento
    await notify_progress(f"Procesando el video: {video_file}...")

    # Lógica para procesar el video
    await asyncio.sleep(1)  # Simulación de inicio de procesamiento
    videos = process_video(video_path, interval_seconds)
    await notify_progress("Extracción de video completada.")

    transcription = split_transcript_audio(video_path)
    await notify_progress("Transcripción completada.")

    rubricas = model_execution(transcription)
    await notify_progress("Modelo de rúbricas ejecutado.")

    # Combina los resultados de las rúbricas y los videos procesados
    rubrica_total = rubricas + videos
    print(rubrica_total)
    # Retorna la página con la tabla de rúbricas
    await notify_progress("Procesamiento completado.")
    return templates.TemplateResponse("index.html", {"request": request, "videos": os.listdir(VIDEO_DIRECTORY), "rubricas": rubrica_total})
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from fastapi import FastAPI, UploadFile, File
# from fastapi.responses import JSONResponse
# import os
# from app.routers import video_processing

# app = FastAPI()

# # Incluir el router de procesamiento de video
# app.include_router(video_processing.router)

# @app.get("/")
# def read_root():
#     return {"message": "Bienvenido a la API de procesamiento de videos para evaluación de rúbricas."}

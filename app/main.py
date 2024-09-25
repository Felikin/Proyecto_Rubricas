from fastapi import FastAPI, UploadFile, File, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import Request
import os
import asyncio
from src.models.transcript_model import model_execution
from src.data.preprocess import split_transcript_audio
from src.models.gpt_model import process_video

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Directorio de videos
VIDEO_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data/raw'))

# Almacena conexiones de WebSocket
connections = []
rubrica_total_global = None  # Variable global para almacenar las rúbricas

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
        try:
            await connection.send_text(message)
        except WebSocketDisconnect:
            connections.remove(connection)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    videos = [f for f in os.listdir(VIDEO_DIRECTORY) if f.endswith(".mp4")]
    return templates.TemplateResponse("index.html", {"request": request, "videos": videos})

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    file_location = os.path.join(VIDEO_DIRECTORY, file.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    videos = [f for f in os.listdir(VIDEO_DIRECTORY) if f.endswith(".mp4")]
    return {"info": f"Archivo {file.filename} subido correctamente", "videos": videos}

@app.get("/results", response_class=HTMLResponse)
async def results_page(request: Request):
    global rubrica_total_global
    return templates.TemplateResponse("results.html", {"request": request, "rubricas": rubrica_total_global})

@app.post("/process-video/")
async def process_video_endpoint(request: Request, video_file: str = Form(...)):
    global rubrica_total_global  # Usa la variable global
    video_path = os.path.join(VIDEO_DIRECTORY, video_file)
    interval_seconds = 60  # Intervalo de tiempo para dividir el video en segmentos

    # Notificación inicial de procesamiento
    await notify_progress(f"Procesando el video: {video_file}...")

    try:
        # Procesamiento del video
        await asyncio.sleep(1)  # Simulación de inicio de procesamiento
        videos = process_video(video_path, interval_seconds)
        await notify_progress("Extracción de video completada.")

        # Transcripción del audio
        transcription = split_transcript_audio(video_path)
        await notify_progress("Transcripción completada.")

        # Ejecución del modelo de rúbricas
        rubricas = model_execution(transcription)
        await notify_progress("Modelo de rúbricas ejecutado.")

        # Combina los resultados de las rúbricas y los videos procesados
        rubrica_total_global = rubricas + videos
        print(rubrica_total_global)
        await notify_progress("Procesamiento completado.")
        return RedirectResponse(url="/results", status_code=303)
    
    except Exception as e:
        # Notificar sobre errores durante el procesamiento
        await notify_progress(f"Error durante el procesamiento: {str(e)}")
        return {"error": "Ocurrió un error durante el procesamiento del video."}
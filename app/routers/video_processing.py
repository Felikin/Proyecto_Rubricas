from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import os
from src.models.transcript_model import model_execution
from src.data.preprocess import split_transcript_audio
from src.models.gpt_model import process_video

router = APIRouter()

@router.post("/upload_video/")
async def upload_video(file: UploadFile = File(...), interval_seconds: int = 60):
    # Guardar el video cargado
    video_path = f"data/raw/{file.filename}"
    with open(video_path, "wb") as video:
        content = await file.read()
        video.write(content)
    
    # Procesar el video y la transcripción
    videos = process_video(video_path, interval_seconds)
    transcription = split_transcript_audio(video_path)
    rubricas = model_execution(transcription)
    rubrica_total = rubricas + videos
    
    return JSONResponse(content=rubrica_total)

@router.get("/process_video/{video_name}")
async def process_video_endpoint(video_name: str, interval_seconds: int = 60):
    video_path = f"data/raw/{video_name}"
    
    if not os.path.exists(video_path):
        return JSONResponse(content={"error": "Video no encontrado"}, status_code=404)
    
    # Procesar el video y la transcripción
    videos = process_video(video_path, interval_seconds)
    transcription = split_transcript_audio(video_path)
    rubricas = model_execution(transcription)
    rubrica_total = rubricas + videos
    
    return JSONResponse(content=rubrica_total)

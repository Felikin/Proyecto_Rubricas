from fastapi import FastAPI, File, UploadFile
from utils import split_transcript_audio, model_execution
import json
import os

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World :D!"}


@app.post("/process_video")
async def process_audio(file: UploadFile = File(...)):
    
    # Escritura temporal del  video en el servidor
    temp_video_path = f"from_fastapi_{file.filename}"
    with open(temp_video_path, "wb") as f:
        f.write(await file.read())

    # Generación de la transcripción de la clase
    transcription = split_transcript_audio(temp_video_path)

    with open("fastapi_transcripcion.txt", "w") as transcription_file:
        transcription_file.write(transcription)
    
    # Evaluación de las rúbricas
    rubricas = model_execution(transcription)
    with open("fastapi_rubricas.txt", "w") as rubricas_file:
        rubricas_file.write(json.dumps(rubricas, ensure_ascii=False))

    # Eliminación del video del servidor
    os.remove(temp_video_path)

    return {"Rúbricas": rubricas}
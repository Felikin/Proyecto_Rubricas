import os
import cv2
from ultralytics import YOLO
from moviepy.editor import VideoFileClip
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def load_video(video_path: str) -> cv2.VideoCapture:
    """
    Carga un video desde la ruta especificada.
    
    Args:
    video_path (str): Ruta al video.

    Returns:
    video (cv2.VideoCapture): video abierto con opencv.
    """
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        raise ValueError(f"Error opening video file: {video_path}")
    return video


def load_yolo_model(model_path: str) -> YOLO:
    """
    Carga un modelo YOLO preentrenado desde la ruta especificada.
    
    Args:
    model_path (str): Ruta al modelo YOLO.

    Returns:
    YOLO: Modelo YOLO cargado.
    """
    return YOLO(model_path)


def extract_audio(video_path: str) -> str:
    """
    Recibe un archivo mp4 y guarda el archivo de audio en formato mp3.
    Args:
        video_path: ruta donde está almacenado el archivo mp4
    """
    video = VideoFileClip(video_path)
    audio = video.audio
    audio_file_name = "data/generated/audio_from_video.mp3"
    audio.write_audiofile(audio_file_name) # type: ignore
    audio.close() # type: ignore
    video.close()

    return audio_file_name


def initialize_gpt_client():
    """Inicializa el cliente GPT usando la API de OpenAI.

    Returns:
        OpenAI: Cliente para realizar llamadas a la API.
    """
    return OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))


def transcript_audio(audio_path: str, client) -> str:
    """
    Recibe un archivo .mp3 y devuelve la transcripción del audio.
    
    Args:
        audio_path: ruta del archivo mp3.
    Returns:
        str: Transcripción del audio mp3.
    """

    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcription.text
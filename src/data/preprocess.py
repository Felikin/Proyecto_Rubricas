import os
import cv2
import base64
import math
import numpy as np
from pydub import AudioSegment
from tqdm import tqdm
from src.data.load_data import extract_audio, transcript_audio, initialize_gpt_client

def encode_image_to_base64(frame: np.ndarray) -> str:
    """Codifica un frame de video a formato base64.

    Args:
        frame (numpy.ndarray): Frame de video en formato numpy.

    Returns:
        str: Imagen codificada en base64.
    """
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    smgframe = cv2.resize(gray_frame, (640,480)) 

    _, buffer = cv2.imencode(".jpg", smgframe)
    return base64.b64encode(buffer).decode('utf-8')


def split_transcript_audio(video_path: str) -> str:
    """
    Recibe un string con la ruta del mp4 a transcribir y devuelve la transcripción de dicho archivo.
    Args:
        audio_path: Ruta del archivo mp4 a transcribir.
    Returns:
        str: Transcripción del archivo.
    """

    audio_path = extract_audio(video_path)
    client = initialize_gpt_client()

    audio = AudioSegment.from_mp3(audio_path)
    diez_minutos = 10 * 60 * 1000 # Duración de los sub audios para su posterior transcripción
    transcripciones = []

    num_fragmentos_10_min = math.ceil(len(audio) / diez_minutos)
    start = 0
    end = diez_minutos
    sub_audio_name = "sub_audio_aux.mp3"

    for i in tqdm(range(num_fragmentos_10_min), desc="Realizando Transcripciones"):
        audio[start:end].export(sub_audio_name, format="mp3")
        transcripciones.append(transcript_audio(sub_audio_name, client))
        start = end
        end += diez_minutos

    transcripcion = " ".join(transcripciones)
    try:
        os.remove(sub_audio_name)
        os.remove(audio_path)
    except Exception as e:
        print(e, "\n")

    return transcripcion
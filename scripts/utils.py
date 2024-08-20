from openai import OpenAI
from langchain_openai import ChatOpenAI
from prompts.prompts import *
from dotenv import load_dotenv
from typing import List
from pydub import AudioSegment
import math
from tqdm import tqdm
import os
from moviepy.editor import VideoFileClip


load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")


def extract_audio(video_path: str) -> str:
    """
    Recibe un archivo mp4 y guarda el archivo de audio en formato mp3.
    Args:
        video_path: ruta donde está almacenado el archivo mp4
    """
    video_file = video_path
    video = VideoFileClip(video_file)
    audio = video.audio

    audio_file_name = "audio_from_video.mp3"

    audio.write_audiofile(audio_file_name) # type: ignore

    audio.close() # type: ignore
    video.close()

    return audio_file_name


def transcript_audio(audio_path: str) -> str:
    """
    Recibe un archivo .mp3 y devuelve la transcripción del audio.
    
    Args:
        audio_path: ruta del archivo mp3.
    Returns:
        str: Transcripción del audio mp3.
    """

    with open(audio_path, "rb") as audio_file:
        client = OpenAI(
            api_key=openai_api_key
        )
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcription.text
    

def model_execution(transcripcion: str) -> List[dict]:
    """
    Recibe una transcrición y devuelve la evaluación de las rúbricas.
    
    Args:
        transcripcion (str): Transcripción de un audio, usualmente una clase.
    Returns:
        List: Lista de diccionarios con la evaluación de las rúbricas.
    """
    
    llm = ChatOpenAI(
        model="gpt-4o-mini-2024-07-18",
        api_key=openai_api_key, # type:ignore
        temperature=0
    )
    chain_rubricas = prompt_rubricas | llm | output_parser
    results = chain_rubricas.invoke(input={"transcripcion": transcripcion})

    return results["rubricas"]


def split_transcript_audio(video_path: str) -> str:
    """
    Recibe un string con la ruta del mp4 a transcribir y devuelve la transcripción de dicho archivo.
    Args:
        audio_path: Ruta del archivo mp4 a transcribir.
    Returns:
        str: Transcripción del archivo.
    """

    audio_path = extract_audio(video_path)

    audio = AudioSegment.from_mp3(audio_path)
    diez_minutos = 10 * 60 * 1000 # Duración de los sub audios para su posterior transcripción
    transcripciones = []

    num_fragmentos_10_min = math.ceil(len(audio) / diez_minutos)
    start = 0
    end = diez_minutos
    sub_audio_name = "sub_audio_aux.mp3"

    for i in tqdm(range(num_fragmentos_10_min)):
        audio[start:end].export(sub_audio_name, format="mp3")
        transcripciones.append(transcript_audio(sub_audio_name))
        start = end
        end += diez_minutos

    transcripcion = " ".join(transcripciones)
    try:
        os.remove(sub_audio_name)
        os.remove(audio_path)
    except Exception as e:
        print(e, "\n")

    return transcripcion
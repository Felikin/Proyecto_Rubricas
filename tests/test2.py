import cv2
import base64
import os
import requests
import time
from openai import OpenAI
from collections import deque
from datetime import datetime
from tqdm import tqdm
from dotenv import load_dotenv
load_dotenv()

def encode_image_to_base64(frame):
    _, buffer = cv2.imencode(".jpg", frame)
    return base64.b64encode(buffer).decode('utf-8')

def send_frame_to_gpt(frame, client):
  
    # Prepare message payload for sending the frame to GPT
    # Evaluate if the previous prediction matches the current situation from the context,
    # and instruct to make the next prediction
    prompt_message = """
        Por favor, analiza la siguiente imagen codificada en base64 proveniente de un video de una clase y 
        1. Presencia del Profesor: Indica si el profesor aparece en cámara en este frame. Devuelve true si aparece, de lo contrario, false.\n
        2. Conteo de Diapositivas: Indica si en este frame se muestra una diapositiva. Si hay una diapositiva presente, 
        proporciona el contenido textual principal de la diapositiva.\n
        3. Contenido de la Diapositiva:\n
           - Gráficos: Indica si en la diapositiva aparece algún gráfico o imagen visual. Devuelve true si hay gráficos presentes,
        de lo contrario, false.\n"
           - Cantidad de Texto: Evalúa la cantidad de texto presente en la diapositiva. Clasifica la cantidad de texto en
        baja, media o alta según la densidad textual.\n\n
        
        Proporciona la salida en un diccionario de la siguiente forma:
        "Camara": "<True/False>",
        "Slide": <True/False>,\n'
        "Contenido": {
            "texto": "<contenido textual principal>",
            "graficos": <True/False>,
            "Cantidad de texto": "<baja/media/alta>"
          }

        No hagas NINGÚN comentario adicional
        """
    

    PROMPT_MESSAGES = {
        "role": "user",
        "content": [
            prompt_message,
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{frame}"}}
        ]
    }

    # Parameters for API call
    params = {
        "model": "gpt-4o-2024-08-06",
        "messages": [PROMPT_MESSAGES],
        "max_tokens": 500,
    }

    # Make the API call
    result = client.chat.completions.create(**params)
    return result.choices[0].message.content

def main():
    video_path = "data/raw/Juan Sebastian Lozano.mp4"
    interval_seconds = 3600
    # Initialize OpenAI client
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

    # Open PC's internal camera
    video = cv2.VideoCapture(video_path)
    fps = int(video.get(cv2.CAP_PROP_FPS))  # Obtener la tasa de FPS real del video
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frames_to_capture = range(0, total_frames, interval_seconds * fps)

    # Queue to hold the texts of the most recent 5 frames
    for frame_index in tqdm(frames_to_capture, desc="Seleccionando frames"):
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = video.read()
        if not ret:
            break
        base64_image = encode_image_to_base64(frame)

        # Send the frame to GPT and get the generated text
        generated_text = send_frame_to_gpt(base64_image, client)
        print(f"Generated Text: {generated_text}")

        # Wait for 1 second
        time.sleep(1)

    # Release the video
    video.release()

if __name__ == "__main__":
    main()
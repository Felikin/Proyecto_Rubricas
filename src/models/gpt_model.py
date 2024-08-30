import cv2
import base64
from typing import List, Dict
from tqdm import tqdm
from dotenv import load_dotenv
from src.data.load_data import load_video, initialize_gpt_client
from src.data.preprocess import encode_image_to_base64
from src.utils.video_utils import process_gpt_outputs
from src.prompts.prompt_templates import generate_prompt_message
load_dotenv()

def process_video(video_path: str, interval_seconds: int) -> Dict:
    """
    Procesa un video para enviar frames a gpt y analizar contenido.

    Args:
    video_path (str): Ruta al archivo de video.
    interval_seconds (int): Proporcion de tiempo a saltar para la detección.

    Returns:
    dict: Detecciones en frames enviados.
    """
    # Cargar el video
    video = load_video(video_path)
    fps = int(video.get(cv2.CAP_PROP_FPS))
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frames_to_capture = range(0, total_frames, interval_seconds * fps)
    # Procesar cada frame seleccionado
    model_output = []
    for frame_index in tqdm(frames_to_capture, desc = "Analizando video"):
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = video.read()
        if not ret:
            break
        base64_image = encode_image_to_base64(frame)
        prompt = generate_prompt_message(base64_image)
        generated_text = send_gpt_request(prompt)
        model_output.append(generated_text)
    video.release()
    cv2.destroyAllWindows()
    results = process_gpt_outputs(model_output)

    return results

def send_gpt_request(prompt_message: dict) -> dict:
    """
    Envía una solicitud a GPT y retorna el resultado.

    Args:
        client: Cliente de OpenAI.
        prompt_message (dict): Mensaje de prompt generado.

    Returns:
        dict: Resultado del análisis del frame.
    """
    client = initialize_gpt_client()
    params = {
        "model": "gpt-4o-2024-08-06",
        "messages": [prompt_message],
        "max_tokens": 500,
    }
    result = client.chat.completions.create(**params)
    return result.choices[0].message.content

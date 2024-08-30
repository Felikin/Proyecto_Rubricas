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
        #generated_text = send_frame_to_gpt(base64_image)
        generated_text = send_gpt_request(prompt)
        print(generated_text)
        model_output.append(generated_text)
        with open(f"data/generated/{frame_index}.png", "wb") as fh:
             fh.write(base64.decodebytes(bytes(base64_image, "utf-8")))
    video.release()
    results = process_gpt_outputs(model_output)
    cv2.destroyAllWindows()

    return results


# def send_frame_to_gpt(frame):
#     """Envía un frame de video a GPT para análisis y obtiene el resultado.

#     Args:
#         frame (str): Frame codificado en base64.
#         client (OpenAI): Cliente de OpenAI.

#     Returns:
#         dict: Resultado del análisis del frame.
#     """
#     client = initialize_gpt_client()

#     prompt_message = """
#         Por favor, analiza la siguiente imagen codificada en base64 proveniente de un video de una clase y 
#         1. Presencia del Profesor: Indica si el profesor aparece en cámara en este frame. Devuelve true si aparece, de lo contrario, false.\n
#         2. Conteo de Diapositivas: Indica si en este frame se muestra una diapositiva. Si hay una diapositiva presente, 
#         proporciona el contenido textual principal de la diapositiva.\n
#         3. Contenido de la Diapositiva:\n
#            - Gráficos: Indica si en la diapositiva aparece algún gráfico o imagen visual. Devuelve true si hay gráficos presentes,
#         de lo contrario, false.\n
#            - Cantidad de Texto: Evalúa la cantidad de texto presente en la diapositiva. Clasifica la cantidad de texto en
#         baja, media o alta según la densidad textual.\n\n
        
#         Proporciona la salida en un diccionario de la siguiente forma:
#         "Camara": "<True/False>",
#         "Slide": "<True/False>",
#         "Contenido": {
#             "texto": "<contenido textual principal>",
#             "graficos": "<True/False>",
#             "Cantidad de texto": "<baja/media/alta>"
#           }

    
#         No hagas NINGÚN (```, json) comentario adicional, ni añadas texto diferente (```, json) al formato de salida, NADA DIFERENTE a la salida. Si no puedes analizar la imagen devuelve todo negativo. 
#     """

#     PROMPT_MESSAGES = {
#         "role": "user",
#         "content": [
#             prompt_message,
#             {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{frame}"}}
#         ]
#     }

#     params = {
#         "model": "gpt-4o-2024-08-06",
#         "messages": [PROMPT_MESSAGES],
#         "max_tokens": 500,
#     }
#     result = client.chat.completions.create(**params)
#     return result.choices[0].message.content


def send_gpt_request(prompt_message):
    """Envía una solicitud a GPT y retorna el resultado.

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

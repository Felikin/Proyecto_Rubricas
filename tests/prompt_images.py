import cv2
from openai import OpenAI
import json
import os
from tqdm import tqdm
from PIL import Image
import base64
import io
from dotenv import load_dotenv
load_dotenv()

# Configura tu clave API de OpenAI
client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY")
)


def select_frames(video_path, interval_seconds=60, resolution=(640, 480)):
    """
    Selecciona frames del video cada cierto intervalo de segundos basado en la tasa de FPS del video.
    Reduce la resolución de los frames seleccionados.
    """
    video = cv2.VideoCapture(video_path)
    fps = int(video.get(cv2.CAP_PROP_FPS))  # Obtener la tasa de FPS real del video
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frames_to_capture = range(0, total_frames, interval_seconds * fps)

    selected_frames = []
    for frame_index in tqdm(frames_to_capture, desc="Seleccionando frames"):
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = video.read()
        if not ret:
            break
        # Reducir resolución
        resized_frame = cv2.resize(frame, resolution)
        selected_frames.append(resized_frame)
    
    video.release()
    return selected_frames

def frame_to_base64(frame):
    """
    Convierte un frame de imagen a base64 para enviarlo a la API de OpenAI.
    """
    _, buffer = cv2.imencode('.jpg', frame)
    img_str = base64.b64encode(buffer).decode('utf-8')
    return img_str

def generate_prompt(frames):
    """
    Genera el prompt para la API de OpenAI a partir de los frames seleccionados.
    """
    prompt = (
        "Por favor, analiza la siguiente imagen codificada en base64 proveniente de un video de una clase y "
        "proporciona la siguiente información en formato JSON:\n\n"
        "1. Presencia del Profesor: Indica si el profesor aparece en cámara en este frame. Devuelve true si aparece, de lo contrario, false.\n"
        "2. Conteo de Diapositivas: Indica si en este frame se muestra una diapositiva. Si hay una diapositiva presente, "
        "proporciona el contenido textual principal de la diapositiva.\n"
        "3. Contenido de la Diapositiva:\n"
        "   - Gráficos: Indica si en la diapositiva aparece algún gráfico o imagen visual. Devuelve true si hay gráficos presentes, "
        "de lo contrario, false.\n"
        "   - Cantidad de Texto: Evalúa la cantidad de texto presente en la diapositiva. Clasifica la cantidad de texto en "
        "baja, media o alta según la densidad textual.\n\n"
        "Proporciona la salida en el siguiente formato JSON:\n\n"
        "{\n"
        '  "frame_number": <número del frame>,\n'
        '  "professor_present": <true/false>,\n'
        '  "slide_present": <true/false>,\n'
        '  "slide_content": {\n'
        '    "text": "<contenido textual principal>",\n'
        '    "graphics_present": <true/false>,\n'
        '    "text_density": "<baja/media/alta>"\n'
        "  }\n"
        "}\n\n"
        "Analiza la siguiente imagen:\n"
    )
    
    for i, frame in enumerate(frames):
        frame_base64 = frame_to_base64(frame)
        prompt += f"Imagen: {frame_base64}\n"
        print(prompt)

    return prompt

def send_to_openai(prompt):
    """
    Envía el prompt a la API de OpenAI y devuelve la respuesta.
    """
    response = client.chat.completions.create(
        model="gpt-4o",  # Usa el modelo adecuado según tus necesidades y disponibilidad
        messages=[
            {"role": "system", "content": "Eres un asistente que analiza contenido de video."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=2048,
        temperature=0.7,
    )
    return response

def process_video(video_path, interval_seconds=60, resolution=(640, 480)):
    """
    Procesa el video, selecciona frames, genera el prompt, y envía la solicitud a OpenAI.
    """
    # Selecciona frames del video
    print("Seleccionando frames...")
    frames = select_frames(video_path, interval_seconds, resolution)

    # Genera el prompt
    print("Generando prompt...")
    prompt = generate_prompt(frames)

    # Envía el prompt a OpenAI
    print("Enviando a OpenAI...")
    response = send_to_openai(prompt)

    # Procesa la respuesta de OpenAI
    result = response.choices[0].message.content
    print("Resultado recibido de OpenAI:\n", result)

    # Guarda el resultado en un archivo JSON
    with open("resultado_openai.json", "w") as outfile:
        json.dump(result, outfile, indent=4)

if __name__ == "__main__":
    video_path = "data/raw/Juan Sebastian Lozano.mp4"  # Asegúrate de proporcionar la ruta correcta al archivo de video
    process_video(video_path, interval_seconds=4000, resolution=(640, 480))

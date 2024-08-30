from collections import deque
from statistics import mode
import json
import re
from tqdm import tqdm

def clean_gpt_output(output: str) -> dict:
    """Limpia el string JSON devuelto por GPT y lo convierte en un diccionario."""
    json_str = re.sub("```|json", "", output)
    try:
        return json.loads(json_str)
    except: 
        return None

def process_gpt_outputs(gpt_outputs: dict) -> list:
    """
    Procesa los resultados generados por GPT a partir de frames de video.

    Args:
        gpt_outputs (dict): Una lista de strings en formato JSON que contienen 
                            los resultados generados por GPT. Cada string representa 
                            el análisis de un frame de video y contiene información 
                            sobre la presencia del profesor, diapositivas, gráficos, 
                            y la cantidad de texto en las diapositivas.

    Returns:
        list: Una lista de diccionarios con las siguientes claves:
            - "nombre" (str): Nombre de la rúbrica
            - "cumple" (bool):  Indica si cumple o no la rúbrica
            - "observacion" (str): Comentario adicional
    """
    professor_count = 0
    slide_count = 0
    graficos = 0
    text_quantities = []

    for output in tqdm(gpt_outputs, desc="Calculando resultados"):
        if output is not None: 
            output_dict = clean_gpt_output(output)
            if output_dict["Camara"] == "True":
                professor_count += 1
            if output_dict["Slide"]:
                slide_count += 1
            if output_dict["Contenido"]["graficos"]:
                graficos += 1
            text_quantities.append(output_dict["Contenido"]["Cantidad de texto"])
        else:
            pass
    
#    most_common_text_quantity = mode(text_quantities)
    
    return [
        {"nombre": "El docente prende la cámara", "cumple": professor_count > len(gpt_outputs)/2, "observacion": "Sin comentarios adicionales"},
        {"nombre": "El número de diapositivas es acorde con el tiempo de la sesión", "cumple": slide_count, "observacion": "Sin comentarios adicionales"},
        {"nombre": "Las diapositivas o material usado incluyen gráficas, evita el exceso de información", "cumple": graficos > len(gpt_outputs)/2, "observacion": "Sin comentarios adicionales"}
        ]
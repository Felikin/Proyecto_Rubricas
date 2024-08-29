from collections import deque
from statistics import mode
import json

def process_gpt_outputs(gpt_outputs):
    professor_count = 0
    slide_count = 0
    text_quantities = []

    for output in gpt_outputs:
        output_dict = json.loads(output)
        if output_dict["Camara"] == "True":
            professor_count += 1
        if output_dict["Slide"]:
            slide_count += 1
        text_quantities.append(output_dict["Contenido"]["Cantidad de texto"])
    
    most_common_text_quantity = mode(text_quantities)
    
    return {
        "Profesor_en_Cámara": professor_count > 0,
        "Diapositivas_presentes": slide_count > 0,
        "Moda_de_Texto": most_common_text_quantity
    }

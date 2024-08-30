from collections import deque
from statistics import mode
import json
import re
from tqdm import tqdm

def process_gpt_outputs(gpt_outputs):
    professor_count = 0
    slide_count = 0
    graficos = 0
    text_quantities = []

    for output in tqdm(gpt_outputs, desc="Calculando resultados"):
        if output is not None: 
            json_str = re.sub("```|json", "", output)
            output_dict = json.loads(json_str)
            if output_dict["Camara"] == "True":
                professor_count += 1
            if output_dict["Slide"]:
                slide_count += 1
            if output_dict["Contenido"]["graficos"]:
                graficos += 1
            text_quantities.append(output_dict["Contenido"]["Cantidad de texto"])
        else:
            pass
    
    most_common_text_quantity = mode(text_quantities)
    
    return {
        "Profesor_en_Cámara": professor_count > len(gpt_outputs)/2,
        "Diapositivas_presentes": slide_count,
        "Moda_de_Texto": most_common_text_quantity,
        "Gráficos": graficos > len(gpt_outputs)/3
    }
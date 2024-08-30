
def generate_prompt_message(frame):
    """Genera el mensaje de prompt para el análisis de la imagen.

    Args:
        frame (str): Frame codificado en base64.

    Returns:
        dict: Diccionario con el mensaje de prompt.
    """
    prompt_message = """
        Por favor, analiza la siguiente imagen codificada en base64 proveniente de un video de una clase y 
        1. Presencia del Profesor: Indica si el profesor aparece en cámara en este frame. Devuelve true si aparece, de lo contrario, false.\n
        2. Conteo de Diapositivas: Indica si en este frame se muestra una diapositiva. Si hay una diapositiva presente, 
        proporciona el contenido textual principal de la diapositiva.\n
        3. Contenido de la Diapositiva:\n
           - Gráficos: Indica si en la diapositiva aparece algún gráfico o imagen visual. Devuelve true si hay gráficos presentes,
        de lo contrario, false.\n
           - Cantidad de Texto: Evalúa la cantidad de texto presente en la diapositiva. Clasifica la cantidad de texto en
        baja, media o alta según la densidad textual.\n\n
        
        Proporciona la salida en un diccionario de la siguiente forma:
        "Camara": "<True/False>",
        "Slide": "<True/False>",
        "Contenido": {
            "texto": "<contenido textual principal>",
            "graficos": "<True/False>",
            "Cantidad de texto": "<baja/media/alta>"
          }

    
        No hagas NINGÚN (```, json) comentario adicional, ni añadas texto diferente (```, json) al formato de salida, NADA DIFERENTE a la salida. Si no puedes analizar la imagen devuelve todo negativo. 
    """

    return {
        "role": "user",
        "content": [
            prompt_message,
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{frame}"}}
        ]
    }

def print_detection_result(detections: list) -> None:
    """
    Suma el total de veces que fue detectado el rostro del profesor en el vídeo.

    Args:
    detections (list): Lista de detecciones realizadas
    """
    sum_persons = sum([1 for detection in detections if detection == "person"])

    if sum_persons >= len(detections) * 0.6:
        print("El profesor encendió la cámara")


def print_slides_count(slides: int) -> None:
    """
    Imprime el número de slides contadas.

    Args:
    slides (int): Número de slides contadas.
    """
    print(f"el número de diapositivas aproximado fue de {slides}") 
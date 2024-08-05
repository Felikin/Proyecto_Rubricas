import cv2
from numpy import ndarray
from tqdm import tqdm
from ultralytics import YOLO
from typing import Generator
from src.data.load_data import load_video, load_yolo_model


def detect_faces(model: YOLO, source: ndarray, conf: float=0.25, classes: list=[0], verbose: bool=False, stream: bool = False) -> str:
    """
    Detecta rostros en un cuadro dado usando el modelo YOLO.

    Args:
    model (YOLO): Modelo YOLO cargado.
    frame (ndarray): Imagen en la que se realizará la detección.
    conf (float): Umbral de confianza para la detección.
    classes (list): Lista de clases a detectar.
    verbose (bool): Si debe imprimir información adicional.
    stream (bool): Si se debe usar el modo de streaming.

    Returns:
    str: Clase detectada en el cuadro.
    """
    detections = model.predict(source=source, conf=conf, classes=classes, verbose=verbose, stream = stream)
    names = model.names
    try:
       class_detected = names[int(detections[0].boxes.cls)]
    except:
        class_detected = None
    return class_detected


def frame_comparison(frame: ndarray, previous_frame: ndarray) -> int:
    """
    Compara dos cuadros para detectar cambios significativos.

    Args:
    frame (ndarray): Cuadro actual.
    previous_frame (ndarray): Cuadro anterior.
    threshold (int): Umbral para detectar un cambio.

    Returns:
    int: 1 si hay un cambio significativo, 0 en caso contrario.
    """
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    previous_gray_frame = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(previous_gray_frame, gray_frame)
    return 1 if cv2.countNonZero(diff) > 1000000 else 0  # Umbral para detectar cambio


def extract_frames(video: cv2.VideoCapture, step_frame: int) -> Generator[int, ndarray]:
    """
    Extrae cuadros de un video a intervalos regulares.

    Args:
    video (cv2.VideoCapture): Objeto de captura de video.
    step_frame (int): Intervalo entre cuadros extraídos.

    Yields:
    tuple: (int, ndarray) Índice del cuadro y cuadro extraído.
    """
    frame_count = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break
        if frame_count % step_frame == 0:
            yield frame_count, frame
        frame_count += 1


def process_video(video_path: str, model_path: str, frame_skip_rate: float =0.001) -> tuple[list, int]:
    """
    Procesa un video para detectar rostros y cambios de cuadro.

    Args:
    video_path (str): Ruta al archivo de video.
    model_path (str): Ruta al modelo YOLO.
    frame_skip_rate (float): Proporción de cuadros a saltar para la detección.

    Returns:
    list: Detecciones en cuadros seleccionados.
    int: Número de cambios significativos de cuadro.
    """
    video = load_video(video_path)
    model = load_yolo_model(model_path)
    previous_frame = None
    TOTAL_FRAMES = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    STEP_FRAME = int(TOTAL_FRAMES * frame_skip_rate)
    detections = []
    count_slides = 0
    for frame_index, frame in tqdm(extract_frames(video, STEP_FRAME), total=TOTAL_FRAMES // STEP_FRAME, desc="Processing video"):
        if previous_frame is not None:
            count_slides += frame_comparison(frame, previous_frame)
        detection = detect_faces(model, frame)
        detections.append((frame_index, detection))
        previous_frame = frame

    video.release()
    cv2.destroyAllWindows()

    return detections, count_slides
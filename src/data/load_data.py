import os
import cv2
from ultralytics import YOLO


def load_video(video_path: str) -> cv2.VideoCapture:
    """
    Carga un video desde la ruta especificada.
    
    Args:
    video_path (str): Ruta al video.

    Returns:
    video (cv2.VideoCapture): video abierto con opencv.
    """
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        raise ValueError(f"Error opening video file: {video_path}")
    return video


def load_yolo_model(model_path: str) -> YOLO:
    """
    Carga un modelo YOLO preentrenado desde la ruta especificada.
    
    Args:
    model_path (str): Ruta al modelo YOLO.

    Returns:
    YOLO: Modelo YOLO cargado.
    """
    return YOLO(model_path)
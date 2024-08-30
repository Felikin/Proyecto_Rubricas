import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import cv2
import base64
import matplotlib.pyplot as plt
from src.data.load_data import load_video
from src.data.preprocess import encode_image_to_base64
from src.data.load_data import initialize_gpt_client
from src.models.gpt_model import send_frame_to_gpt
from src.visualization.visualize_detections import print_gpt
from src.utils.video_utils import process_gpt_outputs
from tqdm import tqdm



def main(video_path, interval_seconds):
    

    # Inicializar cliente GPT
    client = initialize_gpt_client()

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
        generated_text = send_frame_to_gpt(base64_image, client)
        model_output.append(generated_text)
        with open(f"data/generated/{frame_index}.png", "wb") as fh:
             fh.write(base64.decodebytes(bytes(base64_image, "utf-8")))
    video.release()
    
    results = process_gpt_outputs(model_output)
    print_gpt(results)

if __name__ == "__main__":
        video_path = "data/raw/Juan Sebastian Lozano.mp4"
        interval_seconds = 60
        main(video_path, interval_seconds)
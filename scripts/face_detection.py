import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.load_data import load_video
from src.models.yolo_model import load_yolo_model, frames_det
from src.visualization.visualize_detections import print_detection_result

def main(video_path):
    video = load_video(video_path)
    model = load_yolo_model("models/yolov8n.pt")
    detections = frames_det(model=model, video=video)
    print_detection_result(detections)

if __name__ == "__main__":
    video_path = 'data/raw/Juan Sebastian Lozano.mp4'
    main(video_path)
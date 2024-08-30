import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.yolo_model import process_video
from src.visualization.visualize_detections import print_detection_result, print_slides_count


def main(video_path: str, model_path: str) -> None:
    detections, slides = process_video(model_path=model_path, video_path=video_path)
    print_detection_result(detections)
    print_slides_count(slides)


if __name__ == "__main__":
    video_path = 'data/raw/Juan Sebastian Lozano.mp4'
    model_path = 'models/yolov8n.pt'
    main(video_path, model_path)
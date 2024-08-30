import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.gpt_model import process_video
from src.visualization.visualize_detections import print_gpt


def main(video_path, interval_seconds):

    results = process_video(video_path, interval_seconds)
    print_gpt(results)

if __name__ == "__main__":
        video_path = "data/raw/Juan Sebastian Lozano.mp4"
        interval_seconds = 1800
        main(video_path, interval_seconds)
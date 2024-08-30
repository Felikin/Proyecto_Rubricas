import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.transcript_model import model_execution
from src.data.preprocess import split_transcript_audio
from src.models.gpt_model import process_video


def main(video_path, interval_seconds):
  videos = process_video(video_path, interval_seconds)
  transcription = split_transcript_audio(video_path)
  rubricas = model_execution(transcription)
  rubrica_total = rubricas+videos
  print(rubrica_total)



if __name__ == "__main__":
  video = "data/raw/Juan Sebastian Lozano.mp4"
  main(video, 60)
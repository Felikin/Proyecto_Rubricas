import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.transcript_model import model_execution
from src.data.preprocess import split_transcript_audio

def main(video_path,):

  transcription = split_transcript_audio(video_path)
  rubricas = model_execution(transcription)
  print(rubricas)

if __name__ == "__main__":
  video = "data/raw/Juan Sebastian Lozano.mp4"
  main(video)
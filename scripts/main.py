import time
from utils import extract_audio, split_transcript_audio, model_execution
import json
import os


def main():

    video_path = "Juan Sebastian Lozano 1.mp4"
    extract_audio(video_path)

    audio_path = "audio_from_video.mp3"
    transcripcion = split_transcript_audio(audio_path)

    with open("transcription.txt", "w", encoding="utf-8") as file:
        file.write(transcripcion)

    rubricas = model_execution(transcripcion)
    with open("rubricas.txt", "w", encoding="utf-8") as file:
        file.write(json.dumps(rubricas, ensure_ascii=False))

    os.remove(audio_path)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"{time.time() - start_time} segundos")
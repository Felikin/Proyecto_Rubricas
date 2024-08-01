import os
import cv2

# def load_video(video_path):
#     if os.path.isfile(video_path):
#         return video_path
#     else:
#         raise ValueError(f"Error opening video file: {video_path}")

def load_video(video_path):
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        raise ValueError(f"Error opening video file: {video_path}")
    return video

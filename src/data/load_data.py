import os

def load_video(video_path):
    if os.path.isfile(video_path):
        return video_path
    else:
        raise ValueError(f"Error opening video file: {video_path}")

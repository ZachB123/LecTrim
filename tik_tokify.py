from moviepy.editor import VideoFileClip
import os

def tiktokify(input_path, output_directory, duration):
    os.makedirs(output_directory, exist_ok=True)

    video_clip = VideoFileClip(input_path)

    total_duration = video_clip.duration

    num_clips = int(total_duration / duration) + (1 if total_duration % duration != 0 else 0)

    for i in range(num_clips):
        start_time = i * duration
        end_time = min((i + 1) * duration, total_duration)
        clip = video_clip.subclip(start_time, end_time)
        output_path = os.path.join(output_directory, f"clip_{i+1}.mp4")
        clip.write_videofile(output_path)

    video_clip.close()


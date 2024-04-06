import os
import numpy as np
from scipy.signal import resample
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import moviepy.editor as mp
from moviepy.editor import *

from wpm_adjuster import wpm_adjust

def trim_video(input_path, output_path, start_time, end_time):
    video_clip = VideoFileClip(input_path)

    trimmed_clip = video_clip.subclip(start_time, end_time)

    trimmed_clip.write_videofile(output_path, codec='libx264', fps=24)

    video_clip.close()
    trimmed_clip.close()

def get_video_length(video_path):
    try:
        video = mp.VideoFileClip(video_path)
        video_duration = video.duration
        return video_duration
    except Exception as e:
        print("Error:", e)
        return 0
def main():
    video_path = "Input/TrimmedCredmeteseLecture.mp4"
    output_path = "Output/TrimmedOut.mp4"
    wpm_adjust(video_path, output_path)
    # wpm = calculate_wpm("CredmeteseMidtermLecture.mp4")
    # length = get_video_length(video_path)
    # wpm = calculate_wpm(video_path)
    # print(wpm)
    # speed_up_video(video_path, "Output/test.mp4", 1.5)
    # reduce_pitch("Output/test.mp4", "Output/rpitch.mp4")
    # speed_up_mp4_turn_into_wav(video_path, "Output/test.wav", 1.5)
    # wpm, text = calculate_wpm(video_path)
    # speed_up_video(video_path, "Output/yo.mp4", TARGET_WPM / wpm)
    # trim_video(video_path, "TrimmedCredmeteseLecture.mp4", 180, 300)


if __name__ == "__main__":
    main()
import os
import numpy as np
from scipy.signal import resample
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import moviepy.editor as mp
from moviepy.editor import *
import argparse
import time

from wpm_adjuster import wpm_adjust
from audio_polisher import remove_pauses
from tik_tokify import tiktokify
from subway_surfers import overlap_subway_surfers

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
import argparse

def main():
    # video_path = "Input/TrimmedCredmeteseLecture.mp4"
    # output_path = "Output/TrimmedOut.mp4"
    # wpm_adjust(video_path, output_path)
    print("temp")
    input_file = "what"
    parser = argparse.ArgumentParser(description="Process video and apply various transformations.")
    parser.add_argument("-i", type=str, required=True, help="Path to the input file")
    parser.add_argument("-o", type=str, required=True, help="Path to the output file")
    parser.add_argument("--wpm", type=int, help="Words per minute desired")
    parser.add_argument("--pause-prune", action="store_true", help="Enable pause prune")
    parser.add_argument("--tik-tokify", type=int, help="set the length of the tik tok videos")
    parser.add_argument("--subway-surfers", action="store_true", help="Adds Subway Surfers to the output video")
    args = parser.parse_args()
    
    input_file = args.i 
    output_file = args.o
    if args.wpm:
        wpm = args.wpm
    else:
        wpm = 290
    pause_prune = args.pause_prune
    subway_surfers = args.subway_surfers
    if args.tik_tokify:
        tik_tokify = args.tik_tokify
    else:
        tik_tokify = -1

    print(f"Args: input_file: {input_file}, output_file: {output_file}, wpm: {wpm}, pause: {pause_prune}, tiktokify: {tik_tokify}, Subway Surfers: {subway_surfers}")

    start_time = time.time()

    if pause_prune:
        remove_pauses(input_file, "remove_pauses_temp.mp4", 0.1)
        wpm_adjust("remove_pauses_temp.mp4", output_file, wpm)
        os.remove("remove_pauses_temp.mp4")
    else:
        wpm_adjust(input_file, output_file, wpm)
    
    if subway_surfers:
        overlap_subway_surfers(output_file)

    if tik_tokify != -1:
        tiktokify(output_file, os.path.splitext(output_file)[0], tik_tokify)

    elapsed_time_minutes = (time.time() - start_time) / 60
    print(f"Elapsed time: {elapsed_time_minutes}")
    

if __name__ == "__main__":
    main()

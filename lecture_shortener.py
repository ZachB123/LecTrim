import os
import numpy as np
from scipy.signal import resample
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import moviepy.editor as mp
from moviepy.editor import *
import argparse

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
    parser.add_argument("--filler-prune", action="store_true", help="Enable filler prune")
    parser.add_argument("--tik-tokify", action="store_true", help="Enable tik-tokify")
    args = parser.parse_args()
    
    input_file = args.i 
    output_file = args.o
    if args.wpm:
        wpm = args.wpm
    else:
        wpm = 320
    filler = args.filler_prune
    tik_tokify = args.tik_tokify

    print(f"Args: input_file: {input_file}, output_file: {output_file}, wpm: {wpm}, filler: {filler}, tiktokify: {tik_tokify}")


if __name__ == "__main__":
    main()

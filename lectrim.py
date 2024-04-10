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
import shutil

from wpm_adjuster import wpm_adjust
from audio_polisher import remove_pauses
from tik_tokify import tiktokify
from subway_surfers import overlap_subway_surfers

def trim_video(input_path, output_path, start_time, end_time):
    video_clip = VideoFileClip(input_path)

    trimmed_clip = video_clip.subclip(start_time, end_time)

    trimmed_clip.write_videofile(output_path, codec='libx264', fps=24)


def get_video_length(video_path):
    try:
        video = mp.VideoFileClip(video_path)
        video_duration = video.duration
        return video_duration
    except Exception as e:
        print("Error:", e)
        return 0
import argparse

def cleanup():
    files_to_remove = [
        "temp_audio.wav",
        "Output/spedup.wav",
        "pause_removed.mp4",
        "pause_clip_data.txt",
        "pause_prune.mp4",
        "wpm.mp4",
        "silence.txt",
        "spedup_vid.mp4"
    ]
    
    directories_to_remove = [
        "PauseClips"
    ]

    for file_path in files_to_remove:
        if os.path.isfile(file_path):
            os.remove(file_path)

    for dir_path in directories_to_remove:
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)


def main():
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
    # don't specify set to default
    if args.wpm is None:
        wpm = 250
    elif args.wpm >= 1:
        wpm = args.wpm
    else:
        # if invalid or negative set to -1 so we don't speed up
        wpm = -1
    pause_prune = args.pause_prune
    subway_surfers = args.subway_surfers
    if args.tik_tokify:
        tik_tokify = args.tik_tokify
    else:
        tik_tokify = -1

    print(f"Args: input_file: {input_file}, output_file: {output_file}, wpm: {wpm}, pause: {pause_prune}, tiktokify: {tik_tokify}, Subway Surfers: {subway_surfers}")

    start_time = time.time()
    video_clip = VideoFileClip(input_file)
    wpm_file = input_file

    if pause_prune:
        pause_prune_file = "pause_prune.mp4"
        # video_clip.write_videofile(pause_prune_file)
        # we must prune the wpm adjusted file which sadly means we must write it to disk
        video_clip = remove_pauses(video_clip, input_file)
        wpm_file = "pause_removed.mp4"


    if wpm >= 1:
        # you can set negative wpm to not adjust this
        # vide is sped up like crazy at this point
        # video_clip.write_videofile("wpm.mp4")
        video_clip = wpm_adjust(wpm_file, wpm)


    
    if subway_surfers:
        overlap_subway_surfers(video_clip).write_videofile(output_file)
    else:
        video_clip.write_videofile(output_file)

    # we can use an actual file here because it doesn't matter for efficiency
    # since we have to write the entire video to disk at some point
    if tik_tokify >= 1:
        tiktokify(output_file, os.path.splitext(output_file)[0], tik_tokify)

    # This moviepy library is so bad it is just safest to clear everything at the end
    cleanup()

    elapsed_time_minutes = (time.time() - start_time) / 60
    print(f"Elapsed time: {elapsed_time_minutes}")
    

if __name__ == "__main__":
    # trim_video("Input/psyc1101-04-03-2024.mp4", "Input/halfpsyc.mp4", 0, 20 * 60)
    cleanup()
    main()
    

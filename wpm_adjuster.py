import os
from moviepy.editor import *
import whisper_timestamped as whisper

TARGET_WPM = 320

def convert_video_path_to_mp3(video, audio_path):
    video.audio.write_audiofile(audio_path)


def calculate_wpm(video):
    # video_duration = get_video_length(video_path)

    # video = mp.VideoFileClip(video_path)
    video_duration = video.duration

    audio_path = "temp_audio.wav"  # Temporary audio file
    # video.audio.write_audiofile(audio_file)
    convert_video_path_to_mp3(video, audio_path)

    
    print("Calculating WPM")
    audio = whisper.load_audio(audio_path)
    model = whisper.load_model("tiny", device="cpu")
    result = whisper.transcribe(model, audio, detect_disfluencies=True, language="en")


    # text = recognizer.recognize_sphinx(audio)
    text = result["text"]

    # Calculate WPM
    word_count = len(text.split())
    wpm = word_count / (video_duration / 60)

    # os.remove(audio_path)

    print(f"WPM calculated {wpm}")

    return wpm, text

def speed_up_mp4_turn_into_wav(input_path, output_path, speedup_factor=2):
    os.system(f'ffmpeg -i {input_path} -filter:a "atempo={float(speedup_factor)}" -vn -acodec pcm_s16le -ar 44100 -y {output_path}')


def speed_up_video(input_file, speed_factor):


    speedup_out = "spedup_vid.mp4"
    os.system(f'ffmpeg -i {input_file} -filter_complex "[0:v]setpts=PTS/{speed_factor}[v];[0:a]atempo={speed_factor}[a]" -map "[v]" -map "[a]" {speedup_out}')
    
    # os.remove(sped_up_audio_file)
    final_clip = VideoFileClip(speedup_out)
    print("Video sped up successfully.")
    return final_clip


def wpm_adjust(input_file, target_wpm=TARGET_WPM):
    video_clip = VideoFileClip(input_file)
    wpm, text = calculate_wpm(video_clip)
    return speed_up_video(input_file, target_wpm / wpm)


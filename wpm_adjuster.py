import os
import speech_recognition as sr
from pydub.playback import play
import moviepy.editor as mp
from moviepy.editor import *
import whisper_timestamped as whisper

TARGET_WPM = 320

def convert_video_path_to_mp3(video, audio_path):
    video.audio.write_audiofile(audio_path)


def calculate_wpm(video_path):
    # video_duration = get_video_length(video_path)

    video = mp.VideoFileClip(video_path)
    video_duration = video.duration

    audio_path = "temp_audio.wav"  # Temporary audio file
    # video.audio.write_audiofile(audio_file)
    convert_video_path_to_mp3(video, audio_path)

    # Use speech recognition to transcribe audio
    # recognizer = sr.Recognizer()
    # audio = None
    # with sr.AudioFile(audio_path) as source:
    #     audio = recognizer.record(source)
    
    print("Calculating WPM")
    audio = whisper.load_audio(audio_path)
    model = whisper.load_model("tiny", device="cpu")
    result = whisper.transcribe(model, audio, detect_disfluencies=True, language="en")


    # text = recognizer.recognize_sphinx(audio)
    text = result["text"]

    # Calculate WPM
    word_count = len(text.split())
    wpm = word_count / (video_duration / 60)

    video.close()
    os.remove(audio_path)

    print("WPM calculated")

    return wpm, text

def speed_up_mp4_turn_into_wav(input_path, output_path, speedup_factor=2):
    os.system(f'ffmpeg -i {input_path} -filter:a "atempo={float(speedup_factor)}" -vn -acodec pcm_s16le -ar 44100 -y {output_path}')


def speed_up_video(input_path, output_path, speed_factor):
    # Load the video clip
    video_clip = VideoFileClip(input_path)

    # Extract audio

    # Speed up the video clip
    sped_up_clip = video_clip.fx(vfx.speedx, speed_factor)

    # Adjust audio duration to match the duration of the sped-up video
    # sped_up_audio_clip = audio_clip.fx(vfx.speedx, speed_factor)
    # sped_up_audio_clip = sped_up_audio_clip.set_duration(sped_up_clip.duration)

    sped_up_audio_file = "Output/spedup.wav"
    speed_up_mp4_turn_into_wav(input_path, sped_up_audio_file, speed_factor)
    sped_up_audio_clip = AudioFileClip(sped_up_audio_file)

    # Apply the sped-up audio to the video
    final_clip = sped_up_clip.set_audio(sped_up_audio_clip)

    # Write the final clip to a new file
    final_clip.write_videofile(output_path, codec='libx264', fps=video_clip.fps)

    # Close the video clip objects
    video_clip.close()
    final_clip.close()

    os.remove(sped_up_audio_file)

    print("Video sped up successfully.")


def wpm_adjust(input_file, output_file, target_wpm=TARGET_WPM):
    wpm, text = calculate_wpm(input_file)
    speed_up_video(input_file, output_file, target_wpm / wpm)
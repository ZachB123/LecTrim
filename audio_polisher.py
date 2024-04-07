import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

def remove_pauses(file_in, file_out, ease=0):

    os.system(f"./silence_timestamp.sh {file_in} -30 0.25")
    silence_file = "silence.txt"

    minimum_duration = 1.0

    # number of clips generated
    count = 0
    # start of next clip
    last = 0

    in_handle = open(silence_file, "r", errors='replace')
    video = VideoFileClip(file_in)
    full_duration = video.duration
    clips = []
    while True:
        line = in_handle.readline()

        if not line:
            break

        end,duration = line.strip().split()

        to = float(end) - float(duration)

        start = float(last)
        clip_duration = float(to) - start
        # Clips less than one seconds don't seem to work
        print("Clip Duration: {} seconds".format(clip_duration))

        if clip_duration < minimum_duration:
            continue

        if full_duration - to < minimum_duration:
            continue

        if start > ease:
            start -= ease

        print("Clip {} (Start: {}, End: {})".format(count, start, to))
        clip = video.subclip(start, to)
        clips.append(clip)
        last = end
        count += 1

    if full_duration - float(last) > minimum_duration:
        print("Clip {} (Start: {}, End: {})".format(count, last, 'EOF'))
        clips.append(video.subclip(float(last)-ease))

    processed_video = concatenate_videoclips(clips)
    processed_video.write_videofile(
        file_out,
        fps=60,
        preset='ultrafast',
        codec='libx264'
    )

    os.remove("silence.txt")

    in_handle.close()
    video.close()

if __name__ == "__main__":
    remove_pauses("Input/TrimmedCredmeteseLecture.mp4", "yuh.mp4", 0.1)


# import os
# from moviepy.editor import VideoFileClip
# import whisper_timestamped as whisper
# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# from moviepy.editor import *

# # REMOVE THIS AT SOME POINT
# def convert_video_path_to_mp3(video, audio_path):
#     video.audio.write_audiofile(audio_path)

# def whisper_transcribe(audio_file_path):

#     audio = whisper.load_audio(audio_file_path)

#     model = whisper.load_model("tiny", device="cpu")

#     result = whisper.transcribe(model, audio, detect_disfluencies=True, language="en")

#     # this is a dictionary with text and segments
#     return result

# def process_filler_words(result):
#     filler_words=[]

#     for text in result["segments"]:
#         for word in text["words"]:
#             if "[*]" in word["text"]:
#                 filler_words.append([word["start"], word["end"]])
#                 final_end_time = result["segments"][-1]["end"]


#     split_times = []
#     for i in range(len(filler_words)):
#         if i == 0:
#             start = 0
#             end = filler_words[i][0]
#         else:
#             start = filler_words[i-1][1]
#             end = filler_words[i][0]  
#             filler_words[i]
            
#         split_times.append([start, end])
    
#     split_times.append([filler_words[-1][1], final_end_time])
#     return split_times, filler_words

# def generate_and_join_subclips(uploaded_file_path, output_filename, split_times):
#     ### split
#     TEMP_DIRECTORY = "TMP"
#     os.makedirs(TEMP_DIRECTORY, exist_ok=True)

#     for i in range(len(split_times)):
#         start_time = split_times[i][0]
#         end_time = split_times[i][1]
#         ffmpeg_extract_subclip(uploaded_file_path, start_time, end_time, targetname=f"{TEMP_DIRECTORY}/{str(i)}.mp4")

#     ### concatenate
#     clips = []
#     for i in range(len(split_times)):
#         clip = f"{TEMP_DIRECTORY}/{str(i)}.mp4"
#         clips.append(VideoFileClip(clip))

#     final_clip = concatenate_videoclips(clips)
#     print(f"DURATION IS: {final_clip.duration}")
#     final_clip.write_videofile(output_filename, codec='libx264', fps=24)
    
#     ## delete all files in tmp folder
#     for i in range(len(split_times)):
#         os.remove(f"{TEMP_DIRECTORY}/{str(i)}.mp4")


# # THIS WILL BE DELETED
# if __name__ == "__main__":
#     # video_path = "Input/TrimmedCredmeteseLecture.mp4"
#     # audio_path = "Output/yo.mp3"
#     # res = whisper_transcribe(audio_path)
#     # split_times, filler = process_filler_words(res)

#     # # print(f"SPLIT_TIMES:\n{split_times}")
#     # # print(f"FILLER_WORDS:\n{filler}")
#     # generate_and_join_subclips(video_path, "plzwork.mp4", split_times)

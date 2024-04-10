import os
import shutil
from moviepy.editor import VideoFileClip, concatenate_videoclips

def remove_pauses(video, file_in, ease=0):

    # file in is needed to calculate the silence times -60 is absolute silence
    os.system(f"./silence_timestamp.sh {file_in} -40 0.5")
    silence_file = "silence.txt"

    minimum_duration = 0.5

    # number of clips generated
    count = 0
    # start of next clip
    last = 0

    in_handle = open(silence_file, "r", errors='replace')
    full_duration = video.duration
    clips = []
    while True:
        line = in_handle.readline()

        if not line:
            break
        # 8:26 it actually started
        # sometimes the silence.txt has like random characters
        # try:
        end, duration = line.strip().split()

        try:
            end = float(end)
            duration = float(duration)
        except Exception as e:
            continue

        to = end - duration

        start = float(last)
        clip_duration = float(to) - start
        # except Exception as e:
        #     continue

        last = end

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
        count += 1

    if full_duration - float(last) > minimum_duration:
        print("Clip {} (Start: {}, End: {})".format(count, last, 'EOF'))
        clips.append(video.subclip(float(last)-ease))

    # tomorrow use ffmpeg to slap all these together cuz moviepy is ass
    clips_dir = "PauseClips"
    clip_data = "pause_clip_data.txt"
    os.makedirs(clips_dir, exist_ok=True)
    # processed_video = concatenate_videoclips(clips)
    with open(clip_data, "w") as file:
        for i in range(len(clips)):
            file_name = f"{clips_dir}/{i + 1}.mp4"
            clips[i].write_videofile(file_name)
            file.write(f"file '{file_name}'\n")

    out = "pause_removed.mp4"
    os.system(f"ffmpeg -f concat -safe 0 -i {clip_data} -c copy {out}")

    processed_video = VideoFileClip(out)

    # os.remove(out)
    # shutil.rmtree(clips_dir)
    # os.remove("silence.txt")

    # in_handle.close()
    # video.close()

    return processed_video

if __name__ == "__main__":
    remove_pauses("Input/TrimmedCredmeteseLecture.mp4", "yuh.mp4", 0.1)

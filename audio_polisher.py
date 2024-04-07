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

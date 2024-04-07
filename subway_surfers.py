from moviepy.editor import *
import math

def crop_rectangular_section(input_file, output_file, top_left_x, top_left_y, width, height):
    # Load the video clip
    clip = VideoFileClip(input_file)
    
    # Extract the rectangular section from the original video
    cropped_clip = clip.crop(x1=top_left_x, y1=top_left_y, x2=top_left_x + width, y2=top_left_y + height)
    
    # Make a copy of the cropped clip to ensure the same duration
    cropped_clip = cropped_clip.copy().set_duration(clip.duration)
    
    # Create a new video with just the cropped section
    final_clip = clips_array([[cropped_clip]])
    
    # Write the final clip to a new file
    final_clip.write_videofile(output_file, codec="libx264")
    
    # Close the clips
    clip.close()
    cropped_clip.close()
    final_clip.close()

def loop_clip(video_path, target_duration, audio=False):
    original_clip = VideoFileClip(video_path, audio=audio)

    # Get the duration of the original video clip
    original_duration = original_clip.duration

    # Calculate how many times the video should be repeated to match the target duration
    repetitions = math.ceil(target_duration / original_duration)

    # Repeat the video clip or truncate it to match the target duration
    repeated_clips = [original_clip] * repetitions
    final_clip = concatenate_videoclips(repeated_clips)
    final_clip = final_clip.subclip(0, target_duration)

    return final_clip

def overlap_subway_surfers(video_path):
    video_clip = VideoFileClip(video_path)
    # width = video_clip.size[0]
    video_height = video_clip.size[1]
    duration = video_clip.duration
    subway_surfers_clip = loop_clip("ShortenedSubwaySurfers.mp4", duration)
    # subway_surfers_clip.resize((height / 3, (height / 3) * (576 / 1280)))
    subway_surfers_clip = subway_surfers_clip.resize(height=(video_height/2))

    subway_surfers_position = (0, video_height * (1/2))

    # # Composite the Subway Surfers clip on top of the video clip
    composite_clip = CompositeVideoClip([video_clip.set_position((0, 0)), subway_surfers_clip.set_position(subway_surfers_position)])

    composite_clip.write_videofile(video_path)
    # return composite_clip
    

if __name__ == "__main__":
    clip = overlapy_subway_surfers("Input/TrimmedCredmeteseLecture.mp4")
    clip.write_videofile("test.mp4")
    # # clip.write_com("test.mp4", codec="libx264", bitrate="1000k")
    # clip.close()
    # vid = loop_clip("ShortenedSubwaySurfers.mp4", 900)
    # vid.duration = 900
    # vid.write_videofile("test.mp4")
    # width is 576
    # height is 1280
    # Example usage:
    # input_file = "ShortenedSubwaySurfers.mp4"
    # input_file = "Input/TrimmedCredmeteseLecture.mp4"

    # input_file_clip = VideoFileClip(input_file)
    # input_width = input_file_clip.size[0]
    # input_height = input_file_clip.size[1]
    # output_file = "CroppedSubwaySurfers.mp4"
    # top_left_x = input_width / 3  # X-coordinate of the top-left corner of the rectangular section
    # top_left_y = 0  # Y-coordinate of the top-left corner of the rectangular section
    # width = input_width / 3  # Width of the rectangular section
    # height = input_height  # Height of the rectangular section
    # print(f"tlx: {top_left_x}, tly: {top_left_y}, width: {width}, height: {height}, input_width: {input_width}, input_height: {input_height}")
    # crop_rectangular_section(input_file, output_file, top_left_x, top_left_y, width, height)
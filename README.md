# LecTrim

Note to future self: Moviepy is terrible and I should never use it again.

## Usage

Make sure ffmpeg is installed on your system
pip install -r requirements.txt

python lecture_shortener.py -i <input_file_path> -o <output_file_path> --wpm <wpm> --pause-prune --tik-tokify <duration> --subway-surfers


For GT1201, Takes in a lecture video and reduces it into a more consumable format

input file and output file are required.
wpm, pause prune and subways surfers are all optional.
If wpm is not specified it will default to 250.
If wpm is 0 or negative the video will not be sped up.
If the tiktokify duration is 0 or negative it will not be tik tokified.



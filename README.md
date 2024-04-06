# LectureShortener

## Usage

python lecture_shortener.py -i <input_file_path> -o <output_file_path> --wpm <wpm> --filler-prune --tik-tokify

-i and -o are required
default values are wpm=320 --filler-prune is set 
--filler-prune and --tiktokify default to false

For GT1201, Takes in a lecture video and reduces it into a more consumable format

- git add .
- git commit -m "message"
- git push
- git pull

## Requirements

- calculate the talking speed of the video
- speed up to a fixed wpm
- detect and remove ums and long pauses - pass in threshold
- split up into like little tik toks maybe somehow? - if pause big enough or like major screen change options
- add subway surfers on the side
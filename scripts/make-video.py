import natsort
import os
from moviepy.editor import *

images_path = "builds/letter-video"
img = [
    f"{images_path}/{image_name}"
    for image_name in natsort.natsorted(os.listdir(images_path))
]

clips = [ImageClip(m, duration=0.5) for m in img[:50]]

concat_clip = concatenate_videoclips(clips, method="compose")
concat_clip.write_videofile("test.mp4", fps=24)

import os
import moviepy.editor as mpy

def convert_video(loaded_video, save_extension, height, vcodec, compression, videoquality, add_to_name):
    video = mpy.VideoFileClip(loaded_video)

    if video.rotation == 90:
         video = video.resize(video.size[::-1])
         video.rotation = 0

    vid_height = video.h
    if height != "":
        if vid_height > height:
            video = video.resize(height=height)

    directory_path, file_name = os.path.split(loaded_video)
    file_name_without_extension = os.path.splitext(file_name)[0]

    savetitle = os.path.join(directory_path, file_name_without_extension + add_to_name + '.' + save_extension)

    video.write_videofile(savetitle, threads=4, fps=24,
                          codec=vcodec,
                          preset=compression,
                          ffmpeg_params=["-crf", videoquality])

    video.close()
    print(f"Converted from {loaded_video} to {savetitle}")

def remove_unconverted(full_path):
    os.remove(full_path)

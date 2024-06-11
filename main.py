import os
import shutil
import time

from image import convert_image, mirror, saturation, reduce_size
from finish_sound import finish_sound
from video import convert_video, remove_unconverted
from utils import count_files_and_calculate_size, remove_unconverted_separately, get_size

# In case of directories
path = r'C:\Users\pauli\Downloads\Bt'
directory = os.fsencode(path)

# In case of a single file
file_path = r'C:\Users\pauli\Desktop\Photos\2017 Ateny\Ateny\20171103_165906.mp4'

## type: 'all', 'vid', 'img'
## vid = convertion to another format, size, parameters
## img = listed above, in image function

type = "img"

# Image parameters
new_extension = "jpg"
remove = "n"  # "y" for removing after conversion, use only if the name or extension is different
enhance_value = 3.5
size_reduction = 0.8
image_quality = 80

# Video parameters
save_extension = "mp4"
# height = "" if not changing, otherwise int
height = 720
vcodec = "libx264"
compression = "slow"
videoquality = "24"
add_to_name = " converted"

video_extensions = ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'mpeg', 'mpg', 'm4v']
image_extensions = ['png', 'jpg', 'jpeg', 'webp', 'gif', 'bmp', 'tiff', 'tif', 'ico', 'svg', 'heif', 'heic', 'jfif']
all_extensions = video_extensions + image_extensions
errors = []

def count_files_size():
    if type == 'all':
        file_count, total_size = count_files_and_calculate_size(path, all_extensions)
        img_file_count, img_total_size = count_files_and_calculate_size(path, image_extensions)
        vid_file_count, vid_total_size = count_files_and_calculate_size(path, video_extensions)
    elif type == 'img':
        file_count, total_size = count_files_and_calculate_size(path, image_extensions)
    elif type == 'vid':
        file_count, total_size = count_files_and_calculate_size(path, video_extensions)
    if type == 'all':
        print(f"Images: {img_file_count}\nVideos: {vid_file_count}\nFiles: {file_count}, Total size: {total_size}\n")
    else:
        print(f"Files: {file_count}, Total size: {total_size}")
    return file_count, total_size

file_count, total_size = count_files_size()

current_count = 0

# Uncomment the desired function
def image(full_path):
    #convert_image(full_path, new_extension, remove)
    #mirror(full_path)
    #saturation(full_path, enhance_value)
    reduce_size(full_path, size_reduction, image_quality)
    #remove_unconverted(full_path) #only if the converted name of the converted file is different


def count(full_path):
    global current_count
    if os.path.isfile(full_path):
        current_count += 1
        print(f"File {current_count} out of {file_count}:")
def single_folder(directory, type):
    global current_count
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        full_path = os.path.join(directory.decode(), filename)
        try:
            if type == 'all':
                if filename.lower().endswith(tuple('.' + ext for ext in image_extensions)):
                    count(full_path)
                    image(full_path)
                elif filename.lower().endswith(tuple('.' + ext for ext in video_extensions)):
                    count(full_path)
                    convert_video(full_path, save_extension, height, vcodec, compression, videoquality, add_to_name)
                    remove_unconverted(full_path)  # only if the converted name of the converted file is different
            elif type == 'img':
                if filename.lower().endswith(tuple('.' + ext for ext in image_extensions)):
                    count(full_path)
                    image(full_path)
            elif type == 'vid':
                if filename.lower().endswith(tuple('.' + ext for ext in video_extensions)):
                    count(full_path)
                    convert_video(full_path, save_extension, height, vcodec, compression, videoquality, add_to_name)
                    remove_unconverted(full_path)  # only if the converted name of the converted file is different
            else:
                print("Wrong file type, try: 'all', 'vid', 'img'")
        except Exception as e:
            print(f"Error processing {filename}, {e}")
            errors.append(full_path)

def subfolders(directory, type):
    for root, dirs, files in os.walk(directory):
        single_folder(root, type)
        #remove_unconverted_separately(root, add_to_name, type)

def single_file(full_path):
    filename = os.path.basename(full_path)
    try:
        if filename.lower().endswith(tuple('.' + ext for ext in image_extensions)):
            image(full_path)
        elif filename.lower().endswith(tuple('.' + ext for ext in video_extensions)):
            convert_video(full_path, save_extension, height, vcodec, compression, videoquality)
        if full_path in errors:
            errors.pop(full_path)
            if full_path in errors:
                errors.remove(full_path)
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        errors.append(full_path)

def view_errors_list(errors):
    try:
        print(f"OPERATION FINISHED WITH {len(errors)} ERRORS:")
        for path in errors:
            size = get_size(path)
            print(f"{path}, size: {size}")
        if len(errors) > 0:
            finish_sound()
            retry = input("Retry? type: r\nCreate a new folder for unprocessed files? type: f\nDelete unprocessed files? type: d")
            if retry.lower() == "f":
                error_folder = os.path.join(os.path.dirname(errors[0]), "unprocessed_files")
                if not os.path.exists(error_folder):
                    os.makedirs(error_folder)
                    print(f"Created error folder at: {error_folder}")
                for path in errors:
                    try:
                        if os.path.exists(path):
                            new_path = os.path.join(error_folder, os.path.basename(path))
                            shutil.move(path, new_path)
                            print(f"Moved {path} to {new_path}")
                        else:
                            print(f"File {path} does not exist.")
                    except Exception as e:
                        print(f"Error moving {path} to {new_path}: {e}")
            elif retry.lower() == "d":
                os.remove(path)
            elif retry.lower() == "r":
                for path in errors:
                    single_file(path)
    except Exception as e:
        print(f"Unexpected error: {e}")

start_time = time.time()

###################################
#Functions calls

subfolders(directory, type)
#single_folder(directory, type)
#single_file(file_path)

#remove_unconverted_separately(directory, add_to_name, type)



end_time = time.time()
elapsed_time = end_time - start_time
hours, rem = divmod(elapsed_time, 3600)
minutes, seconds = divmod(rem, 60)

view_errors_list(errors)

new_file_count, new_total_size = count_files_size()

print(f"FINISHED\nProcessed {current_count} files, including {len(errors)} errors.\nReduced total size from {total_size} to {new_total_size}\nElapsed time: {int(hours)} hours, {int(minutes)} minutes, {seconds:.2f} seconds")
finish_sound()
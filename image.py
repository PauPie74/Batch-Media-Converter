from PIL import Image, ImageOps, ImageEnhance
import os
from utils import get_size

###########################################
# File manipulation
###########################################
def convert_image(path, new_extension, remove):
    img = Image.open(path)
    img_rgb = img.convert('RGB')
    directory_path = os.path.dirname(path)
    filename = os.path.basename(path)
    new_filename = os.path.splitext(filename)[0] + '.' + new_extension
    new_full_path = os.path.join(directory_path, new_filename)
    img_rgb.save(new_full_path)
    if remove == 'y':
        if path != new_full_path:
            os.remove(path)
    print(f"Converted {filename} to {new_filename}")

def reduce_size(full_path, reduce_factor, quality):
    original_size = get_size(full_path)
    img = Image.open(full_path)
    img = img.convert('RGB')

    try:
        img = ImageOps.exif_transpose(img)
    except Exception as e:
        print(f"Warning: EXIF data could not be processed properly. {e}")

    new_width = int(img.width * reduce_factor)
    new_height = int(img.height * reduce_factor)
    img.thumbnail((new_width, new_height))
    img.save(full_path, optimize=True, quality=quality)
    filename = os.path.basename(full_path)
    try:
        new_size = get_size(full_path)
        print(f"{filename}: {original_size} to {new_size}")
    except:
         print(f"{filename}: unable to fetch size details")

###########################################
# Image manipulation
###########################################
def mirror(full_path):
    img = Image.open(full_path)
    img = ImageOps.exif_transpose(img)
    img_mirror = ImageOps.mirror(img)
    img_mirror.save(full_path)
    filename = os.path.basename(full_path)
    print(f"MIRRORED: {filename}")

def saturation(full_path, enhance_value):
    img = Image.open(full_path)
    img = ImageOps.exif_transpose(img)
    converter = ImageEnhance.Color(img)
    img_con = converter.enhance(enhance_value)
    img_con.save(full_path)
    filename = os.path.basename(full_path)
    print(f"COLOR ENHANCED by {enhance_value}: {filename} ")
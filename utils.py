import os

video_extensions = ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'mpeg', 'mpg', 'm4v']
image_extensions = ['png', 'jpg', 'jpeg', 'webp', 'gif', 'bmp', 'tiff', 'tif', 'ico', 'svg', 'heif', 'heic', 'jfif']
all_extensions = video_extensions + image_extensions

def format_size(size_in_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']:
            if size_in_bytes < 1024:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024
        return f"{size_in_bytes:.2f} YB"

def get_size(path):
    size_in_bytes = os.path.getsize(path)
    size = format_size(size_in_bytes)
    return size

def count_files_and_calculate_size(directory, extensions):
    total_size = 0
    file_count = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            if f.lower().endswith(tuple(extensions)):
                file_count += 1
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
    total_size = format_size(total_size)
    return file_count, total_size

def remove(directory, filename, add_to_name):
    file_name_without_extension, ext = os.path.splitext(filename)
    directory = os.path.dirname(directory)
    if file_name_without_extension.endswith(add_to_name):
        original_file_name = file_name_without_extension.replace(add_to_name, '')
        for ext in all_extensions:
            new_original_file_name = original_file_name + '.' + ext
            original_file_path = os.path.join(directory, new_original_file_name)
            if os.path.exists(original_file_path):
                os.remove(original_file_path)
                print(f"Removed {new_original_file_name}")

def remove_unconverted_separately(directory, add_to_name, type):
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        full_path = os.path.join(directory.decode(), filename)
        if type == 'all':
            if filename.lower().endswith(tuple('.' + ext for ext in image_extensions)):
                remove(full_path, filename, add_to_name)
            elif filename.lower().endswith(tuple('.' + ext for ext in video_extensions)):
                remove(full_path, filename, add_to_name)
        elif type == 'img':
            if filename.lower().endswith(tuple('.' + ext for ext in image_extensions)):
                remove(full_path, filename, add_to_name)
        elif type == 'vid':
            if filename.lower().endswith(tuple('.' + ext for ext in video_extensions)):
                remove(full_path, filename, add_to_name)

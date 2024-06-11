import os
from finish_sound import finish_sound

path = r'C:\Users\pauli\Downloads\Clip'
directory = os.fsencode(path)


def find_duplicated_names(directory):
    files_list = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            filename = os.fsdecode(file)
            full_path = os.path.join(root, file)
            if filename in files_list:
                files_list[filename].append(full_path)
            else:
                files_list[filename] = [full_path]

    for filename, paths in files_list.items():
        if len(paths) > 1:
            print(f"Duplicate files for '{filename}':")
            for path in paths:
                print(path)


def rename_file(directory, part_to_delete, rename_to):
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        full_path = os.path.join(path, filename)
        new_name = filename.replace(part_to_delete, rename_to).strip()
        print(new_name)
        new_full_path = os.path.join(path, new_name)
        os.rename(full_path, new_full_path)
    print("FINISHED")


def find_rename_move(directory, extension):
    #takes files with certain extension, renames it to number and move to the root folder
    i = 1
    for root, dirs, files in os.walk(directory):
        for file in os.listdir(root):
            filename = os.fsdecode(file)
            if filename.endswith('.' + extension):
                full_path = os.path.join(root.decode(), filename)
                img = Image.open(full_path)
                new_filename = f"{i}.{extension}"
                i += 1
                new_full_path = os.path.join(directory.decode(), new_filename)
                print(new_full_path)
                img.save(new_full_path)
    print("FINISHED")

#find_duplicated_names(directory)
#rename_file(directory, part_to_delete, rename_to)
#find_rename_move(directory, "jpg")



finish_sound()
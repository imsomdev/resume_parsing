import os

def delete(filename):
    file_path = f'/path_to_folder/{filename}'
    os.remove(file_path)
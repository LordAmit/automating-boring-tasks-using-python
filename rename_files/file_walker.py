from typing import List
from natsort import natsorted, ns
import custom_log as c_log
import os
current_mode = None



def get_mode():
    return current_mode


def get_files() -> List:

    file_paths = []
    dir_path = os.getcwd()
    for folderName, sub_folders, filenames in os.walk(dir_path):
        sub_folders.clear()
        for filename in filenames:

            file_path = os.path.join(folderName, filename)

            file_paths.append(file_path)
    return natsorted(file_paths, key=lambda y: y.lower())
    # file_paths = sorted(file_paths, key=str, reverse=True)
    # return file_paths

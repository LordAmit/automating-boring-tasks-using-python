from os import path as Path
from typing import List
import custom_log as l
import sys, os


def walk(path: str) -> List:
    """
    walks through a path to return list of absolute path of images with png or jpg extensions
    :param path: to the directory where images will be searched for
    :return: List of string path of images
    """
    image_paths = []
    l.log("checking path integrity")
    if Path.exists(path):
        l.log([path, "exists"])
    else:
        l.log("path does not exist")
        exit()
    for folderName, subfolders, filenames in os.walk(path):
        for filename in filenames:
            if (filename.endswith('jpg') or
                    filename.endswith('.png') or
                    filename.endswith('.bmp') or
                    filename.endswith('.jpeg')):
                file_path = os.path.join(folderName, filename)

                l.log([file_path, filename])
                image_paths.append(file_path)
    return image_paths

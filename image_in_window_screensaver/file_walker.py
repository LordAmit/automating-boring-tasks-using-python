from os import path as Path
from typing import List
import custom_log as l
import os
import argument_handler as argh


def walk(mode=None) -> List:
    """
    walks through a path to return list of absolute path of images with png or jpg extensions
    :param mode: can be
    :param path: to the directory where images will be searched for
    :return: List of string path of images
    """
    image_paths = []
    path: str = argh.get_path()
    if mode:
        path += mode
    l.log(path)
    ignore: str = argh.get_ignore_word()
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
                if ignore and is_exclude_image(file_path, ignore):
                    continue
                image_paths.append(file_path)
    return image_paths


def is_exclude_image(image_path: str, ignore_word: str) -> str:
    import custom_log as l
    l.log(ignore_word)
    # exit()
    if ',' in ignore_word:
        list_ignores = ignore_word.split(',')

        for word in list_ignores:
            if image_path.lower().find(word) is not -1:
                l.log(["found entry in list_ignore: ", image_path, word])
                return True
    else:
        if image_path.lower().find(ignore_word) is not -1:
            l.log(["found entry in list_ignore: ", image_path, ignore_word])
            return True
    return False
